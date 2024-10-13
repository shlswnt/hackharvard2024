"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { DashboardIcon } from "@radix-ui/react-icons";
import { cn } from "@/lib/utils";

export function MainNav() {
  const pathname = usePathname();

  const navItems = [{ name: "Home", href: "/", icon: DashboardIcon }];

  return (
    <nav className="flex flex-col items-center space-y-4">
      {navItems.map((item) => {
        const isActive = pathname === item.href;
        return (
          <Link
            key={item.name}
            href={item.href}
            className={cn(
              "relative flex items-center p-2 rounded-md transition-colors duration-200 w-full",
              isActive
                ? "bg-secondary text-secondary-foreground"
                : "text-secondary-foreground hover:bg-muted"
            )}
          >
            {/* {isActive && (
              <div className="absolute left-[-12px] top-0 h-full w-1 bg-black rounded-tr-md rounded-br-md"></div>
            )} */}
            <item.icon className="w-6 h-6" />
          </Link>
        );
      })}
    </nav>
  );
}
