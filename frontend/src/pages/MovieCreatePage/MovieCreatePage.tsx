import { useState } from "react";
import type { FormEvent } from "react";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Link, useNavigate } from "react-router-dom";

import { createMovie } from "../../api/movies";

import "./MovieCreatePage.css";

export function MovieCreatePage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [titulo, setTitulo] = useState("");
  const [dataLancamento, setDataLancamento] = useState("");
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

  function parseList(value: string): string[] {
    return value
      .split(",")
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
  }

  const mutation = useMutation({
    mutationFn: () =>
      createMovie({
        titulo: titulo.trim(),

        data_lancamento:
          dataLancamento || null,

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

    onSuccess: (movie) => {
      queryClient.invalidateQueries({
        queryKey: ["movies"],
      });

      navigate(
        `/movies/${movie.sk_movie_id}`
      );
    },
  });

  function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    mutation.mutate();
  }

  return (
    <main className="movie-create-page">
      <Link
        to="/"
        className="movie-create-page__back"
      >
        ← Voltar para o catálogo
      </Link>

      <h1>Cadastrar filme</h1>

      <form
        className="movie-create-form"
        onSubmit={handleSubmit}
      >
        <div className="movie-create-form__field">
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

        <div className="movie-create-form__row">

          <div className="movie-create-form__field">
            <label htmlFor="ano_lancamento">
              Ano
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

          <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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

        <div className="movie-create-form__field">
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
          <p className="movie-create-form__error">
            {mutation.error.message}
          </p>
        )}

        <button
          type="submit"
          disabled={mutation.isPending}
        >
          {mutation.isPending
            ? "Cadastrando..."
            : "Cadastrar filme"}
        </button>
      </form>
    </main>
  );
}