import yt_dlp
import os
from typing import Dict, Any, Optional, Callable
import threading

class VideoService:
    """Service for handling video downloads using yt-dlp"""
    
    def __init__(self, upload_folder='./uploads'):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def extract_info(self, url: str) -> Dict[str, Any]:
        """Extract video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'upload_date': info.get('upload_date', ''),
                'view_count': info.get('view_count', 0),
                'description': info.get('description', ''),
                'thumbnail': info.get('thumbnail', ''),
                'available_formats': self._extract_formats(info),
                'available_subtitles': list(info.get('subtitles', {}).keys())
            }
    
    def extract_playlist_info(self, url: str) -> Dict[str, Any]:
        """Extract playlist information"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' not in info:
                raise ValueError("Not a valid playlist URL")
            
            videos = []
            for entry in info['entries']:
                if entry:
                    videos.append({
                        'url': f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                        'title': entry.get('title', 'Unknown'),
                        'duration': entry.get('duration', 0)
                    })
            
            return {
                'title': info.get('title', 'Unknown Playlist'),
                'description': info.get('description', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'video_count': len(videos),
                'videos': videos
            }
    
    def download_video(self, 
                      url: str, 
                      format: str = 'mp4', 
                      quality: str = '720p',
                      output_path: Optional[str] = None,
                      progress_callback: Optional[Callable] = None,
                      include_subtitles: bool = False,
                      include_thumbnail: bool = False) -> Dict[str, Any]:
        """Download a video with specified options"""
        
        if output_path is None:
            output_path = self.upload_folder
        
        output_template = os.path.join(output_path, '%(title)s.%(ext)s')
        
        # Build format string based on quality and format
        format_str = self._build_format_string(format, quality)
        
        ydl_opts = {
            'format': format_str,
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        # Add subtitle options
        if include_subtitles:
            ydl_opts['writesubtitles'] = True
            ydl_opts['writeautomaticsub'] = True
            ydl_opts['subtitleslangs'] = ['en', 'es', 'fr', 'de']
        
        # Add thumbnail option
        if include_thumbnail:
            ydl_opts['writethumbnail'] = True
        
        # Audio-only formats
        if format in ['mp3', 'flac', 'aac', 'ogg', 'wav', 'm4a', 'wma']:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192' if format == 'mp3' else '0',
            }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            filename = ydl.prepare_filename(info)
            
            # For audio conversions, adjust the extension
            if format in ['mp3', 'flac', 'aac', 'ogg', 'wav', 'm4a', 'wma']:
                filename = os.path.splitext(filename)[0] + f'.{format}'
            
            return {
                'title': info.get('title', 'Unknown'),
                'file_path': filename,
                'file_size': os.path.getsize(filename) if os.path.exists(filename) else 0,
                'duration': info.get('duration', 0),
                'format': format,
                'quality': quality
            }
    
    def _extract_formats(self, info: Dict) -> list:
        """Extract available formats from video info"""
        formats = []
        seen = set()
        
        for fmt in info.get('formats', []):
            height = fmt.get('height')
            if height and height not in seen:
                seen.add(height)
                formats.append({
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext', 'mp4'),
                    'quality': f"{height}p",
                    'filesize': fmt.get('filesize', 0)
                })
        
        # Sort by quality (height)
        formats.sort(key=lambda x: int(x['quality'][:-1]) if x['quality'][:-1].isdigit() else 0, reverse=True)
        
        return formats
    
    def _build_format_string(self, format: str, quality: str) -> str:
        """Build yt-dlp format string based on format and quality"""
        
        # If quality is "best", return best available
        if quality.lower() == 'best available':
            return 'best'
        
        # Extract height from quality string (e.g., "720p" -> 720)
        height = quality.replace('p', '') if 'p' in quality else quality
        
        # Video formats
        if format in ['mp4', 'mkv', 'webm', 'avi', 'mov', 'flv', 'wmv']:
            return f'bestvideo[height<={height}][ext={format}]+bestaudio[ext=m4a]/best[height<={height}]'
        
        # Audio formats will be handled separately in download_video
        return 'best'
    
    @staticmethod
    def get_supported_formats() -> Dict[str, list]:
        """Get list of supported formats"""
        return {
            'video_formats': [
                {'id': 'mp4', 'name': 'MP4 (Video)', 'description': 'Most compatible video format', 'extension': 'mp4'},
                {'id': 'mkv', 'name': 'MKV (Video)', 'description': 'High-quality video container', 'extension': 'mkv'},
                {'id': 'webm', 'name': 'WebM (Video)', 'description': 'Web-optimized format', 'extension': 'webm'},
                {'id': 'avi', 'name': 'AVI (Video)', 'description': 'Legacy video format', 'extension': 'avi'},
                {'id': 'mov', 'name': 'MOV (Video)', 'description': 'QuickTime format', 'extension': 'mov'},
                {'id': 'flv', 'name': 'FLV (Video)', 'description': 'Flash video format', 'extension': 'flv'},
                {'id': 'wmv', 'name': 'WMV (Video)', 'description': 'Windows Media format', 'extension': 'wmv'},
            ],
            'audio_formats': [
                {'id': 'mp3', 'name': 'MP3 (Audio)', 'description': 'Standard audio format', 'extension': 'mp3'},
                {'id': 'flac', 'name': 'FLAC (Audio)', 'description': 'Lossless audio format', 'extension': 'flac'},
                {'id': 'aac', 'name': 'AAC (Audio)', 'description': 'High-quality audio', 'extension': 'aac'},
                {'id': 'ogg', 'name': 'OGG (Audio)', 'description': 'Vorbis audio format', 'extension': 'ogg'},
                {'id': 'wav', 'name': 'WAV (Audio)', 'description': 'Uncompressed audio', 'extension': 'wav'},
                {'id': 'm4a', 'name': 'M4A (Audio)', 'description': 'MPEG-4 audio', 'extension': 'm4a'},
                {'id': 'wma', 'name': 'WMA (Audio)', 'description': 'Windows Media audio', 'extension': 'wma'},
            ]
        }
