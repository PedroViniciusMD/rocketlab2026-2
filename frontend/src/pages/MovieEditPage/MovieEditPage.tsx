import { useEffect, useState } from "react";
import type { FormEvent } from "react";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  getMovieById,
  updateMovie,
} from "../../api/movies";

import "./MovieEditPage.css";

export function MovieEditPage() {
  const { movieId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [titulo, setTitulo] = useState("");
  const [anoLancamento, setAnoLancamento] = useState("");
  const [duracaoMinutos, setDuracaoMinutos] = useState("");
  const [statusFilme, setStatusFilme] = useState("");
  const [sinopse, setSinopse] = useState("");
  const [urlPoster, setUrlPoster] = useState("");
  const [urlBackdrop, setUrlBackdrop] = useState("");

  const [generos, setGeneros] = useState("");
  const [diretores, setDiretores] = useState("");
  const [atores, setAtores] = useState("");
  const [roteiristas, setRoteiristas] = useState("");
  const [produtoras, setProdutoras] = useState("");

  const {
    data: movie,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["movie", movieId],
    queryFn: () => getMovieById(movieId!),
    enabled: !!movieId,
  });

  useEffect(() => {
    if (!movie) {
      return;
    }

    setTitulo(movie.titulo);

    setAnoLancamento(
      movie.ano_lancamento?.toString() ?? ""
    );

    setDuracaoMinutos(
      movie.duracao_minutos?.toString() ?? ""
    );

    setStatusFilme(movie.status_filme ?? "");
    setSinopse(movie.sinopse ?? "");
    setUrlPoster(movie.url_poster ?? "");
    setUrlBackdrop(movie.url_backdrop ?? "");

    setGeneros(movie.generos.join(", "));
    setDiretores(movie.diretores.join(", "));
    setAtores(movie.atores.join(", "));
    setRoteiristas(movie.roteiristas.join(", "));
    setProdutoras(movie.produtoras.join(", "));
  }, [movie]);

  function parseList(value: string): string[] {
    return value
      .split(",")
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
  }

  const mutation = useMutation({
    mutationFn: () =>
      updateMovie(movieId!, {
        titulo: titulo.trim(),

        ano_lancamento:
          anoLancamento
            ? Number(anoLancamento)
            : null,

        duracao_minutos:
          duracaoMinutos
            ? Number(duracaoMinutos)
            : null,

        status_filme:
          statusFilme.trim() || null,

        sinopse:
          sinopse.trim() || null,

        url_poster:
          urlPoster.trim() || null,

        url_backdrop:
          urlBackdrop.trim() || null,

        generos: parseList(generos),
        diretores: parseList(diretores),
        atores: parseList(atores),
        roteiristas: parseList(roteiristas),
        produtoras: parseList(produtoras),
      }),

    onSuccess: (updatedMovie) => {
      queryClient.invalidateQueries({
        queryKey: ["movies"],
      });

      queryClient.setQueryData(
        ["movie", movieId],
        updatedMovie
      );

      navigate(`/movies/${movieId}`);
    },
  });

  function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    mutation.mutate();
  }

  if (isLoading) {
    return <p>Carregando filme...</p>;
  }

  if (isError || !movie) {
    return <p>Erro ao carregar o filme.</p>;
  }

  return (
    <main className="movie-edit-page">
      <Link
        to={`/movies/${movieId}`}
        className="movie-edit-page__back"
      >
        ← Voltar para o filme
      </Link>

      <h1>Editar filme</h1>

      <form
        className="movie-edit-form"
        onSubmit={handleSubmit}
      >
        <div className="movie-edit-form__field">
          <label htmlFor="titulo">
            Título *
          </label>

          <input
            id="titulo"
            type="text"
            value={titulo}
            onChange={(event) =>
              setTitulo(event.target.value)
            }
            required
            maxLength={500}
          />
        </div>

        <div className="movie-edit-form__row">
          <div className="movie-edit-form__field">
            <label htmlFor="ano_lancamento">
              Ano de lançamento
            </label>

            <input
              id="ano_lancamento"
              type="number"
              min="1888"
              value={anoLancamento}
              onChange={(event) =>
                setAnoLancamento(
                  event.target.value
                )
              }
            />
          </div>

          <div className="movie-edit-form__field">
            <label htmlFor="duracao_minutos">
              Duração
            </label>

            <input
              id="duracao_minutos"
              type="number"
              min="1"
              placeholder="Minutos"
              value={duracaoMinutos}
              onChange={(event) =>
                setDuracaoMinutos(
                  event.target.value
                )
              }
            />
          </div>
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="status_filme">
            Status
          </label>

          <input
            id="status_filme"
            type="text"
            value={statusFilme}
            onChange={(event) =>
              setStatusFilme(event.target.value)
            }
            maxLength={50}
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="sinopse">
            Sinopse
          </label>

          <textarea
            id="sinopse"
            value={sinopse}
            onChange={(event) =>
              setSinopse(event.target.value)
            }
            maxLength={4000}
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="url_poster">
            URL do poster
          </label>

          <input
            id="url_poster"
            type="url"
            value={urlPoster}
            onChange={(event) =>
              setUrlPoster(event.target.value)
            }
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="url_backdrop">
            URL do backdrop
          </label>

          <input
            id="url_backdrop"
            type="url"
            value={urlBackdrop}
            onChange={(event) =>
              setUrlBackdrop(event.target.value)
            }
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="generos">
            Gêneros
          </label>

          <input
            id="generos"
            type="text"
            placeholder="Ação, Drama, Comédia"
            value={generos}
            onChange={(event) =>
              setGeneros(event.target.value)
            }
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="diretores">
            Diretores
          </label>

          <input
            id="diretores"
            type="text"
            placeholder="Diretor 1, Diretor 2"
            value={diretores}
            onChange={(event) =>
              setDiretores(event.target.value)
            }
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="atores">
            Atores
          </label>

          <input
            id="atores"
            type="text"
            placeholder="Ator 1, Ator 2"
            value={atores}
            onChange={(event) =>
              setAtores(event.target.value)
            }
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="roteiristas">
            Roteiristas
          </label>

          <input
            id="roteiristas"
            type="text"
            placeholder="Roteirista 1, Roteirista 2"
            value={roteiristas}
            onChange={(event) =>
              setRoteiristas(
                event.target.value
              )
            }
          />
        </div>

        <div className="movie-edit-form__field">
          <label htmlFor="produtoras">
            Produtoras
          </label>

          <input
            id="produtoras"
            type="text"
            placeholder="Produtora 1, Produtora 2"
            value={produtoras}
            onChange={(event) =>
              setProdutoras(
                event.target.value
              )
            }
          />
        </div>

        {mutation.isError && (
          <p className="movie-edit-form__error">
            {mutation.error.message}
          </p>
        )}

        <div className="movie-edit-form__actions">
          <Link
            to={`/movies/${movieId}`}
            className="movie-edit-form__cancel"
          >
            Cancelar
          </Link>

          <button
            type="submit"
            disabled={mutation.isPending}
          >
            {mutation.isPending
              ? "Salvando..."
              : "Salvar alterações"}
          </button>
        </div>
      </form>
    </main>
  );
}