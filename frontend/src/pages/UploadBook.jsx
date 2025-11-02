import React, { useState, useRef } from "react";
import { api } from "../api";

const UploadBook = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");
  const fileInputRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = fileInputRef.current?.files[0];
    if (!file) {
      setMessage("⚠️ Please select a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("file", file);

    try {
      const response = await api.post("/books/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage(`✅ ${response.data.message || "Book uploaded successfully!"}`);
      setTitle("");
      setDescription("");
      fileInputRef.current.value = ""; // clear file input
    } catch (error) {
      console.error("❌ Upload error:", error);
      const msg =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "❌ Upload failed. Please try again.";
      setMessage(msg);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-2xl font-bold mb-4 text-center">📚 Upload New Book</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Book Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border p-2 rounded"
          required
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="border p-2 rounded"
        ></textarea>
        <input
          type="file"
          accept="application/pdf"
          ref={fileInputRef}
          className="border p-2 rounded"
          required
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded"
        >
          Upload Book
        </button>
      </form>

      {message && (
        <p
          className={`text-center mt-4 ${
            message.startsWith("✅")
              ? "text-green-600"
              : message.startsWith("⚠️")
              ? "text-yellow-600"
              : "text-red-600"
          }`}
        >
          {message}
        </p>
      )}
    </div>
  );
};

export default UploadBook;
