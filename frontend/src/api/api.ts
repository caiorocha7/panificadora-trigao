import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Interceptador para injetar o token JWT em cada requisição
apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token; // Pega o token do store
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;