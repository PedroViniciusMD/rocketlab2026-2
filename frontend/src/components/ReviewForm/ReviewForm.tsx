import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createReview } from "../../api/movies";

import "./ReviewForm.css";

interface ReviewFormProps {
  movieId: string;
}

export function ReviewForm({
  movieId,
}: ReviewFormProps) {
  const queryClient = useQueryClient();

  const [nome, setNome] = useState("");
  const [nota, setNota] = useState("");
  const [comentario, setComentario] = useState("");

  const mutation = useMutation({
    mutationFn: () =>
      createReview(movieId, {
        nome,
        nota: Number(nota),
        comentario,
      }),

    onSuccess: () => {
      setNome("");
      setNota("");
      setComentario("");

      queryClient.invalidateQueries({
        queryKey: ["movie", movieId],
      });
    },
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();

    mutation.mutate();
  }

  return (
    <section className="review-form">
      <h2>Avaliar este filme</h2>

      <form onSubmit={handleSubmit}>
        <div className="review-form__field">
          <label htmlFor="nome">
            Nome
          </label>

          <input
            id="nome"
            type="text"
            value={nome}
            onChange={(event) =>
              setNome(event.target.value)
            }
            required
            maxLength={120}
          />
        </div>

        <div className="review-form__field">
          <label htmlFor="nota">
            Nota
          </label>

          <input
            id="nota"
            type="number"
            min="0"
            max="10"
            step="0.1"
            value={nota}
            onChange={(event) =>
              setNota(event.target.value)
            }
            required
          />
        </div>

        <div className="review-form__field">
          <label htmlFor="comentario">
            Comentário
          </label>

          <textarea
            id="comentario"
            value={comentario}
            onChange={(event) =>
              setComentario(event.target.value)
            }
            required
            maxLength={4000}
          />
        </div>

        {mutation.isError && (
          <p className="review-form__error">
            {mutation.error.message}
          </p>
        )}

        {mutation.isSuccess && (
          <p className="review-form__success">
            Avaliação enviada com sucesso.
          </p>
        )}

        <button
          type="submit"
          disabled={mutation.isPending}
        >
          {mutation.isPending
            ? "Enviando..."
            : "Enviar avaliação"}
        </button>
      </form>
    </section>
  );
}