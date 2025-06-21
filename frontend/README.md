# Frontend - CRUD API Server Python

This is the React frontend for the CRUD API Server Python project. It provides a modern, user-friendly interface for managing courses via the backend FastAPI API.

## Tech Stack
- **React** (with hooks)
- **Vite** (for fast development and build)
- **Tailwind CSS** (for styling)
- **ESLint** (for code quality)

## Features
- Add, view, edit, and delete courses
- Responsive and clean UI
- Interacts with the FastAPI backend via REST API

## Development

- Frontend code: `frontend/`

You can run backend and frontend separately for development if you prefer:

**Frontend:**
```sh
cd frontend
npm install
npm run dev
```
- The app will be available at [http://localhost:3000](http://localhost:3000)

**Backend:**
See the backend `README.md` for instructions on running the API server.

## Project Structure
- Main entry: `src/main.jsx`
- App component: `src/App.jsx`
- API logic: `src/api.js`
- UI components: `src/components/`

## Customization
- Update API endpoint URLs in `src/api.js` if your backend runs on a different host/port.
- Modify styles in `src/App.css` or use Tailwind classes.

## Building for Production
```sh
npm run build
```
The production-ready files will be in the `dist/` directory.