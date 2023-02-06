import React from "react";
import { Link, Navigate } from "react-router-dom";
import { connect } from "react-redux";

const Home = ({ isAuthenticated }) => {
  if (!isAuthenticated) {
    return <Navigate replace to="/login" />;
  }
  return (
    <div className="container">
      <div className="bg-light p-5 rounded-lg m-3">
        <h1 className="display-4">Hello, world!</h1>
        <p className="lead">
          This is a simple hero unit, a simple jumbotron-style component for
          calling extra attention to featured content or information.
        </p>
        <hr className="my-4" />
        <p>
          It uses utility classes for typography and spacing to space content
          out within the larger container.
        </p>
        <Link className="btn btn-primary btn-lg" to="/login" role="button">
          Login
        </Link>
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.Auth.isAuthenticated,
});

export default connect(mapStateToProps)(Home);
