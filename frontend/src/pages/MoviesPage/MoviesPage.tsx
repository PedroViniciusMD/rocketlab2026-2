import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { getMovies } from "../../api/movies";
import { MovieCard } from "../../components/MovieCard/MovieCard";
import { Pagination } from "../../components/Pagination/Pagination";

import "./MoviesPage.css";

export function MoviesPage() {
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1);
    }, 500);

    return () => {
      clearTimeout(timeout);
    };
  }, [search]);

  const {
    data,
    isLoading,
    isError,
  } = useQuery({
    queryKey: [
      "movies",
      page,
      debouncedSearch,
    ],
    queryFn: () =>
      getMovies(
        page,
        20,
        debouncedSearch
      ),
  });

  if (isLoading) {
    return <p>Carregando filmes...</p>;
  }

  if (isError) {
    return <p>Erro ao carregar filmes.</p>;
  }

  return (
    <main className="movies-page">
      <header className="movies-page__header">
        <h1>Catálogo de filmes</h1>

        <p>
          {data?.total} filmes encontrados
        </p>
      </header>

      <div className="movies-page__search">
        <input
          type="text"
          placeholder="Buscar filme..."
          value={search}
          onChange={(event) =>
            setSearch(event.target.value)
          }
        />
      </div>

      <section className="movies-grid">
        {data?.items.map((movie) => (
          <MovieCard
            key={movie.sk_movie_id}
            movie={movie}
          />
        ))}
      </section>

      <Pagination
        page={page}
        totalPages={data?.total_pages ?? 0}
        onPageChange={setPage}
      />
    </main>
  );
}