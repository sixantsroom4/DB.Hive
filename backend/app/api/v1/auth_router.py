from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
from pydantic import BaseModel
from ...core.firebase import verify_token, create_or_update_user_profile, get_user_profile

router = APIRouter()

class UserProfile(BaseModel):
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None

async def get_current_user(authorization: str = Header(None)):
    """
    현재 인증된 사용자의 정보를 가져옵니다.
    """
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        token = authorization.split(' ')[1]
        return verify_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/verify-token")
async def verify_auth_token(authorization: str = Header(None)):
    """
    Firebase ID 토큰을 검증합니다.
    """
    try:
        user = await get_current_user(authorization)
        profile = get_user_profile(user["uid"])
        return {
            "user": {
                **user,
                "profile": profile
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/profile")
async def update_profile(
    profile: UserProfile,
    current_user = Depends(get_current_user)
):
    """
    사용자 프로필을 업데이트합니다.
    """
    try:
        create_or_update_user_profile(current_user["uid"], profile.dict())
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
async def get_profile(current_user = Depends(get_current_user)):
    """
    현재 사용자의 프로필을 가져옵니다.
    """
    profile = get_user_profile(current_user["uid"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile 