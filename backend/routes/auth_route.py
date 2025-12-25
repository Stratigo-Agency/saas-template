from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Body
from pydantic import BaseModel, EmailStr
from controller.auth_controller import AuthController

router = APIRouter()
auth_controller = AuthController()

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class OAuthRequest(BaseModel):
    provider: str
    redirect_url: Optional[str] = None

class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    website: Optional[str] = None
    bio: Optional[str] = None
    [key: str]: any  # Allow additional fields

class AuthResponse(BaseModel):
    success: bool
    user: Optional[dict] = None
    session: Optional[dict] = None
    url: Optional[str] = None
    error: Optional[str] = None

@router.get("/session", response_model=AuthResponse)
async def get_session(authorization: Optional[str] = Header(None)):
    """Get the current session."""
    try:
        session = await auth_controller.get_session(authorization)
        if session:
            return {"success": True, "user": session.get("user")}
        else:
            return {"success": False, "error": "No session found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signup", response_model=AuthResponse)
async def sign_up(request: SignUpRequest):
    """Sign up a new user."""
    try:
        result = await auth_controller.sign_up(request.email, request.password)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signin", response_model=AuthResponse)
async def sign_in(request: SignInRequest):
    """Sign in a user."""
    try:
        result = await auth_controller.sign_in(request.email, request.password)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/oauth", response_model=AuthResponse)
async def sign_in_with_oauth(request: OAuthRequest):
    """Sign in with OAuth provider."""
    try:
        if request.provider not in ['google', 'github', 'facebook']:
            raise HTTPException(status_code=400, detail='Invalid OAuth provider')
        result = await auth_controller.sign_in_with_oauth(request.provider, request.redirect_url)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signout", response_model=AuthResponse)
async def sign_out(authorization: Optional[str] = Header(None)):
    """Sign out a user."""
    try:
        result = await auth_controller.sign_out(authorization)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile", response_model=dict)
async def get_user_profile(authorization: Optional[str] = Header(None)):
    """Get user profile."""
    if not authorization:
        raise HTTPException(status_code=401, detail='Not authenticated')
    try:
        profile = await auth_controller.get_user_profile(authorization)
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/profile", response_model=AuthResponse)
async def update_user_profile(
    request: UpdateProfileRequest,
    authorization: Optional[str] = Header(None)
):
    """Update user profile."""
    if not authorization:
        raise HTTPException(status_code=401, detail='Not authenticated')
    try:
        profile_dict = request.dict(exclude_unset=True)
        result = await auth_controller.update_user_profile(authorization, profile_dict)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

