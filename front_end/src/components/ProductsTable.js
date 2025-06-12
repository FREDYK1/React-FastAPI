import react, { useEffect, useContext } from 'react';
import { Table } from 'react-bootstrap';
import { ProductContext } from '../ProductContext';

const ProductsTable = () => {
    const { products, setProducts } = useContext(ProductContext);

    useEffect(() => {
    fetch("http://127.0.0.1:8000/products")
    .then(response => { response.json(); })
    .then(results => { console.log(results)
    setProducts({data: [...results.data]})
    })
    })

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
                    <tbody>
                    </tbody>
            </thead>
        </Table>
    );
}

export default ProductsTable;