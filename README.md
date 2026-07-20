# fyr.js public website

The public site for Fyr: a Flask-rendered documentation and examples site that uses Fyr in the browser and Three.js for its page-specific loading scenes.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy to Vercel

Vercel detects the `app` Flask instance in `app.py` and runs it as a Python function. Static assets live in `public/assets`, which Vercel serves from its CDN. No separate serverless route is necessary for this informational site.

```powershell
npm i -g vercel
vercel
```

The site has no authentication, sign-up flow, database, contact form, or user data collection.
