from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.movies.models import DimMovie, MovieReview, PersonType
from app.movies.repository import MovieRepository
from app.movies.schemas import (
    MovieCreate,
    MovieDetailResponse,
    MovieListItem,
    MovieListResponse,
    MovieUpdate,
    PerformanceResponse,
    ReviewCreate,
    ReviewResponse,
    ReviewSummaryResponse,
)


class MovieService:

    @staticmethod
    async def list_movies(
        session: AsyncSession,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> MovieListResponse:
        movies, total = await MovieRepository.list_movies(
            session=session,
            page=page,
            page_size=page_size,
            search=search,
        )

        items = [
            MovieService._to_list_item(movie)
            for movie in movies
        ]

        total_pages = (
            (total + page_size - 1) // page_size
            if total > 0
            else 0
        )

        return MovieListResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    @staticmethod
    async def get_movie_by_id(
        session: AsyncSession,
        movie_id: str,
    ) -> MovieDetailResponse | None:
        movie = await MovieRepository.get_by_id(
            session=session,
            movie_id=movie_id,
        )

        if movie is None:
            return None

        return MovieService._to_detail_response(movie)

    @staticmethod
    def _to_list_item(
        movie: DimMovie,
    ) -> MovieListItem:
        nota_media = None

        if movie.reviews_summary is not None:
            nota_media = (
                movie.reviews_summary.nota_media_usuarios
            )

        return MovieListItem(
            sk_movie_id=movie.sk_movie_id,
            titulo=movie.titulo,
            ano_lancamento=movie.ano_lancamento,
            url_poster=movie.url_poster,
            generos=[
                genre.nome_genero
                for genre in movie.genres
            ],
            nota_media=nota_media,
        )

    @staticmethod
    def _to_detail_response(
        movie: DimMovie,
    ) -> MovieDetailResponse:
        diretores = []
        atores = []
        roteiristas = []

        for person in movie.people:
            if person.tipo_pessoa == "Diretor":
                diretores.append(person.nome_pessoa)

            elif person.tipo_pessoa == "Ator":
                atores.append(person.nome_pessoa)

            elif person.tipo_pessoa == "Roteirista":
                roteiristas.append(person.nome_pessoa)

        performance = None

        if movie.performance is not None:
            performance = PerformanceResponse.model_validate(
                movie.performance
            )

        resumo_avaliacoes = None

        if movie.reviews_summary is not None:
            resumo_avaliacoes = (
                ReviewSummaryResponse.model_validate(
                    movie.reviews_summary
                )
            )

        avaliacoes = [
            ReviewResponse.model_validate(review)
            for review in movie.reviews
        ]

        return MovieDetailResponse(
            sk_movie_id=movie.sk_movie_id,
            id_filme=movie.id_filme,
            titulo=movie.titulo,
            data_lancamento=movie.data_lancamento,
            ano_lancamento=movie.ano_lancamento,
            duracao_minutos=movie.duracao_minutos,
            status_filme=movie.status_filme,
            sinopse=movie.sinopse,
            url_poster=movie.url_poster,
            url_backdrop=movie.url_backdrop,
            generos=[
                genre.nome_genero
                for genre in movie.genres
            ],
            diretores=diretores,
            atores=atores,
            roteiristas=roteiristas,
            produtoras=[
                company.nome_produtora
                for company in movie.companies
            ],
            performance=performance,
            resumo_avaliacoes=resumo_avaliacoes,
            avaliacoes=avaliacoes,
        )
    
    @staticmethod
    async def create_movie(
        session: AsyncSession,
        data: MovieCreate,
    ) -> MovieDetailResponse:
        
        existing_movie = await MovieRepository.get_by_title(
        session=session,
        title=data.titulo,
        )
        
        if existing_movie is not None:
            raise ValueError(
                "Já existe um filme cadastrado com esse título."
            )
        
        movie_id = str(uuid4())

        movie = DimMovie(
            id_filme=movie_id,
            titulo=data.titulo.strip(),
            data_lancamento=data.data_lancamento,
            ano_lancamento=data.ano_lancamento,
            duracao_minutos=data.duracao_minutos,
            status_filme=data.status_filme,
            sinopse=data.sinopse,
            url_poster=data.url_poster,
            url_backdrop=data.url_backdrop,
        )

        movie.genres = await MovieService._resolve_genres(
            session=session,
            names=data.generos,
        )

        movie.companies = await MovieService._resolve_companies(
            session=session,
            names=data.produtoras,
        )

        people = []

        people.extend(
            await MovieService._resolve_people(
                session=session,
                names=data.diretores,
                person_type="Diretor",
            )
        )

        people.extend(
            await MovieService._resolve_people(
                session=session,
                names=data.atores,
                person_type="Ator",
            )
        )

        people.extend(
            await MovieService._resolve_people(
                session=session,
                names=data.roteiristas,
                person_type="Roteirista",
            )
        )

        movie.people = people

        try:
            await MovieRepository.create_movie(
                session=session,
                movie=movie,
            )

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        created_movie = await MovieRepository.get_by_id(
            session=session,
            movie_id=movie.sk_movie_id,
        )

        if created_movie is None:
            raise RuntimeError(
                "O filme foi criado, mas não pôde ser recuperado."
                )
        
        return MovieService._to_detail_response(
            created_movie
        )
    
    @staticmethod
    async def _resolve_genres(
        session: AsyncSession,
        names: list[str],
    ):
        genres = []

        normalized_names = MovieService._normalize_names(
            names
        )

        for name in normalized_names:
            genre = await MovieRepository.get_genre_by_name(
                session=session,
                name=name,
            )

            if genre is None:
                genre = await MovieRepository.create_genre(
                    session=session,
                    name=name,
                )

            genres.append(genre)

        return genres
    
    
    @staticmethod
    async def _resolve_companies(
        session: AsyncSession,
        names: list[str],
    ):
        companies = []

        normalized_names = MovieService._normalize_names(
            names
        )

        for name in normalized_names:
            company = (
                await MovieRepository.get_company_by_name(
                    session=session,
                    name=name,
                )
            )

            if company is None:
                company = (
                    await MovieRepository.create_company(
                        session=session,
                        name=name,
                    )
                )

            companies.append(company)

        return companies
    
    @staticmethod
    async def _resolve_people(
        session: AsyncSession,
        names: list[str],
        person_type: PersonType,
    ):
        people = []

        normalized_names = MovieService._normalize_names(
            names
        )

        for name in normalized_names:
            person = (
                await MovieRepository.get_person_by_name_and_type(
                    session=session,
                    name=name,
                    person_type=person_type,
                )
            )

            if person is None:
                person = await MovieRepository.create_person(
                    session=session,
                    name=name,
                    person_type=person_type,
                )

            people.append(person)

        return people
        
        
    @staticmethod
    def _normalize_names(
        names: list[str],
    ) -> list[str]:
        normalized = []
        seen = set()

        for name in names:
            clean_name = name.strip()

            if not clean_name:
                continue

            key = clean_name.lower()

            if key in seen:
                continue

            seen.add(key)
            normalized.append(clean_name)

        return normalized
    
    
    @staticmethod
    async def update_movie(
        session: AsyncSession,
        movie_id: str,
        data: MovieUpdate,
    ) -> MovieDetailResponse | None:
        movie = await MovieRepository.get_by_id(
            session=session,
            movie_id=movie_id,
        )

        if movie is None:
            return None

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if "titulo" in update_data:
            new_title = update_data["titulo"].strip()

            existing_movie = await MovieRepository.get_by_title(
                session=session,
                title=new_title,
            )

            if (
                existing_movie is not None
                and existing_movie.sk_movie_id != movie.sk_movie_id
            ):
                raise ValueError(
                    "Já existe um filme cadastrado com esse título."
                )

            movie.titulo = new_title

        simple_fields = [
            "data_lancamento",
            "ano_lancamento",
            "duracao_minutos",
            "status_filme",
            "sinopse",
            "url_poster",
            "url_backdrop",
        ]

        for field in simple_fields:
            if field in update_data:
                setattr(
                    movie,
                    field,
                    update_data[field],
                )

        if "generos" in update_data:
            movie.genres = await MovieService._resolve_genres(
                session=session,
                names=update_data["generos"] or [],
            )

        if "produtoras" in update_data:
            movie.companies = await MovieService._resolve_companies(
                session=session,
                names=update_data["produtoras"] or [],
            )

        people_changed = any(
            field in update_data
            for field in (
                "diretores",
                "atores",
                "roteiristas",
            )
        )

        if people_changed:
            current_diretores = [
                person.nome_pessoa
                for person in movie.people
                if person.tipo_pessoa == "Diretor"
            ]

            current_atores = [
                person.nome_pessoa
                for person in movie.people
                if person.tipo_pessoa == "Ator"
            ]

            current_roteiristas = [
                person.nome_pessoa
                for person in movie.people
                if person.tipo_pessoa == "Roteirista"
            ]

            diretores = update_data.get(
                "diretores",
                current_diretores,
            )

            atores = update_data.get(
                "atores",
                current_atores,
            )

            roteiristas = update_data.get(
                "roteiristas",
                current_roteiristas,
            )

            people = []

            people.extend(
                await MovieService._resolve_people(
                    session=session,
                    names=diretores or [],
                    person_type="Diretor",
                )
            )

            people.extend(
                await MovieService._resolve_people(
                    session=session,
                    names=atores or [],
                    person_type="Ator",
                )
            )

            people.extend(
                await MovieService._resolve_people(
                    session=session,
                    names=roteiristas or [],
                    person_type="Roteirista",
                )
            )

            movie.people = people

        try:
            await MovieRepository.update_movie(
                session=session,
                movie=movie,
            )

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        updated_movie = await MovieRepository.get_by_id(
            session=session,
            movie_id=movie.sk_movie_id,
        )

        if updated_movie is None:
            raise RuntimeError(
                "O filme foi atualizado, mas não pôde ser recuperado."
            )

        return MovieService._to_detail_response(
            updated_movie
        )
        
        
    @staticmethod
    async def delete_movie(
        session: AsyncSession,
        movie_id: str,
    ) -> bool:
        movie = await MovieRepository.get_by_id(
            session=session,
            movie_id=movie_id,
        )

        if movie is None:
            return False

        try:
            await MovieRepository.delete_movie(
                session=session,
                movie=movie,
            )

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        return True
    
    
    @staticmethod
    async def create_review(
        session: AsyncSession,
        movie_id: str,
        data: ReviewCreate,
    ) -> ReviewResponse | None:
        movie = await MovieRepository.get_by_id(
            session=session,
            movie_id=movie_id,
        )

        if movie is None:
            return None

        review = MovieReview(
            sk_movie_id=movie.sk_movie_id,
            nome=data.nome.strip(),
            nota=data.nota,
            comentario=data.comentario.strip(),
        )

        try:
            await MovieRepository.create_review(
                session=session,
                review=review,
            )

            count, average = await MovieRepository.get_review_stats(
                session=session,
                movie_id=movie.sk_movie_id,
            )

            await MovieRepository.save_review_summary(
                session=session,
                movie_id=movie.sk_movie_id,
                count=count,
                average=average,
            )

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        await session.refresh(review)

        return ReviewResponse.model_validate(review)
        