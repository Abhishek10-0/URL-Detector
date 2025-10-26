import React, { useState } from 'react';
import { AlertCircle, Shield, CheckCircle, XCircle, Loader } from 'lucide-react';

const URLScanner = () => {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeURL = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5001/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure backend is running on port 5000');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getVerdictStyle = (verdict) => {
    const styles = {
      CLEAN: 'bg-green-100 text-green-800 border-green-300',
      'LOW RISK': 'bg-blue-100 text-blue-800 border-blue-300',
      WARNING: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      SUSPICIOUS: 'bg-orange-100 text-orange-800 border-orange-300',
      MALICIOUS: 'bg-red-100 text-red-800 border-red-300',
    };
    return styles[verdict] || styles.WARNING;
  };

  const getVerdictIcon = (verdict) => {
    if (verdict === 'CLEAN') return <CheckCircle className="w-8 h-8" />;
    if (verdict === 'MALICIOUS') return <XCircle className="w-8 h-8" />;
    return <AlertCircle className="w-8 h-8" />;
  };

  const getSeverityBadge = (severity) => {
    const styles = {
      critical: 'bg-red-600 text-white',
      high: 'bg-orange-600 text-white',
      medium: 'bg-yellow-600 text-white',
      low: 'bg-blue-600 text-white',
    };
    return styles[severity] || styles.medium;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <Shield className="w-16 h-16 text-purple-400" />
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">
            URL Security Scanner
          </h1>
          <p className="text-gray-300 text-lg">
            Detect malicious patterns in URLs • SQL Injection • XSS • Command Injection & More
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
          <div className="space-y-4">
            <label className="block text-sm font-semibold text-gray-700">
              Enter URL to Analyze
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && analyzeURL()}
                placeholder="https://example.com/page?id=123"
                className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition"
              />
              <button
                onClick={analyzeURL}
                disabled={loading}
                className="px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    Scanning...
                  </>
                ) : (
                  'Analyze'
                )}
              </button>
            </div>
            {error && (
              <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Verdict Card */}
            <div className={`rounded-2xl shadow-xl p-8 border-2 ${getVerdictStyle(result.verdict)}`}>
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  {getVerdictIcon(result.verdict)}
                  <div>
                    <h2 className="text-3xl font-bold">{result.verdict}</h2>
                    <p className="text-sm opacity-80 mt-1">Security Assessment</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-4xl font-bold">{result.risk_score}</div>
                  <div className="text-sm opacity-80">/ 100 Risk Score</div>
                </div>
              </div>

              {/* URL Info */}
              <div className="bg-white bg-opacity-50 rounded-lg p-4 mt-4">
                <p className="text-sm font-semibold mb-1">Analyzed URL:</p>
                <p className="text-xs break-all font-mono">{result.url}</p>
              </div>
            </div>

            {/* Threats Detected */}
            {result.threats_detected && result.threats_detected.length > 0 && (
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <AlertCircle className="w-6 h-6 text-red-600" />
                  Threats Detected ({result.threats_detected.length})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.threats_detected.map((threat, idx) => (
                    <span
                      key={idx}
                      className="px-4 py-2 bg-red-100 text-red-800 rounded-full text-sm font-semibold"
                    >
                      {threat.replace(/_/g, ' ')}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Detailed Findings */}
            {result.reasons && result.reasons.length > 0 && (
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <h3 className="text-2xl font-bold text-gray-800 mb-6">
                  Detailed Findings ({result.reasons.length})
                </h3>
                <div className="space-y-4">
                  {result.reasons.map((reason, idx) => (
                    <div
                      key={idx}
                      className="border-l-4 border-purple-500 bg-gray-50 p-4 rounded-r-lg"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <span className="font-semibold text-gray-800">
                            {reason.category}
                          </span>
                          <span className={`ml-3 px-2 py-1 rounded text-xs font-semibold ${getSeverityBadge(reason.severity)}`}>
                            {reason.severity.toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <p className="text-gray-700 mb-2">{reason.description}</p>
                      {reason.evidence && (
                        <div className="bg-gray-100 p-2 rounded text-xs font-mono text-gray-600 mt-2">
                          Evidence: {reason.evidence}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Metadata */}
            {result.metadata && (
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <h3 className="text-2xl font-bold text-gray-800 mb-4">URL Metadata</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 mb-1">Length</p>
                    <p className="text-lg font-semibold">{result.metadata.url_length}</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 mb-1">Encoding Layers</p>
                    <p className="text-lg font-semibold">{result.metadata.encoding_layers}</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 mb-1">Entropy</p>
                    <p className="text-lg font-semibold">{result.metadata.entropy}</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 mb-1">Protocol</p>
                    <p className="text-lg font-semibold">{result.metadata.is_https ? 'HTTPS ✓' : 'HTTP ⚠️'}</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 mb-1">Domain</p>
                    <p className="text-sm font-semibold break-all">{result.metadata.domain}</p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-xs text-gray-600 mb-1">Has IP</p>
                    <p className="text-lg font-semibold">{result.metadata.has_ip ? 'Yes ⚠️' : 'No ✓'}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-400 text-sm">
          <p>Powered by Advanced Pattern Detection Engine v3.0</p>
          <p className="mt-2">Detects SQL Injection, XSS, Command Injection, Path Traversal & More</p>
        </div>
      </div>
    </div>
  );
};

export default URLScanner;