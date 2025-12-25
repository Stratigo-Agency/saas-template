from typing import Optional, Dict, Any
from supabase import Client, create_client
from lib.supabase import supabase
from fastapi import HTTPException
import os

class AuthController:
    def __init__(self):
        self.supabase: Client = supabase
        self.supabase_url = os.getenv('SUPABASE_URL')
    
    def _get_user_client(self, access_token: str) -> Client:
        """Create a Supabase client with user's access token."""
        # Use anon key for user operations (the token provides the auth)
        anon_key = os.getenv('SUPABASE_ANON_KEY')
        if not anon_key:
            raise ValueError('SUPABASE_ANON_KEY not set')
        user_client = create_client(self.supabase_url, anon_key)
        user_client.auth.set_session({'access_token': access_token, 'refresh_token': ''})
        return user_client
    
    async def get_session(self, authorization: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get the current session from the authorization token."""
        if not authorization:
            return None
        
        try:
            # Extract token from "Bearer <token>" format
            token = authorization.replace('Bearer ', '') if authorization.startswith('Bearer ') else authorization
            
            # Verify the token and get user
            response = self.supabase.auth.get_user(token)
            if response.user:
                return {
                    'user': {
                        'id': response.user.id,
                        'email': response.user.email,
                        'user_metadata': response.user.user_metadata,
                        'created_at': response.user.created_at,
                    }
                }
            return None
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    async def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        """Sign up a new user."""
        try:
            response = self.supabase.auth.sign_up({
                'email': email,
                'password': password
            })
            
            if response.user:
                return {
                    'success': True,
                    'user': {
                        'id': response.user.id,
                        'email': response.user.email,
                        'user_metadata': response.user.user_metadata,
                        'created_at': response.user.created_at,
                    }
                }
            else:
                raise HTTPException(status_code=400, detail='Failed to create user')
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in a user."""
        try:
            response = self.supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            
            if response.user and response.session:
                return {
                    'success': True,
                    'user': {
                        'id': response.user.id,
                        'email': response.user.email,
                        'user_metadata': response.user.user_metadata,
                        'created_at': response.user.created_at,
                    },
                    'session': {
                        'access_token': response.session.access_token,
                        'refresh_token': response.session.refresh_token,
                        'expires_at': response.session.expires_at,
                    }
                }
            else:
                raise HTTPException(status_code=401, detail='Invalid credentials')
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
    
    async def sign_in_with_oauth(self, provider: str, redirect_url: Optional[str] = None) -> Dict[str, Any]:
        """Sign in with OAuth provider."""
        try:
            options = {'provider': provider}
            if redirect_url:
                options['options'] = {'redirect_to': redirect_url}
            
            response = self.supabase.auth.sign_in_with_oauth(options)
            
            return {
                'success': True,
                'url': response.url
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def sign_out(self, authorization: Optional[str] = None) -> Dict[str, Any]:
        """Sign out a user."""
        try:
            if authorization:
                token = authorization.replace('Bearer ', '') if authorization.startswith('Bearer ') else authorization
                user_client = self._get_user_client(token)
                user_client.auth.sign_out()
            return {'success': True}
        except Exception as e:
            # Even if sign out fails on Supabase side, we consider it successful
            # since the token will expire anyway
            return {'success': True}
    
    async def get_user_profile(self, authorization: str) -> Optional[Dict[str, Any]]:
        """Get user profile."""
        session = await self.get_session(authorization)
        if not session or not session.get('user'):
            raise HTTPException(status_code=401, detail='Not authenticated')
        
        user = session['user']
        return {
            'id': user['id'],
            'email': user['email'],
            'full_name': user.get('user_metadata', {}).get('full_name', ''),
            'created_at': user['created_at'],
            **user.get('user_metadata', {})
        }
    
    async def update_user_profile(self, authorization: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile."""
        session = await self.get_session(authorization)
        if not session or not session.get('user'):
            raise HTTPException(status_code=401, detail='Not authenticated')
        
        try:
            token = authorization.replace('Bearer ', '') if authorization.startswith('Bearer ') else authorization
            user_client = self._get_user_client(token)
            
            # Get current user metadata
            current_user_response = user_client.auth.get_user(token)
            current_metadata = current_user_response.user.user_metadata or {}
            
            # Update user metadata
            from datetime import datetime
            updated_metadata = {
                **current_metadata,
                **profile,
                'updated_at': datetime.now().isoformat()
            }
            
            response = user_client.auth.update_user({
                'data': updated_metadata
            })
            
            if response.user:
                return {
                    'success': True,
                    'user': {
                        'id': response.user.id,
                        'email': response.user.email,
                        'user_metadata': response.user.user_metadata,
                        'created_at': response.user.created_at,
                    }
                }
            else:
                raise HTTPException(status_code=400, detail='Failed to update profile')
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

