import React, { useState, useEffect } from "react";
import Layout from "./components/Layout/Layout";
import LoadingSpinner from "./components/LoadingSpinner/LoadingSpinner";
import "./App.css";

const App = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulating data fetching or any loading process
    setTimeout(() => {
      setLoading(false); // Set loading to false after 2 seconds (simulated)
    }, 2000);
  }, []);

  return <div className="App">{loading ? <LoadingSpinner /> : <Layout />}</div>;
};

export default App;
