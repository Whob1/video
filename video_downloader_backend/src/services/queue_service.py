import uuid
import threading
import time
from datetime import datetime
from typing import Dict, Any, Callable, Optional
from queue import PriorityQueue
import json

class QueueService:
    """Service for managing download queue with priority support"""
    
    def __init__(self, max_concurrent=3):
        self.max_concurrent = max_concurrent
        self.queue = PriorityQueue()
        self.tasks = {}  # task_id -> task_info
        self.running_tasks = {}  # task_id -> thread
        self.paused = False
        self.lock = threading.Lock()
        self.worker_thread = None
        self.running = False
    
    def start(self):
        """Start the queue processor"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
            self.worker_thread.start()
    
    def stop(self):
        """Stop the queue processor"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
    
    def add_task(self, 
                 task_type: str, 
                 task_data: Dict[str, Any], 
                 priority: int = 0,
                 callback: Optional[Callable] = None) -> str:
        """Add a task to the queue"""
        task_id = str(uuid.uuid4())
        
        task_info = {
            'task_id': task_id,
            'task_type': task_type,
            'priority': priority,
            'status': 'pending',
            'data': task_data,
            'callback': callback,
            'created_at': datetime.utcnow(),
            'started_at': None,
            'completed_at': None,
            'progress': 0.0,
            'error': None
        }
        
        with self.lock:
            self.tasks[task_id] = task_info
            # Priority queue uses negative priority for higher priority first
            self.queue.put((-priority, time.time(), task_id))
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        with self.lock:
            return self.tasks.get(task_id)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue status"""
        with self.lock:
            total = len(self.tasks)
            pending = sum(1 for t in self.tasks.values() if t['status'] == 'pending')
            running = sum(1 for t in self.tasks.values() if t['status'] == 'running')
            completed = sum(1 for t in self.tasks.values() if t['status'] == 'completed')
            failed = sum(1 for t in self.tasks.values() if t['status'] == 'failed')
            cancelled = sum(1 for t in self.tasks.values() if t['status'] == 'cancelled')
            
            return {
                'total_tasks': total,
                'pending': pending,
                'running': running,
                'completed': completed,
                'failed': failed,
                'cancelled': cancelled,
                'max_concurrent': self.max_concurrent,
                'queue_paused': self.paused
            }
    
    def get_all_tasks(self, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get all tasks with optional filtering"""
        with self.lock:
            tasks = list(self.tasks.values())
            
            if status:
                tasks = [t for t in tasks if t['status'] == status]
            
            # Sort by created_at descending
            tasks.sort(key=lambda x: x['created_at'], reverse=True)
            
            # Apply pagination
            total_count = len(tasks)
            tasks = tasks[offset:offset + limit]
            
            # Remove callback functions from response (not JSON serializable)
            tasks_response = []
            for task in tasks:
                task_copy = task.copy()
                task_copy.pop('callback', None)
                # Convert datetime objects to ISO format
                for key in ['created_at', 'started_at', 'completed_at']:
                    if task_copy.get(key):
                        task_copy[key] = task_copy[key].isoformat()
                tasks_response.append(task_copy)
            
            return {
                'tasks': tasks_response,
                'total_count': total_count,
                'has_more': (offset + limit) < total_count
            }
    
    def pause_queue(self):
        """Pause queue processing"""
        self.paused = True
    
    def resume_queue(self):
        """Resume queue processing"""
        self.paused = False
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a specific task"""
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task['status'] in ['pending', 'running']:
                    task['status'] = 'cancelled'
                    task['completed_at'] = datetime.utcnow()
                    return True
        return False
    
    def clear_completed(self):
        """Clear completed tasks from history"""
        with self.lock:
            to_remove = [tid for tid, task in self.tasks.items() if task['status'] == 'completed']
            for tid in to_remove:
                del self.tasks[tid]
    
    def clear_failed(self):
        """Clear failed tasks from history"""
        with self.lock:
            to_remove = [tid for tid, task in self.tasks.items() if task['status'] == 'failed']
            for tid in to_remove:
                del self.tasks[tid]
    
    def update_task_progress(self, task_id: str, progress: float, **kwargs):
        """Update task progress"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['progress'] = progress
                for key, value in kwargs.items():
                    self.tasks[task_id][key] = value
    
    def _process_queue(self):
        """Background worker to process queued tasks"""
        while self.running:
            try:
                # Check if we can start new tasks
                if self.paused or len(self.running_tasks) >= self.max_concurrent:
                    time.sleep(1)
                    continue
                
                # Get next task from queue (with timeout)
                try:
                    priority, timestamp, task_id = self.queue.get(timeout=1)
                except:
                    continue
                
                with self.lock:
                    if task_id not in self.tasks:
                        continue
                    
                    task = self.tasks[task_id]
                    
                    # Skip if task was cancelled
                    if task['status'] == 'cancelled':
                        continue
                    
                    # Mark task as running
                    task['status'] = 'running'
                    task['started_at'] = datetime.utcnow()
                
                # Execute task in a separate thread
                thread = threading.Thread(target=self._execute_task, args=(task_id,), daemon=True)
                self.running_tasks[task_id] = thread
                thread.start()
                
            except Exception as e:
                print(f"Error in queue processor: {e}")
                time.sleep(1)
    
    def _execute_task(self, task_id: str):
        """Execute a single task"""
        try:
            task = self.tasks[task_id]
            callback = task.get('callback')
            
            if callback:
                # Execute the callback
                result = callback(task)
                
                with self.lock:
                    if task['status'] != 'cancelled':
                        task['status'] = 'completed'
                        task['completed_at'] = datetime.utcnow()
                        task['result'] = result
            
        except Exception as e:
            with self.lock:
                task = self.tasks[task_id]
                task['status'] = 'failed'
                task['completed_at'] = datetime.utcnow()
                task['error'] = str(e)
        
        finally:
            # Remove from running tasks
            with self.lock:
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]
