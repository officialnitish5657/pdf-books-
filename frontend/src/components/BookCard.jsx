import React from "react";
import { Link } from "react-router-dom";

export default function BookCard({book}){
  return (
    <div className="border rounded-lg p-4 shadow-sm">
      <div className="h-40 bg-gray-100 mb-3 flex items-center justify-center">
        {/* optionally show cover if you generate one */}
        <span className="text-gray-400">Cover</span>
      </div>
      <h3 className="font-semibold">{book.title}</h3>
      <p className="text-sm text-gray-600 truncate">{book.description}</p>
      <div className="mt-3 flex gap-2">
        <Link to={`/books/${book.id}`} className="px-3 py-1 border rounded">Details</Link>
        <Link to={`/books/${book.id}/pages`} className="px-3 py-1 bg-blue-600 text-white rounded">Open Book</Link>
      </div>
    </div>
  );
}
