import { useTranslations } from 'next-intl';
import Image from 'next/image';
import logo from '@/public/logo.png'

function Navbar() {
  const t = useTranslations('Authentication');

  return (
    <nav className="w-full h-auto px-10 bg-sepia flex flex-row justify-around items-center">
      <a href="/">
        <Image src={logo} alt = "Nature transforms your life" width={200}/>
      </a>
      <ul className="list-none w-full h-full flex flex-row justify-around items-center">
        <li>
          {t('About us')}
        </li>
        <li>

        </li>
      </ul>
    </nav>
  )
}

export default Navbar