import asyncio

from app.db.session import AsyncSessionLocal
from app.movies.service import MovieService


async def main():
    async with AsyncSessionLocal() as session:
        response = await MovieService.list_movies(
            session=session,
            page=1,
            page_size=5,
        )

        print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())