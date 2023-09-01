'use client'

import { Form } from '@/components/Forms';
import { useTranslations } from 'next-intl';
import { useState } from 'react'
import { motion } from 'framer-motion'

export default function Authentication() {
  const t = useTranslations('Authentication');
  const [formState, setFormState] = useState<'login' | 'register'>('login')

  const renderFormState = () => {
    switch (formState) {
      case 'login':
        return <Form.Login />
      case'register':
        return <Form.Register />
      default:
        return null
    }
  }
  
  return (
    <main className="w-full h-screen px-12 max-[768px]:px-4 py-5 bg-black bg-clip-padding backdrop-filter backdrop-blur-md bg-opacity-95">
      <div className="w-full h-full flex flex-col justify-center items-center gap-5">
        {renderFormState()}
        <div className="w-16 h-auto p-2 bg-blue-600 rounded-3xl cursor-pointer" onClick={() => setFormState(formState === 'login' ? 'register' : 'login')}>
          <motion.div className="bg-white w-5 h-5 rounded-full"
            animate={{
              x: formState === 'register' ? 29 : 0
            }}
            transition = {{
              type: "spring",
              duration: 0.5
            }}
          />
        </div>
      </div>
    </main>
  )
}
