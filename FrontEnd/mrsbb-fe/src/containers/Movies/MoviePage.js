import React, { useEffect, useState } from "react";
import { Navigate, useParams } from "react-router-dom";
import { connect } from "react-redux";
import "./CSS/MoviePage.css";

import Heading from "../../components/Heading";
import Rating from "../../components/Rating";

const MoviePage = ({ isAuthenticated }) => {
  const [userId, setUserId] = useState(-1);
  const [movie, setMovie] = useState([]);
  const [rating, setRating] = useState({});
  const [isRated, setIsRated] = useState(false);
  const [isRatedAnnouncement, setIsRatedAnnouncement] = useState(
    "You haven't rated this movie yet"
  );
  const [helpAnnouncement, setHelpAnnouncement] = useState(
    "You can rate this movie by clicking on the stars above"
  );

  const movieId = parseInt(useParams().id);

  const createRatingRequest = async (ratingValue) => {
    setRating(ratingValue);
    const url = `${process.env.REACT_APP_API_URL}/rating/create/`;
    const body = JSON.stringify({
      userId: userId,
      movieId: movieId,
      rating: ratingValue,
    });
    const response = await fetch(url, {
      method: "POST",
      header: {
        "Content-Type": "application/json",
      },
      body,
    });
    const responseJson = await response.json();

    if (responseJson) {
      if (responseJson.status !== "failed") {
        setRating(responseJson);
        setIsRated(true);
        setIsRatedAnnouncement("Your rating for this movie is:");
        setHelpAnnouncement(
          "You can change your rating by clicking on the stars above"
        );
      }
      // alert(responseJson);
    }
  };

  const updateRatingRequest = async (newRatingValue) => {
    const url = `${process.env.REACT_APP_API_URL}/rating/update/`;
    const body = JSON.stringify({
      userId: userId,
      movieId: movieId,
      rating: newRatingValue,
    });
    const response = await fetch(url, {
      method: "PUT",
      header: {
        "Content-Type": "application/json",
      },
      body,
    });
    const responseJson = await response.json();

    if (responseJson) {
      if (responseJson.status === "changed") {
      }
      // alert(responseJson.status);
    }
  };

  useEffect(() => {
    const getMovieRequest = async () => {
      const url = `${process.env.REACT_APP_API_URL}/movie/d?query=${movieId}`;
      const response = await fetch(url, {
        method: "GET",
        header: {
          "Content-Type": "application/json",
        },
      });
      const responseJson = await response.json();

      if (responseJson) {
        setMovie(responseJson);
      }
    };

    const getRatingRequest = async (userId, movieId) => {
      if (userId === -1) return;
      const url = `${process.env.REACT_APP_API_URL}/rating/read/`;
      const body = JSON.stringify({ userId, movieId });
      const response = await fetch(url, {
        method: "POST",
        header: {
          "Content-Type": "application/json",
          Accept: "*/*",
        },
        body,
      });
      if (response.status === 200) {
        const responseJson = await response.json();

        if (responseJson.status !== "failed") {
          setRating(responseJson);
          setIsRated(true);
          setIsRatedAnnouncement("Your rating for this movie is:");
          setHelpAnnouncement(
            "You can change your rating by clicking on the stars above"
          );
        }
      }
    };

    getMovieRequest();
    setUserId(localStorage.getItem("userId"));
    getRatingRequest(userId, movieId);
  }, [movieId, userId]);

  if (isAuthenticated === false) {
    return <Navigate replace to="/login" />;
  }

  return (
    <div className="container-fluid movie-app">
      <div className="d-flex justify-content-between mt-4 mb-4 ">
        <Heading heading={movie.movieTitle} />
      </div>
      <div className="row row-cols-auto">
        <div className="d-flex justify-content-start m-3">
          <div className="image-container">
            <img
              src={movie.moviePoster}
              style={{ width: "300px", height: "500px" }}
              alt="movie"
            ></img>
            <div className="overlay d-flex align-items-center justify-content-center">
              {movie.movieTitle}
            </div>
          </div>
          <div className="m-4 col">
            <h3> - - </h3>
            <h2>Genres</h2>
            <h3>{movie.movieGenre}</h3>
            <h3> - - </h3>
            <h3>{isRatedAnnouncement}</h3>
            <Rating
              count={5}
              onChange={isRated ? updateRatingRequest : createRatingRequest}
              value={rating.rating}
              size={25}
              half={false}
            />
            <h3> - - </h3>
            <h3>{helpAnnouncement}</h3>
            <h3> - - </h3>
          </div>
        </div>
        <div className="title"></div>
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.Auth.isAuthenticated,
});

export default connect(mapStateToProps)(MoviePage);
