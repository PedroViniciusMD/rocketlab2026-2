import { useQuery } from "@tanstack/react-query";

import { getMovies } from "../../api/movies";
import { MovieCard } from "../../components/MovieCard/MovieCard";

import "./MoviesPage.css";

export function MoviesPage() {
  const {
    data,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["movies", 1],
    queryFn: () => getMovies(1, 20),
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
        <h1>RocketFlix</h1>

        <p>
         Encontre seu próximo filme favorito entre {data?.total} opções.
        </p>
      </header>

      <section className="movies-grid">
        {data?.items.map((movie) => (
          <MovieCard
            key={movie.sk_movie_id}
            movie={movie}
          />
        ))}
      </section>
    </main>
  );
}