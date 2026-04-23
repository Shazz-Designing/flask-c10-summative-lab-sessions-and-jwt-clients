# Expense Tracker API with Sessions

## Description
This is a Flask backend API with a React frontend that allows users to sign up, log in, and manage their personal expenses. The application uses session-based authentication to maintain user login state across requests.

## Features
- User authentication (signup, login, logout, session check)
- Session-based authentication with persistent login
- Full CRUD for expenses
- Pagination for expenses
- Protected routes (users can only access their own data)
- React frontend integrated with Flask backend

## Installation
```bash
pipenv install
pipenv shell
```

## Database Setup
```bash
flask db upgrade
python seed.py
```

## Run the Application

### Start Backend
```bash
flask run
```

### Start Frontend
```bash
npm install
npm start
```

## API Endpoints

### Auth
- POST /signup  
- POST /login  
- DELETE /logout  
- GET /me  

### Expenses
- POST /expenses  
- GET /expenses?page=1&per_page=5  
- GET /expenses/<id>  
- PATCH /expenses/<id>  
- DELETE /expenses/<id>  

## Notes
- Authentication is handled using Flask sessions.
- The frontend communicates with the backend via a proxy.
- Session persists across page refresh.
- Each user can only access their own data.