import { Outlet } from 'react-router-dom';
import Navbar from './Navbar'; // Correção: importação default, sem chaves

const MainLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main>
        <div className="container mx-auto px-6 py-8">
          <Outlet /> {/* As páginas da rota serão renderizadas aqui */}
        </div>
      </main>
    </div>
  );
};

export default MainLayout;