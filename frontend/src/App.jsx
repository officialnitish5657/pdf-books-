import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Books from "./pages/Books";
import BookDetails from "./pages/BookDetails";
import BookReader from "./pages/BookReader";
import UploadBook from "./pages/UploadBook";
import Navbar from "./components/Navbar";


export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/books" element={<Books />} />
        <Route path="/books/:id" element={<BookDetails />} />
        <Route path="/books/:id/read" element={<BookReader />} />


        <Route path="/upload" element={<UploadBook />} />

      </Routes>
    </Router>
  );
}
