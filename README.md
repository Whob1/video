# Universal Video Downloader Web App

A comprehensive, full-stack web application for downloading videos, playlists, and audio with seamless Google Drive cloud integration.

## 🚀 Features

- **Single Video Downloads**: Download individual videos with format and quality selection
- **Playlist Support**: Process entire playlists automatically
- **Bulk URL Processing**: Download multiple videos from different sources simultaneously
- **Google Drive Integration**: Automatic cloud upload with OAuth2 authentication
- **Real-time Progress Tracking**: Live updates for downloads and uploads
- **Queue Management**: Advanced queue system with pause/resume functionality
- **Modern UI**: Responsive React frontend with Tailwind CSS
- **Multiple Formats**: Support for MP4, MKV, WebM, MP3, FLAC, AAC, and more
- **Cloud-Only Mode**: Direct-to-cloud downloads without local storage

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** with Flask framework
- **yt-dlp** for video downloading
- **SQLAlchemy** for database operations
- **Flask-SocketIO** for real-time updates
- **Google API Client** for Drive integration

### Frontend
- **React 18** with modern hooks
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **WebSocket** for real-time communication

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16.0 or higher
- Git
- FFmpeg (automatically installed with yt-dlp)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/universal-video-downloader.git
cd universal-video-downloader
```

### 2. Backend Setup
```bash
cd video_downloader_backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 4. Frontend Setup
```bash
cd ../video-downloader-frontend
npm install
```

### 5. Start the Application
Backend (Terminal 1):
```bash
cd video_downloader_backend
source venv/bin/activate
python src/main.py
```

Frontend (Terminal 2):
```bash
cd video-downloader-frontend
npm run dev
```

### 6. Access the Application
- Frontend Development: http://localhost:5173
- Backend API: http://localhost:5000
- Integrated Application: http://localhost:5000 (after building frontend)

## 🔧 Production Deployment

### Build Frontend
```bash
cd video-downloader-frontend
npm run build
cp -r dist/* ../video_downloader_backend/src/static/
```

### Production Environment
```bash
# Set production environment variables
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://username:password@localhost/dbname

# Start with production server
cd video_downloader_backend
source venv/bin/activate
python src/main.py
```

## 📖 Google Drive Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Drive API
4. Create OAuth2 credentials
5. Add authorized redirect URIs:
   - `http://localhost:5000/auth/google/callback` (development)
   - `https://yourdomain.com/auth/google/callback` (production)
6. Update `.env` file with client credentials

## 🎯 Usage

### Single Video Download
1. Select "Single Video" tab
2. Paste video URL
3. Choose format and quality
4. Configure options (subtitles, thumbnails, Google Drive)
5. Click "Download Video"

### Playlist Download
1. Select "Playlist" tab
2. Paste playlist URL
3. Configure settings
4. Click "Download Playlist"

### Bulk Downloads
1. Select "Bulk URLs" tab
2. Enter multiple URLs (one per line)
3. Configure settings
4. Click "Download All"

## 📊 API Documentation

The application provides a comprehensive REST API. Key endpoints:

- `POST /api/downloads/single` - Single video download
- `POST /api/playlists/download` - Playlist download
- `GET /api/queue/status` - Queue status
- `GET /api/downloads/formats` - Supported formats

For complete API documentation, see the full documentation file.

## 🔒 Security Features

- OAuth2 authentication for Google Drive
- Secure token storage and management
- CORS protection
- Input validation and sanitization
- Rate limiting and queue management

## 🐛 Troubleshooting

### Common Issues

**Installation Problems**:
- Ensure Python 3.8+ is installed
- Install system development tools (`build-essential` on Ubuntu)
- Update pip: `pip install --upgrade pip`

**Download Failures**:
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Check network connectivity
- Verify platform support

**Google Drive Issues**:
- Verify OAuth2 credentials
- Check API quotas and limits
- Ensure proper redirect URI configuration

## 📁 Project Structure

```
universal-video-downloader/
├── video_downloader_backend/
│   ├── src/
│   │   ├── main.py              # Flask application entry point
│   │   ├── models/              # Database models
│   │   ├── routes/              # API route blueprints
│   │   ├── services/            # Business logic services
│   │   └── static/              # Static files (built frontend)
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
├── video-downloader-frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   └── components/          # UI components
│   ├── package.json             # Node.js dependencies
│   └── dist/                    # Built frontend files
└── README.md                    # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
- [React](https://reactjs.org/) for the frontend framework
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [shadcn/ui](https://ui.shadcn.com/) for UI components

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ by Manus AI**

