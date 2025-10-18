function QueueStatus({ status }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Queue Status
      </h3>
      
      <div className="space-y-4">
        {/* Total Tasks */}
        <div className="flex justify-between items-center pb-3 border-b border-gray-200">
          <span className="text-sm font-medium text-gray-700">Total Tasks</span>
          <span className="text-2xl font-bold text-gray-900">{status.total_tasks}</span>
        </div>

        {/* Status Breakdown */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-yellow-400 mr-2"></div>
              <span className="text-sm text-gray-600">Pending</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">{status.pending}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-blue-400 mr-2"></div>
              <span className="text-sm text-gray-600">Running</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">{status.running}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-green-400 mr-2"></div>
              <span className="text-sm text-gray-600">Completed</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">{status.completed}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-red-400 mr-2"></div>
              <span className="text-sm text-gray-600">Failed</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">{status.failed}</span>
          </div>
          
          {status.cancelled > 0 && (
            <div className="flex justify-between items-center">
              <div className="flex items-center">
                <div className="w-3 h-3 rounded-full bg-gray-400 mr-2"></div>
                <span className="text-sm text-gray-600">Cancelled</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">{status.cancelled}</span>
            </div>
          )}
        </div>

        {/* Queue Info */}
        <div className="pt-3 border-t border-gray-200 text-sm text-gray-600">
          <div className="flex justify-between">
            <span>Max Concurrent</span>
            <span className="font-medium text-gray-900">{status.max_concurrent}</span>
          </div>
          {status.queue_paused && (
            <div className="mt-2 text-yellow-600 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Queue Paused
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default QueueStatus
