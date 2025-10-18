from flask import Blueprint, request, jsonify, redirect
from services.google_drive_service import GoogleDriveService
import os

auth_bp = Blueprint('auth', __name__)

# Global service instance (will be initialized in main.py)
drive_service = None

def init_services(drive_svc):
    """Initialize service instances"""
    global drive_service
    drive_service = drive_svc

@auth_bp.route('/google-drive/status', methods=['GET'])
def get_drive_status():
    """Get Google Drive authentication status"""
    if not drive_service:
        return jsonify({
            'authenticated': False,
            'message': 'Google Drive not configured'
        }), 200
    
    try:
        if drive_service.is_authenticated():
            quota = drive_service.get_storage_quota()
            return jsonify({
                'authenticated': True,
                'user_email': quota.get('user_email'),
                'storage_quota': {
                    'total': quota.get('total'),
                    'used': quota.get('used'),
                    'available': quota.get('available')
                }
            }), 200
        else:
            return jsonify({'authenticated': False}), 200
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'error': str(e)
        }), 200

@auth_bp.route('/google-drive/auth-url', methods=['GET'])
def get_auth_url():
    """Get Google OAuth2 authentication URL"""
    if not drive_service:
        return jsonify({'error': 'Google Drive not configured'}), 500
    
    try:
        auth_url, state = drive_service.get_auth_url()
        return jsonify({
            'auth_url': auth_url,
            'state': state
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/google-drive/callback', methods=['GET'])
def google_drive_callback():
    """Handle Google OAuth2 callback"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return f"<html><body><h1>Authentication failed</h1><p>{error}</p></body></html>", 400
    
    if not code:
        return "<html><body><h1>Authentication failed</h1><p>No authorization code received</p></body></html>", 400
    
    try:
        tokens = drive_service.exchange_code(code)
        # In a real application, store these tokens securely in a database
        return "<html><body><h1>Authentication successful!</h1><p>You can close this window and return to the application.</p></body></html>", 200
    except Exception as e:
        return f"<html><body><h1>Authentication failed</h1><p>{str(e)}</p></body></html>", 500

@auth_bp.route('/google-drive/set-credentials', methods=['POST'])
def set_credentials():
    """Set Google Drive credentials from stored tokens"""
    data = request.get_json()
    
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    
    if not access_token or not refresh_token:
        return jsonify({'error': 'Access token and refresh token are required'}), 400
    
    try:
        drive_service.set_credentials(access_token, refresh_token)
        return jsonify({
            'status': 'success',
            'message': 'Credentials set successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
