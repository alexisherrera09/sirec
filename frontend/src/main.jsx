import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import FormularioPublico from "./pages/FormularioPublico.jsx";
import Panel from "./pages/Panel.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FormularioPublico />} />
        <Route path="/panel" element={<Panel />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
