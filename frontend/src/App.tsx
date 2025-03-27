import React from "react";
import Navbar from "./components/Navbar";

const App: React.FC = () => {
  return (
    <div className="bg-gray-100 dark:bg-gray-900 min-h-screen">
      <Navbar />
      <h1 className="text-center text-3xl font-bold text-gray-900 dark:text-white mt-10"></h1>
    </div>
  );
};

export default App;
