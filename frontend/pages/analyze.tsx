import { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { Send, Copy } from "lucide-react";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Analyze() {
  const [caseText, setCaseText] = useState("");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!caseText.trim()) {
      toast.error("Please enter case details");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/analyze-case`,
        {
          case_text: caseText,
          detention_days: 0,
          max_sentence_days: 0,
          chargesheet_filed: false,
        }
      );

      if (response.data.success) {
        setAnalysis(response.data);
        toast.success("Case analyzed successfully!");
      }
    } catch (error) {
      toast.error("Error analyzing case");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-dark">
      <Header apiStatus="healthy" onRefresh={() => {}} />
      <Toaster position="top-right" />

      <main className="max-w-4xl mx-auto px-4 py-32">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-5xl font-bold gradient-text mb-8">Case Analyzer</h1>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="card glass">
              <textarea
                value={caseText}
                onChange={(e) => setCaseText(e.target.value)}
                placeholder="Enter case details..."
                className="w-full h-64 bg-darker rounded-lg p-4 text-white border border-border focus:border-primary focus:outline-none"
              />
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="btn-primary w-full mt-6 flex items-center justify-center gap-2"
              >
                <Send size={20} />
                {loading ? "Analyzing..." : "Analyze Case"}
              </button>
            </div>

            <div className="card glass">
              {!analysis ? (
                <p className="text-gray-400 text-center py-20">Results appear here</p>
              ) : (
                <div>
                  <pre className="bg-darker text-gray-300 p-4 rounded-lg overflow-auto max-h-64 text-sm">
                    {JSON.stringify(analysis, null, 2)}
                  </pre>
                  <button className="btn-secondary w-full mt-4 flex items-center justify-center gap-2">
                    <Copy size={18} />
                    Copy
                  </button>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}
