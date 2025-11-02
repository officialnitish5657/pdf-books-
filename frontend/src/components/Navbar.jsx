import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ padding: "15px", background: "#222", color: "#fff" }}>
      <Link to="/" style={{ color: "white", marginRight: "20px" }}>Home</Link>
      <Link to="/books" style={{ color: "white" }}>Books</Link>
      <Link to="/upload" style={{ color: "white" }}>Uploads</Link>
    </nav>
  );
}
