
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-blue)](https://www.docker.com/)
# Shop Management System

## Overview
This project is a shop management system developed using FastApi and SQLAlchemy. It provides functionalities for managing users, products, categories, orders, comments, and images. Additionally, it offers RESTful API routes for common operations related to user management, orders, products, categories, comments, and file handling.

## Models Overview
- **User**: Represents a user of the system with attributes such as name, email, phone number, etc.
- **Product**: Represents a product available in the shop with attributes like name, stock, price, etc.
- **Category**: Represents a category to which products can be associated.
- **Order**: Represents an order made by a user, containing information like quantity, total price, etc.
- **Comment**: Represents a comment left by a user on a product.
- **Image**: Represents an image associated with a product.

## Description
This project is a shop management system developed using FastApi and SQLAlchemy. It provides functionalities for managing users, products, categories, orders, comments, and images. Additionally, it offers RESTful API routes for common operations related to user management, orders, products, categories, comments, and file handling.

## Technologies Used
- **Python**: Utilized for backend development and business logic implementation.
- **FastAPI**: Chosen as the web framework for its performance, ease of use, and automatic generation of OpenAPI documentation.
- **SQLAlchemy**: Employed for database management and Object-Relational Mapping (ORM) between Python classes and database tables.
- **Docker**: Employed for containerization, facilitating easy deployment and scalability of the application.
- **Supervisor**: Utilized for process control and monitoring to ensure the reliability and availability of the application.

## Skills Demonstrated
- **Backend Development**: Proficient in developing web applications using FastApi, designing RESTful APIs, and handling HTTP requests and responses.
- **Database Management**: Skilled in designing database schemas, implementing data models using SQLAlchemy, and performing CRUD operations on database entities.
- **Containerization**: Experienced in containerizing applications using Docker for portability, consistency, and isolation of development environments.
- **Process Management**: Proficient in managing application processes using Supervisor, ensuring system reliability, and monitoring performance metrics.

## Installation
1. Clone the repository: `git clone https://github.com/mosishon/shop-backend.git`
2. Build Container: `docker build -t shop .`
3. Rename `.env.sample` to `.env` and update the `.env` file with the appropriate values for your environment settings.

## Usage
1. Define your database schema by extending the provided base class `Base` and creating your model classes.
2. Customize the models according to your shop's requirements, modifying attributes and relationships as needed.
3. Implement the provided RESTful API routes in your application for managing users, orders, products, categories, comments, and images.
4. Utilize Docker for containerization and Supervisor for process management to deploy and monitor your application.

## Contributors
- [Your Name](https://github.com/your_username)

## License
This project is licensed under the [MIT License](LICENSE).
