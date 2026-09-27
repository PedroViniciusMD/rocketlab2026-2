import { Route, Routes } from "react-router-dom";

import { MoviesPage } from "./pages/MoviesPage/MoviesPage";
import { MovieDetailPage } from "./pages/MovieDetailPage/MovieDetailPage";
import { MovieCreatePage } from "./pages/MovieCreatePage/MovieCreatePage";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<MoviesPage />}
      />

      <Route
        path="/movies/new"
        element={<MovieCreatePage />}
      />

      <Route
        path="/movies/:movieId"
        element={<MovieDetailPage />}
      />
    </Routes>
  );
}

export default App;