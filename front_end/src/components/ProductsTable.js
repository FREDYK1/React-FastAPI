import React, { useEffect, useContext } from 'react';
import { Table } from 'react-bootstrap';
import { ProductContext } from '../ProductContext';

const ProductsTable = () => {
    const { products, setProducts } = useContext(ProductContext);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/products")
            .then(response => response.json())
            .then(data => {
                setProducts(Array.isArray(data) ? data : []);
            })
            .catch(error => {
                console.error("Failed to fetch:", error);
            });
    }, [setProducts])

    return (
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Quantity In Stock</th>
                    <th>Quantity Price</th>
                    <th>Quantity Sold</th>
                    <th>Unit Price</th>
                    <th>Revenue</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {products && products.map(product => (
                    <tr key={product.id}>
                        <td>{product.id}</td>
                        <td>{product.name}</td>
                        <td>{product.quantity_in_stock}</td>
                        <td>{product.quantity_price}</td>
                        <td>{product.quantity_sold}</td>
                        <td>{product.unit_price}</td>
                        <td>{product.revenue}</td>
                    </tr>
                ))}
            </tbody>
        </Table>
    );
}

export default ProductsTable;