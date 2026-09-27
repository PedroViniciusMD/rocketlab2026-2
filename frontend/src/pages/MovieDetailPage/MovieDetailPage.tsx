import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { getMovieById } from "../../api/movies";

import "./MovieDetailPage.css";

export function MovieDetailPage() {
  const { movieId } = useParams();

  const {
    data: movie,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["movie", movieId],
    queryFn: () => getMovieById(movieId!),
    enabled: !!movieId,
  });

  if (isLoading) {
    return <p>Carregando filme...</p>;
  }

  if (isError || !movie) {
    return <p>Erro ao carregar o filme.</p>;
  }

  return (
    <main className="movie-detail-page">
      <Link
        to="/"
        className="movie-detail-page__back"
      >
        ← Voltar para o início do catálogo
      </Link>

      <section className="movie-detail">
        {movie.url_poster ? (
          <img
            className="movie-detail__poster"
            src={movie.url_poster}
            alt={`Poster de ${movie.titulo}`}
          />
        ) : (
          <div className="movie-detail__poster-placeholder">
            Sem imagem
          </div>
        )}

        <div className="movie-detail__content">
          <h1>{movie.titulo}</h1>

          <p>
            Ano:{" "}
            {movie.ano_lancamento ?? "Não informado"}
          </p>

          <p>
            Duração:{" "}
            {movie.duracao_minutos
              ? `${movie.duracao_minutos} min`
              : "Não informada"}
          </p>

          <p>
            Gêneros:{" "}
            {movie.generos.length > 0
              ? movie.generos.join(", ")
              : "Não informado"}
          </p>

          <p>
            Diretores:{" "}
            {movie.diretores.length > 0
              ? movie.diretores.join(", ")
              : "Não informado"}
          </p>

          <p>
            Produtoras:{" "}
            {movie.produtoras.length > 0
              ? movie.produtoras.join(", ")
              : "Não informado"}
          </p>

          <p>
            Atores:{" "}
            {movie.atores.length > 0
                ? movie.atores.join(", ")
                : "Não informado"}
          </p>

          <h2>Sinopse</h2>

          <p>
            {movie.sinopse ?? "Sinopse não disponível."}
          </p>
        
          <h2>Desempenho financeiro</h2>

          <p>
            Orçamento:{" "}
            {movie.performance?.orcamento_brl != null
                ? movie.performance.orcamento_brl.toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                })
                : "Não informado"}
          </p>

          <p>
            Receita:{" "}
            {movie.performance?.receita_brl != null
                ? movie.performance.receita_brl.toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                })
                : "Não informado"}
          </p>

          <p>
            Lucro:{" "}
            {movie.performance?.lucro_brl != null
                ? movie.performance.lucro_brl.toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                })
                : "Não informado"}
          </p>

          <h2>Avaliação dos usuários</h2>

          <p>
            Média:{" "}
            {movie.resumo_avaliacoes?.nota_media_usuarios
              ?.toFixed(1) ?? "Sem avaliações"}
          </p>

          <p>
            Quantidade de avaliações:{" "}
            {movie.resumo_avaliacoes
              ?.qtd_avaliacoes_usuarios ?? 0}
          </p>
        </div>
      </section>

      <section className="movie-reviews">
        <h2>Avaliações</h2>

        {movie.avaliacoes.length === 0 ? (
          <p>Este filme ainda não possui avaliações.</p>
        ) : (
          movie.avaliacoes.map((review) => (
            <article
              key={review.sk_movie_review_id}
              className="movie-review"
            >
              <div className="movie-review__header">
                <strong>{review.nome}</strong>

                <span>
                  Nota: {review.nota.toFixed(1)}
                </span>
              </div>

              <p>{review.comentario}</p>
            </article>
          ))
        )}
      </section>
    </main>
  );
}