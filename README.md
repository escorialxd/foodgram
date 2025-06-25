# Foodgram – Recipe Sharing Platform

## Service URL

- [https://foodgram.vadim-polegaev-kittygram.ru/](https://foodgram.vadim-polegaev-kittygram.ru/)

## Project Overview

Foodgram is a web-based platform for sharing culinary recipes, built with Django REST Framework. Users can create, browse, and favorite recipes, follow authors, and generate shopping lists.

## Key Features

### Users

- **Registration and authentication** via email
- **User profiles** with avatar upload
- **Follow/unfollow** other authors
- View **followers** and **following** lists

### Recipes

- **Create, update, and delete** recipes
- **Image upload** (Base64 format)
- **Add ingredients** with quantity specifications
- **Tag** recipes for categorization
- Specify **cooking time**

### Favorites

- Add recipes to **Favorites**
- Browse **Favorite recipes** list

### Shopping List

- Add recipes to **Shopping Cart**
- **Download shopping list** as a PDF
- **Automatic aggregation** of required ingredients

### Ingredients & Tags

- Pre-populated **ingredients** database
- **Tagging system** for recipe categorization
- **Unique constraints** to prevent duplicates

## Technology Stack

### Backend

- **Python 3.13**
- **Django 5.2**
- **Django REST Framework 3.15.2**
- **Djoser 2.3.1**
- **PostgreSQL**
- **Pillow 11.2.1**
- **Poetry**

### Authentication

- **Token-based authentication**
- **JWT tokens** (djangorestframework-simplejwt)
- **Custom** registration flow

## Project Structure

```
foodgram/
├── api/                    # API application
│   ├── recipes/            # Recipe API
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users/              # User API
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── recipes/                # Recipes app
│   ├── models.py           # Data models
│   ├── admin.py            # Admin panel
│   ├── fields.py           # Custom fields
│   └── management/         # Management commands
├── users/                  # Users app
│   ├── models.py           # Custom User model
│   └── admin.py            # Admin panel
├── project_root/           # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL routes
│   └── wsgi.py             # WSGI configuration
├── data/                   # Import data
│   ├── ingredients.json    # Ingredients JSON dump
│   └── ingredients.csv     # Ingredients CSV file
├── media/                  # Uploaded files
├── static/                 # Static files
├── requirements.txt        # Dependencies (alternative)
├── pyproject.toml          # Poetry configuration
├── Dockerfile              # Docker setup
└── manage.py               # Django CLI
```

## Data Models

### User

- Extends Django’s **User** model
- **Email** used as login field
- Supports **avatar** uploads

### Recipe

- Linked to **author** (User)
- Includes **title**, **description**, **image**
- **Cooking time** field
- Many-to-many relations with **ingredients** and **tags**

### Ingredient

- **Name** and **measurement unit**
- **Unique constraint** on (name, unit)

### Tag

- **Name**, **color** (HEX), and **slug**
- Used for recipe categorization

### RecipeIngredient

- Through model connecting **recipes** and **ingredients**
- Stores **amount** per ingredient

### Favorite

- Connects **User** and **Recipe** for favorites

### ShoppingCart

- Connects **User** and **Recipe** for shopping lists

### Subscription

- Connects **Users** to allow following

## Installation and Setup

### Prerequisites

- **Python 3.13**
- **Poetry**
- **PostgreSQL**

### 1. Clone the repository

```bash
git clone <repository-url>
cd foodgram
```

### 2. Install dependencies

```bash
# Install Poetry (if not already installed)
pip install poetry

# Install project dependencies
poetry install
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL settings
db_engine=django.db.backends.postgresql
DB_NAME=foodgram_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# For SQLite (default)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

### 4. Apply database migrations

```bash
poetry run python manage.py migrate
```

### 5. Create a superuser

```bash
poetry run python manage.py createsuperuser
```

### 6. Import data (optional)

```bash
# Import ingredients from JSON
poetry run python manage.py load_ingredients data/ingredients.json

# Import ingredients from CSV
poetry run python manage.py load_ingredients data/ingredients.csv
```

### 7. Run the development server

```bash
poetry run python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/users/` – User registration
- `POST /api/auth/token/login/` – Obtain token
- `POST /api/auth/token/logout/` – Logout

### Users

- `GET /api/users/` – List users
- `GET /api/users/{id}/` – Retrieve user profile
- `GET /api/users/me/` – Retrieve current user
- `PATCH /api/users/me/` – Update profile

### Subscriptions

- `GET /api/users/subscriptions/` – My subscriptions
- `POST /api/users/{id}/subscribe/` – Follow user
- `DELETE /api/users/{id}/subscribe/` – Unfollow user

### Recipes

- `GET /api/recipes/` – List recipes
- `POST /api/recipes/` – Create recipe
- `GET /api/recipes/{id}/` – Retrieve recipe
- `PATCH /api/recipes/{id}/` – Update recipe
- `DELETE /api/recipes/{id}/` – Delete recipe

### Favorites

- `GET /api/recipes/favorite/` – My favorites
- `POST /api/recipes/{id}/favorite/` – Add to favorites
- `DELETE /api/recipes/{id}/favorite/` – Remove from favorites

### Shopping Cart

- `GET /api/recipes/download_shopping_cart/` – Download shopping list
- `POST /api/recipes/{id}/shopping_cart/` – Add to cart
- `DELETE /api/recipes/{id}/shopping_cart/` – Remove from cart

### Ingredients & Tags

- `GET /api/ingredients/` – List ingredients
- `GET /api/tags/` – List tags

## Docker

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t foodgram .

# Run the container
docker run -p 8000:8000 foodgram
```

## Management Commands

```bash
# Import ingredients
poetry run python manage.py load_ingredients <file_path>

# Create tags
poetry run python manage.py create_tags
```

## License

This project is intended for educational purposes.

## Author

**Vadim Polegaev**

