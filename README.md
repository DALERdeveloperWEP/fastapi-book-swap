# 📚 FastAPI Book Swap

A mini RESTful API built with **FastAPI** and **PostgreSQL** for a peer-to-peer book swapping / buying platform. Users can list books they own, browse available books, and send buy/swap requests — all backed by a clean SQLAlchemy ORM data layer.

---

## ✨ Features

- **User management** — register and manage user profiles (with Telegram ID, phone, email, avatar, and role support)
- **Book listings** — add books with images, pricing, and availability/sharing flags
- **Buy requests** — submit buy/swap requests with delivery method, quantity, and status tracking (`pending`, `accepted`, `rejected`)
- **Auto table creation** — SQLAlchemy creates all tables on startup
- **Environment-based config** — database credentials loaded from a `.env` file via Pydantic Settings

---

## 🗂️ Project Structure

```
fastapi-mini-book-project/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── router.py        # Central APIRouter
│   │   ├── user.py          # User endpoints
│   │   ├── book.py          # Book endpoints
│   │   └── swap.py          # Buy/swap request endpoints
│   ├── models/
│   │   ├── user.py          # User SQLAlchemy model
│   │   ├── book.py          # Book SQLAlchemy model
│   │   └── swap.py          # BuyRequest SQLAlchemy model
│   ├── schemas/             # Pydantic request/response schemas
│   └── core/
│       ├── config.py        # Pydantic Settings (reads .env)
│       ├── database.py      # SQLAlchemy engine, Base, SessionLocal
│       ├── dependencies.py  # FastAPI dependency (get_db)
│       └── security.py      # Auth / security utilities
├── requirements.txt
├── .env                     # Your local secrets (not committed)
├── .env.local               # Template for environment variables
└── .gitignore
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.135 |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL (via psycopg2-binary) |
| Validation | Pydantic v2 |
| Config | pydantic-settings |
| Server | Uvicorn |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/DALERdeveloperWEP/fastapi-book-swap.git
cd fastapi-book-swap
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.local` to `.env` and fill in your PostgreSQL credentials:

```bash
cp .env.local .env
```

```env
db_name=your_database_name
db_user=your_db_user
db_pass=your_db_password
db_host=localhost
db_port=5432
```

### 5. Run the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at **http://127.0.0.1:8000**

Interactive docs: **http://127.0.0.1:8000/docs**

---

## 🗃️ Data Models

### User
| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key, auto-increment |
| `first_name` | String(24) | Required |
| `last_name` | String(24) | Required |
| `telegram_id` | String(11) | Required, unique |
| `phone` | String(15) | Optional, unique |
| `email` | String(255) | Optional, unique |
| `avatar` | String | Optional |
| `role` | String | Default: `user` |
| `created_at` | DateTime | Auto-set on create |
| `updated_at` | DateTime | Auto-set on update |

### Book
| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key, auto-increment |
| `title` | String(255) | Required |
| `book_image` | String | Required (image path/URL) |
| `user_id` | Integer | FK → `users.id` (CASCADE delete) |
| `price` | Float | Required |
| `is_available` | Boolean | Default: `True` |
| `share` | Boolean | Default: `False` |
| `created_at` | DateTime | Auto-set on create |
| `updated_at` | DateTime | Auto-set on update |

### BuyRequest
| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key, auto-increment |
| `book_id` | Integer | FK → `books.id` (RESTRICT delete) |
| `user_id` | Integer | FK → `users.id` (CASCADE delete) |
| `total_books` | Integer | Required |
| `delivery_method` | String(64) | Required |
| `status` | String(24) | Default: `pending` |

---

## 📡 API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check / home |
| *More endpoints coming soon* | `/api/...` | User, Book, Swap routes |

> Interactive Swagger UI available at `/docs` when the server is running.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).