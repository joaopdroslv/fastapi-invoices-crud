# FastAPI Invoice Management API

## Overview

This FastAPI-based RESTful API manages users and invoices. It provides endpoints for creating, retrieving, updating, and deleting users and invoices, ensuring efficient management of financial transactions.

## Features

- User management (CRUD operations)
- Invoice management (CRUD operations)
- Linking invoices to users
- Marking invoices as paid

## API Endpoints

### User Endpoints

| Method | Endpoint                    | Description                              |
| ------ | --------------------------- | ---------------------------------------- |
| GET    | `/users/`                   | Retrieve all users                       |
| GET    | `/users/{user_id}`          | Retrieve a specific user by ID           |
| GET    | `/users/{user_id}/invoices` | Retrieve invoices associated with a user |
| POST   | `/users/`                   | Create a new user                        |
| PUT    | `/users/{user_id}`          | Update a user's details                  |
| DELETE | `/users/{user_id}`          | Delete a user                            |

### Invoice Endpoints

| Method | Endpoint                     | Description                       |
| ------ | ---------------------------- | --------------------------------- |
| GET    | `/invoices/`                 | Retrieve all invoices             |
| GET    | `/invoices/{invoice_id}`     | Retrieve a specific invoice by ID |
| POST   | `/invoices/`                 | Create a new invoice              |
| PUT    | `/invoices/{invoice_id}/pay` | Mark an invoice as paid           |
| PUT    | `/invoices/{invoice_id}`     | Update invoice details            |
| DELETE | `/invoices/{invoice_id}`     | Delete an invoice                 |
