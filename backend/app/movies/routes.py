from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.movies.schemas import (
    MovieCreate,
    MovieDetailResponse,
    MovieListResponse,
    MovieUpdate,
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
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
    try:
        return await MovieService.create_movie(
            session=session,
            data=data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error
        

@router.patch(
    "/{movie_id}",
    response_model=MovieDetailResponse,
)
async def update_movie(
    movie_id: str,
    data: MovieUpdate,
    session: AsyncSession = Depends(get_db),
) -> MovieDetailResponse:
    try:
        movie = await MovieService.update_movie(
            session=session,
            movie_id=movie_id,
            data=data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado.",
        )

    return movie


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie(
    movie_id: str,
    session: AsyncSession = Depends(get_db),
) -> None:
    deleted = await MovieService.delete_movie(
        session=session,
        movie_id=movie_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado.",
        )
        
        
@router.post(
    "/{movie_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    movie_id: str,
    data: ReviewCreate,
    session: AsyncSession = Depends(get_db),
) -> ReviewResponse:
    review = await MovieService.create_review(
        session=session,
        movie_id=movie_id,
        data=data,
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme não encontrado.",
        )

    return review


@router.patch(
    "/{movie_id}/reviews/{review_id}",
    response_model=ReviewResponse,
)
async def update_review(
    movie_id: str,
    review_id: str,
    data: ReviewUpdate,
    session: AsyncSession = Depends(get_db),
) -> ReviewResponse:
    review = await MovieService.update_review(
        session=session,
        movie_id=movie_id,
        review_id=review_id,
        data=data,
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Filme ou avaliação não encontrado.",
        )

    return review
