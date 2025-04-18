# 🧠 Tesseract OCR API (Image + PDF | Bengali Supported | FastAPI + Swagger)

This is a self-hosted REST API for extracting text from **images and PDFs** using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [OCRmyPDF](https://ocrmypdf.readthedocs.io).  
It's powered by [FastAPI](https://fastapi.tiangolo.com/) with built-in Swagger docs and packaged as a Docker container.

---

## ✅ Features

- 🖼️ OCR for image files (`.jpg`, `.png`, etc.)
- 📄 OCR for PDF files (`.pdf`) using `ocrmypdf`
- 🌍 Language support: **English** and **Bengali** (Bangla)
- 📚 OpenAPI & Swagger UI for testing and docs
- ⚙️ REST API — easy to integrate anywhere
- 🐳 Fully Dockerized (zero local dependencies)

---

## 📦 Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI server with image + PDF OCR
│   └── requirements.txt     # Python dependencies
├── Dockerfile               # Builds image with Tesseract + OCRmyPDF
├── docker-compose.yml       # Runs API container
└── README.md                # Project documentation
```

---

## 🐳 How to Run (Docker)

### First Time:
```bash
docker-compose up --build
```

This will:
- Build the image
- Install Tesseract with Bengali support
- Install OCRmyPDF and run the API server

### Next Time (no need to rebuild):
```bash
docker-compose up -d
```

To stop it:
```bash
docker-compose down
```

---

## 🌐 API Endpoints

### 🔤 `POST /ocr` — Image OCR

Extract text from an image file.

**Request (multipart/form-data):**
- `file`: image file (`.jpg`, `.png`, etc.)
- `lang`: language code (optional, default is `eng`)

**Response:**
```json
{
  "text": "Extracted text here..."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/ocr \
  -F "file=@sample.png" \
  -F "lang=ben"
```

---

### 📄 `POST /ocr/pdf` — PDF OCR

Extract text from a PDF using `ocrmypdf`.

**Request (multipart/form-data):**
- `file`: PDF file
- `lang`: language code (optional, default is `eng`)

**Response:**
```json
{
  "text": "Text extracted from the PDF file..."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/ocr/pdf \
  -F "file=@document.pdf" \
  -F "lang=eng"
```

---

## 🔍 API Docs with Swagger

After running the container, open your browser:

```
http://localhost:8000/docs
```

You'll see interactive, auto-generated documentation with a "Try it out" feature.

---

## 🌍 Supported Languages

Currently installed:

- `eng` – English
- `ben` – Bengali (Bangla)

Tesseract supports 100+ languages.

---

## ➕ Add More Language Support

To add more languages, edit the `Dockerfile` and install the desired language packs.

### Example:

To add Arabic (`ara`) and Hindi (`hin`), update this section:

```Dockerfile
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ben \
    tesseract-ocr-ara \
    tesseract-ocr-hin \
    ...
```

Then rebuild the image:

```bash
docker-compose up --build
```

You can find the full list of available languages here:  
🔗 https://github.com/tesseract-ocr/tessdata

Use the language code as the value for the `lang` parameter in the API.

---

## 📝 License

This project is MIT licensed — feel free to use and modify it for personal or commercial use.

---

## 🙌 Contribute

Pull requests are welcome! You can help by:
- Adding more language support
- Improving PDF/image processing
- Adding auth, usage limits, or queue support