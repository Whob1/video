import { useState, useEffect } from 'react'
import io from 'socket.io-client'
import DownloadForm from './components/DownloadForm'
import QueueStatus from './components/QueueStatus'
import TaskList from './components/TaskList'

function App() {
  const [socket, setSocket] = useState(null)
  const [queueStatus, setQueueStatus] = useState({
    total_tasks: 0,
    pending: 0,
    running: 0,
    completed: 0,
    failed: 0,
    cancelled: 0
  })
  const [tasks, setTasks] = useState([])
  const [driveStatus, setDriveStatus] = useState({ authenticated: false })

  // Initialize WebSocket connection
  useEffect(() => {
    const newSocket = io('http://localhost:5000')
    
    newSocket.on('connect', () => {
      console.log('Connected to server')
    })
    
    newSocket.on('queue_status_update', (status) => {
      setQueueStatus(status)
    })
    
    newSocket.on('disconnect', () => {
      console.log('Disconnected from server')
    })
    
    setSocket(newSocket)
    
    return () => newSocket.close()
  }, [])

  // Fetch initial queue status
  useEffect(() => {
    fetchQueueStatus()
    fetchTasks()
    fetchDriveStatus()
    
    // Refresh every 5 seconds
    const interval = setInterval(() => {
      fetchQueueStatus()
      fetchTasks()
    }, 5000)
    
    return () => clearInterval(interval)
  }, [])

  const fetchQueueStatus = async () => {
    try {
      const response = await fetch('/api/queue/status')
      const data = await response.json()
      setQueueStatus(data)
    } catch (error) {
      console.error('Error fetching queue status:', error)
    }
  }

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/queue/tasks?limit=20')
      const data = await response.json()
      setTasks(data.tasks || [])
    } catch (error) {
      console.error('Error fetching tasks:', error)
    }
  }

  const fetchDriveStatus = async () => {
    try {
      const response = await fetch('/api/auth/google-drive/status')
      const data = await response.json()
      setDriveStatus(data)
    } catch (error) {
      console.error('Error fetching drive status:', error)
    }
  }

  const handleDownloadComplete = () => {
    fetchQueueStatus()
    fetchTasks()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Universal Video Downloader
          </h1>
          <p className="mt-1 text-sm text-gray-600">
            Download videos, playlists, and audio from various platforms
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Download Forms */}
          <div className="lg:col-span-2 space-y-6">
            <DownloadForm onDownloadStart={handleDownloadComplete} />
            <TaskList tasks={tasks} onRefresh={fetchTasks} />
          </div>

          {/* Right Column - Status */}
          <div className="space-y-6">
            <QueueStatus status={queueStatus} />
            
            {/* Google Drive Status */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Google Drive
              </h3>
              {driveStatus.authenticated ? (
                <div>
                  <div className="flex items-center text-green-600 mb-2">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    Connected
                  </div>
                  {driveStatus.user_email && (
                    <p className="text-sm text-gray-600">{driveStatus.user_email}</p>
                  )}
                  {driveStatus.storage_quota && (
                    <div className="mt-4">
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Storage</span>
                        <span>
                          {(driveStatus.storage_quota.used / (1024 * 1024 * 1024)).toFixed(2)} GB / 
                          {(driveStatus.storage_quota.total / (1024 * 1024 * 1024)).toFixed(2)} GB
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${(driveStatus.storage_quota.used / driveStatus.storage_quota.total) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <p className="text-sm text-gray-600 mb-4">
                    Connect your Google Drive to enable cloud uploads
                  </p>
                  <button 
                    onClick={async () => {
                      const response = await fetch('/api/auth/google-drive/auth-url')
                      const data = await response.json()
                      window.open(data.auth_url, '_blank')
                    }}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                  >
                    Connect Google Drive
                  </button>
                </div>
              )}
            </div>

            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Stats
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Total Downloads</span>
                  <span className="text-lg font-semibold text-gray-900">
                    {queueStatus.total_tasks}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Successful</span>
                  <span className="text-lg font-semibold text-green-600">
                    {queueStatus.completed}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Failed</span>
                  <span className="text-lg font-semibold text-red-600">
                    {queueStatus.failed}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
