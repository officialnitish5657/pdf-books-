import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default function BookDetails() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [rating, setRating] = useState(0);

  useEffect(() => {
    axios.get(`${API_URL}/books`).then(res => {
      const found = res.data.find(b => b.id === parseInt(id));
      setBook(found);
    });
  }, [id]);

  const handleRate = async () => {
    await axios.post(`${API_URL}/books/${id}/rate`, new FormData(Object.assign(document.forms[0])));
    alert("Rated successfully!");
  };

  if (!book) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>{book.title}</h2>
      <p>{book.description}</p>
      {book.cover_image && <img src={`${API_URL}${book.cover_image}`} alt={book.title} width="300" />}
      <p>⭐ Rating: {book.rating?.toFixed(1) || 0}</p>
      <Link to={`/books/${book.id}/read`}>📖 Read Book</Link>
      <br /><br />
      <a href={`${API_URL}/static/pdfs/${book.filename}`} download>⬇️ Download PDF</a>
      <hr />
      <h3>Rate this book</h3>
      <form onSubmit={e => { e.preventDefault(); handleRate(); }}>
        <input type="number" name="rating" min="0" max="5" step="0.5" value={rating} onChange={e => setRating(e.target.value)} />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
