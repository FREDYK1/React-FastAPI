import react from "react";
import { Navbar, Nav, Form, FormControl, Button, Badge } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NavBar = () => {
    return (
        <Navbar bg="dark" expand="lg" variant="dark" className="border-bottom border-primary" style={{ boxShadow: '0 2px 0 #0d6efd' }}>
            <Navbar.Brand href="#home">Inventory Management App</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Badge className="mt-2 ms-3" bg="primary">Products In stock</Badge>
                </Nav>
                <Form className="d-flex align-items-center">
                    <Link to="/addproduct" className="btn btn-primary btn-sm me-3">Add Product</Link>
                    <FormControl type="text" placeholder="Search" className="me-2 bg-dark text-light border-secondary" />
                    <Button type="submit" variant="outline-primary">Search</Button>
                </Form>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;
