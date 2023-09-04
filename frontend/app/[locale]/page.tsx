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
    <main className="w-full h-screen bg-clip-padding backdrop-filter backdrop-blur-md bg-opacity-95">
      <section className="w-full h-full rounded-lg flex flex-row flex-nowrap justify-center items-center">
        <motion.img src = 'https://images.unsplash.com/photo-1627855974700-2be88ada572f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80' alt = "Register Image" className="w-[70%] h-full cursor-pointer" onClick={() => formState === 'login' ? setFormState('register') : setFormState('login')}
        animate = {{
          left: formState === 'login' ? '0%' : '30%',
          position: 'absolute',
        }}
        transition = {{
          duration: 0.4
        }}
        />
        <motion.div
        className="w-[30%] h-full"
        animate = {{
          left: formState === 'login' ? '70%': '0%',
          position: 'absolute',
        }}
        transition = {{
          duration: 0.3
        }}
        >
          {renderFormState()}
        </motion.div>
      </section>
    </main>
  )
}
