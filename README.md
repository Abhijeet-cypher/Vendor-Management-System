# Project Title: Vendor Management System
## Brief Description:
The Vendor Management System (VMS) is a web-based application designed to streamline the management of vendors and purchase orders. It provides a centralized platform for businesses to manage vendor relationships, track purchase orders, and analyze vendor performance. With features for user authentication, CRUD operations on vendors and purchase orders, and performance metrics tracking, the VMS aims to simplify vendor management processes and improve operational efficiency.

### Technologies Used
- Django
- Django REST Framework
- SQLite
- JSON Web Tokens (JWT)

### Installation

To set up the Vendor Management System locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your_username/vendor-management-system.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd vendor-management-system
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations:**
   ```bash
   python manage.py runserver
   ```
5. **Run the test Suite:**
   ```bash
   python manage.py test
   ```

# API Documentation

### Signup

- **Endpoint:** `/api/signup/`
- **Method:** POST
- **Description:** Endpoint for user registration.
- **Request Format:**
  ```json
  {
      "username": "string",
      "password": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string"
  }
  ```
- **Response Format:**
   - **Status Code:** 201 Created
  ```json
  {
    "message": "User created successfully"
  }
  ```
  - **Status Code:** 400 Bad Request
   ```json
   {
    "error": "Error details"
   }
   ```
### Logout

- **Endpoint:** POST `/api/logout/`
- **Description:** Endpoint for user logout.
- **Request Header:** {Authorization 'Bearer ' + 'token_string'}
- **Notes:** Requires a valid refresh token. Only allows POST requests. Requires authentication.

### Obtain JWT Token

- **Endpoint:** POST /api/login/
- **Description:** Endpoint for obtaining a JWT token.
- **Request Body:** { "username": "string", "password": "string" }
- **Notes:** Only allows POST requests. Does not require authentication.

### Vendors List

- **Endpoint:** GET /api/vendors/ (for listing), POST /api/vendors/ (for creating)
- **Description:** Endpoint for listing vendors and creating a new vendor.
- **Request Body (POST):** Vendor data
- **Response (GET):** List of vendors
- **Response (POST):** Created vendor details
- **Notes:** Requires authentication.

### Retrieve Vendor

- **Endpoint:** GET `/api/vendors/{vendor_id}/`
- **Description:** Endpoint for retrieving details of a specific vendor.
- **Response:** Vendor details
- **Notes:** Requires authentication.

### Update Vendor

- **Endpoint:** PUT `/api/vendors/{vendor_id}/update/`
- **Description:** Endpoint for updating details of a specific vendor.
- **Request Body:** Updated vendor data
- **Response:** Updated vendor details
- **Notes:** Requires authentication.

### Delete Vendor

- **Endpoint:** DELETE `/api/vendors/{vendor_id}/delete/`
- **Description:** Endpoint for deleting a specific vendor.
- **Response:** Success message
- **Notes:** Requires authentication.

### Purchase Order

- **Endpoint:** POST `/api/purchase_orders/ (for creating), GET /api/purchase_order/ (for listing)`
- **Description:** Endpoint for creating and listing purchase orders.
- **Request Body (POST):** Purchase order data
- **Response (GET):** List of purchase orders
- **Response (POST):** Created purchase order details

### Retrieve Purchase Order

- **Endpoint:** GET `/api/purchase_orders/{po_id}/`
- **Description:** Endpoint for retrieving details of a specific purchase order.
- **Response:** Purchase order details

### Update Purchase Order

- **Endpoint:** PUT `/api/purchase_order/{po_id}/update/`
- **Description:** Endpoint for updating details of a specific purchase order.
- **Request Body:** Updated purchase order data
- **Response:** Updated purchase order details

### Delete Purchase Order

- **Endpoint:** DELETE `/api/purchase_order/{po_id}/delete/`
- **Description:** Endpoint for deleting a specific purchase order.
- **Response:** Success message

### Retrieve Vendor Performance Metrics

- **Endpoint:** GET `/api/vendors/{vendor_id}/performance/`
- **Description:** Endpoint for retrieving performance metrics of a specific vendor.
- **Response:** Vendor performance metrics

### Acknowledge Purchase Order

- **Endpoint:** POST `/api/purchase_order/{po_id}/acknowledge/`
- **Description:** Endpoint for acknowledging a purchase order.
- **Response:** Success message

## Instructions to Run Test Suite
1. Prerequisites:
   - Ensure that the project dependencies are installed. You can install them using ```pip install -r requirements.txt```.
2. Run Tests:
   - Navigate to the project directory in your terminal.
   - Run the command ``` python manage.py test ``` to execute the test suite.
3. View Test Results:
   - After running the tests, review the output in the terminal to see the results of each test case.
   - Any failed assertions or errors will be displayed in the output.
