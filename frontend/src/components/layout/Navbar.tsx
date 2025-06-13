import { NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../ui/Button';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-3 flex justify-between items-center">
        <NavLink to="/" className="text-xl font-bold text-gray-800">
          Padaria Trigão
        </NavLink>
        <div className="flex items-center space-x-4">
          <NavLink to="/products" className="text-gray-600 hover:text-blue-600">Produtos</NavLink>
          {isAuthenticated ? (
            <>
              <NavLink to="/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</NavLink>
              <span className="text-gray-700">Olá, {user?.username}</span>
              <Button onClick={handleLogout} variant="secondary" size="sm">
                Logout
              </Button>
            </>
          ) : (
            <NavLink to="/login">
              <Button size="sm">Login</Button>
            </NavLink>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;