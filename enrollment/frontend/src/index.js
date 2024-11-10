import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "./components/ui/provider"
import App from "./App";


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Provider>
    <App />
  </Provider>
);