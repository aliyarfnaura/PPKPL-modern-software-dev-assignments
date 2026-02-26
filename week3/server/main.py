import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load API Key dari .env
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Inisialisasi MCP Server
mcp = FastMCP("Movie MCP Server")

# TOOL 1: Search Movie by Title
@mcp.tool()
async def search_movie(title: str):
    """
    Search movie berdasarkan judul
    """
    if not title:
        return {"error": "Movie title is required"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{BASE_URL}/search/movie",
                params={"api_key": API_KEY, "query": title}
            )

            if response.status_code != 200:
                return {"error": "API request failed"}

            data = response.json()

            if not data.get("results"):
                return {"error": "Movie not found"}

            movie = data["results"][0]

            return {
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "overview": movie.get("overview"),
                "rating": movie.get("vote_average")
            }

    except httpx.RequestError:
        return {"error": "Connection timeout or failed"}

# TOOL 2: Get Popular Movies
@mcp.tool()
async def get_popular_movies():
    """
    Ambil 5 film populer dari TMDB
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{BASE_URL}/movie/popular",
                params={"api_key": API_KEY}
            )

            if response.status_code != 200:
                return {"error": "API request failed"}

            data = response.json()

            if not data.get("results"):
                return {"error": "No popular movies found"}

            return [
                {
                    "title": movie.get("title"),
                    "rating": movie.get("vote_average")
                }
                for movie in data["results"][:5]
            ]

    except httpx.RequestError:
        return {"error": "Connection timeout or failed"}

if __name__ == "__main__":
    mcp.run(transport="stdio")