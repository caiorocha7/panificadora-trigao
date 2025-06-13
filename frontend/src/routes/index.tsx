import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Layout
import MainLayout from '../components/layout/MainLayout';

// Pages
import LoginPage from '../pages/LoginPage';
import ProductsPage from '../pages/ProductsPage';
import DashboardPage from '../pages/DashboardPage';
// Placeholder para futuras páginas
const CreateOrderPage = () => <div>Página para Criar Pedido</div>; 
const MyOrdersPage = () => <div>Página de Histórico de Pedidos</div>;
const AdminProductsPage = () => <div>Página para Gerenciar Produtos (Admin)</div>;

// Auth
import ProtectedRoute from './ProtectedRoute';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        {/* Rotas com a Navbar e Layout Padrão */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<ProductsPage />} />
          <Route path="/products" element={<ProductsPage />} />
          
          {/* Rotas Privadas */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/orders/new" element={<CreateOrderPage />} />
            <Route path="/my-orders" element={<MyOrdersPage />} />
            {/* Rota somente para Admin (exemplo) */}
            <Route path="/admin/products" element={<AdminProductsPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;