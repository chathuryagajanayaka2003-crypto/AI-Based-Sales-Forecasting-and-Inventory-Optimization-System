import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>Sales Forecasting System</h2>

      <div>
        <Link to="/">Dashboard</Link>
        <Link to="/sales">Sales</Link>
        <Link to="/inventory">Inventory</Link>
        <Link to="/forecast">Forecast</Link>
      </div>
    </nav>
  );
}

export default Navbar;