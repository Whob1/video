from flask import Blueprint, request, jsonify
from services.video_service import VideoService
from services.queue_service import QueueService
from services.google_drive_service import GoogleDriveService
import os

downloads_bp = Blueprint('downloads', __name__)

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

@downloads_bp.route('/formats', methods=['GET'])
def get_formats():
    """Get supported download formats"""
    formats = VideoService.get_supported_formats()
    return jsonify(formats), 200

@downloads_bp.route('/extract-info', methods=['POST'])
def extract_info():
    """Extract video information without downloading"""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        info = video_service.extract_info(url)
        return jsonify(info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@downloads_bp.route('/single', methods=['POST'])
def download_single():
    """Initiate single video download"""
    data = request.get_json()
    
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    format = data.get('format', 'mp4')
    quality = data.get('quality', '720p')
    include_subtitles = data.get('include_subtitles', False)
    include_thumbnail = data.get('include_thumbnail', False)
    upload_to_drive = data.get('upload_to_drive', False)
    cloud_only = data.get('cloud_only', False)
    
    # Create download task
    def download_task(task):
        """Task callback for downloading video"""
        try:
            from datetime import datetime
            
            # Update task status
            queue_service.update_task_progress(task['task_id'], 0, status='downloading')
            
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
                url=url,
                format=format,
                quality=quality,
                progress_callback=progress_hook,
                include_subtitles=include_subtitles,
                include_thumbnail=include_thumbnail
            )
            
            # Upload to Google Drive if requested
            if upload_to_drive and drive_service and drive_service.is_authenticated():
                def upload_progress(percent):
                    queue_service.update_task_progress(
                        task['task_id'],
                        percent,
                        status='uploading'
                    )
                
                drive_result = drive_service.upload_file(
                    result['file_path'],
                    progress_callback=upload_progress
                )
                result['google_drive_url'] = drive_result.get('web_view_link')
                
                # Remove local file if cloud_only mode
                if cloud_only:
                    try:
                        os.remove(result['file_path'])
                        result['file_path'] = None
                    except:
                        pass
            
            return result
            
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")
    
    # Add task to queue
    task_data = {
        'url': url,
        'format': format,
        'quality': quality,
        'include_subtitles': include_subtitles,
        'include_thumbnail': include_thumbnail,
        'upload_to_drive': upload_to_drive,
        'cloud_only': cloud_only
    }
    
    task_id = queue_service.add_task(
        task_type='download',
        task_data=task_data,
        callback=download_task
    )
    
    return jsonify({
        'task_id': task_id,
        'status': 'queued',
        'message': 'Download task created successfully'
    }), 201

@downloads_bp.route('/bulk', methods=['POST'])
def download_bulk():
    """Initiate bulk URL downloads"""
    data = request.get_json()
    
    urls = data.get('urls', [])
    if not urls:
        return jsonify({'error': 'URLs are required'}), 400
    
    format = data.get('format', 'mp4')
    quality = data.get('quality', '720p')
    include_subtitles = data.get('include_subtitles', False)
    include_thumbnail = data.get('include_thumbnail', False)
    upload_to_drive = data.get('upload_to_drive', False)
    cloud_only = data.get('cloud_only', False)
    
    task_ids = []
    
    # Create download task for each URL
    for url in urls:
        if not url.strip():
            continue
        
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
                raise Exception(f"Download failed: {str(e)}")
        
        # Add task to queue
        task_data = {
            'url': url.strip(),
            'format': format,
            'quality': quality,
            'include_subtitles': include_subtitles,
            'include_thumbnail': include_thumbnail,
            'upload_to_drive': upload_to_drive,
            'cloud_only': cloud_only
        }
        
        task_id = queue_service.add_task(
            task_type='download',
            task_data=task_data,
            callback=download_task
        )
        task_ids.append(task_id)
    
    return jsonify({
        'total_urls': len(urls),
        'valid_urls': len(task_ids),
        'task_ids': task_ids,
        'status': 'processing'
    }), 201
