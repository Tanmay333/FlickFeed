import { useState, useEffect } from "react";
import { FaSearch, FaSun, FaMoon, FaUserCircle, FaBars } from "react-icons/fa";
import { Menu } from "@headlessui/react";

const Navbar = () => {
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [menuOpen, setMenuOpen] = useState<boolean>(false); // Mobile menu state

  // Apply dark mode class to the HTML tag
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-md fixed w-full top-0 left-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            FlickFeed!
          </div>

          {/* Search Bar (Desktop) */}
          <div className="relative w-72 hidden md:block">
            <input
              type="text"
              placeholder="Search movies..."
              className="w-full pl-10 pr-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none"
            />
            <FaSearch className="absolute left-3 top-3 text-gray-500 dark:text-gray-400" />
          </div>

          {/* Icons */}
          <div className="flex items-center space-x-4">
            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-full bg-gray-200 dark:bg-gray-700"
            >
              {darkMode ? <FaSun className="text-yellow-500" /> : <FaMoon />}
            </button>

            {/* Mobile Menu Toggle Button */}
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 md:hidden"
            >
              <FaBars className="text-gray-900 dark:text-white" />
            </button>

            {/* Profile Dropdown */}
            <Menu as="div" className="relative">
              <Menu.Button className="p-2 rounded-full bg-gray-200 dark:bg-gray-700">
                <FaUserCircle className="text-gray-900 dark:text-white" />
              </Menu.Button>

              <Menu.Items className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 shadow-lg rounded-md p-2">
                <Menu.Item>
                  {({ active }) => (
                    <button
                      className={`${
                        active ? "bg-gray-100 dark:bg-gray-700" : ""
                      } w-full text-left px-4 py-2 text-gray-900 dark:text-white`}
                    >
                      Profile
                    </button>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <button
                      className={`${
                        active ? "bg-gray-100 dark:bg-gray-700" : ""
                      } w-full text-left px-4 py-2 text-gray-900 dark:text-white`}
                    >
                      Logout
                    </button>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Menu>
          </div>
        </div>
      </div>

      {/* Mobile Search Bar */}
      {menuOpen && (
        <div className="relative w-full md:hidden px-4 pb-4">
          <input
            type="text"
            placeholder="Search movies..."
            className="w-full pl-10 pr-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none"
          />
          <FaSearch className="absolute left-6 top-3 text-gray-500 dark:text-gray-400" />
        </div>
      )}
    </nav>
  );
};

export default Navbar;
