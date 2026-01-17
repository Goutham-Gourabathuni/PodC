import os
import uuid
import httpx
import aiofiles
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = os.path.join("backend", "storage", "audio")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves an uploaded file to the local disk.
    """
    file_id = str(uuid.uuid4())
    filename = upload_file.filename or "unknown"
    _, ext = os.path.splitext(filename)
    if not ext:
        ext = ".mp3" # Default fallback
        
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await upload_file.read(1024 * 1024):  # Read 1MB chunks
            await out_file.write(content)
            
    return file_path

async def download_audio_from_url(url: str) -> str:
    """
    Downloads audio file from a direct URL.
    """
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp3") # Simplified extension handling
    
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream('GET', url) as response:
                if response.status_code != 200:
                    raise HTTPException(status_code=400, detail=f"Failed to download: {response.status_code}")
                
                async with aiofiles.open(file_path, 'wb') as out_file:
                    async for chunk in response.aiter_bytes():
                        await out_file.write(chunk)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")
            
    return file_path
