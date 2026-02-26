import os
import logging
import asyncio
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# ─── Logging Setup ───────────────────────────────────────────────────────────
# Hanya pakai stderr, JANGAN FileHandler (MSIX sandbox tidak bisa tulis file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # stderr only
    ]
)
logger = logging.getLogger(__name__)

# ─── Config ──────────────────────────────────────────────────────────────────
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Genre mapping TMDB
GENRE_MAP = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "science fiction": 878,
    "sci-fi": 878,
    "thriller": 53,
    "war": 10752,
    "western": 37
}

# ─── Init MCP ────────────────────────────────────────────────────────────────
mcp = FastMCP("Movie MCP Server")

# ─── Auth Validation ─────────────────────────────────────────────────────────
def validate_api_key() -> bool:
    """Cek apakah API key sudah di-set di environment."""
    if not API_KEY:
        logger.error("TMDB_API_KEY tidak ditemukan di environment variables")
        return False
    return True

# ─── Helper: Request dengan Retry ────────────────────────────────────────────
async def fetch_with_retry(url: str, params: dict) -> dict | None:
    """
    Melakukan HTTP GET dengan retry dan exponential backoff.
    Return None jika semua percobaan gagal.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Request ke {url} (percobaan {attempt}/{MAX_RETRIES})")
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, params=params)

                # Rate limit handling (HTTP 429)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", RETRY_DELAY * attempt))
                    logger.warning(f"Rate limit tercapai. Menunggu {retry_after} detik...")
                    await asyncio.sleep(retry_after)
                    continue

                if response.status_code != 200:
                    logger.error(f"API error: status {response.status_code}")
                    return None

                logger.info(f"Request berhasil: {url}")
                return response.json()

        except httpx.TimeoutException:
            logger.warning(f"Timeout pada percobaan {attempt}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY * attempt)

        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY * attempt)

    logger.error(f"Semua {MAX_RETRIES} percobaan gagal untuk {url}")
    return None

# ─── TOOL 1: Search Movie by Title ───────────────────────────────────────────
@mcp.tool()
async def search_movie(title: str):
    """
    Search movie berdasarkan judul
    """
    logger.info(f"search_movie dipanggil dengan judul: '{title}'")

    if not validate_api_key():
        return {"error": "API key tidak dikonfigurasi. Set TMDB_API_KEY di file .env"}

    if not title or not title.strip():
        logger.warning("search_movie dipanggil tanpa judul")
        return {"error": "Movie title is required"}

    data = await fetch_with_retry(
        f"{BASE_URL}/search/movie",
        {"api_key": API_KEY, "query": title.strip()}
    )

    if data is None:
        return {"error": "Gagal menghubungi TMDB API. Coba lagi nanti."}

    if not data.get("results"):
        logger.info(f"Film '{title}' tidak ditemukan")
        return {"error": f"Film '{title}' tidak ditemukan"}

    movie = data["results"][0]
    logger.info(f"Film ditemukan: {movie.get('title')}")

    return {
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "overview": movie.get("overview"),
        "rating": movie.get("vote_average")
    }

# ─── TOOL 2: Get Popular Movies ──────────────────────────────────────────────
@mcp.tool()
async def get_popular_movies():
    """
    Ambil 5 film populer dari TMDB
    """
    logger.info("get_popular_movies dipanggil")

    if not validate_api_key():
        return {"error": "API key tidak dikonfigurasi. Set TMDB_API_KEY di file .env"}

    data = await fetch_with_retry(
        f"{BASE_URL}/movie/popular",
        {"api_key": API_KEY}
    )

    if data is None:
        return {"error": "Gagal menghubungi TMDB API. Coba lagi nanti."}

    if not data.get("results"):
        return {"error": "No popular movies found"}

    movies = [
        {
            "title": movie.get("title"),
            "rating": movie.get("vote_average")
        }
        for movie in data["results"][:5]
    ]

    logger.info(f"Berhasil mengambil {len(movies)} film populer")
    return movies

# ─── TOOL 3: Get Now Playing ─────────────────────────────────────────────────
@mcp.tool()
async def get_now_playing():
    """
    Ambil 5 film yang sedang tayang di bioskop saat ini
    """
    logger.info("get_now_playing dipanggil")

    if not validate_api_key():
        return {"error": "API key tidak dikonfigurasi. Set TMDB_API_KEY di file .env"}

    data = await fetch_with_retry(
        f"{BASE_URL}/movie/now_playing",
        {"api_key": API_KEY}
    )

    if data is None:
        return {"error": "Gagal menghubungi TMDB API. Coba lagi nanti."}

    if not data.get("results"):
        return {"error": "No movies currently playing"}

    movies = [
        {
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average")
        }
        for movie in data["results"][:5]
    ]

    logger.info(f"Berhasil mengambil {len(movies)} film yang sedang tayang")
    return movies

# ─── TOOL 4: Get Top Rated ───────────────────────────────────────────────────
@mcp.tool()
async def get_top_rated():
    """
    Ambil 5 film dengan rating tertinggi sepanjang masa dari TMDB
    """
    logger.info("get_top_rated dipanggil")

    if not validate_api_key():
        return {"error": "API key tidak dikonfigurasi. Set TMDB_API_KEY di file .env"}

    data = await fetch_with_retry(
        f"{BASE_URL}/movie/top_rated",
        {"api_key": API_KEY}
    )

    if data is None:
        return {"error": "Gagal menghubungi TMDB API. Coba lagi nanti."}

    if not data.get("results"):
        return {"error": "No top rated movies found"}

    movies = [
        {
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average")
        }
        for movie in data["results"][:5]
    ]

    logger.info(f"Berhasil mengambil {len(movies)} film top rated")
    return movies

# ─── TOOL 5: Search Movie by Genre ───────────────────────────────────────────
@mcp.tool()
async def search_movie_by_genre(genre: str):
    """
    Cari 5 film populer berdasarkan genre.
    Genre yang tersedia: action, adventure, animation, comedy, crime,
    documentary, drama, family, fantasy, history, horror, music,
    mystery, romance, sci-fi, thriller, war, western
    """
    logger.info(f"search_movie_by_genre dipanggil dengan genre: '{genre}'")

    if not validate_api_key():
        return {"error": "API key tidak dikonfigurasi. Set TMDB_API_KEY di file .env"}

    if not genre or not genre.strip():
        return {"error": "Genre is required"}

    genre_lower = genre.strip().lower()
    genre_id = GENRE_MAP.get(genre_lower)

    if not genre_id:
        available = ", ".join(GENRE_MAP.keys())
        logger.warning(f"Genre '{genre}' tidak ditemukan")
        return {"error": f"Genre '{genre}' tidak dikenali. Genre yang tersedia: {available}"}

    data = await fetch_with_retry(
        f"{BASE_URL}/discover/movie",
        {
            "api_key": API_KEY,
            "with_genres": genre_id,
            "sort_by": "popularity.desc"
        }
    )

    if data is None:
        return {"error": "Gagal menghubungi TMDB API. Coba lagi nanti."}

    if not data.get("results"):
        return {"error": f"Tidak ada film ditemukan untuk genre '{genre}'"}

    movies = [
        {
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average")
        }
        for movie in data["results"][:5]
    ]

    logger.info(f"Berhasil mengambil {len(movies)} film genre {genre}")
    return movies

# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not validate_api_key():
        logger.critical("Server tidak bisa start: TMDB_API_KEY tidak ditemukan")
        exit(1)

    logger.info("Movie MCP Server starting...")
    mcp.run(transport="stdio")