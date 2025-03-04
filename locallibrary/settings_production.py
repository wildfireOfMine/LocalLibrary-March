from decouple import config, Csv
ALLOWED_HOSTS = ['.vercel.app']
DEBUG = False
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": config("POSTGRES_HOST"),
        "PORT": 5432,
        "NAME": config("POSTGRES_DATABASE"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD")
    }
}