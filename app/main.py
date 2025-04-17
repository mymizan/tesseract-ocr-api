from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io
import tempfile
import subprocess
import os

app = FastAPI(
    title="Tesseract OCR API",
    description="Extract text from images or PDFs using Tesseract with Bengali language support.",
    version="2.0.0"
)

# CORS middleware (optional, remove if unnecessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
async def ocr_image(
    file: UploadFile = File(...),
    lang: str = Form(default="eng")
):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image, lang=lang)
        return {"text": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ocr/pdf")
async def ocr_pdf(
    file: UploadFile = File(...),
    lang: str = Form(default="eng")
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf.flush()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_pdf:
                subprocess.run([
                    "ocrmypdf",
                    "-l", lang,
                    "--force-ocr",
                    temp_pdf.name,
                    output_pdf.name
                ], check=True)

                with open(output_pdf.name, "rb") as f:
                    result_text = subprocess.check_output(["pdftotext", output_pdf.name, "-"])
                
                os.unlink(temp_pdf.name)
                os.unlink(output_pdf.name)

                return {"text": result_text.decode("utf-8")}

    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": f"OCRmyPDF failed: {e}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})