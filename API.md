# API Reference

Complete API reference for the Universal Video Downloader Web App.

## Base URL

```
http://localhost:5000/api  (Development)
https://yourdomain.com/api (Production)
```

## Authentication

Currently uses session-based authentication. Future versions will support API key authentication.

## Response Format

All responses are in JSON format:

```json
{
  "data": {},
  "error": null,
  "message": "Success"
}
```

## Error Handling

HTTP Status Codes:
- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

Error Response:
```json
{
  "error": "Error type",
  "message": "Detailed error description"
}
```

## Endpoints

### Downloads

#### Get Supported Formats

```http
GET /api/downloads/formats
```

Response:
```json
{
  "video_formats": [
    {
      "id": "mp4",
      "name": "MP4 (Video)",
      "description": "Most compatible video format",
      "extension": "mp4"
    }
  ],
  "audio_formats": [
    {
      "id": "mp3",
      "name": "MP3 (Audio)",
      "description": "Standard audio format",
      "extension": "mp3"
    }
  ]
}
```

#### Extract Video Information

```http
POST /api/downloads/extract-info
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

Response:
```json
{
  "title": "Video Title",
  "duration": 212,
  "uploader": "Channel Name",
  "upload_date": "2009-10-25",
  "view_count": 1000000,
  "description": "Video description",
  "thumbnail": "https://thumbnail-url.jpg",
  "available_formats": [
    {
      "format_id": "22",
      "ext": "mp4",
      "quality": "720p",
      "filesize": 45678901
    }
  ],
  "available_subtitles": ["en", "es", "fr"]
}
```

#### Download Single Video

```http
POST /api/downloads/single
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "mp4",
  "quality": "720p",
  "include_subtitles": true,
  "include_thumbnail": false,
  "upload_to_drive": true,
  "cloud_only": false
}
```

Parameters:
- `url` (string, required) - Video URL
- `format` (string, optional) - Output format (default: "mp4")
- `quality` (string, optional) - Video quality (default: "720p")
- `include_subtitles` (boolean, optional) - Download subtitles (default: false)
- `include_thumbnail` (boolean, optional) - Download thumbnail (default: false)
- `upload_to_drive` (boolean, optional) - Upload to Google Drive (default: false)
- `cloud_only` (boolean, optional) - Only store in cloud (default: false)

Response:
```json
{
  "task_id": "uuid-string",
  "status": "queued",
  "message": "Download task created successfully"
}
```

#### Download Bulk URLs

```http
POST /api/downloads/bulk
Content-Type: application/json

{
  "urls": [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2"
  ],
  "format": "mp4",
  "quality": "720p",
  "include_subtitles": false,
  "include_thumbnail": true,
  "upload_to_drive": true,
  "cloud_only": false
}
```

Response:
```json
{
  "total_urls": 2,
  "valid_urls": 2,
  "task_ids": ["uuid-1", "uuid-2"],
  "status": "processing"
}
```

### Playlists

#### Get Playlist Information

```http
POST /api/playlists/info
Content-Type: application/json

{
  "playlist_url": "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
}
```

Response:
```json
{
  "title": "Playlist Title",
  "description": "Playlist description",
  "uploader": "Channel Name",
  "video_count": 25,
  "videos": [
    {
      "url": "https://www.youtube.com/watch?v=video1",
      "title": "Video 1 Title",
      "duration": 180
    }
  ]
}
```

#### Download Playlist

```http
POST /api/playlists/download
Content-Type: application/json

{
  "playlist_url": "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf",
  "format": "mp4",
  "quality": "720p",
  "include_subtitles": true,
  "include_thumbnail": true,
  "upload_to_drive": true,
  "cloud_only": false,
  "max_videos": 50
}
```

Response:
```json
{
  "playlist_title": "Playlist Title",
  "total_videos": 25,
  "task_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "status": "processing",
  "message": "Playlist processing initiated"
}
```

### Queue Management

#### Get Queue Status

```http
GET /api/queue/status
```

Response:
```json
{
  "total_tasks": 10,
  "pending": 3,
  "running": 2,
  "completed": 4,
  "failed": 1,
  "cancelled": 0,
  "max_concurrent": 3,
  "queue_paused": false
}
```

#### Get All Tasks

```http
GET /api/queue/tasks?status=running&limit=20&offset=0
```

Query Parameters:
- `status` (string, optional) - Filter by status
- `limit` (integer, optional) - Results per page (default: 50, max: 100)
- `offset` (integer, optional) - Pagination offset (default: 0)

Response:
```json
{
  "tasks": [
    {
      "task_id": "uuid-string",
      "url": "https://www.youtube.com/watch?v=example",
      "title": "Video Title",
      "status": "running",
      "progress": 45.5,
      "download_speed": "2.5 MB/s",
      "eta": "00:02:30",
      "created_at": "2025-09-12T23:10:00Z",
      "format": "mp4",
      "quality": "720p"
    }
  ],
  "total_count": 10,
  "has_more": false
}
```

#### Get Task Details

```http
GET /api/queue/tasks/{task_id}
```

Response:
```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "progress": 100.0,
  "file_path": "/downloads/video-title.mp4",
  "file_size": 45678901,
  "created_at": "2025-09-12T23:10:00Z",
  "completed_at": "2025-09-12T23:12:05Z",
  "google_drive_url": "https://drive.google.com/file/d/file-id/view"
}
```

#### Control Queue

```http
POST /api/queue/control
Content-Type: application/json

