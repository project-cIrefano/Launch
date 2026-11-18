# TAZA FOOD CORNER — Django Food Delivery & Dine-in Website

A redesigned, responsive Django project based on the five-page TAZA FOOD CORNER wireframe supplied by the project owner. The interface uses a strict **red, black and white** palette, with a white/dark theme switch that stays within those colours.

## 1. Design mapping — follows the supplied five-page layout

| Supplied page | What the page contains | Implemented URL |
|---|---|---|
| Page 1 — Home | TAZA FOOD CORNER logo; EN/Bangla interface-label toggle; white/dark theme; cart; menu drawer; Delivery and Dine-in routes; Sign in; three featured offer banners; footer links for opening hours, feedback, FAQ, contact and about | `/` |
| Page 2 — All Products | All products/items; product count; category filters; search; unit labels; quantity selector; add to cart | `/menu/` |
| Page 3 — Outlet Finder | Browser location permission requested after a click; Leaflet map using OpenStreetMap tiles; radius filter; outlet list with phone numbers and opening hours; select an outlet | `/outlets/?mode=DINE_IN` |
| Page 4 — Confirmed Order | Order number; order type; order status; payment status; selected items and totals; link to payment options | `/orders/<order-number>/confirmed/` |
| Page 5 — Payment Option | Cash on delivery / cash at outlet; demo-only bKash and card options; amount due; payment status | `/orders/<order-number>/payment/` |

The menu drawer includes **Offers, Coupons, Order history, Delivery, Find an outlet, Outlet opening hours, Feedback, FAQ, Contact us and About**.

## 2. Technology stack

- **Python 3.15 + Django 6.1.3** for the backend and server-rendered pages.
- **Django REST Framework** for the product, nearby-outlet and customer-order API endpoints.
- **HTML5, CSS3 and vanilla JavaScript** for the responsive frontend.
- **SQLite by default** for the easiest first run; **MySQL with XAMPP** is supported through environment variables.
- **Leaflet + OpenStreetMap** for the outlet map; no Google Maps API key is required for this learning project.
- Django authentication and Django Admin for account and management tasks.

Django 6.1.3 supports Python 3.15. The project pins that version because the development machine shown in the support conversation uses Python 3.15. If you use another Python release, check Django's official compatibility table before changing the pin.

## 3. Windows setup (recommended: use a NEW folder)

> This is a revised project with a clean initial migration. Extract this ZIP into a **new folder**, for example `E:\IRFA\taza_food_corner_project`. Do not copy the old `db.sqlite3` into this project. Your previous project folder is not changed.

Open VS Code terminal / PowerShell and enter the extracted folder:

```powershell
cd E:\IRFA\taza_food_corner_project
```

Create and activate a virtual environment:

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `py -3.15` is not recognised, use this instead:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install packages using the active environment's Python:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Confirm that Python points inside `.venv`:

```powershell
python -c "import sys; print(sys.executable)"
python -c "import django; print(django.get_version())"
```

The executable path should end with `.venv\Scripts\python.exe` and the Django version should be `6.1.3`.

Create database tables using the included migration (you do **not** need to run `makemigrations` for the first setup):

```powershell
python manage.py migrate
```

Add sample menu, outlets and coupons:

```powershell
python manage.py seed_demo
```

Create your administrator:

```powershell
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver
```

Open the website at <http://127.0.0.1:8000/>.

Admin panel: <http://127.0.0.1:8000/admin/>.

## 4. Demo user flow

1. Open the home page.
2. Select **Delivery** to visit the product menu, or **Dine-in** to open the outlet finder.
3. On the outlet finder, click **Use my location**. The browser asks for permission. If permission is denied, the outlet list can still be used manually.
4. Set the radius and choose an outlet. The sample records are demo locations around Chattogram.
5. Add products to your cart. The product cards show item units and let you choose a quantity.
6. Open the cart and continue to checkout. Add a delivery address for delivery, or an outlet for dine-in. Optional coupons: `WELCOME10`, `TAZA50`, `FAMILYFEAST`.
7. Place the order. The confirmed order screen shows the order number and the order/payment summary.
8. Continue to the payment page and select a payment option.

## 5. Demo data warning — replace before real use

The `seed_demo` command creates illustrative outlet records with placeholder phone numbers and approximate demo coordinates. These are **not verified real branches or contact numbers**. Before presenting the project as a real business website, sign in to Django Admin and replace each demo outlet's:

- Outlet name and full address
- Phone number
- Latitude and longitude
- Opening hours

You can also add or edit categories, product names, prices, images, availability, featured status, coupons and feedback in Django Admin.

## 6. Main URLs

| URL | Purpose |
|---|---|
| `/` | Home page and featured offer banners |
| `/menu/` | All food items |
| `/cart/` | Shopping cart and quantities |
| `/outlets/?mode=DINE_IN` | Dine-in outlet finder/map |
| `/outlets/?mode=DELIVERY` | Outlet finder for delivery source selection |
| `/checkout/` | Delivery/dine-in checkout |
| `/orders/<number>/confirmed/` | Confirmed order page |
| `/orders/<number>/payment/` | Payment options |
| `/orders/` | Signed-in customer's order history |
| `/offers/` | Featured offers |
| `/coupons/` | Coupon list |
| `/feedback/` | Feedback form |
| `/faq/` | Frequently asked questions |
| `/contact/` | Contact page |
| `/about/` | About Taza Food Corner |
| `/opening-hours/` | Outlet opening hours |
| `/staff/` | Staff order-status dashboard (staff user only) |
| `/delivery/` | Delivery status dashboard (staff user only) |
| `/admin/` | Django Admin |

