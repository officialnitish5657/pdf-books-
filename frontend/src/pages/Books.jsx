import React, { useEffect, useState } from "react";
import { api } from "../api";
import { Link } from "react-router-dom";

export default function Books() {
  const [books, setBooks] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const res = await api.get("/books/");
        setBooks(res.data);
      } catch (err) {
        console.error("❌ Error fetching books:", err);
        setError("Failed to load books.");
      }
    };
    fetchBooks();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>All Books</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {books.length === 0 ? (
          <p>Loading books...</p>
        ) : (
          books.map((book) => (
            <div
              key={book.id}
              style={{
                width: "200px",
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "10px",
              }}
            >
              {book.cover_image ? (
                <img
                  src={`${api.defaults.baseURL}${book.cover_image}`}
                  alt={book.title}
                  width="180"
                  height="250"
                  style={{ objectFit: "cover" }}
                />
              ) : (
                <div
                  style={{
                    width: "180px",
                    height: "250px",
                    background: "#eee",
                  }}
                ></div>
              )}
              <h4>{book.title}</h4>
              <p>⭐ {book.rating?.toFixed(1) || 0}</p>
              <Link to={`/books/${book.id}/`}>Details</Link>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
