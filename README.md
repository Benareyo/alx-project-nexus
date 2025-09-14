# Benareyo Bridal Market Backend

## 🚀 Project Overview
**Benareyo Bridal Market Backend** is a fully-featured backend for a bridal e-commerce platform that focuses on traditional Habshan dress collections. The system provides advanced virtual try-on experiences, live fashion shows, secure transactions, and complete product management for dresses, jewelry, groom suits, and accessories.

This project demonstrates scalable backend architecture, robust API design, and modern backend engineering best practices.

---

## 🎯 Project Goals
- **User Management:** Secure registration, authentication, and profile management with JWT.
- **Product & Collection Management:** CRUD operations for dresses, jewelry, and groom items, organized by collection and designer.
- **Virtual Try-On:** Advanced AR technology for trying dresses before purchase.
- **Fashion Shows:** Live streaming events for designers' collections with purchase links.
- **Filtering, Sorting & Pagination:** Efficient product discovery for users.
- **Reviews & Ratings:** Users can review items, providing feedback and ratings.
- **Payment System:** Secure payment handling for purchases and rentals.
- **Appointment Booking:** Schedule virtual consultations with designers.

---

## 📦 Technology Stack
- **Django:** Backend framework for scalable and secure APIs.
- **PostgreSQL:** Relational database optimized for complex queries and performance.
- **JWT (JSON Web Tokens):** Secure user authentication and role-based access.
- **Swagger/OpenAPI:** Comprehensive API documentation for frontend integration.
- **Docker:** Containerized deployment for consistent environments.
- **GitHub Actions:** CI/CD automation for testing and deployment.

---

## 🗂 Database Design
### Key Entities:
- **Users:** `id`, `username`, `email`, `password`, `role`
- **Products:** `id`, `name`, `designer`, `price`, `collection_id`, `category`, `type`, `image_url`
- **Collections:** `id`, `name`, `description`
- **Reviews:** `id`, `user_id`, `product_id`, `rating`, `comment`
- **Bookings:** `id`, `user_id`, `appointment_date`, `designer_id`, `status`
- **Payments:** `id`, `user_id`, `amount`, `payment_method`, `status`

### Relationships:
- A **Collection** has multiple **Products**.
- A **Product** can have multiple **Reviews** from different **Users**.
- A **User** can book appointments and make payments for multiple products.
- Designers are linked to **Collections** and **Bookings**.

---

## ⚡ Key Features
### 1. CRUD Operations
- Create, read, update, delete products, collections, and designer info.
- User registration, login, and profile management.

### 2. Virtual Try-On
- Upload photo or use camera to try dresses with AR visualization.
- Real-time body fit prediction and movement simulation.
- Share sessions with friends.

### 3. Fashion Shows
- Live streaming for featured collections.
- Designer info, collection overview, and “shop this collection” feature.

### 4. Filtering, Sorting, Pagination
- Filter by category, designer, price, collection.
- Sort by price or popularity.
- Paginated responses for large product sets.

### 5. Reviews & Ratings
- Leave ratings and comments for products.
- View average rating per item and designer.

### 6. Payment System
- Secure transactions using encrypted payment methods.
- Supports rent or purchase options for dresses.
- Payment records linked to user accounts.

### 7. Appointments & Consultations
- Schedule virtual consultations with designers.
- Manage appointment status and confirmations.

---

## 🔒 API Security
- **Authentication:** JWT-based secure access.
- **Authorization:** Role-based access control for designers, admins, and users.
- **Rate Limiting:** Protect API from abuse.
- **Data Encryption:** Passwords and sensitive data encrypted in storage and during transmission.

---

## 📑 API Documentation
API endpoints are fully documented using **Swagger/OpenAPI**, providing frontend developers a clear guide to integration. Hosted documentation will be provided.

---

## 🏗 Implementation & Git Commit Workflow
- feat: set up Django project with PostgreSQL  
- feat: implement user authentication with JWT  
- feat: add product, collection, and booking APIs  
- feat: integrate virtual try-on endpoints  
- feat: add fashion show endpoints  
- perf: optimize database queries with indexing  
- docs: add API usage instructions in Swagger  

---

## 📌 To-Do
- [ ] Add frontend integration endpoints
- [ ] Write unit and integration tests
- [ ] Deploy backend to production server
- [ ] Add more collections and products
- [ ] Integrate AR virtual try-on with frontend

---

## 💡 Notes
This backend serves as the foundation for an **interactive, scalable, and secure bridal e-commerce platform**. Future enhancements can include AI-based recommendations, social sharing, and multi-currency payment support.

