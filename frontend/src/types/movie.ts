export interface MovieListItem {
  sk_movie_id: string;
  titulo: string;
  ano_lancamento: number | null;
  url_poster: string | null;
  generos: string[];
  nota_media: number | null;
}

export interface MovieListResponse {
  items: MovieListItem[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}