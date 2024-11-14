import React from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "./components/ui/provider";
import App from "./App";

const root = createRoot(document.getElementById("root"));
root.render(
  <Provider>
    <App />
  </Provider>
);  