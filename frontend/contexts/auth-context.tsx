'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { 
  User,
  signInWithPopup,
  GithubAuthProvider,
  signOut as firebaseSignOut,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  sendEmailVerification,
  sendPasswordResetEmail
} from 'firebase/auth'
import { auth } from '@/lib/firebase'
import axios from 'axios'

interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  signInWithGithub: () => Promise<void>
  signInWithEmail: (email: string, password: string) => Promise<void>
  signUpWithEmail: (email: string, password: string) => Promise<void>
  sendVerificationEmail: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Firebase 인증 상태 변경 감지
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      if (user) {
        // 토큰 가져오기
        const token = await user.getIdToken()
        
        try {
          // 백엔드에서 토큰 검증
          const response = await axios.post('http://localhost:8001/api/v1/auth/verify-token', null, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          
          // 사용자 정보 설정
          setUser(user)
          setError(null)
        } catch (error) {
          console.error('Token verification failed:', error)
          setError('Authentication failed')
          await firebaseSignOut(auth)
        }
      } else {
        setUser(null)
      }
      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  const signInWithGithub = async () => {
    try {
      setError(null)
      const provider = new GithubAuthProvider()
      await signInWithPopup(auth, provider)
    } catch (error) {
      console.error('GitHub sign in failed:', error)
      setError('GitHub 로그인에 실패했습니다')
    }
  }

  const signInWithEmail = async (email: string, password: string) => {
    try {
      setError(null)
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      if (!userCredential.user.emailVerified) {
        setError('이메일 인증이 필요합니다. 이메일을 확인해주세요.')
        await firebaseSignOut(auth)
        return
      }
    } catch (error: any) {
      console.error('Email sign in failed:', error)
      switch (error.code) {
        case 'auth/user-not-found':
          setError('등록되지 않은 이메일입니다')
          break
        case 'auth/wrong-password':
          setError('잘못된 비밀번호입니다')
          break
        default:
          setError('로그인에 실패했습니다')
      }
    }
  }

  const signUpWithEmail = async (email: string, password: string) => {
    try {
      setError(null)
      const userCredential = await createUserWithEmailAndPassword(auth, email, password)
      await sendEmailVerification(userCredential.user)
      setError('인증 이메일을 발송했습니다. 이메일을 확인해주세요.')
      await firebaseSignOut(auth)
    } catch (error: any) {
      console.error('Email sign up failed:', error)
      switch (error.code) {
        case 'auth/email-already-in-use':
          setError('이미 사용 중인 이메일입니다')
          break
        case 'auth/weak-password':
          setError('비밀번호가 너무 약합니다')
          break
        default:
          setError('회원가입에 실패했습니다')
      }
    }
  }

  const sendVerificationEmail = async () => {
    try {
      if (user && !user.emailVerified) {
        await sendEmailVerification(user)
        setError('인증 이메일을 발송했습니다. 이메일을 확인해주세요.')
      }
    } catch (error) {
      console.error('Send verification email failed:', error)
      setError('인증 이메일 발송에 실패했습니다')
    }
  }

  const resetPassword = async (email: string) => {
    try {
      await sendPasswordResetEmail(auth, email)
      setError('비밀번호 재설정 이메일을 발송했습니다')
    } catch (error: any) {
      console.error('Password reset failed:', error)
      switch (error.code) {
        case 'auth/user-not-found':
          setError('등록되지 않은 이메일입니다')
          break
        default:
          setError('비밀번호 재설정 이메일 발송에 실패했습니다')
      }
    }
  }

  const signOut = async () => {
    try {
      await firebaseSignOut(auth)
      setUser(null)
    } catch (error) {
      console.error('Sign out failed:', error)
      setError('로그아웃에 실패했습니다')
    }
  }

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        loading, 
        error, 
        signInWithGithub, 
        signInWithEmail,
        signUpWithEmail,
        sendVerificationEmail,
        resetPassword,
        signOut 
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 