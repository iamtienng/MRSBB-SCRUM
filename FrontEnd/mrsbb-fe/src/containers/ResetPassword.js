import React, { useState } from "react";
import { Navigate, Link } from "react-router-dom";
import { connect } from "react-redux";
import { reset_password } from "../actions/Auth";
import "./Containers.css";

const ResetPassword = ({ reset_password }) => {
  const [requestSent, setRequestSent] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
  });

  const { email } = formData;

  const onChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e) => {
    e.preventDefault();
    reset_password(email);
    setRequestSent(true);
  };

  if (requestSent) {
    return <Navigate replace to="/" />;
  }

  return (
    <div className="container-mrsbb">
      <div
        className="shadow p-3 mt-5 mb-5 bg-body rounded align-middle"
        style={{ width: 500, height: "auto" }}
      >
        <h2>Find Your Account</h2>
        <hr />
        <form onSubmit={(e) => onSubmit(e)}>
          <p>
            Please enter your email and we will help you create a new password.
          </p>
          <div className="form-group">
            <input
              className="form-control form-control-lg mb-3"
              type="email"
              placeholder="Email"
              name="email"
              value={email}
              onChange={(e) => onChange(e)}
              required
            />
          </div>
          <hr />
          <div className="d-flex flex-row-reverse">
            <button
              className="btn btn-primary mb-3"
              type="submit"
              style={{
                border: "none",
                backgroundColor: "black",
              }}
            >
              Reset Password
            </button>
            <Link to="/login">
              <button className="btn btn-secondary mb-3 me-3" type="submit">
                Cancel
              </button>
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default connect(null, { reset_password })(ResetPassword);
