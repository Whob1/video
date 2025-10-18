import { useState } from 'react'

function DownloadForm({ onDownloadStart }) {
  const [activeTab, setActiveTab] = useState('single')
  const [url, setUrl] = useState('')
  const [bulkUrls, setBulkUrls] = useState('')
  const [format, setFormat] = useState('mp4')
  const [quality, setQuality] = useState('720p')
  const [includeSubtitles, setIncludeSubtitles] = useState(false)
  const [includeThumbnail, setIncludeThumbnail] = useState(false)
  const [uploadToDrive, setUploadToDrive] = useState(false)
  const [cloudOnly, setCloudOnly] = useState(false)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const formats = {
    video: ['mp4', 'mkv', 'webm', 'avi', 'mov', 'flv', 'wmv'],
    audio: ['mp3', 'flac', 'aac', 'ogg', 'wav', 'm4a', 'wma']
  }

  const qualities = ['1080p', '720p', '480p', '360p', 'best available']

  const handleSingleDownload = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await fetch('/api/downloads/single', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url,
          format,
          quality,
          include_subtitles: includeSubtitles,
          include_thumbnail: includeThumbnail,
          upload_to_drive: uploadToDrive,
          cloud_only: cloudOnly
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setMessage('Download started successfully!')
        setUrl('')
        onDownloadStart()
      } else {
        setMessage(`Error: ${data.error}`)
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handlePlaylistDownload = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await fetch('/api/playlists/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          playlist_url: url,
          format,
          quality,
          include_subtitles: includeSubtitles,
          include_thumbnail: includeThumbnail,
          upload_to_drive: uploadToDrive,
          cloud_only: cloudOnly
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setMessage(`Playlist download started! ${data.total_videos} videos queued.`)
        setUrl('')
        onDownloadStart()
      } else {
        setMessage(`Error: ${data.error}`)
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleBulkDownload = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    const urls = bulkUrls.split('\n').filter(u => u.trim())

    try {
      const response = await fetch('/api/downloads/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          urls,
          format,
          quality,
          include_subtitles: includeSubtitles,
          include_thumbnail: includeThumbnail,
          upload_to_drive: uploadToDrive,
          cloud_only: cloudOnly
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setMessage(`Bulk download started! ${data.valid_urls} videos queued.`)
        setBulkUrls('')
        onDownloadStart()
      } else {
        setMessage(`Error: ${data.error}`)
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex -mb-px">
          <button
            onClick={() => setActiveTab('single')}
            className={`px-6 py-4 text-sm font-medium border-b-2 ${
              activeTab === 'single'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Single Video
          </button>
          <button
            onClick={() => setActiveTab('playlist')}
            className={`px-6 py-4 text-sm font-medium border-b-2 ${
              activeTab === 'playlist'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Playlist
          </button>
          <button
            onClick={() => setActiveTab('bulk')}
            className={`px-6 py-4 text-sm font-medium border-b-2 ${
              activeTab === 'bulk'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Bulk URLs
          </button>
        </nav>
      </div>

      {/* Form Content */}
      <div className="p-6">
        <form onSubmit={
          activeTab === 'single' ? handleSingleDownload :
          activeTab === 'playlist' ? handlePlaylistDownload :
          handleBulkDownload
        }>
          {/* URL Input */}
          {activeTab !== 'bulk' ? (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {activeTab === 'single' ? 'Video URL' : 'Playlist URL'}
              </label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                placeholder={`Enter ${activeTab} URL`}
                required
              />
            </div>
          ) : (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                URLs (one per line)
              </label>
              <textarea
                value={bulkUrls}
                onChange={(e) => setBulkUrls(e.target.value)}
                rows="5"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter URLs, one per line"
                required
              />
            </div>
          )}

          {/* Format and Quality */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Format
              </label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <optgroup label="Video Formats">
                  {formats.video.map(f => (
                    <option key={f} value={f}>{f.toUpperCase()}</option>
                  ))}
                </optgroup>
                <optgroup label="Audio Formats">
                  {formats.audio.map(f => (
                    <option key={f} value={f}>{f.toUpperCase()}</option>
                  ))}
                </optgroup>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quality
              </label>
              <select
                value={quality}
                onChange={(e) => setQuality(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                {qualities.map(q => (
                  <option key={q} value={q}>{q}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Options */}
          <div className="space-y-3 mb-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={includeSubtitles}
                onChange={(e) => setIncludeSubtitles(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Include Subtitles</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={includeThumbnail}
                onChange={(e) => setIncludeThumbnail(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Include Thumbnail</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={uploadToDrive}
                onChange={(e) => setUploadToDrive(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Upload to Google Drive</span>
            </label>
            {uploadToDrive && (
              <label className="flex items-center ml-6">
                <input
                  type="checkbox"
                  checked={cloudOnly}
                  onChange={(e) => setCloudOnly(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">Cloud Only (don't save locally)</span>
              </label>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : `Download ${activeTab === 'single' ? 'Video' : activeTab === 'playlist' ? 'Playlist' : 'All'}`}
          </button>

          {/* Message */}
          {message && (
            <div className={`mt-4 p-3 rounded-md text-sm ${
              message.includes('Error') ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'
            }`}>
              {message}
            </div>
          )}
        </form>
      </div>
    </div>
  )
}

export default DownloadForm
