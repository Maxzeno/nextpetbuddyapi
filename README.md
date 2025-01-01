# NextPetBuddy Backend

## Description
Django backend API for the NextPetBuddy application. This backend handles the management of pets, orders, and payments.

## Prerequisites
Ensure you have the following installed:

- [Python](https://www.python.org) (Version 3.8 or higher)
- [pip](https://pip.pypa.io/en/stable/) (Python package installer)

Additionally, configure the following environment variables in a `.env` file:

```bash
SECRET_KEY=<Secret key>

DEBUG=<true or false - debug mode>

TRY_LOCAL_DB=<true or false - if false uses db set below>
TRY_LOCAL_STORAGE=<true or false - if false uses cloudinary storage set below>
TRY_LOCAL_EMAIL=<true or false - if false uses email settings set below>

DATABASES_DEFAULT_ENGINE=<Database engine - use this "django.db.backends.postgresql">
DATABASES_DEFAULT_NAME=<Database name>
DATABASES_DEFAULT_HOST=<Database host>
DATABASES_DEFAULT_PORT=<Database port>
DATABASES_DEFAULT_USER=<Database user>
DATABASES_DEFAULT_PASSWORD=<Database password>

PAYSTACK_SECRET_KEY=<Your Paystack secret key>

CLOUDINARY_STORAGE_CLOUD_NAME=<Storage name>
CLOUDINARY_STORAGE_API_KEY=<Storage API key>
CLOUDINARY_STORAGE_API_SECRET=<Storage API secret>

EMAIL_HOST=<Email host>
EMAIL_HOST_USER=<Email user>
EMAIL_HOST_PASSWORD=<Email password>
EMAIL_PORT=<Email port>
EMAIL_USE_TLS=<true or false - email use TLS>

ALLOWED_HOST=<domain the backend is hosted on>
FRONTEND_BASE_URL=<domain of frontend>

```

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Maxzeno/nextpetbuddyapi.git
   cd nextpetbuddyapi
   ```

2. **Create a virtual environment**:
   It's recommended to create a virtual environment for your project:
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     env\Scripts\activate.bat
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**:
   Install the necessary Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**:
   Run the following command to apply the migrations:
   ```bash
   python manage.py migrate
   ```

6. **Run the server locally**:
   After installing dependencies and applying migrations, you can start the Django development server by running:
   ```bash
   python manage.py runserver
   ```

   The API will be accessible at `http://localhost:8000/`.
