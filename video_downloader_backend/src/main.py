from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Import services
from services.video_service import VideoService
from services.queue_service import QueueService
from services.google_drive_service import GoogleDriveService

# Import routes
from routes.downloads import downloads_bp, init_services as init_download_services
from routes.playlists import playlists_bp, init_services as init_playlist_services
from routes.queue import queue_bp, init_services as init_queue_services
from routes.auth import auth_bp, init_services as init_auth_services

# Import models
from models import init_db

# Create Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 1073741824))

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize services
upload_folder = os.getenv('UPLOAD_FOLDER', './uploads')
os.makedirs(upload_folder, exist_ok=True)

video_service = VideoService(upload_folder=upload_folder)
queue_service = QueueService(max_concurrent=int(os.getenv('MAX_CONCURRENT_DOWNLOADS', 3)))

# Initialize Google Drive service if configured
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
google_redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')

drive_service = None
if google_client_id and google_client_secret:
    drive_service = GoogleDriveService(
        client_id=google_client_id,
        client_secret=google_client_secret,
        redirect_uri=google_redirect_uri
    )

# Initialize route services
init_download_services(video_service, queue_service, drive_service)
init_playlist_services(video_service, queue_service, drive_service)
init_queue_services(queue_service)
init_auth_services(drive_service)

# Register blueprints
app.register_blueprint(downloads_bp, url_prefix='/api/downloads')
app.register_blueprint(playlists_bp, url_prefix='/api/playlists')
app.register_blueprint(queue_bp, url_prefix='/api/queue')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Serve frontend
@app.route('/')
def serve_frontend():
    """Serve the frontend application"""
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    index_file = os.path.join(static_folder, 'index.html')
    
    if os.path.exists(index_file):
        return send_from_directory(static_folder, 'index.html')
    else:
        return """
        <html>
        <head><title>Universal Video Downloader</title></head>
        <body>
            <h1>Universal Video Downloader API</h1>
            <p>The backend API is running. Please build the frontend and copy it to the static folder.</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li>GET /api/downloads/formats - Get supported formats</li>
                <li>POST /api/downloads/extract-info - Extract video info</li>
                <li>POST /api/downloads/single - Download single video</li>
                <li>POST /api/downloads/bulk - Download multiple videos</li>
                <li>POST /api/playlists/info - Get playlist info</li>
                <li>POST /api/playlists/download - Download playlist</li>
                <li>GET /api/queue/status - Get queue status</li>
                <li>GET /api/queue/tasks - Get all tasks</li>
                <li>GET /api/queue/tasks/{id} - Get task details</li>
                <li>POST /api/queue/control - Control queue</li>
                <li>GET /api/auth/google-drive/status - Check Drive auth status</li>
                <li>GET /api/auth/google-drive/auth-url - Get Drive auth URL</li>
            </ul>
        </body>
        </html>
        """

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('get_queue_status')
def handle_get_queue_status():
    """Send queue status to client"""
    status = queue_service.get_queue_status()
    emit('queue_status', status)

# Background task to emit queue updates
def background_queue_updates():
    """Send periodic queue updates to all clients"""
    import time
    while True:
        time.sleep(2)  # Update every 2 seconds
        status = queue_service.get_queue_status()
        socketio.emit('queue_status_update', status)

# Initialize database
def initialize_database():
    """Initialize the database"""
    init_db()
    print("Database initialized successfully")

if __name__ == '__main__':
    # Parse command line arguments
    if '--init-db' in sys.argv:
        initialize_database()
    
    # Start queue service
    queue_service.start()
    
    # Start background task for queue updates
    import eventlet
    eventlet.spawn(background_queue_updates)
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Universal Video Downloader on port {port}")
    print(f"Upload folder: {upload_folder}")
    print(f"Google Drive configured: {drive_service is not None}")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
