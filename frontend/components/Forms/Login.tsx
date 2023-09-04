import { useTranslations } from 'next-intl';
import Image from 'next/image'
import logo from '@/public/logo.png'
import Button from '../Button';

export default function LoginForm() {

  const t = useTranslations('Authentication');

  return (
    <form className="w-full h-full px-5 flex flex-col justify-center items-center gap-10 max-[768px]:w-full bg-sepia">
      <Image src={logo} alt = "Nature transforms your life" className="w-[30%] h-auto rounded-full absolute -top-[10px]"/>
      <h1 className="text-5xl font-extrabold text-transparent font-outline-2">{t('Sign In')}</h1>
      <div
        className="h-auto flex w-[75%] max-[768px]:w-full flex-col justify-center items-start gap-2 relative">
        <input
          type="email"
          id="email"
          placeholder={t("E-mail") || "E-mail"}
          required
          className="peer focus:border-white h-full w-full p-4 bg-transparent rounded-md placeholder-transparent outline-none border border-gray-400 text-white transition-all duration-[250ms]"
        />
        <label
          htmlFor="email"
          className="absolute -top-8 left-0 text-white peer-placeholder-shown:text-xl peer-placeholder-shown:top-3 peer-placeholder-shown:left-4 peer-placeholder-shown:text-gray-400 peer-focus:-top-8 peer-focus:left-0 peer-focus:text-[1.20rem] peer-focus:text-white transition-all duration-[250ms] peer-focus:overflow-x-hidden peer-focus:whitespace-nowrap"
        >
          {t("E-mail")}
        </label>
      </div>
      <div
        className="h-auto w-[75%] max-[768px]:w-full flex flex-col justify-center items-start gap-2 relative">
        <input
          type="password"
          id="password"
          placeholder={t("Password") || "Password"}
          required
          className="peer focus:border-white h-full w-full p-4 bg-transparent rounded-md placeholder-transparent outline-none border border-gray-400 text-white transition-all duration-[250ms]"
        />
        <label
          htmlFor="email"
          className="absolute -top-8 left-0 text-white peer-placeholder-shown:text-xl peer-placeholder-shown:top-3 peer-placeholder-shown:left-4 peer-placeholder-shown:text-gray-400 peer-focus:-top-8 peer-focus:left-0 peer-focus:text-[1.20rem] peer-focus:text-white transition-all duration-[250ms] peer-focus:overflow-x-hidden peer-focus:whitespace-nowrap"
        >
          {t("Password")}
        </label>
      </div>
      <div className="flex flex-row w-[75%] max-[768px]:w-full justify-between items-center">
        <a href="/forgot-your-password">
          <p className="text-white text-xl">{t('Forgot your password?')}</p>
        </a>
      </div>
      <div className="w-[75%] max-[768px]:w-full">
        <Button text={t('Sign In')} onClick={() => console.log('teste')}/>
      </div>
    </form>
  )
}