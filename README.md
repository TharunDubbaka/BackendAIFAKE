# AI Fake Review Detector – Backend

FastAPI app with a Gemini AI agent that classifies reviews as fake or genuine.

## Env

Create a `.env` (or use the existing one) with:

- `GEMINI_API_KEY` – Google AI Studio API key
- `SECRET` – app secret
- `DEBUG` – `True` or `False`

## Run

From the `backend` folder:

```bash
cd backend
pip install -r requirements.txt
```

Then start the server with **one** of these (use the module form if `uvicorn` command is not found):

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

or:

```bash
python run.py
```

Server runs at **http://localhost:5000**.

## Endpoints

- `GET /health` – health check
- `POST /api/check-review` – body (JSON):
  - `review_text` (string)
  - `review_source` (string, optional)
  - `stay_date` (string, optional)
  - `stay_type` (string, optional: `business` | `family` | `solo`)
  - `stars` (number 1–5, optional)

Response: `{ "is_fake": bool, "genuine_score": number, "fake_score": number, "reason": string }`

## Frontend

Start the frontend from the project root:

```bash
npm run dev
```

It will call `http://localhost:5000` for the New Review check. Start the backend before using “Check This Review”.

This is a hackathon project which we did
