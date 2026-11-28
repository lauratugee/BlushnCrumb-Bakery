# Blush n Crumb deployment notes

The project includes a Render blueprint for a demo deployment. It creates a web service and a PostgreSQL database in Frankfurt. The free Render web service can sleep while idle, and Render's free PostgreSQL database expires after 30 days; do not use that database for important or long-lived orders. See [Render's free plan limitations](https://render.com/docs/free). A lasting deployment needs a paid persistent database/service or another host with persistent storage.

## API endpoints

- `GET /api/products/` lists products that are in stock.
- `POST /api/orders/` creates an authenticated order. Send `order_type`, optional `delivery_address`, and an `items` list containing `product_id` and `quantity`.
- `GET /api/my-orders/` returns only the signed-in customer's orders.
- `/api-auth/login/` provides login for the browsable API.

Order requests require an authenticated customer. Product information is public. Stock and delivery address are validated by the API.

## Local setup

1. Install the dependencies with `python -m pip install -e .`.
2. Apply migrations with `python manage.py migrate`.
3. Create a staff account with `python manage.py createsuperuser` if needed.
4. Start the local server with `python manage.py runserver`.

## Hosting checklist

For the included Render blueprint, commit and push the project, connect the GitHub repository to Render, and apply `render.yaml`. Render generates `DJANGO_SECRET_KEY` and supplies `DATABASE_URL`. Do not commit real secrets.

For another Django-capable host, configure these environment variables in its dashboard:

- `DJANGO_SECRET_KEY`: a unique, long random secret.
- `DJANGO_DEBUG`: `false`.
- `DJANGO_ALLOWED_HOSTS`: the exact host name assigned to the site.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: the site's HTTPS origin, including `https://`.
- `DJANGO_SECURE_SSL_REDIRECT`: `true` when HTTPS is configured by the host.

Install the project dependencies, run `python manage.py migrate`, and run `python manage.py collectstatic --noinput`. Start the app with `gunicorn config.wsgi:application` on Linux-based hosts. Create a staff account on the host before managing products and orders. The hosted database starts empty; products and users in your local SQLite database are not copied automatically.

The default database is SQLite. For a hosted deployment, use persistent storage supported by the selected host or configure its managed PostgreSQL database before accepting real orders. The local SQLite file is excluded from Git and is not automatically carried into a deployment.
