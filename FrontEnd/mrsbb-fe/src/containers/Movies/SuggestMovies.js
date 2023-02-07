import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { connect } from "react-redux";
import "./CSS/SuggestMovies.css";

import MovieList from "../../components/MovieList";
import Heading from "../../components/Heading";

const SuggestMovies = ({ isAuthenticated, user }) => {
  const [userID, setUserID] = useState(-1);
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const getMovieRequest = async () => {
      const url = `http://127.0.0.1:8000/movie/pred-top-ten`;
      const response = await fetch(url, {
        method: "POST",
        header: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ userID: userID }),
      });
      const responseJson = await response.json();

      if (responseJson) {
        let movies_data_ordered = [];
        for (let i in responseJson.movies_order) {
          movies_data_ordered.push(
            responseJson.movies_data.find(
              (movie) => movie.movieId === responseJson.movies_order[i]
            )
          );
        }
        setMovies(movies_data_ordered);
      }
    };
    setUserID(user?.id);
    getMovieRequest();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userID]);

  if (isAuthenticated === false) {
    return <Navigate replace to="/login" />;
  }

  return (
    <div className="container-fluid movie-app">
      <div className="d-flex justify-content-between mt-4 mb-4 ">
        <Heading heading="Top 10 Recommended Movies For You" />
      </div>
      <div className="row row-cols-auto">
        <MovieList movies={movies} />
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.Auth.isAuthenticated,
  user: state.Auth.user,
});

export default connect(mapStateToProps)(SuggestMovies);
