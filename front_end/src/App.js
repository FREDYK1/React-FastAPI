import react from 'react';
import NavBar from './components/NavBar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ProductProvider } from './ProductContext';
import ProductsTable  from './components/ProductsTable';

function App() {
  return (
    <div>
        <Router>
            <ProductProvider>
                <NavBar />
                <ProductsTable />
            </ProductProvider>
        </Router>
    </div>
  );
}

export default App;