import asyncio

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.movies.repository import MovieRepository

settings = get_settings()

print("DATABASE_URL:", settings.database_url)


async def main():
    async with AsyncSessionLocal() as session:
        movies, total = await MovieRepository.list_movies(
            session=session,
            page=1,
            page_size=5,
        )

        print("Total:", total)

        for movie in movies:
            print(
                movie.titulo,
                [genre.nome_genero for genre in movie.genres],
            )


if __name__ == "__main__":
    asyncio.run(main())