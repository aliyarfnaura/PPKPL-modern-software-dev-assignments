# Week 3 — Movie MCP Server (TMDB)

A local MCP server that wraps the [TMDB API](https://www.themoviedb.org/) to search movies and retrieve popular films. Runs via STDIO transport and integrates with Claude Desktop.

---

## Prerequisites

- Python 3.10+
- A free TMDB API key → [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
- Claude Desktop installed → [https://claude.ai/download](https://claude.ai/download)

---

## Project Structure

```
week3/
├── server/
│   ├── main.py          # MCP server entrypoint
│   ├── .env             # API key (not committed to git)
│   ├── venv/            # Python virtual environment
├── assignment.md            
└── README.md
```

---

## Environment Setup

### 1. Clone / navigate to the project

```bash
cd week3/server
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install mcp httpx python-dotenv
```

Or using a requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
mcp
httpx
python-dotenv
```

### 4. Set up environment variables

Create a `.env` file inside `week3/server/`:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

---

## Running the Server Locally

```bash
cd week3/server
venv\Scripts\activate   # Windows
python main.py
```

The server runs in STDIO mode — no visible output is expected if it starts successfully.

---

## Configuring Claude Desktop

### Windows (Standard Installation)

Edit the config file at:
```
C:\Users\<YourUser>\AppData\Roaming\Claude\claude_desktop_config.json
```

> **Note for MSIX/Windows Store installation of Claude Desktop:** The config file is located at:
> `C:\Users\<YourUser>\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`

Add the following:

```json
{
  "mcpServers": {
    "movie-server": {
      "command": "C:\\path\\to\\week3\\server\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\week3\\server\\main.py"
      ],
      "env": {
        "TMDB_API_KEY": "your_tmdb_api_key_here"
      }
    }
  }
}
```

Replace `C:\\path\\to\\` with the actual path to your project.

> **If your project is on a non-C: drive (e.g., D:):** Claude Desktop MSIX cannot access other drives directly. Create a symbolic link first:
> ```powershell
> # Run PowerShell as Administrator
> New-Item -ItemType SymbolicLink -Path "C:\week3" -Target "D:\your\path\to\week3"
> ```
> Then use `C:\\week3\\server\\venv\\Scripts\\python.exe` in the config above.

### Mac

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "movie-server": {
      "command": "/path/to/week3/server/venv/bin/python",
      "args": ["/path/to/week3/server/main.py"],
      "env": {
        "TMDB_API_KEY": "your_tmdb_api_key_here"
      }
    }
  }
}
```

After saving the config, **fully quit Claude Desktop** (including from the system tray) and reopen it. The server status should show **running** under Settings → Developer → Local MCP Servers.

---

## Tool Reference

### `search_movie`

Search for a movie by title using TMDB.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `title`   | string | Yes      | The movie title to search for |

**Example input:**
> "cari film Inception" / "search movie The Dark Knight"

**Example output:**
```json
{
  "title": "Inception",
  "release_date": "2010-07-15",
  "overview": "A thief who steals corporate secrets through dream-sharing technology...",
  "rating": 8.4
}
```

**Error cases:**
- Empty title → `{"error": "Movie title is required"}`
- Not found → `{"error": "Film 'X' tidak ditemukan"}`
- API failure → `{"error": "Gagal menghubungi TMDB API. Coba lagi nanti."}`
- Invalid API key → `{"error": "API key tidak dikonfigurasi. Set TMDB_API_KEY di file .env"}`

---

### `get_popular_movies`

Retrieve the current top 5 popular movies from TMDB.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)*  | —    | —        | No parameters needed |

**Example input:**
> "tampilkan film populer" / "get popular movies"

**Example output:**
```json
[
  { "title": "28 Years Later: The Bone Temple", "rating": 7.18 },
  { "title": "Mercy", "rating": 7.09 },
  { "title": "Shelter", "rating": 7.02 },
  { "title": "A Woman Scorned", "rating": 6.30 },
  { "title": "The Orphans", "rating": 6.10 }
]
```

---

### `get_now_playing`

Retrieve the top 5 movies currently playing in cinemas.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)*  | —    | —        | No parameters needed |

**Example input:**
> "film apa yang sedang tayang di bioskop sekarang"

