'use client'

import { Form } from '@/components/Forms';
import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

export default function Authentication() {
  const [formState, setFormState] = useState<'login' | 'register'>('login')

  const [window_width, setWindowWidth] = useState<any>();

  useEffect(() => {
    // Function to update the window width
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    // Check if window is defined (client-side) before adding the event listener
    if (typeof window !== 'undefined') {
      // Initial window width
      handleResize();

      // Add event listener to update width on window resize
      window.addEventListener('resize', handleResize);

      // Cleanup the event listener when component unmounts
      return () => {
        window.removeEventListener('resize', handleResize);
      };
    }
  }, []);


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

  const renderFormByResponsivity = () => {
    if (window_width >  768){
      return (
        <section className="w-full h-full rounded-lg flex flex-row flex-nowrap justify-center items-center">
          <motion.img src = 'https://images.unsplash.com/photo-1627855974700-2be88ada572f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80' alt = "Register Image" style={{
            width: window_width > 768 ? '70%': '100%',
            height: window_width > 768 ? '100%' : '70%',
            cursor: 'pointer',
          }} onClick={() => formState === 'login' ? setFormState('register') : setFormState('login')}
          animate = {{
            left: formState === 'login' ? '0%' : '30%',
            position: 'absolute',
          }}
          transition = {{
            duration: 0.4
          }}
          />
          <motion.div
          style={{
            width: window_width > 768 ? '30%': '100%',
            height: window_width > 768 ? '100%' : '30%',
            cursor: 'pointer',
          }}
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
      )
    } else {
      return (
        <section className="w-full h-full rounded-lg flex flex-col flex-nowrap justify-center items-center">
          <motion.img src = 'https://images.unsplash.com/photo-1627855974700-2be88ada572f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80' alt = "Register Image" 
          style={{
            width: window_width > 768 ? '70%': '100%',
            height: window_width > 768 ? '100%' : '70%',
            cursor: 'pointer',
          }}
          onClick={() => formState === 'login' ? setFormState('register') : setFormState('login')}
          animate = {{
            top: formState === 'login' ? '0%' : '30%',
            left: '0%',
            position: 'absolute',
          }}
          transition = {{
            duration: 0.4
          }}
          />
          <motion.div
          style={{
            width: window_width > 768 ? '30%': '100%',
            height: window_width > 768 ? '100%' : '30%',
            cursor: 'pointer',
          }}
          animate = {{
            top: formState === 'login' ? '70%': '0%',
            left: '0%',
            position: 'absolute',
          }}
          transition = {{
            duration: 0.3
          }}
          >
            {renderFormState()}
          </motion.div>
        </section>
      )
    }
  }
  
  return (
    <main className="w-full h-screen bg-clip-padding backdrop-filter backdrop-blur-md bg-opacity-95">
      {renderFormByResponsivity()}
    </main>
  )
}
