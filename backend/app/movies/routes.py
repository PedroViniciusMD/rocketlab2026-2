from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.movies.schemas import (
    MovieCreate,
    MovieDetailResponse,
    MovieListResponse,
)
from app.movies.service import MovieService

router = APIRouter()

@router.get(
    "",
    response_model=MovieListResponse,
)
async def list_movies(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
    ),
    session: AsyncSession = Depends(get_db),
) -> MovieListResponse:
    return await MovieService.list_movies(
        session=session,
        page=page,
        page_size=page_size,
        search=search,
    )


@router.get(
    "/{movie_id}",
    response_model=MovieDetailResponse,
)
async def get_movie(
    movie_id: str,
    session: AsyncSession = Depends(get_db),
) -> MovieDetailResponse:
    movie = await MovieService.get_movie_by_id(
        session=session,
        movie_id=movie_id,
    )

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado.",
        )

    return movie


@router.post(
    "",
    response_model=MovieDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_movie(
    data: MovieCreate,
    session: AsyncSession = Depends(get_db),
) -> MovieDetailResponse:
    return await MovieService.create_movie(
        session=session,
        data=data,
    )