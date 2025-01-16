"use client"

import { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/navigation'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string>('')
  const [success, setSuccess] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError('파일을 선택해주세요')
      return
    }
    if (!name.trim()) {
      setError('데이터셋 이름을 입력해주세요')
      return
    }

    setUploading(true)
    setError('')
    setSuccess(false)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', name)
    formData.append('description', description)

    try {
      console.log('Uploading file:', file.name)
      console.log('Dataset name:', name)
      console.log('Description:', description)

      const response = await axios.post('http://localhost:8001/api/v1/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      console.log('Upload response:', response.data)
      setSuccess(true)
      
      // 3초 후 explore 페이지로 이동
      setTimeout(() => {
        router.push('/explore')
      }, 3000)
    } catch (error) {
      console.error('Upload error:', error)
      setError('파일 업로드에 실패했습니다. 다시 시도해주세요.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-surface-secondary py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-surface-DEFAULT rounded-lg shadow-sm border border-border-DEFAULT p-8">
          <h1 className="text-3xl font-semibold text-gray-900 mb-8">데이터셋 업로드</h1>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="file" className="block text-sm font-medium text-gray-700 mb-2">
                파일 선택
              </label>
              <input
                type="file"
                id="file"
                accept=".csv,.json"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
            </div>

            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                데이터셋 이름
              </label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="block w-full rounded-md border border-border-DEFAULT px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
                placeholder="데이터셋의 이름을 입력하세요"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                설명 (선택사항)
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="block w-full rounded-md border border-border-DEFAULT px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
                placeholder="데이터셋에 대한 설명을 입력하세요"
              />
            </div>

            {error && (
              <div className="text-red-600 text-sm">{error}</div>
            )}

            {success && (
              <div className="text-green-600 text-sm">
                파일이 성공적으로 업로드되었습니다. 잠시 후 데이터셋 목록 페이지로 이동합니다...
              </div>
            )}

            <button
              type="submit"
              disabled={uploading}
              className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
                ${uploading 
                  ? 'bg-blue-400 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                }`}
            >
              {uploading ? '업로드 중...' : '업로드'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
} 