# Math Edu Monorepo

Monorepo with:
- `backend/`: Django + DRF + JWT API for math learning platform.
- `frontend/`: React + Vite + Tailwind + shadcn-style UI.

## Backend

### Stack
- Django
- Django REST Framework
- SimpleJWT
- django-cors-headers

### Domain models
- `Course`
- `Module`
- `Lesson` (`video_url`)
- `Problem`
- `Enrollment`
- `Attempt`

### API base
- `/api/v1/`

### Endpoints
- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/refresh/`
- `GET /api/v1/auth/me/`
- `GET /api/v1/courses/`
- `GET /api/v1/courses/{id|slug}/`
- `POST /api/v1/courses/{id}/enroll/`
- `GET /api/v1/courses/{id}/tree/`
- `GET /api/v1/lessons/{id}/`
- `POST /api/v1/attempts/submit/`
- `GET /api/v1/me/enrollments/`

### Seed
```bash
cd backend
python manage.py seed_demo
```

Creates:
- 1 course: `Подготовка к НИШ и РФМШ по математике`
- 2 modules
- 2 lessons
- 6 problems (3 per lesson)
- optional demo user: `student / student12345`

### Run
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8001
```

## Frontend

### Stack
- React + Vite + TypeScript
- Tailwind CSS
- shadcn/ui-style component setup

### Pages
- `/` Home
- `/courses/:courseId` Course detail
- `/learn/:courseId/:lessonId` Learn layout
- `/login` Login + Register

### Run
```bash
cd frontend
npm install
npm run dev
```

Default API URL:
- `http://127.0.0.1:8001/api/v1`

Override with:
- `VITE_API_BASE_URL`

## Env (backend)
Copy `backend/.env.example` and adjust values.
