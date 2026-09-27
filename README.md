# RocketLab 2026.2 — RocketFlix
 
Projeto desenvolvido para a atividade DEV do RocketLab 2026.2.
 
A aplicação consiste em um sistema de catálogo e avaliação de filmes. O sistema permite visualizar o catálogo, consultar informações detalhadas dos filmes, cadastrar, editar e excluir filmes, pesquisar títulos e registrar avaliações.
 
## Tecnologias utilizadas
 
**Frontend**
- React
- TypeScript
- Vite
- TanStack Query
- React Router DOM
- HTML / CSS

**Backend**
- Python
- FastAPI
- SQLAlchemy 2.0
- Alembic
- SQLite
- Pydantic
## Estrutura do projeto
 
```text 
rocketlab2026-2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── db/
│   │   └── movies/
│   │       ├── models.py
│   │       ├── repository.py
│   │       ├── routes.py
│   │       ├── schemas.py
│   │       └── service.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   └── load_csvs.py
│   │
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│  
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
|   |   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── types/
│   │   ├── App.tsx
|   |   ├── App.css/
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
└── README.md
```
 
## Funcionalidades
 
A aplicação implementa:
 
- cadastro de novos filmes;
- catálogo paginado de filmes;
- busca de filmes por título;
- visualização dos detalhes de cada filme;
- visualização das avaliações associadas ao filme;
- visualização da média das avaliações;
- edição individual de filmes;
- exclusão individual de filmes;
- criação de novas avaliações;
- atualização automática da média de avaliações;
- prevenção de múltiplas avaliações de um mesmo usuário para o mesmo filme;
- interface responsiva;
- cache e gerenciamento das requisições com TanStack Query.
 
## Banco de dados
 
O projeto utiliza SQLite e SQLAlchemy 2.0. O modelo segue uma estrutura baseada em dimensões, fatos e tabelas de associação.
 
As tabelas são criadas exclusivamente pelas migrations do Alembic.

O banco padrão é `backend/rocketlab.db`. A configuração da conexão fica no arquivo `.env`:
 
```env
DATABASE_URL=sqlite+aiosqlite:///./rocketlab.db
```
 
> Como o caminho do SQLite é relativo, o backend deve ser iniciado a partir da pasta `backend`. Caso contrário, um novo arquivo `rocketlab.db` pode ser criado em outro diretório.
 
## Dados iniciais
 
Os arquivos CSV fornecidos para a atividade são armazenados em `backend/data/raw/`. A atividade disponibiliza os CSVs como fonte inicial para população das tabelas.
 
Para facilitar a carga inicial foi criado o script `backend/data/load_csvs.py`, responsável por carregar os CSVs e persistir os registros no banco SQLite.
 
Durante a carga também é realizado um tratamento simples dos títulos dos filmes para remover aspas externas existentes em alguns registros dos CSVs. Exemplo: `"""blessed"""` é armazenado como `blessed`. Aspas internas que fazem parte legitimamente do título não são removidas.
 
### Observação sobre as avaliações importadas
 
A base possui duas representações relacionadas às avaliações:
 
- `movie_reviews`: avaliações individuais dos usuários;
- `dim_reviews`: resumo das avaliações de cada filme.

Foi identificado que alguns filmes possuem valores em `dim_reviews` que não correspondem exatamente às avaliações presentes em `movie_reviews`. Por esse motivo, ao cadastrar uma nova avaliação para um filme, o backend recalcula o resumo utilizando os registros reais existentes em `movie_reviews`
 
## Regra para avaliações duplicadas
 
Um mesmo nome não pode registrar mais de uma avaliação para o mesmo filme. Por exemplo, caso Pedro já tenha avaliado determinado filme, uma nova tentativa utilizando `Pedro`, `pedro` ou `PEDRO` é considerada uma avaliação duplicada.
 
O backend retorna uma mensagem semelhante a: *"Você Pedro já avaliou esse filme."*
 
A comparação é realizada de forma case-insensitive, mas o nome original informado pelo usuário é preservado no banco.

## Edição de filmes
 
A atualização dos filmes é realizada utilizando `PATCH /api/v1/movies/{movie_id}`. Foi escolhido PATCH porque a operação representa uma atualização de dados de um recurso existente.
 
## Rotas da API
 
A API utiliza o prefixo `/api/v1`.
 
### Filmes
 
| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/v1/movies` | Lista filmes de forma paginada |
| GET | `/api/v1/movies?search=título` | Busca filmes pelo título |
| GET | `/api/v1/movies/{movie_id}` | Retorna os detalhes de um filme |
| POST | `/api/v1/movies` | Cadastra um novo filme |
| PATCH | `/api/v1/movies/{movie_id}` | Atualiza um filme |
| DELETE | `/api/v1/movies/{movie_id}` | Exclui um filme |
 
### Avaliações
 
| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/movies/{movie_id}/reviews` | Adiciona uma avaliação ao filme |
 
> A aplicação final não utiliza uma rota PATCH de reviews.
 
### Outros endpoints
 
| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica se a API está funcionando |
| GET | `/docs` | Documentação Swagger gerada pelo FastAPI |
 
## Como executar o projeto
 
### Pré-requisitos
 
- Python 3.11 ou superior
- Node.js
- npm
- Git
### 1. Clonar o repositório
 
```bash
git clone <URL_DO_REPOSITORIO>
cd rocketlab2026-2
```
 
### 2. Configurar o backend
 
```bash
cd backend
python3 -m venv .venv
```
 
Ative o ambiente virtual:
 
```bash
# macOS / Linux
source .venv/bin/activate
 
# Windows
.venv\Scripts\activate
```
 
Instale as dependências:
 
```bash
pip install -e ".[dev]"
```
 
Crie o arquivo `.env` com base no exemplo:
 
```bash
cp .env.example .env
```
 
A configuração padrão utiliza:
 
```env
DATABASE_URL=sqlite+aiosqlite:///./rocketlab.db
```
 
### 3. Criar as tabelas
 
Ainda dentro de `backend`, execute:
 
```bash
alembic upgrade head
```
 
### 4. Adicionar os arquivos CSV
 
Coloque os arquivos fornecidos para a atividade dentro de `backend/data/raw/`:
 
```text
backend/
└── data/
    ├── raw/
    │   ├── dim_movies.csv
    │   ├── dim_genres.csv
    │   ├── dim_companies.csv
    │   ├── dim_people.csv
    │   └── ...
    └── load_csvs.py
```
 
### 5. Carregar os dados
 
Ainda dentro da pasta `backend`, execute:
 
```bash
python -m data.load_csvs
```
 
O script lê os CSVs presentes em `data/raw/` e popula as tabelas correspondentes.
 
### 6. Iniciar o backend
 
É importante executar o comando estando dentro de `backend/`:
 
```bash
uvicorn app.main:app --reload
```
 
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health check: http://localhost:8000/health
### 7. Configurar o frontend
 
Abra outro terminal e, a partir da raiz do projeto:
 
```bash
cd frontend
npm install
```
 
### 8. Iniciar o frontend
 
```bash
npm run dev
```
 
O Vite exibirá no terminal o endereço local da aplicação. Abra esse endereço no navegador. O backend deve permanecer executando simultaneamente em `http://localhost:8000`.
 
## Fluxo principal da aplicação
 
O catálogo inicial utiliza `GET /api/v1/movies`. O TanStack Query realiza a chamada à API e mantém os resultados em cache.
 
- A pesquisa por título utiliza o parâmetro `?search=`. A barra de busca possui **DEBOUNCE**, evitando uma nova requisição a cada tecla digitada.
- A paginação utiliza os parâmetros `?page=1&page_size=20`.
- Ao selecionar um filme, o frontend acessa `/movies/{movie_id}` e consulta os detalhes utilizando `GET /api/v1/movies/{movie_id}`.
 

## Decisões de implementação

- utilização de timeout nas requisições HTTP para evitar que o usuário fique aguardando indefinidamente em caso de falha ou lentidão da API;
- uso de `sk_movie_id` para identificar os filmes nas rotas individuais;
- títulos duplicados não podem ser cadastrados novamente pela aplicação;
- a comparação de títulos para novos cadastros desconsidera diferenças entre maiúsculas e minúsculas;
- um mesmo nome não pode avaliar o mesmo filme mais de uma vez;
- a média de avaliações é recalculada após a criação de uma nova review;
- alguns registros importados podem possuir médias inicialmente inconsistentes em `dim_reviews`;
- o frontend utiliza **debounce** na busca;
- as consultas e mutations são gerenciadas com TanStack Query;
- a interface foi organizada em componentes reutilizáveis;
