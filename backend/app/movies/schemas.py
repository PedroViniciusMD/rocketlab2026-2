from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# Responses
class GenreResponse(BaseModel): #
    model_config = ConfigDict(from_attributes=True)

    sk_genre_id: str
    nome_genero: str


class PersonResponse(BaseModel): #
    model_config = ConfigDict(from_attributes=True)

    sk_person_id: str
    nome_pessoa: str
    tipo_pessoa: str


class CompanyResponse(BaseModel): #
    model_config = ConfigDict(from_attributes=True)

    sk_company_id: str
    nome_produtora: str
    

class PerformanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orcamento_usd: float | None = None
    receita_usd: float | None = None
    lucro_usd: float = 0

    orcamento_brl: float | None = None
    receita_brl: float | None = None
    lucro_brl: float = 0

    popularidade: float | None = None

    nota_tmdb: float | None = None
    qtd_tmdb: int | None = None

    nota_imdb: float | None = None
    qtd_imdb: int | None = None
    

class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sk_movie_review_id: str
    nome: str
    nota: float
    comentario: str
    created_at: datetime
    

class ReviewSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    qtd_avaliacoes_usuarios: int
    nota_media_usuarios: float | None = None
    

class MovieDetailResponse(BaseModel):
    sk_movie_id: str
    id_filme: str

    titulo: str

    data_lancamento: date | None = None
    ano_lancamento: int | None = None
    duracao_minutos: int | None = None

    status_filme: str | None = None
    sinopse: str | None = None

    url_poster: str | None = None
    url_backdrop: str | None = None

    generos: list[str] = Field(default_factory=list)

    diretores: list[str] = Field(default_factory=list)
    atores: list[str] = Field(default_factory=list)
    roteiristas: list[str] = Field(default_factory=list)

    produtoras: list[str] = Field(default_factory=list)

    performance: PerformanceResponse | None = None

    resumo_avaliacoes: ReviewSummaryResponse | None = None

    avaliacoes: list[ReviewResponse] = Field(
        default_factory=list,
    )


class MovieListItem(BaseModel):
    sk_movie_id: str
    titulo: str
    ano_lancamento: int | None = None
    url_poster: str | None = None

    generos: list[str] = Field(
        default_factory=list,
    )

    nota_media: float | None = None
    
    
class MovieListResponse(BaseModel): #Paginação
    items: list[MovieListItem]

    page: int
    page_size: int
    total: int
    total_pages: int
    
    
# Creates
class MovieCreate(BaseModel):
    titulo: str = Field(
        min_length=1,
        max_length=500,
    )

    data_lancamento: date | None = None

    ano_lancamento: int | None = Field(
        default=None,
        ge=1888,
    )

    duracao_minutos: int | None = Field(
        default=None,
        gt=0,
    )

    status_filme: str | None = Field(
        default=None,
        max_length=50,
    )

    sinopse: str | None = Field(
        default=None,
        max_length=4000,
    )

    url_poster: str | None = Field(
        default=None,
        max_length=2048,
    )

    url_backdrop: str | None = Field(
        default=None,
        max_length=2048,
    )

    generos: list[str] = Field(
        default_factory=list,
    )

    diretores: list[str] = Field(
        default_factory=list,
    )

    atores: list[str] = Field(
        default_factory=list,
    )

    roteiristas: list[str] = Field(
        default_factory=list,
    )

    produtoras: list[str] = Field(
        default_factory=list,
    )
    

class ReviewCreate(BaseModel):
    nome: str = Field(
        min_length=1,
        max_length=120,
    )

    nota: float = Field(
        ge=0,
        le=10,
    )

    comentario: str = Field(
        min_length=1,
        max_length=4000,
    )
    
# Updates
class MovieUpdate(BaseModel):
    titulo: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )

    data_lancamento: date | None = None

    ano_lancamento: int | None = Field(
        default=None,
        ge=1888,
    )

    duracao_minutos: int | None = Field(
        default=None,
        gt=0,
    )

    status_filme: str | None = Field(
        default=None,
        max_length=50,
    )

    sinopse: str | None = Field(
        default=None,
        max_length=4000,
    )

    url_poster: str | None = Field(
        default=None,
        max_length=2048,
    )

    url_backdrop: str | None = Field(
        default=None,
        max_length=2048,
    )

    generos: list[str] | None = None

    diretores: list[str] | None = None

    atores: list[str] | None = None

    roteiristas: list[str] | None = None

    produtoras: list[str] | None = None


class ReviewUpdate(BaseModel):
    nota: float | None = Field(
        default=None,
        ge=0,
        le=10,
    )

    comentario: str | None = Field(
        default=None,
        min_length=1,
        max_length=4000,
    )
 