from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import URLDetector
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize detector
detector = URLDetector()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "URL Detector API",
        "version": "1.0"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """Main endpoint to analyze URL"""
    try:
        # Get URL from request
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400
        
        url = data['url'].strip()
        
        if not url:
            return jsonify({
                "success": False,
                "error": "URL cannot be empty"
            }), 400
        
        # Basic URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url  # Add https if missing
        
        # Analyze URL
        result = detector.analyze_url(url)
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "An error occurred while analyzing the URL",
            "details": str(e)
        }), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple URLs at once"""
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                "success": False,
                "error": "URLs array is required"
            }), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list):
            return jsonify({
                "success": False,
                "error": "URLs must be an array"
            }), 400
        
        results = []
        for url in urls:
            try:
                if not (url.startswith('http://') or url.startswith('https://')):
                    url = 'https://' + url
                result = detector.analyze_url(url)
                results.append(result)
            except Exception as e:
                results.append({
                    "success": False,
                    "url": url,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "results": results,
            "total": len(results)
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 URL Detector API Starting...")
    print("📡 Server running on http://localhost:5001")
    print("🔗 Frontend should connect to: http://localhost:5001/api/analyze")
    app.run(debug=True, host='0.0.0.0', port=5001)