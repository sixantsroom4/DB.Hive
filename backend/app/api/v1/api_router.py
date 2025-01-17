from fastapi import APIRouter, UploadFile, Form, Depends
from typing import Optional
from datetime import datetime
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile,
    dataset_name: str = Form(...),
    description: str = Form(...)
):
    try:
        # 파일 저장 디렉토리 생성
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 파일명에 타임스탬프 추가
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        # 파일 저장
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        return {
            "filename": filename,
            "dataset_name": dataset_name,
            "description": description,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
