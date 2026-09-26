import type { MovieListItem } from "../../types/movie";

import "./MovieCard.css";

interface MovieCardProps {
  movie: MovieListItem;
}

export function MovieCard({ movie }: MovieCardProps) {
  return (
    <article className="movie-card">
      {movie.url_poster ? (
        <img
          className="movie-card__poster"
          src={movie.url_poster}
          alt={`Poster de ${movie.titulo}`}
        />
      ) : (
        <div className="movie-card__poster-placeholder">
          Sem imagem
        </div>
      )}

      <div className="movie-card__content">
        <h2 className="movie-card__title">
          {movie.titulo}
        </h2>

        <p className="movie-card__year">
          {movie.ano_lancamento ?? "Ano não informado"}
        </p>

        <p className="movie-card__genres">
          {movie.generos.length > 0
            ? movie.generos.join(", ")
            : "Gênero não informado"}
        </p>

        <p className="movie-card__rating">
          Nota:{" "}
          {movie.nota_media !== null
            ? movie.nota_media.toFixed(1)
            : "Sem avaliações"}
        </p>
      </div>
    </article>
  );
}