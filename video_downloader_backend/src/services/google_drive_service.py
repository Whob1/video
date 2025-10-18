from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os
from typing import Dict, Any, Optional
import pickle

class GoogleDriveService:
    """Service for Google Drive integration"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.credentials = None
    
    def get_auth_url(self) -> str:
        """Get Google OAuth2 authorization URL"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )
        
        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return auth_url, state
    
    def exchange_code(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )
        
        flow.fetch_token(code=code)
        self.credentials = flow.credentials
        
        return {
            'access_token': self.credentials.token,
            'refresh_token': self.credentials.refresh_token,
            'token_expiry': self.credentials.expiry.isoformat() if self.credentials.expiry else None
        }
    
    def set_credentials(self, access_token: str, refresh_token: str, token_expiry: Optional[str] = None):
        """Set credentials from stored tokens"""
        from datetime import datetime
        
        token_uri = "https://oauth2.googleapis.com/token"
        
        self.credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
    
    def refresh_token(self) -> Dict[str, Any]:
        """Refresh access token"""
        if not self.credentials:
            raise ValueError("No credentials set")
        
        self.credentials.refresh(Request())
        
        return {
            'access_token': self.credentials.token,
            'token_expiry': self.credentials.expiry.isoformat() if self.credentials.expiry else None
        }
    
    def upload_file(self, file_path: str, folder_id: Optional[str] = None, 
                   mime_type: Optional[str] = None,
                   progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Upload a file to Google Drive"""
        if not self.credentials:
            raise ValueError("Not authenticated with Google Drive")
        
        # Refresh credentials if expired
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
        
        service = build('drive', 'v3', credentials=self.credentials)
        
        file_name = os.path.basename(file_path)
        file_metadata = {'name': file_name}
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Determine mime type if not provided
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        
        request = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink, size'
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status and progress_callback:
                progress_callback(int(status.progress() * 100))
        
        return {
            'file_id': response.get('id'),
            'name': response.get('name'),
            'web_view_link': response.get('webViewLink'),
            'size': response.get('size')
        }
    
    def create_folder(self, folder_name: str, parent_folder_id: Optional[str] = None) -> str:
        """Create a folder in Google Drive"""
        if not self.credentials:
            raise ValueError("Not authenticated with Google Drive")
        
        # Refresh credentials if expired
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
        
        service = build('drive', 'v3', credentials=self.credentials)
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        folder = service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        return folder.get('id')
    
    def list_files(self, folder_id: Optional[str] = None, page_size: int = 100) -> list:
        """List files in Google Drive"""
        if not self.credentials:
            raise ValueError("Not authenticated with Google Drive")
        
        # Refresh credentials if expired
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
        
        service = build('drive', 'v3', credentials=self.credentials)
        
        query = ""
        if folder_id:
            query = f"'{folder_id}' in parents"
        
        results = service.files().list(
            pageSize=page_size,
            q=query,
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)"
        ).execute()
        
        return results.get('files', [])
    
    def get_storage_quota(self) -> Dict[str, Any]:
        """Get storage quota information"""
        if not self.credentials:
            raise ValueError("Not authenticated with Google Drive")
        
        # Refresh credentials if expired
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
        
        service = build('drive', 'v3', credentials=self.credentials)
        
        about = service.about().get(fields="storageQuota, user").execute()
        
        quota = about.get('storageQuota', {})
        user = about.get('user', {})
        
        return {
            'user_email': user.get('emailAddress'),
            'total': int(quota.get('limit', 0)),
            'used': int(quota.get('usage', 0)),
            'available': int(quota.get('limit', 0)) - int(quota.get('usage', 0))
        }
    
    def is_authenticated(self) -> bool:
        """Check if service is authenticated"""
        return self.credentials is not None and (
            not self.credentials.expired or 
            (self.credentials.expired and self.credentials.refresh_token)
        )
