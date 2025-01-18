# Mishipay
# Inventory Management System

This project is an Inventory Management System built using Django, MongoDB, HTML, CSS, and JavaScript. It is designed to efficiently manage products, stock levels, suppliers, and sales. The system supports CRUD operations for managing products and suppliers, facilitates stock management, and enables tracking of sales orders.

## Features

### Mandatory Features
1. **Add Product**: Add a new product to the inventory with validation for stock quantity, price, and product details. Ensures no duplicate product records.
2. **List Products**: Retrieve a list of all products in the inventory, including their name, description, price, stock quantity, and supplier details.
3. **Add Supplier**: Add a new supplier to the system with validation of email and phone format. Ensures no duplicate supplier records.
4. **List Suppliers**: Retrieve a list of all suppliers, including their name, email, phone, and address details.
5. **Add Stock Movement**: Record incoming stock ("In") or outgoing stock ("Out") and update stock levels accordingly.
6. **Create Sale Order**: Create sale orders by selecting products, verifying sufficient stock, and calculating the total price. Updates stock after each sale.
7. **Cancel Sale Order**: Cancel an existing sale order and set its status to "Cancelled," updating stock levels accordingly.
8. **Complete Sale Order**: Mark an order as "Completed" and update the stock levels accordingly.
9. **List Sale Orders**: Retrieve a list of all sale orders, including product name, quantity, total price, sale date, status, and additional notes.
10. **Stock Level Check**: Check the current stock level for each product.

### Additional Features (Bonus points)
- **User Interface**: A user-friendly UI that integrates seamlessly with backend functionality.
- **Filtering**: Implement filtering options (e.g., by product category, order status).
- **Data Validation**: Ensure all inputs are properly validated (e.g., email formats, phone numbers, stock levels).

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB

## Installation

### Prerequisites
- Python 3.x
- Django
- MongoDB

### Steps
1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <project-directory>
