# 🌍 TravelGuide Project

A Web-Based Tourism Management Information System, web with mobile integration application built with **Django**, **PostgreSQL**, and **React Native**. 
This project supports multiple user roles such as Admin, Tourist, Tourism Officer, Business Owner, and Event Organizer.

---

## 🚀 Features

### Web (Django)
- Admin dashboard with custom UI
- Role-based dashboard redirection
- Tourist spot/category/location management
- Secure JWT authentication
- User registration with role assignment

### Mobile (React Native)
- Modern UI Tourist Dashboard
- JWT-based login
- AR features (in development)
- Profile + Settings screens
- Filter tourist spots by location or category

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/louwinzky/TravelGuide.git
cd TravelGuide


🔒 Authentication Endpoints

    POST /api/auth/token/ – Get JWT token

    POST /api/auth/token/refresh/ – Refresh token

    GET /api/auth/me/ – Get user profile (JWT required)

    POST /api/auth/register/ – Register new user

    POST /api/auth/logout/ – Logout and blacklist token
