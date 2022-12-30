import axios from "axios";

const http = axios.create({
    baseURL: "http://localhost:5001",
    headers:
    {"Content-type": "multipart/form-data"}
});

export default http;