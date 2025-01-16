// File: /Users/jjpark/Desktop/DB.Hive/frontend/components/Header.tsx

"use client"

import { useState } from 'react'
import Link from 'next/link'
import { MagnifyingGlassIcon } from '@heroicons/react/24/solid'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

export default function Header() {
  const [menuOpen, setMenuOpen] = useState<boolean>(false)

  return (
    <header className="bg-gh-bg text-white sticky top-0 z-50">
      <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
        {/* Left: Logo & Brand */}
        <div className="flex items-center space-x-4">
          <Link href="/" className="text-xl font-bold">
            DB Hive
          </Link>
        </div>

        {/* Middle: Menu (Desktop) */}
        <nav className="hidden md:flex items-center space-x-6">
          <Link href="/explore" className="hover:text-gray-200">
            Explore
          </Link>
          <Link href="/upload" className="hover:text-gray-200">
            Upload
          </Link>
        </nav>

        {/* Middle: Search Bar */}
        <div className="hidden md:flex flex-1 mx-6">
          <div className="relative w-full">
            <MagnifyingGlassIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-10 pr-3 py-2 rounded-md bg-gray-200 text-gray-900 focus:outline-none"
            />
          </div>
        </div>

        {/* Right: Profile / Auth */}
        <div className="hidden md:flex items-center space-x-4">
          <button className="px-4 py-2 bg-blue-600 rounded-md hover:bg-blue-700">
            Sign In
          </button>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <button onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle Menu">
            {menuOpen ? (
              <XMarkIcon className="h-6 w-6" />
            ) : (
              <Bars3Icon className="h-6 w-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {menuOpen && (
        <div className="md:hidden bg-gh-bg px-4 pb-4">
          <nav className="flex flex-col space-y-2 text-white">
            <Link href="/explore" className="hover:text-gray-200" onClick={() => setMenuOpen(false)}>
              Explore
            </Link>
            <Link href="/upload" className="hover:text-gray-200" onClick={() => setMenuOpen(false)}>
              Upload
            </Link>
            <div className="relative mt-2">
              <MagnifyingGlassIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search..."
                className="w-full pl-10 pr-3 py-2 rounded-md bg-gray-200 text-gray-900 focus:outline-none"
              />
            </div>
            <button
              className="mt-2 px-4 py-2 bg-blue-600 rounded-md hover:bg-blue-700"
              onClick={() => setMenuOpen(false)}
            >
              Sign In
            </button>
          </nav>
        </div>
      )}
    </header>
  )
}
