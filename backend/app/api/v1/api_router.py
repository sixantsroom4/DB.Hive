from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional, List
import logging
from ...core.firebase import upload_file_to_firebase, save_dataset_metadata, get_all_datasets
from datetime import datetime
from .auth_router import get_current_user

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/datasets")
async def get_datasets(current_user = Depends(get_current_user)):
    """업로드된 데이터셋 목록을 반환합니다."""
    try:
        datasets = get_all_datasets()  # 모든 사용자의 데이터셋 표시
        return {"datasets": datasets}
    except Exception as e:
        logger.error(f"Error listing datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-datasets")
async def get_my_datasets(current_user = Depends(get_current_user)):
    """현재 사용자의 데이터셋 목록을 반환합니다."""
    try:
        datasets = get_all_datasets(user_id=current_user["uid"])
        return {"datasets": datasets}
    except Exception as e:
        logger.error(f"Error listing user datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    current_user = Depends(get_current_user)
):
    try:
        logger.info(f"Receiving upload request - File: {file.filename}, Name: {name}, User: {current_user['email']}")
        
        # 파일명 생성 (timestamp를 추가하여 고유성 보장)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        
        # 파일 데이터 읽기
        file_data = await file.read()
        file_size = len(file_data)
        
        # Firebase Storage에 업로드
        file_url = upload_file_to_firebase(
            file_data,
            filename,
            file.content_type or 'application/octet-stream',
            current_user["uid"]
        )
        
        logger.info(f"File uploaded to Firebase Storage: {file_url}")
        
        # Firestore에 메타데이터 저장
        doc_id = save_dataset_metadata(
            filename=filename,
            original_name=file.filename,
            description=description or "",
            file_url=file_url,
            size=file_size,
            user_id=current_user["uid"]
        )
        
        logger.info(f"Metadata saved to Firestore with ID: {doc_id}")
        
        return {
            "id": doc_id,
            "filename": filename,
            "original_name": file.filename,
            "description": description,
            "file_url": file_url,
            "size": file_size,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
