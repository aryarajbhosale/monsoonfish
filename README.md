# Logo Processing Service

A FastAPI-based image processing service that accepts a logo image upload, generates three processed variants (Silhouette, Border, and Grayscale), stores them on the server, and automatically sends the generated outputs via email as attachments.

## Features

* Upload PNG, JPG, and JPEG logo images
* File size validation (maximum 5 MB)
* Silhouette generation using contour detection and contour filling
* Border generation using edge detection
* Grayscale image generation
* Automatic email delivery with generated outputs attached
* Environment variable based configuration
* REST API built using FastAPI
* User-friendly web interface

---

## Project Structure

```text
.
├── main.py
├── routes/
│   └── process.py
├── services/
│   ├── image_processor.py
│   └── email_service.py
├── utils/
│   └── validators.py
├── static/
│   └── index.html
├── outputs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Technologies Used

* Python 3.12
* FastAPI
* OpenCV
* Pillow
* NumPy
* SMTP (Gmail App Password Authentication)
* HTML/CSS/JavaScript

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd logo-processing-service
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from `.env.example`.

Example:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_APP_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=recipient@example.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### Gmail Configuration

1. Enable 2-Step Verification on your Google Account.
2. Generate an App Password.
3. Use the generated App Password instead of your Gmail password.

---

## Run the Application

```bash
uvicorn main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

---

## API Endpoint

### POST `/api/process`

Processes an uploaded logo image.

### Request

Content-Type:

```text
multipart/form-data
```

Form field:

```text
file
```

### Success Response

```json
{
  "silhouette": "generated",
  "border": "generated",
  "grayscale": "generated",
  "email_status": "sent"
}
```

---

## Validation Rules

| Rule              | Value          |
| ----------------- | -------------- |
| Allowed Formats   | PNG, JPG, JPEG |
| Maximum File Size | 5 MB           |
| Empty File Upload | Not Allowed    |

---

## Generated Outputs

| Output     | Description                                                  |
| ---------- | ------------------------------------------------------------ |
| Silhouette | Solid filled shape of the logo without internal details      |
| Border     | Edge-only version generated using contour and edge detection |
| Grayscale  | Standard grayscale representation of the uploaded logo       |

Generated files are stored in:

```text
outputs/
```

---

## Email Workflow

After successful processing:

1. Silhouette image is generated.
2. Border image is generated.
3. Grayscale image is generated.
4. All generated images are attached to an email.
5. Email is sent automatically using SMTP.

Email Subject:

```text
Processed Logo Output Results
```

---

## Error Handling

| Status Code | Description                 |
| ----------- | --------------------------- |
| 400         | Empty or missing file       |
| 413         | File size exceeds 5 MB      |
| 415         | Unsupported file type       |
| 500         | Internal processing failure |

---

## Future Improvements

* ZIP download of all generated outputs
* Drag-and-drop upload support
* Cloud storage integration
* Docker deployment
* Additional image processing filters

---

## Author

Aryaraj Bhosale

Built as part of the MonsoonFish Internship Assignment.
