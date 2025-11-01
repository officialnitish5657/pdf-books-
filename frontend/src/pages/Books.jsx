import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000";

export default function Books() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/books/`).then(res => setBooks(res.data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>All Books</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {books.map(book => (
          <div key={book.id} style={{ width: "200px", border: "1px solid #ddd", borderRadius: "8px", padding: "10px" }}>
            {book.cover_image ? (
              <img src={`${API_URL}${book.cover_image}`} alt={book.title} width="180" height="250" style={{ objectFit: "cover" }} />
            ) : (
              <div style={{ width: "180px", height: "250px", background: "#eee" }}></div>
            )}
            <h4>{book.title}</h4>
            <p>⭐ {book.rating?.toFixed(1) || 0}</p>
            <Link to={`/books/${book.id}`}>Details</Link>
          </div>
        ))}
      </div>
    </div>
  );
}
