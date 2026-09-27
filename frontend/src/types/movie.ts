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

export interface Performance {
  orcamento_usd: number | null;
  receita_usd: number | null;
  lucro_usd: number;
  orcamento_brl: number | null;
  receita_brl: number | null;
  lucro_brl: number;
  popularidade: number | null;
  nota_tmdb: number | null;
  qtd_tmdb: number | null;
  nota_imdb: number | null;
  qtd_imdb: number | null;
}

export interface ReviewSummary {
  qtd_avaliacoes_usuarios: number;
  nota_media_usuarios: number | null;
}

export interface Review {
  sk_movie_review_id: string;
  nome: string;
  nota: number;
  comentario: string;
  created_at: string;
}

export interface MovieDetail {
  sk_movie_id: string;
  id_filme: string;
  titulo: string;
  data_lancamento: string | null;
  ano_lancamento: number | null;
  duracao_minutos: number | null;
  status_filme: string | null;
  sinopse: string | null;
  url_poster: string | null;
  url_backdrop: string | null;

  generos: string[];
  diretores: string[];
  atores: string[];
  roteiristas: string[];
  produtoras: string[];

  performance: Performance | null;
  resumo_avaliacoes: ReviewSummary | null;
  avaliacoes: Review[];
}

export interface MovieCreate {
  titulo: string;
  data_lancamento: string | null;
  ano_lancamento: number | null;
  duracao_minutos: number | null;
  status_filme: string | null;
  sinopse: string | null;
  url_poster: string | null;
  url_backdrop: string | null;
  generos: string[];
  diretores: string[];
  atores: string[];
  roteiristas: string[];
  produtoras: string[];
}

export interface MovieUpdate {
  titulo?: string;
  ano_lancamento?: number | null;
  duracao_minutos?: number | null;
  status_filme?: string | null;
  sinopse?: string | null;
  url_poster?: string | null;
  url_backdrop?: string | null;
  generos?: string[];
  diretores?: string[];
  atores?: string[];
  roteiristas?: string[];
  produtoras?: string[];
}

export interface ReviewCreate {
  nome: string;
  nota: number;
  comentario: string;
}