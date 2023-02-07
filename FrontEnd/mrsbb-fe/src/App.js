import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Layout from "./hocs/Layout";

import Home from "./containers/Others/Home";
import Login from "./containers/Authentication/Login";
import Signup from "./containers/Authentication/Signup";
import Activate from "./containers/Authentication/Activate";
import ResetPassword from "./containers/Authentication/ResetPassword";
import ResetPasswordConfirm from "./containers/Authentication/ResetPasswordConfirm";
import SearchMovies from "./containers/Movies/SearchMovies";
import PageNotFound from "./containers/Others/PageNotFound";

import { Provider } from "react-redux";
import Store from "./Store";
import SuggestMovies from "./containers/Movies/SuggestMovies";
import MoviePage from "./containers/Movies/MoviePage";

const App = () => (
  <Provider store={Store}>
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/signup" element={<Signup />} />
          <Route exact path="/reset-password" element={<ResetPassword />} />
          <Route
            exact
            path="/password/reset/confirm/:uid/:token"
            element={<ResetPasswordConfirm />}
          />
          <Route exact path="/activate/:uid/:token" element={<Activate />} />
          <Route exact path="/search" element={<SearchMovies />} />
          <Route exact path="/suggest" element={<SuggestMovies />} />
          <Route exact path="/movie/:id" element={<MoviePage />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  </Provider>
);

export default App;
