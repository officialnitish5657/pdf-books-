import axios from "axios";

export const api = axios.create({
  baseURL:
    import.meta.env.MODE === "development"
      ? "http://127.0.0.1:8000"
      : "https://backend-mdmn.onrender.com/", // ⚡ replace with your actual Render backend URL
});
