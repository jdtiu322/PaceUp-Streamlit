# Streamlit Cloud Deployment

## 1. Push this project to GitHub
Make sure these files are in the repo root:
- `app.py`
- `requirements.txt`
- `config.py`
- `services/`
- `screens/`
- `components/`

Do not commit real secrets.

## 2. Create the app in Streamlit Community Cloud
- Open Streamlit Community Cloud
- Click `Create app`
- Select your GitHub repo and branch
- Set the entrypoint to `app.py`

## 3. Add secrets
In the app settings, open `Secrets` and paste values based on `.streamlit/secrets.toml.example`.

Required top-level secrets:
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `FIREBASE_WEB_API_KEY`

Required Firebase section:
- `[firebase]` service account credentials

## 4. Firebase setup
- Firebase Authentication: enable Email/Password
- Firestore: ensure your database exists
- Service account must have Firestore + Auth admin access for the project

## 5. Notes
- This app now prefers `st.secrets` in deployment and falls back to local `.env` / `firebase_config.json` only for local development.
- Local development uses non-secure refresh cookies so `http://localhost` can persist sign-in across browser refreshes.
- For HTTPS deployment, set `AUTH_COOKIE_SECURE=true` in Streamlit secrets or environment variables.
