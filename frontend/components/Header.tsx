import Link from "next/link";
import { motion } from "framer-motion";
import { Menu, X } from "lucide-react";
import { useState } from "react";

interface HeaderProps {
  apiStatus: "healthy" | "down" | "checking";
  onRefresh: () => void;
}

export default function Header({ apiStatus, onRefresh }: HeaderProps) {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { href: "/analyze", label: "Analyzer" },
    { href: "/bail-check", label: "Bail Check" },
    { href: "/generate", label: "Generate" },
    { href: "/search", label: "Search" },
  ];

  return (
    <motion.header
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-border"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/">
          <div className="text-3xl font-bold gradient-text cursor-pointer hover:scale-110 transition-transform">
            ⚖️ JusticeBot
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex gap-8 items-center">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href}>
              <span className="text-gray-300 hover:text-primary transition-colors cursor-pointer">
                {link.label}
              </span>
            </Link>
          ))}

          <button
            onClick={onRefresh}
            className={`px-3 py-1 rounded-full text-sm ${
              apiStatus === "healthy"
                ? "bg-green-500 bg-opacity-20 text-green-300"
                : "bg-red-500 bg-opacity-20 text-red-300"
            }`}
          >
            {apiStatus === "healthy" ? "🟢 Live" : "🔴 Offline"}
          </button>
        </nav>

        {/* Mobile Menu */}
        <button
          className="md:hidden"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        {isOpen && (
          <motion.div
            className="absolute top-full left-0 right-0 bg-card border-b border-border p-4 flex flex-col gap-4"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href}>
                <span className="text-gray-300 hover:text-primary transition-colors">
                  {link.label}
                </span>
              </Link>
            ))}
          </motion.div>
        )}
      </div>
    </motion.header>
  );
}
