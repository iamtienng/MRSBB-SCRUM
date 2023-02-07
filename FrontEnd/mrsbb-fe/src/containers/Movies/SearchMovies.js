import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { connect } from "react-redux";
import "./CSS/SearchMovies.css";

import MovieList from "../../components/MovieList";
import Heading from "../../components/Heading";
import SearchBox from "../../components/SearchBox";

const SearchMovies = ({ isAuthenticated }) => {
  const [movies, setMovies] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const getMovieRequest = async () => {
      const url = `http://127.0.0.1:8000/movie/s?query=${search}`;
      const response = await fetch(url);
      const responseJson = await response.json();

      if (responseJson) {
        console.log(responseJson);
        setMovies(responseJson);
      }
    };
    getMovieRequest();
  }, [search]);

  if (isAuthenticated === false) {
    return <Navigate replace to="/login" />;
  }

  return (
    <div className="container-fluid movie-app">
      <div className="d-flex justify-content-between mt-4 mb-4 ">
        <Heading heading="Type to Search" />
      </div>
      <div className="d-flex justify-content-between mt-4 mb-4 ">
        <SearchBox
          search={search}
          setSearch={setSearch}
          className="search-box"
        />
      </div>
      <div className="row row-cols-auto">
        <MovieList movies={movies} />
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.Auth.isAuthenticated,
});

export default connect(mapStateToProps)(SearchMovies);
