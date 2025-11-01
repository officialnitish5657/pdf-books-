import React, { useEffect, useState, useRef, useCallback } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api";

const PAGE_BATCH = 5;

export default function BookReader() {
  const { id } = useParams();
  const [pages, setPages] = useState([]);
  const [start, setStart] = useState(0);
  const [totalPages, setTotalPages] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const observer = useRef();

  // 🧩 Fetch pages from backend
  const fetchPages = useCallback(async () => {
    if (loading) return;
    if (totalPages !== null && start >= totalPages) return;

    setLoading(true);
    try {
      const res = await api.get(`/books/${id}/pages?start=${start}&count=${PAGE_BATCH}`);
      const { pages: newPages, total_pages } = res.data;
      setTotalPages(total_pages);

      if (newPages && newPages.length > 0) {
        setPages((prev) => [...prev, ...newPages]);
        setStart((prev) => prev + newPages.length);
      }
    } catch (err) {
      console.error("❌ Fetch error:", err);
      setError("Failed to load book pages.");
    } finally {
      setLoading(false);
    }
  }, [id, start, loading, totalPages]);

  useEffect(() => {
    fetchPages(); // Load first batch
  }, [id]);

  // 🧭 Infinite scroll observer
  const lastPageRef = useCallback(
    (node) => {
      if (loading) return;
      if (observer.current) observer.current.disconnect();

      observer.current = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting) fetchPages();
        },
        { rootMargin: "300px" }
      );

      if (node) observer.current.observe(node);
    },
    [loading, fetchPages]
  );

  if (error)
    return <div className="text-center text-red-500 mt-10">{error}</div>;

  return (
    <div className="bg-gray-100 min-h-screen flex flex-col items-center py-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        📖 Reading Book #{id}
      </h2>

      {pages.map((url, i) => {
        const isLast = i === pages.length - 1;
        return (
          <div
            key={i}
            ref={isLast ? lastPageRef : null}
            className="w-10/12 md:w-8/12 mb-8 rounded-lg bg-white shadow-lg overflow-hidden transition-all duration-700 hover:shadow-2xl"
          >
            {/* ✅ Use dynamic baseURL from api.js */}
            <img
              src={`${api.defaults.baseURL}${url}`}
              alt={`Page ${i + 1}`}
              className="w-full object-contain"
              loading="lazy"
            />
          </div>
        );
      })}

      {loading && (
        <p className="text-blue-500 text-center animate-pulse">Loading...</p>
      )}

      {totalPages !== null && start >= totalPages && (
        <p className="text-gray-400 mt-8">✅ You reached the end!</p>
      )}
    </div>
  );
}
