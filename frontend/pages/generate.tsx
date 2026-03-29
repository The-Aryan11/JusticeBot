import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Generate() {
  return (
    <div className="min-h-screen bg-gradient-dark">
      <Header apiStatus="healthy" onRefresh={() => {}} />
      <main className="max-w-4xl mx-auto px-4 py-32">
        <h1 className="text-5xl font-bold gradient-text mb-8">Bail Application Generator</h1>
        <div className="card glass">
          <p className="text-gray-400">Coming Soon</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
