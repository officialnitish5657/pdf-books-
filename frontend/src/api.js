import axios from "axios";

export const api = axios.create({
  baseURL:"https://backend-mdmn.onrender.com/", // ⚡ replace with your actual Render backend URL
});
