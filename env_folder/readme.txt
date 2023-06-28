В данной папке находятся папки с env файлами для различных окружений: development, production и тд
Какое окружение булет использоваться для тестового прогона задается переменной окружения ENVIRONMENT_NAME
По умолчанию используется ENVIRONMENT_NAME=development

Каждый .env должен содержать следующие переменные:
# base_url
BASE_URL=www.google.com
API_URLll=${BASE_URL}/api
# db
DB_NAME = postgress
DB_USER = user
DB_PASSWORD = password
DB_HOST = host
DB_PORT = port
# user1 credentials
USER1_EMAIL=email1
USER1_PASSWORD=password1