## 7. REST API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/products/` | Returns active menu products; optional `?category=burgers` |
| GET | `/api/outlets/nearby/?lat=22.35&lng=91.80&radius=10` | Returns outlets within the radius, sorted by distance |
| GET | `/api/orders/` | Returns orders for the authenticated user |

The nearby-outlets API uses a Haversine distance calculation on the server. Browser geolocation is requested only after the customer presses the location button. Geolocation is available on `localhost` during development and on secure HTTPS sites after deployment.

The map loads tiles from the official `https://tile.openstreetmap.org/{z}/{x}/{y}.png` endpoint and requires an internet connection. The project sends a cross-origin Referer policy and keeps visible OpenStreetMap attribution. Do not bulk-download tiles or disable browser caching. OpenStreetMap's standard tile service is best-effort and may block traffic that violates its tile policy or comes through a blocked network. If tiles remain blocked, use a tile provider with a suitable service plan/API key or host your own tiles; the outlet list and manual selection still work.

## 8. MySQL / XAMPP setup

SQLite is the default and is best for the first run. To use MySQL instead:

1. Start **MySQL** in XAMPP.
2. Open phpMyAdmin and create a database named `taza_food_corner` with `utf8mb4` character set/collation.
3. In the same PowerShell terminal, set:

```powershell
$env:DB_ENGINE="mysql"
$env:DB_NAME="taza_food_corner"
$env:DB_USER="root"
$env:DB_PASSWORD=""
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

4. Run:

```powershell
python manage.py migrate
python manage.py seed_demo
```

The MySQL database is separate from the SQLite database. Keep `DB_ENGINE=sqlite` when you want to run the SQLite version again.

## 9. Weather and menu assistant widgets

The shared site layout includes a weather card and a Groq-powered menu assistant. To enable them, set API keys in the same PowerShell session before starting Django:

```powershell
$env:OPENWEATHER_API_KEY="your-openweather-api-key"
$env:GROQ_API_KEY="your-groq-api-key"
$env:GROQ_MODEL="openai/gpt-oss-20b"
python manage.py runserver
```

Create keys with OpenWeather and xAI, and keep them server-side; do not put them in JavaScript or commit them. Without a key, the corresponding widget displays a configuration message. The weather card initially shows Chattogram weather; visitors can choose to share their browser location for local weather. The assistant answers menu and ordering questions and directs visitors to the menu for current prices and availability.

## 10. Payment safety

Cash on delivery and pay-at-outlet are workflow options. The bKash and card entries are **demo-only**: selecting them marks the sample order as paid for a classroom demonstration, but no real transaction takes place. The project does not ask for or store card numbers, CVV, PINs or banking passwords. For real online payments, integrate a provider's official hosted checkout and verify payment callbacks on the server.

## 10. Helpful commands

```powershell
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
python manage.py test
```

A new project database starts clean because `db.sqlite3` is not included in the ZIP. The `store/0001_initial.py` migration is included, so the first `migrate` creates tables in dependency order.

## 11. Before deployment

- Set a strong `DJANGO_SECRET_KEY` in the environment.
- Set `DJANGO_DEBUG=False` and configure `DJANGO_ALLOWED_HOSTS`.
- Use a persistent PostgreSQL or MySQL database on Vercel; its function filesystem is not persistent, so SQLite is not suitable for deployed orders, products or sessions.
- Use HTTPS, secure cookies, production static-file hosting, logging and database backups.
- Replace demo outlet data with verified business information.
- Add real email/SMS delivery notifications and a real payment gateway only when required.
- Run Django's deployment checks and have permissions/payment flows reviewed before accepting real customer orders.

This is a substantial student/demo starter project, not an audited commercial platform.

## 12. Deploying on Vercel

This repository is a Django application. Import the GitHub repository with the root directory set to `./`, choose the **Django** preset if it is offered, and leave the build, output and install commands on automatic. Vercel detects `manage.py`, and `STATIC_ROOT` is configured for static-file collection.

Before deploying, add these variables in Vercel for both **Production** and **Preview**:

| Variable | Value |
|---|---|
| `DJANGO_SECRET_KEY` | A new, long random secret; do not use the example value. |
| `DJANGO_DEBUG` | `False` |
| `DATABASE_URL` | A connection URL for a persistent PostgreSQL database. |
| `OPENWEATHER_API_KEY` | Optional; enables weather. |
| `GROQ_API_KEY` | Optional; enables the menu assistant. |
| `GROQ_MODEL` | Optional; defaults to `openai/gpt-oss-20b`. |

Vercel's deployment hostnames are added to Django's allowed-host list automatically. Add any custom domain to `DJANGO_ALLOWED_HOSTS` as a comma-separated list. `DATABASE_URL` takes precedence over `DB_ENGINE`; PostgreSQL URLs should use the `postgres://` or `postgresql://` scheme. Remote MySQL remains available with `DB_ENGINE=mysql` and the `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` variables.

After the database is connected, link this checkout to the Vercel project with `vercel link`. Then apply the included migrations and add starter menu data once using the production environment:

```sh
vercel env run --environment=production -- python manage.py migrate --noinput
vercel env run --environment=production -- python manage.py seed_demo
```

For local development, pull the Vercel Development variables with `vercel env pull .env.local --environment=development`; Django loads `.env.local` automatically. Do not commit `.env`, `.env.local`, database URLs, Django secrets, or API keys. Vercel environment-variable changes require a new deployment to take effect.

## Restaurant logo

The supplied black-and-gold restaurant emblem is installed at `store/static/store/images/taza-logo.png`. The header and footer load it through Django's `{% static %}` template tag in `store/templates/store/base.html`. To replace it later, overwrite that PNG with your new logo using the same filename, or update the image path in `base.html`.