{
  "action": "pause"
}
```

Actions:
- `pause` - Pause queue processing
- `resume` - Resume queue processing
- `clear_completed` - Clear completed tasks
- `clear_failed` - Clear failed tasks

Response:
```json
{
  "status": "success",
  "message": "Queue paused successfully",
  "queue_status": {
    "queue_paused": true,
    "running_tasks": 0
  }
}
```

#### Control Task

```http
POST /api/queue/tasks/{task_id}/control
Content-Type: application/json

{
  "action": "cancel"
}
```

Actions:
- `cancel` - Cancel task

Response:
```json
{
  "status": "success",
  "message": "Task cancelled successfully"
}
```

### Google Drive Authentication

#### Get Drive Status

```http
GET /api/auth/google-drive/status
```

Response:
```json
{
  "authenticated": true,
  "user_email": "user@example.com",
  "storage_quota": {
    "total": 15000000000,
    "used": 5000000000,
    "available": 10000000000
  }
}
```

#### Get Authentication URL

```http
GET /api/auth/google-drive/auth-url
```

Response:
```json
{
  "auth_url": "https://accounts.google.com/oauth2/auth?client_id=...",
  "state": "random-state-string"
}
```

#### Set Credentials

```http
POST /api/auth/google-drive/set-credentials
Content-Type: application/json

{
  "access_token": "ya29.a0AfH6SMBx...",
  "refresh_token": "1//0gHdPuQh..."
}
```

Response:
```json
{
  "status": "success",
  "message": "Credentials set successfully"
}
```

## WebSocket Events

Connect to: `ws://localhost:5000/socket.io`

### Client Events

#### Connect
```javascript
socket.on('connect', () => {
  console.log('Connected to server');
});
```

#### Get Queue Status
```javascript
socket.emit('get_queue_status');
```

### Server Events

#### Connection Confirmed
```javascript
socket.on('connected', (data) => {
  console.log(data.message);
});
```

#### Queue Status Update
```javascript
socket.on('queue_status_update', (status) => {
  console.log('Queue status:', status);
  // status: { total_tasks, pending, running, completed, failed, cancelled }
});
```

#### Download Progress
```javascript
socket.on('download_progress', (data) => {
  console.log('Progress:', data);
  // data: { task_id, progress, download_speed, eta, status }
});
```

## Rate Limiting

Currently no rate limiting is implemented. For production, implement rate limiting using Flask-Limiter or similar.

## Examples

### Python Example

```python
import requests

API_BASE = "http://localhost:5000/api"

# Get supported formats
response = requests.get(f"{API_BASE}/downloads/formats")
formats = response.json()

# Download single video
download_data = {
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "mp4",
    "quality": "720p"
}
response = requests.post(f"{API_BASE}/downloads/single", json=download_data)
task = response.json()
print(f"Task ID: {task['task_id']}")

# Check task status
task_id = task['task_id']
response = requests.get(f"{API_BASE}/queue/tasks/{task_id}")
status = response.json()
print(f"Status: {status['status']}, Progress: {status['progress']}%")
```

### JavaScript Example

```javascript
const API_BASE = 'http://localhost:5000/api';

// Get supported formats
fetch(`${API_BASE}/downloads/formats`)
  .then(res => res.json())
  .then(formats => console.log(formats));

// Download single video
const downloadData = {
  url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
  format: 'mp4',
  quality: '720p'
};

fetch(`${API_BASE}/downloads/single`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(downloadData)
})
  .then(res => res.json())
  .then(task => {
    console.log('Task ID:', task.task_id);
    
    // Check task status
    return fetch(`${API_BASE}/queue/tasks/${task.task_id}`);
  })
  .then(res => res.json())
  .then(status => console.log('Status:', status));
```

### WebSocket Example

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected');
  socket.emit('get_queue_status');
});

socket.on('queue_status_update', (status) => {
  console.log('Queue:', status);
});

socket.on('download_progress', (data) => {
  console.log(`Progress: ${data.progress}%`);
});
```

## Support

For API issues and questions:
- GitHub Issues: https://github.com/your-username/video/issues
- Documentation: `/Universal_Video_Downloader_Documentation.md`
