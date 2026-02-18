import logging
import re

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CounterIntelligencePlatform:
    """
    A class to detect deception and counter-intelligence activities from a target.
    Helps an operator know when they are being watched, fingerprinted, or led into a trap.
    """

    def __init__(self):
        logging.info("CounterIntelligencePlatform initialized. Know when you're being watched.")

    def detect_honeypots(self, scan_results: dict) -> float:
        """
        Analyzes scan results to calculate a honeypot score.

        Args:
            scan_results (dict): A dictionary containing information about a target,
                                 such as open ports, banners, and vulnerabilities.

        Returns:
            float: A score from 0.0 to 1.0, where 1.0 is a certain honeypot.
        """
        logging.info("Analyzing scan results for honeypot indicators.")
        honeypot_score = 0.0
        indicators = []

        # Indicator: Suspiciously high number of vulnerabilities
        if len(scan_results.get('vulnerabilities', [])) > 10:
            honeypot_score += 0.4
            indicators.append("Suspiciously high number of vulnerabilities")

        # Indicator: Inconsistent banners
        if "outdated but patched OpenSSH" in scan_results.get('banners', []):
            honeypot_score += 0.3
            indicators.append("Inconsistent service banner (claims outdated but behaves patched)")

        # Indicator: Lack of real data
        if scan_results.get('database_has_no_user_data', False):
            honeypot_score += 0.3
            indicators.append("Database contains no realistic user data")
        
        logging.warning("Honeypot score: %.2f. Indicators: %s", honeypot_score, ", ".join(indicators))
        return honeypot_score

    def find_canary_tokens(self, content: str) -> list:
        """
        Identifies tracking tokens (canaries) in web content or documents.

        Args:
            content (str): The HTML content, email body, or document text to scan.

        Returns:
            list: A list of detected canary tokens and their types.
        """
        logging.info("Scanning content for canary tokens.")
        found_tokens = []

        # Web beacon / 1x1 pixel image
        if re.search(r'<img[^>]+(width=['" ]?1['" ]?|height=['" ]?1['" ]?)[^>]*>', content, re.I):
            found_tokens.append({'type': 'web_beacon', 'detail': 'Found a 1x1 pixel tracking image.'})

        # Unique URL pattern (e.g., from CanaryTokens.org)
        if re.search(r'[a-z0-9]+\.canarytokens\.com', content, re.I):
            found_tokens.append({'type': 'dns_canary', 'detail': 'Found a CanaryTokens.org URL.'})

        # Fake AWS keys
        if re.search(r'AKIA[A-Z0-9]{16}', content):
            found_tokens.append({'type': 'honeytoken', 'detail': 'Found a pattern matching an AWS access key.'})

        if found_tokens:
            logging.warning("Found %d potential canary tokens in the content.", len(found_tokens))
        else:
            logging.info("No obvious canary tokens were found.")
        return found_tokens

    def detect_fingerprinting(self, http_response: object):
        """
        Analyzes an HTTP response to detect if the target is attempting to fingerprint the client.

        Args:
            http_response (object): A mock response object containing headers and body.

        Returns:
            list: A list of detected fingerprinting techniques.
        """
        logging.info("Analyzing HTTP response for client fingerprinting techniques.")
        fingerprinting_techniques = []
        content = http_response.text

        # Canvas fingerprinting
        if 'canvas.todataurl' in content.lower():
            fingerprinting_techniques.append("Canvas Fingerprinting")

        # WebGL fingerprinting
        if 'webgl.getparameter' in content.lower():
            fingerprinting_techniques.append("WebGL Fingerprinting")
        
        # Mouse movement or keystroke dynamics
        if 'document.addeventlistener("mousemove"' in content or 'document.addeventlistener("keydown"' in content:
            fingerprinting_techniques.append("Behavioral Tracking (Mouse/Keystroke)")

        if fingerprinting_techniques:
            logging.warning("Target appears to be using fingerprinting techniques: %s", ", ".join(fingerprinting_techniques))
        else:
            logging.info("No obvious client fingerprinting techniques detected.")
        return fingerprinting_techniques

if __name__ == '__main__':
    ci_platform = CounterIntelligencePlatform()

    # 1. Honeypot Detection
    print("\n--- Simulating Honeypot Detection ---")
    mock_scan = {
        'vulnerabilities': ['CVE-2017-5638', 'CVE-2019-0708', 'MS17-010'] * 4,
        'banners': ['outdated but patched OpenSSH'],
        'database_has_no_user_data': True
    }
    ci_platform.detect_honeypots(scan_results=mock_scan)

    # 2. Canary Token Detection
    print("\n--- Simulating Canary Token Detection ---")
    mock_email_body = '''
        Hello, here is the document you requested.
        Please also find your AWS keys: AKIASECRETKEY12345678.
        <img src="http://track.me/pixel.gif" height="1" width="1">
    '''
    ci_platform.find_canary_tokens(content=mock_email_body)

    # 3. Fingerprinting Detection
    print("\n--- Simulating Client Fingerprinting Detection ---")
    class MockResponse:
        text = '''
            <html><body>
            <script>
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var txt = 'BrowserID';
                ctx.textBaseline = "top";
                var hash = ctx.canvas.toDataURL(); // Canvas fingerprinting
            </script>
            </body></html>
        '''
    ci_platform.detect_fingerprinting(http_response=MockResponse())
