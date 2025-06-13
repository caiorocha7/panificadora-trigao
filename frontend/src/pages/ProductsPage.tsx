import { useState, useEffect } from 'react';
import apiClient from '../api/api';

interface Product {
  id: number;
  product_name: string;
  price: number;
  unit: string;
  section: string;
}

const ProductsPage = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        // Rota pública (ou que necessite de login básico)
        const response = await apiClient.get('/products/');
        setProducts(response.data);
      } catch (err) {
        setError('Não foi possível carregar os produtos.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <p className="text-center mt-8">Carregando produtos...</p>;
  if (error) return <p className="text-center mt-8 text-red-500">{error}</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Catálogo de Produtos</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <div key={product.id} className="bg-white p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow">
            <h2 className="text-lg font-semibold text-gray-800">{product.product_name}</h2>
            <p className="text-gray-600 mt-2">Seção: {product.section}</p>
            <p className="text-2xl font-bold text-blue-600 mt-4">
              R$ {product.price.toFixed(2)}
              <span className="text-sm font-normal text-gray-500"> / {product.unit}</span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductsPage;