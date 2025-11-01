import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api";

export default function BookDetails() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [rating, setRating] = useState(0);
  const [loading, setLoading] = useState(true);

  // ✅ Fetch single book by ID
  useEffect(() => {
    const fetchBook = async () => {
      try {
        const res = await api.get(`/books/${id}`);
        setBook(res.data);
      } catch (err) {
        console.error("❌ Error fetching book:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchBook();
  }, [id]);

  // ✅ Handle rating
  const handleRate = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append("rating", rating);

      await api.post(`/books/${id}/rate`, formData);
      alert("✅ Rated successfully!");
    } catch (err) {
      console.error("❌ Rating error:", err);
      alert("Failed to submit rating.");
    }
  };

  if (loading) return <p>Loading...</p>;
  if (!book) return <p>Book not found.</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>{book.title}</h2>
      <p>{book.description}</p>

      {book.cover_image && (
        <img
          src={`${api.defaults.baseURL}${book.cover_image}`}
          alt={book.title}
          width="300"
          style={{ borderRadius: "10px" }}
        />
      )}

      <p>⭐ Rating: {book.rating?.toFixed(1) || 0}</p>

      <Link to={`/books/${book.id}/read`}>📖 Read Book</Link>
      <br /><br />

      <a
        href={`${api.defaults.baseURL}/static/pdfs/${book.filename}`}
        download
      >
        ⬇️ Download PDF
      </a>

      <hr />

      <h3>Rate this book</h3>
      <form onSubmit={handleRate}>
        <input
          type="number"
          name="rating"
          min="0"
          max="5"
          step="0.5"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
          style={{ marginRight: "10px", padding: "5px" }}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
