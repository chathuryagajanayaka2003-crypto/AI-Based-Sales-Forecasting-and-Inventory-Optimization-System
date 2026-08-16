import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Sales from "./pages/Sales";
import Inventory from "./pages/Inventory";
import Forecast from "./pages/Forecast";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/sales" element={<Sales />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/forecast" element={<Forecast />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;