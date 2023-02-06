import React, { useState } from "react";
import { Navigate, useParams } from "react-router-dom";
import { connect } from "react-redux";
import { verify } from "../actions/Auth";
import "./Containers.css";

const Activate = ({ verify }) => {
  const [verified, setVerified] = useState(false);
  const { uid, token } = useParams();

  const verify_account = () => {
    verify(uid, token);
    setVerified(true);
    return <Navigate replace to="/" />;
  };

  if (verified) {
    return <Navigate replace to="/" />;
  }

  verify_account();

  return (
    <div className="container-mrsbb">
      <div className="shadow p-3 mt-5 mb-5 bg-body rounded align-middle">
        <div
          className="d-flex flex-column justify-content-center align-items-center"
          style={{ marginTop: "0" }}
        >
          <h1>Verify your Account</h1>
          <button
            className="btn btn-primary"
            onClick={(e) => verify_account(e)}
            style={{ marginTop: "50px" }}
            type="button"
          >
            Verify
          </button>
        </div>
      </div>
    </div>
  );
};

export default connect(null, { verify })(Activate);
