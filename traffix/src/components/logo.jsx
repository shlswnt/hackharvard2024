'use client';

import Image from "next/image";

import { useTheme } from "next-themes";

export function Logo() {
  const { resolvedTheme } = useTheme();
  
  return (
    <Image
      src={resolvedTheme === "dark" ? "/logo-light.svg" : "/logo-dark.svg"}
      alt="logo"
      width={32}
      height={32}
    />
  );
}
