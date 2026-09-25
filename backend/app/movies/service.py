from sqlalchemy.ext.asyncio import AsyncSession

from app.movies.models import DimMovie
from app.movies.repository import MovieRepository
from app.movies.schemas import (
    MovieDetailResponse,
    MovieListItem,
    MovieListResponse,
    PerformanceResponse,
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
        