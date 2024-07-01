Train API Service
A Django REST Framework (DRF) based API service for train management.

Installation from GitHub

1. Install PostgreSQL and create a database.

2. Clone the repository:
`git clone https://github.com/dvkim28/train_api_service.git
cd train_api_service
`
3. Set up a virtual environment and activate it:

``python -m venv venv``

``source venv/bin/activate  # On Windows use `venv\Scripts\activate``

4. Install dependencies:

`pip install -r requirements.txt
`

5. Set environment variables:

`export DB_HOST=<your_db_hostname>
export DB_NAME=<your_db_name>
export DB_USER=<your_db_username>
export DB_PASSWORD=<your_db_password>
export SECRET_KEY=<your_secret_key>`

6. Apply migrations and run the server:

`python manage.py migrate
python manage.py runserver`

Running with Docker
Ensure Docker is installed on your system.

1. Build Docker containers:
`docker-compose build`
2. Start Docker containers:
`docker-compose up`

Accessing the API

1. Create a user:
`POST /api/v1/user/register/`
2. Obtain an access token:
`POST /api/v1/user/token/`

Features:
1. JFT authenticated
2. Admin panel /admin/
3. Documentations is located at /api/schema/swagger-ui/
4. Managing orders and tickets
6. Creating full journeys with stations, train, train type, crew.
7. Filterting routes by destination and source