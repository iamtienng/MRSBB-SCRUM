import React from "react";
import { useNavigate } from "react-router-dom";

const MovieList = (props) => {
  let navigate = useNavigate();
  const navigateToMoviePage = (movie) => {
    // console.log(movie.movieId);
    let path = `/movie/${movie.movieId}`;
    navigate(path);
  };
  return (
    <>
      {props.movies.map((movie) => (
        <div
          className="image-container d-flex justify-content-start m-3"
          onClick={() => {
            navigateToMoviePage(movie);
          }}
        >
          <img
            src={movie.posterUrl}
            style={{ width: "300px", height: "500px" }}
            alt="movie"
          ></img>
          <div className="overlay d-flex align-items-center justify-content-center">
            {movie.title}
          </div>
        </div>
      ))}
    </>
  );
};

export default MovieList;
