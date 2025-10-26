import re
import math
from urllib.parse import urlparse, unquote, parse_qs
from typing import Dict, List, Tuple
from collections import Counter

class URLDetector:
    """Simplified URL Pattern Detector for Web API"""

    def __init__(self):
        # Whitelists
        self.whitelist_ips = [
            r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            r"^192\.168\.\d{1,3}\.\d{1,3}",
            r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            r"^172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}",
        ]

        self.whitelist_ports = [80, 443, 8080, 8443, 8000, 8888, 3000, 3001, 5000, 5001, 4200, 4000, 9000, 9090, 8096, 32400, 8123]

        self.trusted_redirect_domains = [
            'google.com', 'youtube.com', 'amazon.com', 'microsoft.com',
            'apple.com', 'linkedin.com', 'twitter.com', 'facebook.com',
            'github.com', 'stackoverflow.com', 'reddit.com', 'wikipedia.org',
            'spotify.com', 'netflix.com', 'ebay.com', 'paypal.com'
        ]

        # All attack patterns
        self.sql_patterns = [
            (r"'\s*(or|and)\s+['\"]*\w+['\"]*\s*=\s*['\"]*\w+", "SQL comparison logic", "critical"),
            (r"'\s*(or|and)\s*'\s*=\s*'", "'OR'=' pattern", "critical"),
            (r"'\s*(or|and)\s+\d+\s*=\s*\d+", "'OR 1=1 pattern", "critical"),
            (r'"\s*(or|and)\s+"', 'Double-quote SQL', "critical"),
            (r"--\s*$", "SQL comment (--)", "critical"),
            (r"#\s*$", "MySQL comment (#)", "critical"),
            (r"/\*.*?\*/", "SQL block comment", "high"),
            (r"\b(union)\s+(select|all)\b", "UNION SELECT", "critical"),
            (r";\s*(select|insert|update|delete|drop)", "Stacked query", "critical"),
            (r"\b(select)\s+[\w\*,\s]{1,50}\s+from\b", "SELECT FROM", "critical"),
            (r"\b(insert)\s+into\s+\w+", "INSERT INTO", "critical"),
            (r"\b(delete)\s+from\s+\w+", "DELETE FROM", "critical"),
            (r"\b(drop)\s+(table|database)", "DROP TABLE", "critical"),
            (r"\binformation_schema\.", "Schema enumeration", "high"),
            (r"0x[0-9a-fA-F]{4,}", "Hex injection", "medium"),
            (r"%27\s*(or|and|union|select)", "URL-encoded SQL", "high"),
        ]

        self.xss_patterns = [
            (r"<script[\s>]", "Script tag", "critical"),
            (r"javascript:\s*[\w\(\[]", "JavaScript protocol", "critical"),
            (r"on(load|error|click)\s*=\s*[\"'][^\"']*(?:alert|eval)", "Event handler XSS", "critical"),
            (r"<iframe[^>]*src", "Iframe tag", "high"),
            (r"<img[^>]+onerror\s*=", "Img onerror", "critical"),
            (r"\b(alert|confirm|prompt)\s*\(", "Popup function", "high"),
            (r"document\.(cookie|write)", "Document manipulation", "critical"),
            (r"eval\s*\([^)]{3,}\)", "Eval function", "critical"),
        ]

        self.path_patterns = [
            (r"\.\./\.\./", "Directory traversal", "critical"),
            (r"%2e%2e[/\\]", "Encoded traversal", "high"),
            (r"(etc/passwd|etc/shadow)", "System file access", "critical"),
            (r"(windows/system32|winnt/system32)", "Windows system", "critical"),
        ]

        self.cmd_patterns = [
            (r"[;&]\s*(cat|ls|rm|wget|curl|chmod)", "Command separator", "critical"),
            (r"\|\s*(whoami|id|uname|pwd)", "Pipe with command", "critical"),
            (r"\$\((cat|ls|whoami|pwd)[^\)]*\)", "Command substitution", "critical"),
            (r"/bin/(bash|sh)", "Shell path", "critical"),
        ]

        self.advanced_patterns = [
            (r"<!ENTITY\s+\w+\s+SYSTEM", "XXE injection", "critical"),
            (r"(callback|webhook)\s*=\s*https?://", "SSRF attempt", "high"),
            (r"__proto__", "Prototype pollution", "critical"),
            (r"%0d%0a", "CRLF injection", "critical"),
            (r"\$\s*(eq|ne|gt|in|or|and)", "NoSQL injection", "high"),
            (r"\{\{[^\}]+\}\}", "Template injection", "high"),
        ]

    def decode_url(self, url: str) -> str:
        decoded = url
        for _ in range(3):
            try:
                new_decoded = unquote(decoded)
                if new_decoded == decoded:
                    break
                decoded = new_decoded
            except:
                break
        return decoded

    def is_whitelisted_ip(self, ip: str) -> bool:
        for pattern in self.whitelist_ips:
            if re.match(pattern, ip):
                return True
        return False

    def is_trusted_domain(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        for trusted in self.trusted_redirect_domains:
            if trusted in domain:
                return True
        return False

    def _calculate_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        counter = Counter(text)
        length = len(text)
        entropy = -sum((count/length) * math.log2(count/length) for count in counter.values())
        return round(entropy, 2)

    def _check_patterns(self, url: str, patterns: List[Tuple]) -> Tuple[bool, List[Dict], int]:
        decoded = self.decode_url(url).lower()
        matches = []
        total_score = 0

        for pattern, description, severity in patterns:
            found = re.findall(pattern, decoded, re.IGNORECASE)
            if found:
                score = {'critical': 20, 'high': 15, 'medium': 10, 'low': 5}[severity]
                matches.append({
                    'description': description,
                    'severity': severity,
                    'score': score,
                    'evidence': str(found[0])[:50] if found else ''
                })
                total_score += score

        return len(matches) > 0, matches, total_score

    def analyze_url(self, url: str) -> Dict:
        """Main analysis function - Returns JSON-ready result"""
        
        # Extract features
        decoded = self.decode_url(url)
        parsed = urlparse(url)
        
        reasons = []
        total_risk_score = 0
        threats_detected = []

        # Check all patterns
        sql_detected, sql_matches, sql_score = self._check_patterns(url, self.sql_patterns)
        xss_detected, xss_matches, xss_score = self._check_patterns(url, self.xss_patterns)
        path_detected, path_matches, path_score = self._check_patterns(url, self.path_patterns)
        cmd_detected, cmd_matches, cmd_score = self._check_patterns(url, self.cmd_patterns)
        adv_detected, adv_matches, adv_score = self._check_patterns(url, self.advanced_patterns)

        # Process SQL Injection
        if sql_detected:
            threats_detected.append("SQL_INJECTION")
            total_risk_score += min(sql_score, 35)
            for match in sql_matches:
                reasons.append({
                    'category': 'SQL Injection',
                    'severity': match['severity'],
                    'description': match['description'],
                    'evidence': match['evidence']
                })

        # Process XSS
        if xss_detected:
            threats_detected.append("XSS")
            total_risk_score += min(xss_score, 35)
            for match in xss_matches:
                reasons.append({
                    'category': 'XSS Attack',
                    'severity': match['severity'],
                    'description': match['description'],
                    'evidence': match['evidence']
                })

        # Process Path Traversal
        if path_detected:
            threats_detected.append("PATH_TRAVERSAL")
            total_risk_score += min(path_score, 25)
            for match in path_matches:
                reasons.append({
                    'category': 'Path Traversal',
                    'severity': match['severity'],
                    'description': match['description'],
                    'evidence': match['evidence']
                })

        # Process Command Injection
        if cmd_detected:
            threats_detected.append("COMMAND_INJECTION")
            total_risk_score += min(cmd_score, 30)
            for match in cmd_matches:
                reasons.append({
                    'category': 'Command Injection',
                    'severity': match['severity'],
                    'description': match['description'],
                    'evidence': match['evidence']
                })

        # Process Advanced Attacks
        if adv_detected:
            threats_detected.append("ADVANCED_ATTACK")
            total_risk_score += min(adv_score, 30)
            for match in adv_matches:
                reasons.append({
                    'category': 'Advanced Attack',
                    'severity': match['severity'],
                    'description': match['description'],
                    'evidence': match['evidence']
                })

        # Feature-based scoring
        encoding_layers = url.count('%') // 2
        if encoding_layers > 1:
            total_risk_score += min(encoding_layers * 5, 15)
            reasons.append({
                'category': 'Suspicious Pattern',
                'severity': 'medium',
                'description': f'Multiple URL encoding layers ({encoding_layers}x)',
                'evidence': 'Obfuscation attempt'
            })

        # IP address check
        ip_match = re.search(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", parsed.netloc)
        if ip_match and not self.is_whitelisted_ip(ip_match.group(1)):
            total_risk_score += 10
            reasons.append({
                'category': 'Suspicious Pattern',
                'severity': 'medium',
                'description': 'IP address instead of domain',
                'evidence': ip_match.group(1)
            })

        # Entropy check
        entropy = self._calculate_entropy(url)
        if entropy > 5.0:
            total_risk_score += 5
            reasons.append({
                'category': 'Suspicious Pattern',
                'severity': 'low',
                'description': f'High randomness (entropy: {entropy})',
                'evidence': 'Possibly obfuscated'
            })

        # Cap at 100
        total_risk_score = min(total_risk_score, 100)

        # Determine verdict
        if total_risk_score >= 70:
            verdict = "MALICIOUS"
            verdict_color = "red"
        elif total_risk_score >= 40:
            verdict = "SUSPICIOUS"
            verdict_color = "orange"
        elif total_risk_score >= 15:
            verdict = "WARNING"
            verdict_color = "yellow"
        elif total_risk_score > 0:
            verdict = "LOW RISK"
            verdict_color = "blue"
        else:
            verdict = "CLEAN"
            verdict_color = "green"

        return {
            "success": True,
            "url": url,
            "decoded_url": decoded,
            "verdict": verdict,
            "verdict_color": verdict_color,
            "risk_score": total_risk_score,
            "threats_detected": threats_detected,
            "reasons": reasons,
            "metadata": {
                "url_length": len(url),
                "encoding_layers": encoding_layers,
                "entropy": entropy,
                "is_https": parsed.scheme == 'https',
                "has_ip": bool(ip_match),
                "domain": parsed.netloc
            }
        }