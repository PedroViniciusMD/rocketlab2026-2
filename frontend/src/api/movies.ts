import type { MovieListResponse } from "../types/movie";

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

  const response = await fetch(
    `${API_URL}/movies?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Erro ao carregar filmes.");
  }

  return response.json();
}