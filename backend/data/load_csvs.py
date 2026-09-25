import asyncio
import csv
from datetime import date
from pathlib import Path

from sqlalchemy import insert

from app.db.session import AsyncSessionLocal
from app.movies.models import (
    DimCompany,
    DimGenre,
    DimMovie,
    DimPerson,
    DimReview,
    FactMoviePerformance,
    MovieReview,
    bridge_movie_company,
    bridge_movie_genre,
    bridge_movie_person,
)

""" Este arquivo é responsável por carregar os csvs disponibilizados usando AsyncSessionLocal
    e tratando valores nulos permitidos pelos models
"""

DATA_DIR = Path(__file__).resolve().parent / "raw"


def empty_to_none(value: str | None):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def to_int(value: str | None):
    value = empty_to_none(value)

    if value is None:
        return None

    return int(float(value))


def to_float(value: str | None):
    value = empty_to_none(value)

    if value is None:
        return None

    return float(value)


def to_date(value: str | None):
    value = empty_to_none(value)

    if value is None:
        return None

    return date.fromisoformat(value)


def read_csv(filename: str):
    path = DATA_DIR / filename

    with path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


async def load_dim_movies(session):
    rows = read_csv("dim_movies.csv")

    data = []

    for row in rows:
        data.append(
            {
                "sk_movie_id": row["sk_movie_id"],
                "id_filme": row["id_filme"],
                "titulo": row["titulo"],
                "data_lancamento": to_date(row["data_lancamento"]),
                "ano_lancamento": to_int(row["ano_lancamento"]),
                "duracao_minutos": to_int(row["duracao_minutos"]),
                "status_filme": empty_to_none(row["status_filme"]),
                "sinopse": empty_to_none(row["sinopse"]),
                "url_poster": empty_to_none(row["url_poster"]),
                "url_backdrop": empty_to_none(row["url_backdrop"]),
            }
        )

    await session.execute(insert(DimMovie), data)

    print(f"dim_movies: {len(data)} registros")


async def load_dim_genres(session):
    rows = read_csv("dim_genres.csv")

    data = [
        {
            "sk_genre_id": row["sk_genre_id"],
            "nome_genero": row["nome_genero"],
        }
        for row in rows
    ]

    await session.execute(insert(DimGenre), data)

    print(f"dim_genres: {len(data)} registros")


async def load_dim_companies(session):
    rows = read_csv("dim_companies.csv")

    data = [
        {
            "sk_company_id": row["sk_company_id"],
            "nome_produtora": row["nome_produtora"],
        }
        for row in rows
    ]

    await session.execute(insert(DimCompany), data)

    print(f"dim_companies: {len(data)} registros")


async def load_dim_people(session):
    rows = read_csv("dim_people.csv")

    data = [
        {
            "sk_person_id": row["sk_person_id"],
            "nome_pessoa": row["nome_pessoa"],
            "tipo_pessoa": row["tipo_pessoa"],
        }
        for row in rows
    ]

    await session.execute(insert(DimPerson), data)

    print(f"dim_people: {len(data)} registros")


async def load_fact_movies_performance(session):
    rows = read_csv("fact_movies_performance.csv")

    data = []

    for row in rows:
        data.append(
            {
                "sk_movie_id": row["sk_movie_id"],
                "orcamento_usd": to_float(row["orcamento_usd"]),
                "receita_usd": to_float(row["receita_usd"]),
                "lucro_usd": to_float(row["lucro_usd"]) or 0,
                "orcamento_brl": to_float(row["orcamento_brl"]),
                "receita_brl": to_float(row["receita_brl"]),
                "lucro_brl": to_float(row["lucro_brl"]) or 0,
                "popularidade": to_float(row["popularidade"]),
                "nota_tmdb": to_float(row["nota_tmdb"]),
                "qtd_tmdb": to_int(row["qtd_tmdb"]),
                "nota_imdb": to_float(row["nota_imdb"]),
                "qtd_imdb": to_int(row["qtd_imdb"]),
            }
        )

    await session.execute(
        insert(FactMoviePerformance),
        data,
    )

    print(
        "fact_movies_performance:"
        f" {len(data)} registros"
    )


async def load_movie_reviews(session):
    rows = read_csv("movies_reviews.csv")

    data = []

    for row in rows:
        data.append(
            {
                "sk_movie_review_id": row["sk_movie_review_id"],
                "sk_movie_id": row["sk_movie_id"],
                "nome": row["nome"],
                "nota": float(row["nota"]),
                "comentario": row["comentario"],
            }
        )

    await session.execute(insert(MovieReview), data)

    print(f"movie_reviews: {len(data)} registros")


async def load_dim_reviews(session):
    rows = read_csv("dim_reviews.csv")

    data = []

    for row in rows:
        data.append(
            {
                "sk_review_id": row["sk_review_id"],
                "sk_movie_id": row["sk_movie_id"],
                "qtd_avaliacoes_usuarios": to_int(
                    row["qtd_avaliacoes_usuarios"]
                )
                or 0,
                "nota_media_usuarios": to_float(
                    row["nota_media_usuarios"]
                ),
            }
        )

    await session.execute(insert(DimReview), data)

    print(f"dim_reviews: {len(data)} registros")


async def load_bridge_movie_genre(session):
    rows = read_csv("bridge_movie_genre.csv")

    data = [
        {
            "sk_movie_id": row["sk_movie_id"],
            "sk_genre_id": row["sk_genre_id"],
        }
        for row in rows
    ]

    await session.execute(
        insert(bridge_movie_genre),
        data,
    )

    print(f"bridge_movie_genre: {len(data)} registros")


async def load_bridge_movie_company(session):
    rows = read_csv("bridge_movie_company.csv")

    data = [
        {
            "sk_movie_id": row["sk_movie_id"],
            "sk_company_id": row["sk_company_id"],
        }
        for row in rows
    ]

    await session.execute(
        insert(bridge_movie_company),
        data,
    )

    print(
        "bridge_movie_company:"
        f" {len(data)} registros"
    )


async def load_bridge_movie_person(session):
    rows = read_csv("bridge_movie_person.csv")

    data = [
        {
            "sk_movie_id": row["sk_movie_id"],
            "sk_person_id": row["sk_person_id"],
        }
        for row in rows
    ]

    await session.execute(
        insert(bridge_movie_person),
        data,
    )

    print(f"bridge_movie_person: {len(data)} registros")


async def main():
    async with AsyncSessionLocal() as session:
        try:
            await load_dim_movies(session)
            await load_dim_genres(session)
            await load_dim_companies(session)
            await load_dim_people(session)

            await load_fact_movies_performance(session)
            await load_movie_reviews(session)
            await load_dim_reviews(session)

            await load_bridge_movie_genre(session)
            await load_bridge_movie_company(session)
            await load_bridge_movie_person(session)

            await session.commit()

            print("\nCarga concluída com sucesso.")

        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())