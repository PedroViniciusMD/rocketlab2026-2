import type { MovieCreate, MovieUpdate, MovieListResponse, MovieDetail, Review, ReviewCreate } from "../types/movie";
import { fetchWithTimeout } from "./client";

const API_URL = "http://localhost:8000/api/v1";

export async function getMovies(
  page = 1,
  pageSize = 20,
  search?: string
): Promise<MovieListResponse> {
  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  });

  if (search) {
    params.set("search", search);
  }

  const response = await fetchWithTimeout(
    `${API_URL}/movies?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Erro ao carregar filmes.");
  }

  return response.json();
}

export async function getMovieById(
  movieId: string
): Promise<MovieDetail> {
  const response = await fetchWithTimeout(
    `${API_URL}/movies/${movieId}`
  );

  if (!response.ok) {
    throw new Error("Erro ao carregar o filme.");
  }

  return response.json();
}

export async function createReview(
  movieId: string,
  data: ReviewCreate
): Promise<Review> {
  const response = await fetchWithTimeout(
    `${API_URL}/movies/${movieId}/reviews`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const errorData = await response.json();

    throw new Error(
      errorData.detail ?? "Erro ao criar avaliação."
    );
  }

  return response.json();
}

export async function createMovie(
  data: MovieCreate
): Promise<MovieDetail> {
  const response = await fetchWithTimeout(
    `${API_URL}/movies`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const errorData = await response.json();

    throw new Error(
      errorData.detail ?? "Erro ao cadastrar filme."
    );
  }

  return response.json();
}

export async function updateMovie(
  movieId: string,
  data: MovieUpdate
): Promise<MovieDetail> {
  const response = await fetchWithTimeout(
    `${API_URL}/movies/${movieId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const errorData = await response.json();

    throw new Error(
      errorData.detail ?? "Erro ao atualizar filme."
    );
  }

  return response.json();
}

export async function deleteMovie(
  movieId: string
): Promise<void> {
  const response = await fetchWithTimeout(
    `${API_URL}/movies/${movieId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    let message = "Erro ao excluir filme.";

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // dando catch no response sem JSON
    }

    throw new Error(message);
  }
}