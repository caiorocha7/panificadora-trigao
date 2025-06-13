import { useAuthStore } from '../store/authStore';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

const DashboardPage = () => {
  const { user } = useAuthStore();
  
  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
      <p className="mt-2 text-lg text-gray-600">
        Bem-vindo(a) de volta, <span className="font-semibold text-blue-600">{user?.username}</span>!
      </p>
      
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link to="/orders/new" className="block p-6 bg-white rounded-lg shadow hover:bg-gray-50">
          <h2 className="text-xl font-bold">Novo Pedido</h2>
          <p className="mt-2 text-gray-600">Crie um novo pedido para um cliente.</p>
        </Link>
        <Link to="/my-orders" className="block p-6 bg-white rounded-lg shadow hover:bg-gray-50">
          <h2 className="text-xl font-bold">Histórico de Pedidos</h2>
          <p className="mt-2 text-gray-600">Veja todos os pedidos registrados no sistema.</p>
        </Link>
        {user?.role === 'admin' && (
           <Link to="/admin/products" className="block p-6 bg-blue-50 rounded-lg shadow hover:bg-blue-100">
             <h2 className="text-xl font-bold text-blue-800">Gerenciar Produtos</h2>
             <p className="mt-2 text-blue-700">Acesso de administrador para editar e adicionar produtos.</p>
           </Link>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;