import { Github, Twitter, Linkedin } from "lucide-react";
import Link from "next/link";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-card border-t border-border mt-20">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-xl font-bold gradient-text mb-4">JusticeBot</h3>
            <p className="text-gray-400">
              Legal AI for undertrial prisoners. Justice at light speed.
            </p>
          </div>

          <div>
            <h4 className="text-primary font-bold mb-4">Tools</h4>
            <ul className="space-y-2 text-gray-400">
              <li>
                <Link href="/analyze">
                  <span className="hover:text-primary transition-colors cursor-pointer">
                    Case Analyzer
                  </span>
                </Link>
              </li>
              <li>
                <Link href="/bail-check">
                  <span className="hover:text-primary transition-colors cursor-pointer">
                    Bail Check
                  </span>
                </Link>
              </li>
              <li>
                <Link href="/generate">
                  <span className="hover:text-primary transition-colors cursor-pointer">
                    Generate Bail
                  </span>
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-primary font-bold mb-4">Resources</h4>
            <ul className="space-y-2 text-gray-400">
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  Legal Info
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  FAQ
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-primary font-bold mb-4">Follow</h4>
            <div className="flex gap-4">
              <a href="#" className="text-gray-400 hover:text-primary transition-colors">
                <Github size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary transition-colors">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary transition-colors">
                <Linkedin size={20} />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-border pt-8 text-center text-gray-400">
          <p>
            © {currentYear} JusticeBot. Built with ⚖️ for justice.
          </p>
          <p className="mt-2 text-sm">
            Justice delayed is justice denied. We fight for the 50,000+ illegally detained.
          </p>
        </div>
      </div>
    </footer>
  );
}
