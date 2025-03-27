import { ReactNode } from "react";
import Navbar from "../components/Navbar";

const MainLayout = ({ children }: { children: ReactNode }) => {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar at the top */}
      <Navbar />
    </div>
  );
};

export default MainLayout;
