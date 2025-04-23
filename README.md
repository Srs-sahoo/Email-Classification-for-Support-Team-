# Email-Classification-for-Support-Team-
The goal of this assignment is to design and implement an email classification system for a 
company's support team. The system should categorize incoming support emails into 
predefined categories while ensuring that personal information (PII) is masked before 
processing. After classification, the masked data should be restored to its original form. 
This project implements a full email classification pipeline with PII masking, traditional machine learning classification, and a FastAPI-based server. It includes:

- **Data Preprocessing** (`utils.py`)
- **Model Training** (`models.py`)
- **Inference Pipeline** (`pipeline.py`)
- **API Server** (`api.py`)
- **Containerization** (`Dockerfile`)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/email_classifier_project.git
   cd email_classifier_project
   ```

2. **Create & activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

---

## 🛠 File Descriptions

### `utils.py`
Contains `mask_pii(text)` which:
- Uses **Regex** and **spaCy NER** to identify PII (emails, phones, names, locations, dates, etc.)
- Replaces each PII instance with a unique token (`<LABEL_xxxxxx>`)
- Returns the **masked text** and a **map of tokens to original values**


### `models.py`
Defines `train_model(data_path)` to:
1. Load the masked dataset (`data/masked_data.csv`).
2. Split into train/test (80/20 split, `random_state=42`).
3. Build a **scikit-learn Pipeline** with `TfidfVectorizer` + `RandomForestClassifier(n_estimators=100)`.
4. Train on the training split, evaluate on the test split, and print a classification report.
5. Serialize the pipeline to `models/email_classifier.pkl` using `joblib`.


### `pipeline.py`
Implements `classify_email(raw_text)` that:
1. Calls `mask_pii(raw_text)` to mask PII.
2. Loads the serialized model pipeline.
3. Runs `pipeline.predict([masked_text])` to obtain the predicted category.
4. Returns a dictionary with:
   - `masked_email`
   - `pii_entities` (map of tokens to originals)
   - `predicted_category`


### `api.py`
Sets up a **FastAPI** server:
- **Endpoint**: `POST /process_email/`
- **Request**: JSON with `"email_text": "<raw_email_string>"`
- **Response**:
  ```json
  {
    "original_email": "...",
    "masked_email": "...",
    "predicted_category": "...",
    "pii_map": {"<LABEL>": "original_value", ...}
  }
  ```
- Error handling via `HTTPException` on failures.


### `Dockerfile`
Containerizes the application:
1. **Base image**: `python:3.12-slim`
2. **Working directory**: `/code`
3. **Copy & install dependencies** from `requirements.txt`
4. **Download spaCy model** (`en_core_web_sm`)
5. **Expose** port `8000`
6. **CMD**: Launch Uvicorn server:
   ```dockerfile
   CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

> **Note:** Ensure `requirements.txt` is spelled correctly (not `requirement.txt`).

---

## 🚀 Usage

### 1. Train the Model

```bash
python - << 'EOF'
from models import train_model
train_model('data/masked_data.csv')
EOF
```

This generates `models/email_classifier.pkl`.


### 2. Run the API Locally

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc


### 3. Test the Endpoint

```bash
curl -X POST http://localhost:8000/process_email/ \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Hi, I’m Alice from Texas. I have a billing question."}'
```


### 4. Build & Run with Docker

```bash
# Build the image
docker build -t email-classifier:latest .

# Run the container
docker run -d -p 8000:8000 email-classifier:latest
```

Access API at http://127.0.0.1:8000/docs#/default/process_email_process_email__post

---

