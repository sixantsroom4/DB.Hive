"use client"

import axios from 'axios'
import { useState, useEffect } from 'react'

interface Dataset {
  id: string
  filename: string
  originalName: string
  description: string
  fileUrl: string
  size: number
  createdAt: string
}

export default function ExplorePage() {
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        const response = await axios.get('http://localhost:8001/api/v1/datasets')
        setDatasets(response.data.datasets)
      } catch (error) {
        console.error('Error fetching datasets:', error)
        setError('Failed to load datasets')
      } finally {
        setLoading(false)
      }
    }

    fetchDatasets()
  }, [])

  // 파일 크기를 읽기 쉬운 형식으로 변환
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  // 날짜 형식 변환
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-secondary py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">Loading datasets...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-surface-secondary py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-red-600 text-center">{error}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-surface-secondary py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="bg-surface-DEFAULT rounded-lg shadow-sm border border-border-DEFAULT p-8">
          <h1 className="text-3xl font-semibold text-gray-900 mb-8">데이터셋 탐색</h1>
          
          {datasets.length === 0 ? (
            <div className="text-center text-gray-500">아직 업로드된 데이터셋이 없습니다.</div>
          ) : (
            <div className="grid gap-6">
              {datasets.map((dataset) => (
                <div
                  key={dataset.id}
                  className="bg-white p-6 rounded-lg border border-border-DEFAULT hover:shadow-md transition-shadow"
                >
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">
                    {dataset.originalName}
                  </h2>
                  {dataset.description && (
                    <p className="text-gray-600 mb-4">{dataset.description}</p>
                  )}
                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                    <div>
                      <span className="font-medium">크기:</span> {formatFileSize(dataset.size)}
                    </div>
                    <div>
                      <span className="font-medium">업로드:</span> {formatDate(dataset.createdAt)}
                    </div>
                  </div>
                  <div className="mt-4">
                    <a
                      href={dataset.fileUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      다운로드
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 