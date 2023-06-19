// components/Navbar.tsx
import React from "react";
import Link from "next/link";
import Image from "next/image";

const Navbar = () => {
  return (
    <nav className="justify-between items-center w-full mb-6 sm:mb-12 2xl:mb-16 pt-3">
      <div className="flex items-center justify-between px-4">
        <div className="flex items-center">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <Image
              src="/assets/images/logo.svg"
              alt="logo"
              width={30}
              height={30}
              className="object-contain"
            />
            <p className="logo_text">convinced</p>
          </Link>
        </div>
          <ul className="flex ml-auto gap-3 md:gap-5">
            <li className="logo_text">
              <Link href="/">Messenger</Link>
            </li>
            <li className="logo_text">
              <Link href="/review">Alien</Link>
            </li>
          </ul>
        </div>
    </nav>
  );
};

export default Navbar;
