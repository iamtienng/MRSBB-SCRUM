import React, { useState } from "react";
import { Navigate, useParams, Link } from "react-router-dom";
import { connect } from "react-redux";
import { reset_password_confirm } from "../actions/Auth";
import "./Containers.css";

const ResetPasswordConfirm = ({ reset_password_confirm }) => {
  const [requestSent, setRequestSent] = useState(false);
  const [formData, setFormData] = useState({
    new_password: "",
    re_new_password: "",
  });
  const { uid, token } = useParams();

  const { new_password, re_new_password } = formData;

  const onChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e) => {
    e.preventDefault();

    reset_password_confirm(uid, token, new_password, re_new_password);
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
        <h2>Choose a New Password</h2>
        <hr />
        <p>
          Create a new password that is at least 6 characters long. A strong
          password is combination of letters, numbers, and punctuation marks.
        </p>
        <form onSubmit={(e) => onSubmit(e)}>
          <div className="form-group mb-3">
            <input
              className="form-control"
              type="password"
              placeholder="New Password"
              name="new_password"
              value={new_password}
              onChange={(e) => onChange(e)}
              minLength="6"
              required
            />
          </div>
          <div className="form-group mb-3">
            <input
              className="form-control"
              type="password"
              placeholder="Confirm New Password"
              name="re_new_password"
              value={re_new_password}
              onChange={(e) => onChange(e)}
              minLength="6"
              required
            />
          </div>
          <hr />

          <div className="d-flex flex-row-reverse">
            <button
              className="btn btn-primary"
              type="submit"
              style={{
                border: "none",
                backgroundColor: "black",
              }}
            >
              Continue
            </button>
            <Link to="/login">
              <button className="btn btn-secondary me-3" type="submit">
                Skip
              </button>
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default connect(null, { reset_password_confirm })(ResetPasswordConfirm);
