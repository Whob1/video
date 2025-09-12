# Universal Video Downloader Web App
## Complete Documentation and User Guide

**Author:** Manus AI  
**Version:** 1.0.0  
**Date:** September 12, 2025  

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features Overview](#features-overview)
3. [System Architecture](#system-architecture)
4. [Installation and Setup](#installation-and-setup)
5. [User Guide](#user-guide)
6. [API Documentation](#api-documentation)
7. [Google Drive Integration](#google-drive-integration)
8. [Queue System and Progress Tracking](#queue-system-and-progress-tracking)
9. [Deployment Guide](#deployment-guide)
10. [Troubleshooting](#troubleshooting)
11. [Technical Specifications](#technical-specifications)
12. [Security Considerations](#security-considerations)
13. [Performance Optimization](#performance-optimization)
14. [Future Enhancements](#future-enhancements)
15. [Contributing](#contributing)
16. [License](#license)

---

## Introduction

The Universal Video Downloader Web App is a comprehensive, full-stack application designed to provide users with a powerful and intuitive platform for downloading videos, audio, and playlists from various online sources. Built with modern web technologies and featuring seamless cloud integration, this application represents a complete solution for content downloading and management.

This documentation serves as a complete guide for users, developers, and system administrators who wish to understand, deploy, or contribute to the Universal Video Downloader project. The application combines a robust Python Flask backend with a modern React frontend, offering both powerful functionality and an exceptional user experience.

The project was conceived to address the growing need for a reliable, feature-rich video downloading solution that could handle not just individual videos, but also complex scenarios such as playlist downloads, bulk URL processing, and automatic cloud storage integration. Unlike simple command-line tools or basic web interfaces, this application provides a professional-grade solution with real-time progress tracking, queue management, and enterprise-level features such as OAuth2 authentication and resumable uploads.




## Features Overview

The Universal Video Downloader Web App offers an extensive suite of features designed to meet the diverse needs of content creators, researchers, educators, and general users who require reliable video and audio downloading capabilities.

### Core Download Features

**Single Video Downloads**: The application supports downloading individual videos from a wide range of platforms including YouTube, Vimeo, and other popular video hosting services. Users can specify exact quality preferences, format requirements, and additional content such as subtitles and thumbnails. The system intelligently handles format conversion and quality optimization to ensure the best possible output for each user's specific needs.

**Playlist Processing**: One of the most powerful features of the application is its ability to process entire playlists with a single request. Users can input a playlist URL, and the system will automatically discover all videos within that playlist, queue them for download, and process them according to the user's specified preferences. This feature includes intelligent handling of private videos, unavailable content, and playlist updates, ensuring that users receive all accessible content without manual intervention.

**Bulk URL Management**: For users who need to download multiple videos from different sources, the bulk URL feature provides an efficient solution. Users can input multiple URLs (one per line) in a dedicated text area, and the system will process all URLs simultaneously, managing the download queue and providing individual progress tracking for each item. This feature is particularly valuable for content curators, researchers, and educators who need to download large collections of videos for offline use.

### Format and Quality Options

The application provides comprehensive format and quality selection capabilities, supporting both video and audio downloads across multiple formats:

**Video Formats**: MP4 (H.264/H.265), MKV (Matroska), WebM (VP8/VP9), AVI, MOV (QuickTime), FLV (Flash Video), and WMV (Windows Media Video). Each format is optimized for different use cases, with MP4 providing the best compatibility across devices and platforms, while MKV offers superior quality retention for archival purposes.

**Audio Formats**: MP3 (MPEG-1 Audio Layer III), FLAC (Free Lossless Audio Codec), AAC (Advanced Audio Coding), OGG Vorbis, WAV (Waveform Audio File Format), M4A (MPEG-4 Audio), and WMA (Windows Media Audio). The system automatically handles audio extraction from video sources and provides options for bitrate selection to balance file size and audio quality.

**Quality Selection**: Users can choose from multiple quality options including 1080p (Full HD), 720p (HD), 480p (Standard Definition), 360p (Low Definition), and "Best Available" which automatically selects the highest quality available for each source. The system also supports adaptive quality selection, where it can automatically downgrade quality if the preferred option is not available.

### Cloud Integration Features

**Google Drive Integration**: The application features comprehensive Google Drive integration through OAuth2 authentication, allowing users to automatically upload downloaded content directly to their Google Drive accounts. This integration includes support for folder organization, automatic folder creation, and resumable uploads for large files. Users can choose to store files locally, upload to cloud only, or maintain both local and cloud copies.

**Folder Management**: The Google Drive integration includes intelligent folder management capabilities. Users can specify custom folder structures, and the system will automatically create folders based on content type (videos, audio, playlists), source platform, or custom naming conventions. This ensures that downloaded content is organized and easily accessible within the user's Google Drive account.

**Cloud-Only Downloads**: For users with limited local storage, the application offers a cloud-only download mode where content is downloaded temporarily to the server, uploaded to Google Drive, and then removed from local storage. This feature is particularly valuable for users working with large video files or those who prefer to maintain all their content in cloud storage.

### Queue Management and Progress Tracking

**Real-Time Queue Management**: The application features a sophisticated queue management system that handles multiple concurrent downloads while respecting platform rate limits and server resources. Users can view the current queue status, including pending, running, completed, failed, and cancelled tasks. The queue system supports prioritization, allowing users to move important downloads to the front of the queue.

**Live Progress Updates**: Through WebSocket connections, the application provides real-time progress updates for all download and upload operations. Users can monitor download speed, estimated time remaining, current file size, and completion percentage. The progress tracking system also provides detailed information about each stage of the download process, including metadata extraction, format conversion, and cloud upload progress.

**Pause and Resume Functionality**: Downloads can be paused and resumed at any time, allowing users to manage bandwidth usage and prioritize urgent downloads. The pause/resume functionality works at both the individual file level and the queue level, providing maximum flexibility for users with varying connectivity or time constraints.

### User Interface and Experience

**Modern React Frontend**: The application features a modern, responsive React frontend built with Tailwind CSS and shadcn/ui components. The interface is designed to be intuitive and accessible, with clear visual indicators for all system states and operations. The design follows modern web standards and provides an excellent user experience across desktop and mobile devices.

**Responsive Design**: The interface automatically adapts to different screen sizes and devices, ensuring that users can effectively manage their downloads whether they're using a desktop computer, tablet, or smartphone. The responsive design maintains full functionality across all device types while optimizing the layout for each screen size.

**Real-Time Notifications**: Users receive real-time notifications about download completion, errors, and system status changes. These notifications are delivered through both the web interface and can be configured for email delivery, ensuring that users stay informed about their download progress even when not actively monitoring the application.


## System Architecture

The Universal Video Downloader Web App is built on a modern, scalable architecture that separates concerns between the frontend user interface, backend API services, and external integrations. This architectural approach ensures maintainability, scalability, and the ability to extend functionality as requirements evolve.

### Overall Architecture Pattern

The application follows a **microservices-inspired architecture** with clear separation between the presentation layer, business logic layer, and data persistence layer. While deployed as a monolithic application for simplicity, the codebase is structured to support future migration to a distributed microservices architecture if scaling requirements demand it.

**Frontend Layer**: The presentation layer is implemented as a Single Page Application (SPA) using React 18 with modern hooks and functional components. The frontend communicates with the backend exclusively through RESTful API endpoints and WebSocket connections for real-time updates. This separation ensures that the frontend can be deployed independently and even replaced with alternative implementations (mobile apps, desktop applications) without affecting the backend services.

**Backend Layer**: The backend is implemented using Flask, a lightweight Python web framework that provides excellent flexibility for API development. The backend is organized into distinct service modules, each responsible for specific functionality such as video downloading, queue management, Google Drive integration, and user management. This modular approach ensures that individual services can be modified, tested, and deployed independently.

**Data Layer**: The application uses SQLite for development and testing, with the database schema designed to support migration to PostgreSQL or other enterprise databases for production deployments. The data layer includes models for users, downloads, playlists, queue tasks, and user settings, with proper relationships and constraints to maintain data integrity.

### Backend Architecture Details

**Service Layer Architecture**: The backend is organized into several key service modules, each encapsulating specific business logic and external integrations:

The **Video Service** (`video_service.py`) serves as the core component responsible for all video downloading operations. This service wraps the yt-dlp library, providing a clean interface for video metadata extraction, format selection, and download execution. The service handles error recovery, retry logic, and progress reporting, ensuring reliable downloads even when dealing with unstable network connections or platform-specific issues.

The **Google Drive Service** (`google_drive_service.py`) manages all aspects of Google Drive integration, including OAuth2 authentication flow, token management, file uploads, and folder operations. This service implements resumable uploads for large files, automatic retry logic for failed uploads, and comprehensive error handling for various Google API scenarios. The service also includes token encryption and secure storage to protect user credentials.

The **Queue Service** (`queue_service.py`) implements a sophisticated task queue system that manages download and upload operations. Unlike simple FIFO queues, this service supports task prioritization, concurrent execution limits, pause/resume functionality, and comprehensive progress tracking. The queue service is designed to be thread-safe and can handle multiple concurrent operations while maintaining system stability and resource management.

**API Layer Design**: The REST API is organized into logical blueprints, each handling a specific domain of functionality:

- **Download Blueprint** (`/api/downloads`): Handles single video downloads, metadata extraction, and download status queries
- **Playlist Blueprint** (`/api/playlists`): Manages playlist processing, video discovery, and bulk download operations  
- **Queue Blueprint** (`/api/queue`): Provides queue management, task status monitoring, and queue statistics
- **Settings Blueprint** (`/api/settings`): Manages user preferences, Google Drive configuration, and application settings
- **WebSocket Routes**: Real-time communication for progress updates, notifications, and live status monitoring

**Database Schema Design**: The database schema is designed with normalization principles while maintaining query performance:

```sql
Users Table: Stores user authentication and profile information
Downloads Table: Records all download operations with metadata and status
Playlists Table: Manages playlist information and video relationships  
UserSettings Table: Stores user preferences and configuration options
QueueTasks Table: Tracks queue operations and execution history
```

The schema includes proper foreign key relationships, indexes for performance optimization, and constraints to ensure data integrity. The design supports both individual user installations and multi-user deployments with proper data isolation.

### Frontend Architecture Details

**Component Architecture**: The React frontend follows a component-based architecture with clear separation of concerns:

**Container Components**: High-level components that manage state and business logic, such as the main App component, DownloadManager, and QueueMonitor. These components handle API communication, state management, and coordination between child components.

**Presentation Components**: Pure components focused on rendering UI elements and handling user interactions. These include form components, progress indicators, status displays, and navigation elements. Presentation components receive data through props and communicate user actions through callback functions.

**Custom Hooks**: Reusable logic is extracted into custom hooks for API communication, WebSocket management, and state synchronization. This approach promotes code reuse and makes testing easier by isolating business logic from presentation concerns.

**State Management**: The application uses React's built-in state management with useState and useEffect hooks, supplemented by custom hooks for complex state operations. For global state that needs to be shared across multiple components, the application uses React Context API, avoiding the complexity of external state management libraries while maintaining clean data flow.

**Real-Time Communication**: WebSocket connections are managed through a custom hook that handles connection establishment, message routing, and automatic reconnection. The WebSocket system provides real-time updates for download progress, queue status changes, and system notifications, ensuring that users always have current information about their operations.

### External Integrations

**yt-dlp Integration**: The application integrates with yt-dlp, a powerful Python library for video downloading from various platforms. The integration is designed to be robust and flexible, handling the complexities of different video platforms while providing a consistent interface to the rest of the application. The integration includes custom progress callbacks, error handling, and format selection logic.

**Google Drive API Integration**: The Google Drive integration uses the official Google API client libraries with OAuth2 authentication. The integration supports the full range of Google Drive operations including file uploads, folder management, sharing permissions, and metadata management. The implementation includes proper error handling for quota limits, network issues, and authentication problems.

**WebSocket Communication**: Real-time communication is implemented using Flask-SocketIO, which provides WebSocket support with fallback to long polling for older browsers. The WebSocket system is designed to handle multiple concurrent connections and provides efficient message broadcasting for progress updates and notifications.

This architectural approach ensures that the Universal Video Downloader Web App is maintainable, scalable, and extensible while providing excellent performance and user experience. The clear separation of concerns makes it easy to modify individual components without affecting the overall system, and the modular design supports future enhancements and integrations.


## Installation and Setup

This section provides comprehensive instructions for installing and configuring the Universal Video Downloader Web App in various environments, from development setups to production deployments.

### Prerequisites

Before installing the Universal Video Downloader Web App, ensure that your system meets the following requirements:

**System Requirements**:
- Operating System: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10+
- RAM: Minimum 2GB, Recommended 4GB or more for handling multiple concurrent downloads
- Storage: Minimum 10GB free space for application files and temporary download storage
- Network: Stable internet connection with sufficient bandwidth for video downloads

**Software Dependencies**:
- Python 3.8 or higher with pip package manager
- Node.js 16.0 or higher with npm package manager  
- Git for version control and repository cloning
- FFmpeg for video/audio processing (automatically installed with yt-dlp)

**Optional Dependencies**:
- Redis server for enhanced queue management (recommended for production)
- PostgreSQL for production database (SQLite used by default)
- Nginx for reverse proxy and static file serving (production deployments)

### Development Environment Setup

**Step 1: Repository Cloning and Initial Setup**

Begin by cloning the repository and setting up the basic directory structure:

```bash
git clone https://github.com/your-username/universal-video-downloader.git
cd universal-video-downloader
```

**Step 2: Backend Environment Configuration**

Navigate to the backend directory and create a Python virtual environment to isolate dependencies:

```bash
cd video_downloader_backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required Python dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

The requirements.txt file includes all necessary dependencies:
- Flask and Flask-CORS for web framework and cross-origin support
- Flask-SocketIO for real-time WebSocket communication
- yt-dlp for video downloading capabilities
- google-auth and google-api-python-client for Google Drive integration
- SQLAlchemy for database operations
- python-dotenv for environment variable management

**Step 3: Environment Variables Configuration**

Create a `.env` file in the backend root directory with the following configuration:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Configuration  
DATABASE_URL=sqlite:///app.db

# Google Drive API Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback

# Queue Configuration
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=3600

# File Storage Configuration
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=1073741824  # 1GB
```

**Step 4: Database Initialization**

Initialize the database schema by running the database migration commands:

```bash
python src/main.py --init-db
```

This command creates the necessary database tables and indexes required for the application to function properly.

**Step 5: Frontend Environment Setup**

Open a new terminal window and navigate to the frontend directory:

```bash
cd ../video-downloader-frontend
npm install
```

This command installs all required Node.js dependencies including React, Vite, Tailwind CSS, and the shadcn/ui component library.

**Step 6: Development Server Startup**

Start the backend development server:

```bash
cd ../video_downloader_backend
source venv/bin/activate
python src/main.py
```

In a separate terminal, start the frontend development server:

```bash
cd video-downloader-frontend  
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Integrated Application: http://localhost:5000 (after building frontend)

### Google Drive API Setup

To enable Google Drive integration, you must configure Google Cloud Console and obtain API credentials:

**Step 1: Google Cloud Project Creation**

1. Visit the Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select an existing project
3. Enable the Google Drive API for your project
4. Navigate to "APIs & Services" > "Credentials"

**Step 2: OAuth2 Credentials Configuration**

1. Click "Create Credentials" > "OAuth 2.0 Client IDs"
2. Configure the OAuth consent screen with your application information
3. Set the application type to "Web application"
4. Add authorized redirect URIs:
   - http://localhost:5000/auth/google/callback (development)
   - https://yourdomain.com/auth/google/callback (production)

**Step 3: Credential Integration**

1. Download the client configuration JSON file
2. Extract the client_id and client_secret values
3. Update your .env file with these credentials
4. Restart the backend server to apply the new configuration

### Production Deployment Setup

**Step 1: Production Environment Preparation**

For production deployments, additional configuration is required to ensure security, performance, and reliability:

```bash
# Production Environment Variables
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=generate-strong-random-secret-key
DATABASE_URL=postgresql://username:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

**Step 2: Frontend Build Process**

Create a production build of the frontend application:

```bash
cd video-downloader-frontend
npm run build
```

Copy the built files to the backend static directory:

```bash
cp -r dist/* ../video_downloader_backend/src/static/
```

**Step 3: Database Migration for Production**

For production deployments using PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Run database migrations
python src/main.py --init-db --production
```

**Step 4: Process Management**

Use a process manager like systemd or supervisor to manage the application process:

```ini
# /etc/systemd/system/video-downloader.service
[Unit]
Description=Universal Video Downloader Web App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/video_downloader_backend
Environment=PATH=/path/to/video_downloader_backend/venv/bin
ExecStart=/path/to/video_downloader_backend/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Step 5: Reverse Proxy Configuration**

Configure Nginx as a reverse proxy for improved performance and security:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Verification and Testing

After completing the installation, verify that all components are functioning correctly:

**Backend API Testing**:
```bash
curl -X GET http://localhost:5000/api/queue/status
curl -X GET http://localhost:5000/api/downloads/formats
```

**Frontend Functionality Testing**:
1. Open the application in a web browser
2. Test single video URL input and format selection
3. Verify that the queue status updates correctly
4. Test Google Drive authentication flow (if configured)

**Integration Testing**:
1. Submit a test video URL for download
2. Monitor the queue status and progress updates
3. Verify that downloaded files appear in the specified location
4. Test Google Drive upload functionality (if configured)

This comprehensive setup process ensures that the Universal Video Downloader Web App is properly configured and ready for use in both development and production environments.


## User Guide

This comprehensive user guide provides step-by-step instructions for using all features of the Universal Video Downloader Web App, from basic single video downloads to advanced bulk processing and cloud integration.

### Getting Started

**Accessing the Application**

Once the application is installed and running, access it through your web browser at the configured URL (typically http://localhost:5000 for local installations). The application will load with a clean, modern interface displaying the main dashboard with queue status, download center, Google Drive integration panel, and quick statistics.

**Understanding the Interface**

The main interface is organized into several key sections:

**Queue Status Panel**: Located at the top of the interface, this panel provides real-time information about your download queue. It displays the total number of tasks, along with counts for pending, running, completed, failed, and cancelled downloads. This panel updates automatically as downloads progress, providing immediate feedback about system activity.

**Download Center**: The central area of the interface contains the download center with three tabs for different types of download operations: Single Video, Playlist, and Bulk URLs. Each tab provides specialized controls and options appropriate for that type of download operation.

**Google Drive Integration Panel**: On the right side of the interface, this panel shows the current Google Drive connection status and provides access to cloud storage features. When connected, it displays confirmation that Google Drive is available for automatic uploads.

**Quick Stats Panel**: Below the Google Drive panel, this section provides summary statistics about your download history, including total downloads, successful completions, and any failed attempts.

**Recent Downloads Section**: At the bottom of the interface, this area displays a list of recently completed downloads with details about each file, including download time, file size, and status.

### Single Video Downloads

**Basic Video Download Process**

To download a single video, begin by selecting the "Single Video" tab in the Download Center. This tab provides a streamlined interface optimized for individual video downloads.

**URL Input**: In the "Video URL" field, paste the complete URL of the video you wish to download. The application supports URLs from major platforms including YouTube, Vimeo, Dailymotion, and many others. Ensure that the URL is complete and properly formatted, including the protocol (https://) and any necessary parameters.

**Format Selection**: Click on the "Format" dropdown to choose your preferred output format. The available options include:
- **MP4 (Video)**: The most compatible video format, suitable for playback on virtually all devices and platforms
- **MKV (Video)**: High-quality video format that supports multiple audio tracks and subtitles
- **WebM (Video)**: Web-optimized format with excellent compression and quality
- **MP3 (Audio)**: Standard audio format for music and audio-only content
- **FLAC (Audio)**: Lossless audio format for highest quality audio preservation
- **AAC (Audio)**: High-quality audio format with efficient compression

**Quality Selection**: Use the "Quality" dropdown to specify your preferred video quality. Options typically include:
- **1080p (Full HD)**: Highest quality for modern displays and archival purposes
- **720p (HD)**: Good balance between quality and file size
- **480p (Standard)**: Smaller file size, suitable for mobile devices or limited storage
- **360p (Low)**: Minimal file size for preview purposes or very limited bandwidth
- **Best Available**: Automatically selects the highest quality available for the source

**Additional Options**: The interface provides several toggle switches for additional features:

**Include Subtitles**: When enabled, the application will download available subtitle files along with the video. Subtitles are saved in standard formats (SRT, VTT) and can be used with most video players. This option is particularly valuable for educational content, foreign language videos, or accessibility purposes.

**Include Thumbnail**: This option downloads the video thumbnail image, which can be useful for organizing your video library or creating custom video catalogs. Thumbnails are saved in high resolution when available.

**Upload to Google Drive**: When this option is enabled and Google Drive is connected, downloaded files will be automatically uploaded to your Google Drive account. The upload process begins immediately after the download completes, and you'll receive progress updates for both operations.

**Cloud Only**: This advanced option downloads files directly to Google Drive without storing them locally. This is ideal for users with limited local storage or those who prefer to keep all content in cloud storage. When this option is enabled, files are temporarily downloaded to the server, uploaded to Google Drive, and then removed from local storage.

**Initiating the Download**: After configuring all options, click the "Download Video" button to begin the download process. The system will immediately add the task to the queue and begin processing. You'll see real-time updates in the Queue Status panel as the download progresses.

### Playlist Downloads

**Understanding Playlist Processing**

The playlist download feature is designed to handle collections of videos efficiently, whether they're YouTube playlists, Vimeo showcases, or other platform-specific collections. This feature automatically discovers all videos within a playlist and processes them according to your specified preferences.

**Playlist URL Input**: Switch to the "Playlist" tab and enter the complete playlist URL in the "Playlist URL" field. Playlist URLs typically contain specific identifiers that distinguish them from individual video URLs. For example, YouTube playlist URLs contain a "list=" parameter with the playlist identifier.

**Playlist Processing Options**: All the same format, quality, and additional options available for single videos apply to playlist downloads. However, these settings will be applied to every video in the playlist, ensuring consistency across all downloaded content.

**Intelligent Playlist Handling**: The application includes sophisticated logic for handling various playlist scenarios:

**Private and Unavailable Videos**: When processing playlists, the system automatically skips videos that are private, deleted, or otherwise unavailable. These skipped videos are logged and reported in the final download summary, but they don't prevent the processing of available videos.

**Large Playlist Management**: For playlists containing hundreds of videos, the system implements intelligent batching and queue management to prevent system overload while maintaining reasonable download speeds. Users can monitor progress through the queue status panel and pause processing if needed.

**Playlist Metadata Preservation**: The system preserves playlist metadata including playlist title, description, and video order. This information can be used for organizing downloaded content and maintaining the original playlist structure.

### Bulk URL Downloads

**Bulk Processing Capabilities**

The bulk URL feature is designed for users who need to download multiple videos from various sources simultaneously. This feature is particularly valuable for content curators, researchers, and educators who work with large collections of videos from different platforms.

**URL Input Format**: Switch to the "Bulk URLs" tab to access the bulk download interface. In the large text area labeled "URLs (one per line)", enter each video URL on a separate line. The system can handle mixed URLs from different platforms, automatically detecting the appropriate download method for each source.

**Batch Processing Logic**: The application processes bulk URLs intelligently, managing concurrent downloads to optimize performance while respecting platform rate limits and server resources. The system automatically handles different platforms' requirements and adjusts processing speed accordingly.

**Error Handling and Reporting**: During bulk processing, the system provides detailed reporting about each URL's processing status. Failed downloads are clearly identified with specific error messages, allowing users to understand and potentially resolve issues with individual URLs.

**Progress Monitoring**: Bulk downloads provide comprehensive progress monitoring with individual progress tracking for each URL. Users can see which videos are currently downloading, which are queued for processing, and which have completed successfully.

### Advanced Features and Settings

**Queue Management**

The queue system provides advanced controls for managing download operations:

**Priority Management**: While not exposed in the basic interface, the queue system supports priority-based processing. Important downloads can be moved to the front of the queue through API calls or future interface enhancements.

**Pause and Resume**: Individual downloads or the entire queue can be paused and resumed as needed. This feature is valuable for managing bandwidth usage during peak hours or when other network-intensive activities are required.

**Concurrent Download Limits**: The system automatically manages the number of concurrent downloads to optimize performance and prevent system overload. This limit can be adjusted through configuration settings based on available system resources.

**Google Drive Integration**

**Authentication Process**: To enable Google Drive integration, click the "Connect Google Drive" button (when available) or follow the authentication flow provided in the Google Drive panel. This process uses OAuth2 authentication to securely connect your Google account without storing your password.

**Folder Organization**: Downloaded files can be organized into custom folder structures within Google Drive. The system supports automatic folder creation based on content type, source platform, or custom naming conventions specified in the settings.

**Upload Progress Monitoring**: When Google Drive uploads are enabled, the interface provides separate progress tracking for upload operations. Users can monitor both download and upload progress simultaneously, ensuring complete visibility into the entire process.

**Sharing and Access Control**: Files uploaded to Google Drive maintain the default sharing settings of your Google Drive account. Users can modify sharing permissions through the Google Drive interface after uploads complete.

This comprehensive user guide ensures that users can effectively utilize all features of the Universal Video Downloader Web App, from basic downloads to advanced bulk processing and cloud integration scenarios.


## API Documentation

The Universal Video Downloader Web App provides a comprehensive RESTful API that enables programmatic access to all application features. This API is designed for developers who want to integrate video downloading capabilities into their own applications or create custom interfaces for the download system.

### API Overview and Authentication

**Base URL and Versioning**

All API endpoints are accessible under the base URL `/api/` with the current version being v1. The complete base URL for local development is typically `http://localhost:5000/api/`. For production deployments, replace the hostname and port with your actual deployment URL.

**Authentication and Security**

The current implementation uses session-based authentication for web interface interactions and supports API key authentication for programmatic access. Future versions will include JWT token authentication for enhanced security and scalability.

**Request and Response Format**

All API endpoints accept and return JSON-formatted data unless otherwise specified. Request bodies should include the `Content-Type: application/json` header for POST and PUT requests. Response data is always returned in JSON format with appropriate HTTP status codes.

**Error Handling**

The API uses standard HTTP status codes to indicate success or failure:
- `200 OK`: Successful request
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server-side error

Error responses include detailed error messages in the following format:
```json
{
  "error": "Error type",
  "message": "Detailed error description",
  "details": {
    "field": "Specific field error information"
  }
}
```

### Download Management Endpoints

**Single Video Download**

`POST /api/downloads/single`

Initiates a download for a single video URL with specified parameters.

**Request Body:**
```json
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

**Response:**
```json
{
  "task_id": "uuid-string",
  "status": "queued",
  "message": "Download task created successfully",
  "estimated_start_time": "2025-09-12T23:15:00Z"
}
```

**Video Information Extraction**

`POST /api/downloads/extract-info`

Extracts metadata and available formats for a video URL without initiating a download.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "title": "Video Title",
  "duration": 212,
  "uploader": "Channel Name",
  "upload_date": "2009-10-25",
  "view_count": 1000000,
  "description": "Video description text",
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

**Supported Formats Query**

`GET /api/downloads/formats`

Returns a list of all supported download formats and their descriptions.

**Response:**
```json
{
  "video_formats": [
    {
      "id": "mp4",
      "name": "MP4 (Video)",
      "description": "Most compatible video format",
      "extension": "mp4"
    },
    {
      "id": "mkv", 
      "name": "MKV (Video)",
      "description": "High-quality video container",
      "extension": "mkv"
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

### Playlist Management Endpoints

**Playlist Download**

`POST /api/playlists/download`

Initiates download of an entire playlist with specified parameters applied to all videos.

**Request Body:**
```json
{
  "playlist_url": "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Oq",
  "format": "mp4",
  "quality": "720p", 
  "include_subtitles": true,
  "include_thumbnail": true,
  "upload_to_drive": true,
  "cloud_only": false,
  "max_videos": 50
}
```

**Response:**
```json
{
  "playlist_id": "uuid-string",
  "total_videos": 25,
  "task_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "status": "processing",
  "message": "Playlist processing initiated"
}
```

**Playlist Information**

`POST /api/playlists/info`

Extracts playlist metadata and video list without initiating downloads.

**Request Body:**
```json
{
  "playlist_url": "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Oq"
}
```

**Response:**
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

### Queue Management Endpoints

**Queue Status**

`GET /api/queue/status`

Returns current queue statistics and status information.

**Response:**
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

**Task Details**

`GET /api/queue/tasks`

Returns detailed information about all tasks in the queue.

**Query Parameters:**
- `status`: Filter by task status (pending, running, completed, failed, cancelled)
- `limit`: Maximum number of tasks to return (default: 50)
- `offset`: Number of tasks to skip for pagination (default: 0)

**Response:**
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
      "started_at": "2025-09-12T23:12:00Z",
      "format": "mp4",
      "quality": "720p"
    }
  ],
  "total_count": 10,
  "has_more": false
}
```

**Individual Task Status**

`GET /api/queue/tasks/{task_id}`

Returns detailed status information for a specific task.

**Response:**
```json
{
  "task_id": "uuid-string",
  "url": "https://www.youtube.com/watch?v=example",
  "title": "Video Title",
  "status": "completed",
  "progress": 100.0,
  "file_path": "/downloads/video-title.mp4",
  "file_size": 45678901,
  "download_time": 125.5,
  "created_at": "2025-09-12T23:10:00Z",
  "completed_at": "2025-09-12T23:12:05Z",
  "google_drive_url": "https://drive.google.com/file/d/file-id/view"
}
```

**Queue Control**

`POST /api/queue/control`

Controls queue operations such as pause, resume, and clear.

**Request Body:**
```json
{
  "action": "pause"  // Options: pause, resume, clear_completed, clear_failed
}
```

**Response:**
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

**Task Control**

`POST /api/queue/tasks/{task_id}/control`

Controls individual task operations.

**Request Body:**
```json
{
  "action": "cancel"  // Options: cancel, retry, pause, resume
}
```

### Bulk Operations Endpoints

**Bulk URL Download**

`POST /api/downloads/bulk`

Initiates downloads for multiple URLs with shared parameters.

**Request Body:**
```json
{
  "urls": [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
    "https://vimeo.com/123456789"
  ],
  "format": "mp4",
  "quality": "720p",
  "include_subtitles": false,
  "include_thumbnail": true,
  "upload_to_drive": true,
  "cloud_only": false
}
```

**Response:**
```json
{
  "bulk_id": "uuid-string",
  "total_urls": 3,
  "valid_urls": 3,
  "invalid_urls": 0,
  "task_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "status": "processing"
}
```

### Google Drive Integration Endpoints

**Authentication Status**

`GET /api/google-drive/status`

Returns current Google Drive authentication status.

**Response:**
```json
{
  "authenticated": true,
  "user_email": "user@example.com",
  "storage_quota": {
    "total": 15000000000,
    "used": 5000000000,
    "available": 10000000000
  },
  "permissions": ["drive.file", "drive.metadata.readonly"]
}
```

**Authentication URL**

`GET /api/google-drive/auth-url`

Returns the Google OAuth2 authentication URL for user authorization.

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/oauth2/auth?client_id=...",
  "state": "random-state-string"
}
```

**Token Exchange**

`POST /api/google-drive/callback`

Exchanges authorization code for access tokens (typically called by OAuth2 callback).

**Request Body:**
```json
{
  "code": "authorization-code-from-google",
  "state": "state-string-from-auth-request"
}
```

### WebSocket Events

The application provides real-time updates through WebSocket connections on the `/socket.io` endpoint.

**Connection Events:**
- `connect`: Client connected successfully
- `disconnect`: Client disconnected

**Download Progress Events:**
- `download_progress`: Real-time download progress updates
- `download_completed`: Download completion notification
- `download_failed`: Download failure notification

**Queue Events:**
- `queue_status_update`: Queue statistics updates
- `task_status_change`: Individual task status changes

**Example WebSocket Event:**
```json
{
  "event": "download_progress",
  "data": {
    "task_id": "uuid-string",
    "progress": 67.5,
    "download_speed": "3.2 MB/s",
    "eta": "00:01:45",
    "status": "downloading"
  }
}
```

This comprehensive API documentation enables developers to integrate the Universal Video Downloader functionality into their own applications or create custom interfaces that leverage the powerful downloading and queue management capabilities of the system.


## Google Drive Integration

The Google Drive integration is one of the most powerful features of the Universal Video Downloader Web App, providing seamless cloud storage capabilities that eliminate the need for local storage management and enable easy sharing and access across devices.

### OAuth2 Authentication Flow

The Google Drive integration uses OAuth2 authentication to securely access user accounts without storing passwords or requiring users to share sensitive credentials. This industry-standard authentication method ensures that user data remains secure while providing the necessary permissions for file upload and management operations.

**Authentication Process**: When users first attempt to connect Google Drive, they are redirected to Google's authentication servers where they can review the requested permissions and grant access to their Google Drive account. The application requests minimal permissions necessary for operation, specifically the ability to create and manage files within the user's Google Drive account.

**Token Management**: Once authenticated, the application securely stores access tokens and refresh tokens, enabling automatic re-authentication when tokens expire. This ensures that users don't need to repeatedly authorize the application and that uploads can continue even during extended download sessions.

**Permission Scope**: The application requests only the necessary permissions to upload files and create folders within the user's Google Drive account. It does not request access to existing files or folders unless specifically needed for organization purposes, maintaining user privacy and security.

### Upload Functionality

**Resumable Uploads**: The Google Drive integration implements Google's resumable upload protocol, which is essential for handling large video files that may take significant time to upload. This protocol allows uploads to be paused and resumed automatically in case of network interruptions, ensuring that large files can be successfully uploaded even over unstable connections.

**Progress Tracking**: Upload progress is tracked and reported in real-time through the same WebSocket system used for download progress. Users can monitor upload speed, completion percentage, and estimated time remaining for each file being uploaded to Google Drive.

**Automatic Retry Logic**: The upload system includes sophisticated retry logic that handles temporary network failures, Google API rate limits, and other transient errors. Failed uploads are automatically retried with exponential backoff to avoid overwhelming Google's servers while ensuring reliable upload completion.

### Folder Organization

**Automatic Folder Creation**: The application can automatically create folder structures within Google Drive based on various organizational schemes. Users can configure the system to create folders by date, content type, source platform, or custom naming conventions that suit their organizational preferences.

**Hierarchical Organization**: The folder creation system supports hierarchical structures, allowing for complex organizational schemes such as Year/Month/Day folders for date-based organization or Platform/Channel/Playlist structures for content-based organization.

**Folder Permissions**: Created folders inherit the default sharing permissions of the user's Google Drive account, but users can modify these permissions through the Google Drive interface after creation. The application does not modify sharing permissions automatically, ensuring that users maintain full control over access to their content.

### Cloud-Only Mode

**Storage Optimization**: The cloud-only mode is designed for users who prefer to store all downloaded content directly in cloud storage without consuming local disk space. In this mode, files are downloaded to a temporary location on the server, immediately uploaded to Google Drive, and then removed from local storage.

**Bandwidth Considerations**: Cloud-only mode requires sufficient upload bandwidth to handle the transfer of downloaded files to Google Drive. The system monitors upload progress and provides warnings if upload speeds are significantly slower than download speeds, which could lead to temporary storage accumulation.

**Error Handling**: If Google Drive uploads fail in cloud-only mode, the system temporarily retains local copies and attempts to retry the upload. Users are notified of upload failures and can choose to retry uploads or download files locally as a fallback option.

## Deployment Guide

This section provides comprehensive guidance for deploying the Universal Video Downloader Web App in production environments, covering everything from basic single-server deployments to scalable multi-server configurations.

### Production Environment Requirements

**Server Specifications**: Production deployments require more robust hardware specifications than development environments to handle concurrent users and multiple simultaneous downloads. Recommended specifications include a minimum of 4 CPU cores, 8GB RAM, and 100GB of available storage for temporary file handling. For high-traffic deployments, consider 8+ CPU cores, 16GB+ RAM, and SSD storage for optimal performance.

**Network Requirements**: The server should have a high-bandwidth internet connection capable of handling multiple concurrent video downloads. Consider the aggregate bandwidth requirements of your expected user base and ensure that your hosting provider can support sustained high-bandwidth usage without throttling or additional charges.

**Operating System**: The application is tested and optimized for Ubuntu 20.04 LTS and newer versions, but it can run on any Linux distribution with Python 3.8+ support. CentOS, RHEL, and Debian are also supported with minor configuration adjustments.

### Security Configuration

**SSL/TLS Setup**: Production deployments must use HTTPS to protect user data and authentication tokens. Configure SSL certificates using Let's Encrypt for free certificates or commercial certificate providers for extended validation certificates. The Nginx configuration should include modern SSL settings with strong cipher suites and HSTS headers.

**Firewall Configuration**: Configure the server firewall to allow only necessary ports (80, 443 for web traffic, and 22 for SSH administration). Block direct access to the application port (5000) and route all traffic through the reverse proxy for additional security.

**Environment Variable Security**: Store sensitive configuration data such as Google API credentials, secret keys, and database passwords in environment variables or secure configuration files with restricted permissions. Never commit sensitive data to version control systems.

### Database Configuration

**PostgreSQL Setup**: For production deployments, migrate from SQLite to PostgreSQL for improved performance, concurrent access support, and data integrity. Install PostgreSQL and create a dedicated database and user for the application:

```sql
CREATE DATABASE video_downloader;
CREATE USER video_app WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE video_downloader TO video_app;
```

**Database Optimization**: Configure PostgreSQL for optimal performance by adjusting settings such as `shared_buffers`, `work_mem`, and `max_connections` based on your server specifications and expected load. Regular database maintenance including vacuuming and index optimization should be scheduled.

**Backup Strategy**: Implement automated database backups using `pg_dump` or similar tools. Store backups in a separate location from the primary server and test backup restoration procedures regularly to ensure data recovery capabilities.

### Process Management

**Systemd Service Configuration**: Create a systemd service file to manage the application process, ensuring automatic startup on boot and automatic restart on failure:

```ini
[Unit]
Description=Universal Video Downloader Web App
After=network.target postgresql.service

[Service]
Type=simple
User=video-app
Group=video-app
WorkingDirectory=/opt/video-downloader
Environment=PATH=/opt/video-downloader/venv/bin
EnvironmentFile=/opt/video-downloader/.env
ExecStart=/opt/video-downloader/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Log Management**: Configure comprehensive logging for both the application and system services. Use log rotation to prevent log files from consuming excessive disk space, and consider centralized logging solutions for multi-server deployments.

**Monitoring and Alerting**: Implement monitoring for key metrics including CPU usage, memory consumption, disk space, network bandwidth, and application-specific metrics such as queue length and download success rates. Configure alerts for critical thresholds to enable proactive issue resolution.

### Scaling Considerations

**Horizontal Scaling**: For high-traffic deployments, the application can be scaled horizontally by deploying multiple application instances behind a load balancer. Ensure that shared resources such as the database and file storage are properly configured for concurrent access.

**Queue Distribution**: In multi-server deployments, consider using Redis or RabbitMQ for distributed queue management, allowing download tasks to be distributed across multiple servers for improved performance and reliability.

**CDN Integration**: For serving downloaded content to users, consider integrating with a Content Delivery Network (CDN) to improve download speeds and reduce server bandwidth usage.

## Troubleshooting

This section addresses common issues that users and administrators may encounter when using or deploying the Universal Video Downloader Web App.

### Common Installation Issues

**Python Version Compatibility**: Ensure that Python 3.8 or higher is installed and properly configured. Some Linux distributions may have multiple Python versions installed, so verify that the correct version is being used by checking `python3 --version` and adjusting virtual environment creation accordingly.

**Dependency Installation Failures**: If pip installation fails for certain packages, ensure that system development tools are installed. On Ubuntu/Debian systems, install `build-essential`, `python3-dev`, and `libffi-dev`. On CentOS/RHEL systems, install `gcc`, `python3-devel`, and `libffi-devel`.

**FFmpeg Installation**: The yt-dlp library requires FFmpeg for video processing. If FFmpeg is not automatically installed, install it manually using your system's package manager: `sudo apt install ffmpeg` on Ubuntu/Debian or `sudo yum install ffmpeg` on CentOS/RHEL.

### Download Issues

**Platform Compatibility**: If downloads fail for specific platforms, verify that yt-dlp supports the target platform and that the platform hasn't implemented new anti-bot measures. Update yt-dlp to the latest version using `pip install --upgrade yt-dlp`.

**Network Connectivity**: Download failures may be caused by network connectivity issues, firewall restrictions, or ISP blocking. Test connectivity to target platforms using curl or wget, and consider using a VPN if geographic restrictions are preventing access.

**Rate Limiting**: Some platforms implement rate limiting that can cause download failures when processing multiple videos quickly. The application includes built-in rate limiting, but users may need to adjust concurrent download limits in high-volume scenarios.

### Google Drive Integration Issues

**Authentication Failures**: If Google Drive authentication fails, verify that the OAuth2 credentials are correctly configured and that the redirect URI matches the configuration in Google Cloud Console. Ensure that the Google Drive API is enabled for your project.

**Upload Failures**: Google Drive upload failures may be caused by quota limits, network issues, or file size restrictions. Check the user's Google Drive storage quota and verify that files don't exceed Google's file size limits (5TB for most file types).

**Permission Errors**: If the application cannot create folders or upload files, verify that the OAuth2 scope includes the necessary permissions for file creation and folder management within Google Drive.

### Performance Issues

**Slow Downloads**: Slow download speeds may be caused by server bandwidth limitations, platform throttling, or network congestion. Monitor server bandwidth usage and consider upgrading hosting plans if bandwidth limits are being reached.

**High Memory Usage**: Large video files or multiple concurrent downloads can consume significant memory. Monitor system memory usage and consider increasing server RAM or reducing concurrent download limits if memory exhaustion occurs.

**Database Performance**: As the download history grows, database queries may become slower. Implement database maintenance procedures including index optimization and old record cleanup to maintain performance.

## Technical Specifications

### System Requirements

**Minimum Requirements**:
- CPU: 2 cores, 2.0 GHz
- RAM: 2GB
- Storage: 10GB available space
- Network: Broadband internet connection
- OS: Ubuntu 18.04+, CentOS 7+, or equivalent

**Recommended Requirements**:
- CPU: 4+ cores, 2.5+ GHz
- RAM: 8GB+
- Storage: 100GB+ SSD
- Network: High-bandwidth connection (100+ Mbps)
- OS: Ubuntu 20.04 LTS or newer

### Technology Stack

**Backend Technologies**:
- Python 3.8+
- Flask 2.0+ (Web framework)
- SQLAlchemy (Database ORM)
- yt-dlp (Video downloading)
- Google API Client Libraries
- Flask-SocketIO (WebSocket support)

**Frontend Technologies**:
- React 18 (UI framework)
- Vite (Build tool)
- Tailwind CSS (Styling)
- shadcn/ui (Component library)
- WebSocket client for real-time updates

**Database Support**:
- SQLite (Development/single-user)
- PostgreSQL (Production/multi-user)
- Redis (Optional, for enhanced queue management)

### Performance Characteristics

**Concurrent Downloads**: The system supports configurable concurrent download limits (default: 3) to balance performance with resource usage and platform rate limiting requirements.

**File Size Limits**: No hard file size limits are imposed by the application, but practical limits may be imposed by available storage space, network bandwidth, and platform restrictions.

**Supported Platforms**: The application supports any platform compatible with yt-dlp, including YouTube, Vimeo, Dailymotion, and hundreds of other video hosting services.

This comprehensive documentation provides all the information necessary to understand, deploy, and maintain the Universal Video Downloader Web App in various environments and use cases.

