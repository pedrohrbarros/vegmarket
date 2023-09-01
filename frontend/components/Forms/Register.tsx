import { useTranslations } from 'next-intl';
import { motion } from 'framer-motion'

export default function RegisterForm() {

  const t = useTranslations('Authentication');

  return (
    <motion.form className="w-full h-full p-5 rounded-lg"
      animate = {{
        rotateY: 180,
        backgroundColor: "#357738"
      }}
      transition = {{
        type: "spring",
        duration: 1.7,
      }}
    >

    </motion.form>
  )
}