**Example output:**
```json
[
  { "title": "Sinners", "release_date": "2025-04-17", "rating": 7.3 },
  { "title": "Final Destination: Bloodlines", "release_date": "2025-05-14", "rating": 6.9 },
  { "title": "Mission: Impossible", "release_date": "2025-05-21", "rating": 7.8 },
  { "title": "Lilo & Stitch", "release_date": "2025-05-22", "rating": 6.5 },
  { "title": "Karate Kid", "release_date": "2025-05-30", "rating": 6.2 }
]
```

---

### `get_top_rated`

Retrieve the top 5 highest-rated movies of all time from TMDB.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)*  | —    | —        | No parameters needed |

**Example input:**
> "tampilkan film dengan rating tertinggi sepanjang masa"

**Example output:**
```json
[
  { "title": "The Shawshank Redemption", "release_date": "1994-09-23", "rating": 8.7 },
  { "title": "The Godfather", "release_date": "1972-03-14", "rating": 8.7 },
  { "title": "Schindler's List", "release_date": "1993-11-29", "rating": 8.6 },
  { "title": "The Dark Knight", "release_date": "2008-07-14", "rating": 8.5 },
  { "title": "12 Angry Men", "release_date": "1957-04-10", "rating": 8.5 }
]
```

---

### `search_movie_by_genre`

Search top 5 popular movies by genre.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `genre`   | string | Yes      | Genre name (see available genres below) |

**Available genres:** action, adventure, animation, comedy, crime, documentary, drama, family, fantasy, history, horror, music, mystery, romance, sci-fi, thriller, war, western

**Example input:**
> "cari film genre horror" / "tampilkan film action populer"

**Example output:**
```json
[
  { "title": "Venom: The Last Dance", "release_date": "2024-10-22", "rating": 6.8 },
  { "title": "Deadpool & Wolverine", "release_date": "2024-07-24", "rating": 7.7 },
  { "title": "Gladiator II", "release_date": "2024-11-13", "rating": 6.9 },
  { "title": "Kraven the Hunter", "release_date": "2024-12-12", "rating": 6.1 },
  { "title": "Captain America: Brave New World", "release_date": "2025-02-12", "rating": 6.2 }
]
```

**Error cases:**
- Empty genre → `{"error": "Genre is required"}`
- Unknown genre → `{"error": "Genre 'X' tidak dikenali. Genre yang tersedia: ..."}`

---

## TMDB API Endpoints Used

| Tool                   | Endpoint                    |
|------------------------|-----------------------------|
| `search_movie`         | `GET /search/movie`         |
| `get_popular_movies`   | `GET /movie/popular`        |
| `get_now_playing`      | `GET /movie/now_playing`    |
| `get_top_rated`        | `GET /movie/top_rated`      |
| `search_movie_by_genre`| `GET /discover/movie`       |

Base URL: `https://api.themoviedb.org/3`

---

## Example Invocation Flow

1. Open Claude Desktop
2. Start a new chat
3. Type one of the following:
   - `"cari film Interstellar"` → triggers `search_movie`
   - `"tampilkan film populer"` → triggers `get_popular_movies`
   - `"film apa yang sedang tayang di bioskop"` → triggers `get_now_playing`
   - `"tampilkan film dengan rating tertinggi sepanjang masa"` → triggers `get_top_rated`
   - `"cari film genre thriller"` → triggers `search_movie_by_genre`
4. Claude will call the MCP tool and return results from TMDB API directly

---

## Reliability Features

- **Auth validation** — every tool checks if `TMDB_API_KEY` is set before making any request. Returns a clear error message if missing.
- **Retry with backoff** — each request is retried up to 3 times with increasing delay if it fails or times out.
- **Rate limit handling** — if TMDB returns HTTP 429, the server automatically waits based on the `Retry-After` header before retrying.
- **Graceful error handling** — all HTTP failures, timeouts, and empty results return structured error messages instead of crashing.
- **Logging** — all tool calls and errors are logged to stderr for debugging.

---

## Notes

- This server uses **STDIO transport** (local mode)
- API key is loaded from `.env` file or passed via Claude Desktop config `env` block
- Logging is output to stderr only (not stdout, which would break STDIO transport)