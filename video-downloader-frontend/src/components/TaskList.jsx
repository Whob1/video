function TaskList({ tasks, onRefresh }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'running': return 'bg-blue-100 text-blue-800'
      case 'completed': return 'bg-green-100 text-green-800'
      case 'failed': return 'bg-red-100 text-red-800'
      case 'cancelled': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-900">
            Recent Downloads
          </h3>
          <button
            onClick={onRefresh}
            className="text-sm text-blue-600 hover:text-blue-700 flex items-center"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
      </div>

      <div className="divide-y divide-gray-200">
        {tasks.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            No downloads yet. Start by adding a video URL above.
          </div>
        ) : (
          tasks.map((task) => (
            <div key={task.task_id} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex justify-between items-start mb-2">
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-gray-900 truncate">
                    {task.data?.url || 'Unknown URL'}
                  </h4>
                  <p className="text-xs text-gray-500 mt-1">
                    {formatDate(task.created_at)}
                  </p>
                </div>
                <span className={`ml-3 px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(task.status)}`}>
                  {task.status}
                </span>
              </div>

              {/* Progress Bar */}
              {task.status === 'running' && (
                <div className="mt-3">
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{Math.round(task.progress)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${task.progress}%` }}
                    ></div>
                  </div>
                  {task.download_speed && (
                    <div className="mt-1 text-xs text-gray-500 flex justify-between">
                      <span>Speed: {task.download_speed}</span>
                      {task.eta && <span>ETA: {task.eta}</span>}
                    </div>
                  )}
                </div>
              )}

              {/* Task Details */}
              <div className="mt-3 flex flex-wrap gap-2">
                {task.data?.format && (
                  <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                    Format: {task.data.format.toUpperCase()}
                  </span>
                )}
                {task.data?.quality && (
                  <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                    Quality: {task.data.quality}
                  </span>
                )}
                {task.data?.upload_to_drive && (
                  <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-blue-100 text-blue-700">
                    <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z" />
                    </svg>
                    Drive Upload
                  </span>
                )}
              </div>

              {/* Error Message */}
              {task.status === 'failed' && task.error && (
                <div className="mt-3 p-2 bg-red-50 rounded text-xs text-red-700">
                  Error: {task.error}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default TaskList
