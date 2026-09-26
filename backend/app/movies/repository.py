from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.movies.models import (
    DimCompany,
    DimGenre,
    DimMovie,
    DimPerson,
    DimReview,
    MovieReview,
    PersonType,
)


class MovieRepository:

    @staticmethod
    async def list_movies( # Listando de forma paginada
        session: AsyncSession,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[DimMovie], int]:
        
        # Filtros de pesquisa usando ilike
        filters = []

        if search:
            filters.append(
                DimMovie.titulo.ilike(f"%{search.strip()}%")
            )

        # Consulta para contar o total de filmes encontrados
        count_query = (
            select(func.count())
            .select_from(DimMovie)
            .where(*filters)
        )

        total_result = await session.execute(count_query)

        total = total_result.scalar_one()

        # Consulta da page solicitada
        offset = (page - 1) * page_size

        query = (
            select(DimMovie)
            .where(*filters)
            .options(
                selectinload(DimMovie.genres),
                selectinload(DimMovie.reviews_summary),
            )
            .order_by(DimMovie.titulo)
            .offset(offset)
            .limit(page_size)
        )

        result = await session.execute(query)

        movies = result.scalars().all()

        return list(movies), total

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        movie_id: str,
    ) -> DimMovie | None:

        query = (
            select(DimMovie)
            .where(DimMovie.sk_movie_id == movie_id)
            .options(
                selectinload(DimMovie.genres),
                selectinload(DimMovie.companies),
                selectinload(DimMovie.people),
                selectinload(DimMovie.performance),
                selectinload(DimMovie.reviews_summary),
                selectinload(DimMovie.reviews),
            )
        )

        result = await session.execute(query)

        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_genre_by_name(
        session: AsyncSession,
        name: str,
    ) -> DimGenre | None:
        query = select(DimGenre).where(
            func.lower(DimGenre.nome_genero) == name.lower()
        )

        result = await session.execute(query)

        return result.scalar_one_or_none()


    @staticmethod
    async def get_company_by_name(
        session: AsyncSession,
        name: str,
    ) -> DimCompany | None:
        query = select(DimCompany).where(
            func.lower(DimCompany.nome_produtora) == name.lower()
        )

        result = await session.execute(query)

        return result.scalar_one_or_none()


    @staticmethod
    async def get_person_by_name_and_type(
        session: AsyncSession,
        name: str,
        person_type: PersonType,
    ) -> DimPerson | None:
        query = select(DimPerson).where(
            and_(
                func.lower(DimPerson.nome_pessoa) == name.lower(),
                DimPerson.tipo_pessoa == person_type,
            )
        )

        result = await session.execute(query)

        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_by_title(
        session: AsyncSession,
        title: str,
    ) -> DimMovie | None:
        query = select(DimMovie).where(
            func.lower(DimMovie.titulo) == title.strip().lower()
        )

        result = await session.execute(query)

        return result.scalars().first()
    
    
    @staticmethod
    async def create_genre(
        session: AsyncSession,
        name: str,
    ) -> DimGenre:
        genre = DimGenre(
            nome_genero=name,
        )

        session.add(genre)

        await session.flush()

        return genre


    @staticmethod
    async def create_company(
        session: AsyncSession,
        name: str,
    ) -> DimCompany:
        company = DimCompany(
            nome_produtora=name,
        )

        session.add(company)

        await session.flush()

        return company


    @staticmethod
    async def create_person(
        session: AsyncSession,
        name: str,
        person_type: PersonType,
    ) -> DimPerson:
        person = DimPerson(
            nome_pessoa=name,
            tipo_pessoa=person_type,
        )

        session.add(person)

        await session.flush()

        return person
    
    @staticmethod
    async def create_movie(
        session: AsyncSession,
        movie: DimMovie,
    ) -> DimMovie:
        session.add(movie)

        await session.flush()

        return movie
    
    @staticmethod
    async def update_movie(
        session: AsyncSession,
        movie: DimMovie,
    ) -> DimMovie:
        session.add(movie)

        await session.flush()

        return movie
    
    
    @staticmethod
    async def delete_movie(
        session: AsyncSession,
        movie: DimMovie,
    ) -> None:
        await session.delete(movie)
        await session.flush()
        

    @staticmethod
    async def get_review_stats(
        session: AsyncSession,
        movie_id: str,
    ) -> tuple[int, float | None]:
        query = select(
            func.count(MovieReview.sk_movie_review_id),
            func.avg(MovieReview.nota),
        ).where(
            MovieReview.sk_movie_id == movie_id
        )

        result = await session.execute(query)

        count, average = result.one()

        return (
            int(count),
            float(average) if average is not None else None,
        )
        
    
    
    @staticmethod
    async def get_review_summary(
        session: AsyncSession,
        movie_id: str,
    ) -> DimReview | None:
        query = select(DimReview).where(
            DimReview.sk_movie_id == movie_id
        )

        result = await session.execute(query)

        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def save_review_summary(
        session: AsyncSession,
        movie_id: str,
        count: int,
        average: float | None,
    ) -> DimReview:
        summary = await MovieRepository.get_review_summary(
            session=session,
            movie_id=movie_id,
        )

        if summary is None:
            summary = DimReview(
                sk_movie_id=movie_id,
                qtd_avaliacoes_usuarios=count,
                nota_media_usuarios=average,
            )

            session.add(summary)

        else:
            summary.qtd_avaliacoes_usuarios = count
            summary.nota_media_usuarios = average

        await session.flush()

        return summary
    
    
    @staticmethod
    async def create_review(
        session: AsyncSession,
        review: MovieReview,
    ) -> MovieReview:
        session.add(review)

        await session.flush()

        return review
    