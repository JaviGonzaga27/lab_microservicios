from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from ..database import get_db_connection
from ..schemas import ImageResponse, ImageSchema
import shutil
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIRECTORY = "uploads/"

# Asegúrate de que el directorio de carga existe
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload/", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}{file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not upload the file")
    
    # Guarda los metadatos en SQLite
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO images (filename, upload_time) VALUES (?, ?)",
        (file.filename, datetime.now())
    )
    image_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return ImageResponse(id=image_id, filename=file.filename, upload_time=datetime.now())

@router.get("/images/{image_name}", response_class=FileResponse)
async def read_image(image_name: str):
    file_path = f"{UPLOAD_DIRECTORY}{image_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

@router.delete("/images/{image_name}")
async def delete_image(image_name: str):
    file_path = f"{UPLOAD_DIRECTORY}{image_name}"
    if os.path.exists(file_path):
        os.remove(file_path)
        
        # Elimina los metadatos de SQLite
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images WHERE filename = ?", (image_name,))
        conn.commit()
        conn.close()
        
        return {"info": f"Image '{image_name}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Image not found")

@router.get("/images/", response_model=list[ImageSchema])
async def list_images():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, upload_time FROM images")
    images = cursor.fetchall()
    conn.close()
    
    return [ImageSchema(id=row[0], filename=row[1], upload_time=row[2]) for row in images]