# Requirements for Benareyo Bridal Market Backend

## Functional Requirements
- **User Management**
  - Users can register, login, and manage profiles.
  - Admin or staff roles can manage collections, dresses, and designers.
- **Designer Management**
  - Designers can add, update, and manage their dresses and collections.
- **Collections & Products**
  - Users can browse collections and dresses.
  - Products include dresses, jewelry, shoes, and groom suits.
- **Virtual Try-On**
  - Users can try dresses using AR technology.
  - Upload photo or use camera for real-time visualization.
- **Fashion Shows**
  - Users can view live and recorded fashion shows.
  - Show collection name, designer, and description.
- **Cart & Orders**
  - Users can add multiple items (dresses, jewelry, etc.) to a cart.
  - Users can checkout and create orders.
  - Cart items reference products and quantity.
- **Payments**
  - Users can pay via different payment methods.
  - Payment is linked 1:1 with orders.
- **Reviews**
  - Users can review dresses after trying or renting.
  - Include rating, comment, and date.
- **Appointments**
  - Users can book appointments for in-person fittings.
  - Track status (pending, confirmed, completed).

## Non-Functional Requirements
- **Database:** PostgreSQL
- **API Authentication:** JWT (secure login, role-based access)
- **API Documentation:** Swagger/OpenAPI for endpoints
- **Performance:** Optimized queries, indexing for high-volume product catalog
- **Security:** Encrypted sensitive data, HTTPS support, rate limiting
- **Scalability:** Backend should handle multiple concurrent users, carts, and virtual try-ons
- **Maintainability:** Clean code, proper version control, and clear documentation

## Relationships
- **One Designer → Many Dresses**
- **One Collection → Many Dresses & Fashion Shows**
- **One User → One Cart**
- **One Cart → Many Cart Items**
- **One User → Many Orders**
- **One Order → Many Order Items**
- **One User → Many Virtual Try-Ons, Reviews, Appointments**
- **One Order → One Payment**
