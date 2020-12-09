import { history } from "./history";
import React from "react";
import { Router } from "react-router-dom";

export const withRouter = (Comp) => () => {
  return (
    <Router history={history}>
      <Comp />
    </Router>
  );
}