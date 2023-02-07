/* eslint-disable jsx-a11y/anchor-is-valid */
import React from "react";
import { Navigate } from "react-router-dom";
import { connect } from "react-redux";
import "./CSS/Home.css";

const Home = ({ isAuthenticated }) => {
  if (isAuthenticated === false) {
    return <Navigate replace to="/login" />;
  }

  return (
    <div class="container px-4 py-5" id="featured-3">
      <h2 class="pb-2 border-bottom">What do you want to do today?</h2>
      <div class="row g-4 py-5 row-cols-1 row-cols-lg-3">
        <div class="feature col">
          <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3"></div>
          <h3 class="fs-2">Search for Movie</h3>
          <p>Please click the link below to search for a movie.</p>
          <a href="/search" class="d-inline-flex align-items-center">
            Go to Search
          </a>
        </div>
        <div class="feature col">
          <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3"></div>
          <h3 class="fs-2">Get Suggested Movies</h3>
          <p>
            Please click the link below to get a list of movies that you might
            like.
          </p>
          <a href="/suggest" class="icon-link d-inline-flex align-items-center">
            Go to Suggestion
          </a>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.Auth.isAuthenticated,
});

export default connect(mapStateToProps)(Home);
