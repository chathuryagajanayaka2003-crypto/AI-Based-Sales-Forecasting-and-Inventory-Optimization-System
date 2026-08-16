import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import Chart from "../components/Chart";

function Dashboard() {

  const salesData = [
    { date: "Jan", sales: 120 },
    { date: "Feb", sales: 180 },
    { date: "Mar", sales: 150 },
    { date: "Apr", sales: 220 },
    { date: "May", sales: 260 },
    { date: "Jun", sales: 240 }
  ];

  return (
    <div>

      <Navbar />

      <main className="dashboard">

        <h1>SALES FORECASTING SYSTEM</h1>

        {/* Statistics */}

        <div className="stats">

          <StatCard
            title="Revenue"
            value="Rs. 245,000"
          />

          <StatCard
            title="Products"
            value="380"
          />

          <StatCard
            title="Sales"
            value="2,121"
          />

          <StatCard
            title="Alerts"
            value="5"
          />

        </div>

        {/* Forecast Chart */}

        <section className="chart-section">

          <h2>Sales Forecast Chart</h2>

          <Chart data={salesData} />

        </section>

        {/* Bottom sections */}

        <div className="bottom-grid">

          <div className="panel">

            <h2>Top Products</h2>

            <p>1. Product A</p>
            <p>2. Product B</p>
            <p>3. Product C</p>
            <p>4. Product D</p>
            <p>5. Product E</p>

          </div>

          <div className="panel">

            <h2>Inventory Alerts</h2>

            <p>Rice 🔴</p>
            <p>Milk 🟡</p>
            <p>Soap 🟢</p>

          </div>

        </div>

      </main>

    </div>
  );
}

export default Dashboard;