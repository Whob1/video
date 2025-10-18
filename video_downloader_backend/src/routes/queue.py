from flask import Blueprint, request, jsonify
from services.queue_service import QueueService

queue_bp = Blueprint('queue', __name__)

# Global service instance (will be initialized in main.py)
queue_service = None

def init_services(queue_svc):
    """Initialize service instances"""
    global queue_service
    queue_service = queue_svc

@queue_bp.route('/status', methods=['GET'])
def get_queue_status():
    """Get overall queue status"""
    status = queue_service.get_queue_status()
    return jsonify(status), 200

@queue_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Get all tasks with optional filtering"""
    status = request.args.get('status')
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    tasks = queue_service.get_all_tasks(status=status, limit=limit, offset=offset)
    return jsonify(tasks), 200

@queue_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Get status of a specific task"""
    task = queue_service.get_task_status(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Remove callback from response (not JSON serializable)
    task_response = task.copy()
    task_response.pop('callback', None)
    
    # Convert datetime objects to ISO format
    for key in ['created_at', 'started_at', 'completed_at']:
        if task_response.get(key):
            task_response[key] = task_response[key].isoformat()
    
    return jsonify(task_response), 200

@queue_bp.route('/control', methods=['POST'])
def control_queue():
    """Control queue operations"""
    data = request.get_json()
    action = data.get('action')
    
    if not action:
        return jsonify({'error': 'Action is required'}), 400
    
    if action == 'pause':
        queue_service.pause_queue()
        message = 'Queue paused successfully'
    elif action == 'resume':
        queue_service.resume_queue()
        message = 'Queue resumed successfully'
    elif action == 'clear_completed':
        queue_service.clear_completed()
        message = 'Completed tasks cleared'
    elif action == 'clear_failed':
        queue_service.clear_failed()
        message = 'Failed tasks cleared'
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    return jsonify({
        'status': 'success',
        'message': message,
        'queue_status': queue_service.get_queue_status()
    }), 200

@queue_bp.route('/tasks/<task_id>/control', methods=['POST'])
def control_task(task_id):
    """Control individual task operations"""
    data = request.get_json()
    action = data.get('action')
    
    if not action:
        return jsonify({'error': 'Action is required'}), 400
    
    if action == 'cancel':
        success = queue_service.cancel_task(task_id)
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Task cancelled successfully'
            }), 200
        else:
            return jsonify({'error': 'Task not found or cannot be cancelled'}), 404
    else:
        return jsonify({'error': 'Invalid action'}), 400
