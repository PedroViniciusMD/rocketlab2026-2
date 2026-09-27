import { Route, Routes } from "react-router-dom";

import { MoviesPage } from "./pages/MoviesPage/MoviesPage";
import { MovieDetailPage } from "./pages/MovieDetailPage/MovieDetailPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<MoviesPage />} />
      <Route
        path="/movies/:movieId"
        element={<MovieDetailPage />}
      />
    </Routes>
  );
}

export default App;