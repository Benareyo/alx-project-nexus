# Benareyo Bridal Market Backend 💍

Backend system for **Bridal Muse Market**, an e-commerce platform for bridal and wedding products.  
This project is part of **ALX ProDev Backend – Project Nexus**.

---

## 🚀 Project Objective
- Build a scalable backend for a real-world e-commerce app.
- Manage products, categories, carts, orders, and users.
- Document backend skills and API design for frontend consumption.

---

## 🛠️ Tech Stack
- Python & Django REST Framework  
- PostgreSQL  
- JWT Authentication  
- Swagger / Postman for API docs  
- Docker & CI/CD

---

## 📦 Features
1. CRUD APIs for Products & Categories  
2. User authentication (signup/login with JWT)  
3. Cart & Order management  
4. Filtering, sorting, pagination  
5. API documentation with Swagger  

---

## 📂 Database Design
- **User** (id, name, email, role)  
- **Product** (id, name, category, price, stock, image)  
- **Category** (id, name, description)  
- **Order** (id, user, products, status, total_price)  
- **Cart** (id, user, product, quantity)  

---

## 🚦 Setup Instructions
```bash
git clone https://github.com/benareyo/benareyo-bridal-backend.git
cd benareyo-bridal-backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

