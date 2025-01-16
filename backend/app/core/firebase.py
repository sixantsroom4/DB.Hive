import firebase_admin
from firebase_admin import credentials, storage, firestore, auth
import os
from typing import Dict, Optional

# Firebase 초기화
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "../../../admin/dbhive-5a328-firebase-adminsdk-yxqs2-0c60412aec.json"))

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'dbhive-5a328.appspot.com'
})

# Storage 버킷 초기화
bucket = storage.bucket()

# Firestore 데이터베이스 초기화
db = firestore.client()

# Auth 함수들
def verify_token(id_token: str) -> Dict:
    """
    Firebase ID 토큰을 검증하고 사용자 정보를 반환합니다.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture")
        }
    except Exception as e:
        raise ValueError(f"Invalid token: {str(e)}")

def get_user_profile(uid: str) -> Optional[Dict]:
    """
    사용자 프로필 정보를 Firestore에서 가져옵니다.
    """
    doc_ref = db.collection('users').document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_or_update_user_profile(uid: str, data: Dict):
    """
    사용자 프로필을 생성하거나 업데이트합니다.
    """
    doc_ref = db.collection('users').document(uid)
    doc_ref.set(data, merge=True)

# Storage 함수들
def upload_file_to_firebase(file_data: bytes, filename: str, content_type: str, user_id: str) -> str:
    """
    Firebase Storage에 파일을 업로드합니다.
    """
    blob = bucket.blob(f'datasets/{user_id}/{filename}')
    blob.upload_from_string(
        file_data,
        content_type=content_type
    )
    blob.make_public()
    return blob.public_url

def save_dataset_metadata(filename: str, original_name: str, description: str, file_url: str, size: int, user_id: str):
    """
    Firestore에 데이터셋 메타데이터를 저장합니다.
    """
    doc_ref = db.collection('datasets').document()
    doc_ref.set({
        'filename': filename,
        'originalName': original_name,
        'description': description,
        'fileUrl': file_url,
        'size': size,
        'userId': user_id,
        'createdAt': firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id

def get_all_datasets(user_id: Optional[str] = None):
    """
    모든 데이터셋 메타데이터를 가져옵니다.
    user_id가 제공되면 해당 사용자의 데이터셋만 반환합니다.
    """
    query = db.collection('datasets').order_by('createdAt', direction=firestore.Query.DESCENDING)
    if user_id:
        query = query.where('userId', '==', user_id)
    
    datasets = []
    for doc in query.stream():
        data = doc.to_dict()
        # 사용자 정보 가져오기
        user_data = get_user_profile(data.get('userId'))
        datasets.append({
            'id': doc.id,
            'filename': data.get('filename'),
            'originalName': data.get('originalName'),
            'description': data.get('description'),
            'fileUrl': data.get('fileUrl'),
            'size': data.get('size'),
            'createdAt': data.get('createdAt'),
            'user': {
                'id': data.get('userId'),
                'name': user_data.get('name') if user_data else None,
                'picture': user_data.get('picture') if user_data else None
            }
        })
    
    return datasets 