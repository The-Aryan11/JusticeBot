import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Shield,
  Zap,
  BarChart3,
  Users,
  Lock,
  Lightbulb,
} from "lucide-react";
import toast, { Toaster } from "react-hot-toast";
import axios from "axios";
import Header from "../components/Header";
import Footer from "../components/Footer";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
      delayChildren: 0.3,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.8,
      ease: "easeOut",
    }
  },
};

export default function Home() {
  const [apiStatus, setApiStatus] = useState<"healthy" | "down" | "checking">("checking");

  useEffect(() => {
    checkAPIHealth();
  }, []);

  const checkAPIHealth = async () => {
    try {
      setApiStatus("checking");
      await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/health`, {
        timeout: 5000,
      });
      setApiStatus("healthy");
      toast.success("Backend connected!", { duration: 2000 });
    } catch (error) {
      setApiStatus("down");
      toast.error("Backend unreachable", { duration: 2000 });
    }
  };

  const features = [
    {
      icon: Shield,
      title: "Case Analyzer",
      description: "Extract case details using AI",
      color: "from-primary to-secondary",
      href: "/analyze",
    },
    {
      icon: Zap,
      title: "Bail Eligibility",
      description: "Check bail under all sections",
      color: "from-primary to-secondary",
      href: "/bail-check",
    },
    {
      icon: BarChart3,
      title: "Bail Application",
      description: "Generate court documents",
      color: "from-primary to-secondary",
      href: "/generate",
    },
    {
      icon: Lock,
      title: "Precedent Search",
      description: "Find relevant SC cases",
      color: "from-primary to-secondary",
      href: "/search",
    },
    {
      icon: Lightbulb,
      title: "Analytics",
      description: "Success predictions",
      color: "from-primary to-secondary",
      href: "/analytics",
    },
    {
      icon: Users,
      title: "Bias Detection",
      description: "Identify discrimination",
      color: "from-primary to-secondary",
      href: "/bias",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-dark">
      <Header apiStatus={apiStatus} onRefresh={checkAPIHealth} />
      <Toaster position="top-right" />

      {/* Hero Section */}
      <motion.section
        className="relative min-h-screen flex items-center justify-center px-4 py-20 overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        {/* Background elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary opacity-10 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-primary opacity-5 rounded-full blur-3xl" />

        <div className="relative z-10 max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-6xl md:text-7xl font-bold mb-6 gradient-text">
              Justice Bot
            </h1>
          </motion.div>

          <motion.p
            className="text-2xl md:text-3xl text-gray-300 mb-8"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            Legal AI for Undertrial Prisoners
          </motion.p>

          <motion.p
            className="text-lg text-gray-400 max-w-2xl mx-auto mb-12"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            Justice delayed is justice denied. JusticeBot fights back by identifying illegally detained prisoners and generating bail applications.
          </motion.p>

          <motion.div
            className="flex flex-wrap gap-4 justify-center"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            <Link href="/analyze">
              <button className="btn-primary flex items-center gap-2 group">
                Start Analysis
                <ArrowRight className="group-hover:translate-x-1 transition-transform" />
              </button>
            </Link>
            <button
              onClick={checkAPIHealth}
              className="btn-secondary flex items-center gap-2"
            >
              <div
                className={`w-3 h-3 rounded-full ${
                  apiStatus === "healthy" ? "bg-green-400" : "bg-red-400"
                }`}
              />
              {apiStatus === "healthy" ? "🟢 Connected" : "🔴 Offline"}
            </button>
          </motion.div>
        </div>
      </motion.section>

      {/* Stats Section */}
      <motion.section
        className="py-20 px-4"
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
      >
        <div className="max-w-6xl mx-auto">
          <motion.h2
            variants={item}
            className="text-4xl font-bold text-center mb-16 gradient-text"
          >
            Impact by Numbers
          </motion.h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { label: "Undertrial Prisoners", value: "4,00,000+" },
              { label: "Illegally Detained", value: "50,000+" },
              { label: "Analysis Time", value: "5 min" },
              { label: "100% Free", value: "₹0" },
            ].map((stat, idx) => (
              <motion.div key={idx} variants={item} className="card glass text-center hover:glow">
                <div className="text-4xl font-bold gradient-text mb-2">{stat.value}</div>
                <div className="text-gray-400 text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        className="py-20 px-4"
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
      >
        <div className="max-w-6xl mx-auto">
          <motion.h2
            variants={item}
            className="text-4xl font-bold text-center mb-16 gradient-text"
          >
            Powerful Features
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <motion.div key={idx} variants={item}>
                  <Link href={feature.href}>
                    <div className="card glass h-full hover:glow cursor-pointer group">
                      <div
                        className={`bg-gradient-to-br ${feature.color} p-3 w-fit rounded-lg mb-4 group-hover:scale-110 transition-transform`}
                      >
                        <Icon className="text-white" size={24} />
                      </div>
                      <h3 className="text-xl font-bold text-primary mb-2">
                        {feature.title}
                      </h3>
                      <p className="text-gray-400">{feature.description}</p>
                    </div>
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        className="py-20 px-4"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
      >
        <div className="max-w-4xl mx-auto card glass text-center glow">
          <h2 className="text-4xl font-bold mb-6 gradient-text">
            Help Free 50,000+ Prisoners
          </h2>
          <p className="text-gray-300 mb-8 text-lg">
            Every illegal detention is a violation of constitutional rights. JusticeBot makes justice faster.
          </p>
          <Link href="/analyze">
            <button className="btn-primary text-lg px-8 py-3">
              Start Now - It's Free
            </button>
          </Link>
        </div>
      </motion.section>

      <Footer />
    </div>
  );
}
