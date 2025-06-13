import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  username: string;
  role: 'admin' | 'user';
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
  checkAuth: () => void;
}

// Função auxiliar para decodificar o JWT de forma simples
const decodeToken = (token: string): User | null => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return { username: payload.sub, role: payload.role };
  } catch (error) {
    console.error("Failed to decode token:", error);
    return null;
  }
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (token) => {
        const user = decodeToken(token);
        set({ user, token, isAuthenticated: !!user });
      },
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
        localStorage.removeItem('auth-storage'); // Garante a limpeza completa
      },
      checkAuth: () => {
        // Esta função é chamada na inicialização para reidratar o estado
        // O middleware 'persist' já faz isso, mas podemos adicionar lógicas aqui se necessário.
        const token = (JSON.parse(localStorage.getItem('auth-storage') || '{}').state)?.token;
        if (token) {
          const user = decodeToken(token);
          if (user) {
            set({ user, token, isAuthenticated: true });
          } else {
             // Token inválido, limpa o estado
            set({ user: null, token: null, isAuthenticated: false });
            localStorage.removeItem('auth-storage');
          }
        }
      },
    }),
    {
      name: 'auth-storage', // Nome da chave no localStorage
    }
  )
);

// Executa a verificação na inicialização da aplicação
useAuthStore.getState().checkAuth();