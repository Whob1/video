from flask import Blueprint, request, jsonify
from services.video_service import VideoService
from services.queue_service import QueueService
from services.google_drive_service import GoogleDriveService
import os

playlists_bp = Blueprint('playlists', __name__)

# Global service instances (will be initialized in main.py)
video_service = None
queue_service = None
drive_service = None

def init_services(video_svc, queue_svc, drive_svc):
    """Initialize service instances"""
    global video_service, queue_service, drive_service
    video_service = video_svc
    queue_service = queue_svc
    drive_service = drive_svc

@playlists_bp.route('/info', methods=['POST'])
def get_playlist_info():
    """Extract playlist information"""
    data = request.get_json()
    playlist_url = data.get('playlist_url')
    
    if not playlist_url:
        return jsonify({'error': 'Playlist URL is required'}), 400
    
    try:
        info = video_service.extract_playlist_info(playlist_url)
        return jsonify(info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlists_bp.route('/download', methods=['POST'])
def download_playlist():
    """Initiate playlist download"""
    data = request.get_json()
    
    playlist_url = data.get('playlist_url')
    if not playlist_url:
        return jsonify({'error': 'Playlist URL is required'}), 400
    
    format = data.get('format', 'mp4')
    quality = data.get('quality', '720p')
    include_subtitles = data.get('include_subtitles', False)
    include_thumbnail = data.get('include_thumbnail', False)
    upload_to_drive = data.get('upload_to_drive', False)
    cloud_only = data.get('cloud_only', False)
    max_videos = data.get('max_videos', None)
    
    try:
        # Get playlist info
        playlist_info = video_service.extract_playlist_info(playlist_url)
        videos = playlist_info['videos']
        
        # Limit videos if max_videos is specified
        if max_videos:
            videos = videos[:max_videos]
        
        task_ids = []
        
        # Create download task for each video
        for video in videos:
            video_url = video['url']
            
            def download_task(task):
                """Task callback for downloading video"""
                try:
                    task_url = task['data']['url']
                    
                    # Progress callback
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
                            queue_service.update_task_progress(
                                task['task_id'], 
                                percent,
                                download_speed=d.get('speed_str', ''),
                                eta=d.get('eta_str', '')
                            )
                    
                    # Download video
                    result = video_service.download_video(
                        url=task_url,
                        format=format,
                        quality=quality,
                        progress_callback=progress_hook,
                        include_subtitles=include_subtitles,
                        include_thumbnail=include_thumbnail
                    )
                    
                    # Upload to Google Drive if requested
                    if upload_to_drive and drive_service and drive_service.is_authenticated():
                        drive_result = drive_service.upload_file(result['file_path'])
                        result['google_drive_url'] = drive_result.get('web_view_link')
                        
                        if cloud_only:
                            try:
                                os.remove(result['file_path'])
                                result['file_path'] = None
                            except:
                                pass
                    
                    return result
                    
                except Exception as e:
                    # Don't fail entire playlist for one video
                    return {'error': str(e), 'url': task_url}
            
            # Add task to queue
            task_data = {
                'url': video_url,
                'format': format,
                'quality': quality,
                'include_subtitles': include_subtitles,
                'include_thumbnail': include_thumbnail,
                'upload_to_drive': upload_to_drive,
                'cloud_only': cloud_only,
                'playlist_title': playlist_info.get('title', 'Unknown Playlist')
            }
            
            task_id = queue_service.add_task(
                task_type='playlist_download',
                task_data=task_data,
                callback=download_task
            )
            task_ids.append(task_id)
        
        return jsonify({
            'playlist_title': playlist_info.get('title'),
            'total_videos': len(videos),
            'task_ids': task_ids,
            'status': 'processing',
            'message': 'Playlist processing initiated'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
