import logging
import requests

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LOTLIntelligence:
    """
    Performs "Living-Off-The-Land" (LOTL) reconnaissance using the target's own infrastructure.
    This allows for stealthy information gathering that is less likely to be detected by
    traditional security monitoring.
    """

    def __init__(self, target_url: str):
        """
        Initializes the LOTL Intelligence engine.

        Args:
            target_url (str): The base URL of the target.
        """
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        logging.info("LOTLIntelligence initialized for target: %s", target_url)

    def abuse_error_pages(self, paths: list):
        """
        Probes known or discovered paths to trigger and analyze error pages for leaked information.
        This is a mock implementation.

        Args:
            paths (list): A list of paths to test (e.g., ['/admin', '/debug/info']).

        Returns:
            dict: A dictionary of information leaked from error pages.
        """
        logging.info("Probing %d paths for information leakage via error pages.", len(paths))
        leaked_info = {}
        # Mock response for a specific path
        if '/nonexistent-path-for-debug' in paths:
            logging.info("Simulating a Django debug error page at '/nonexistent-path-for-debug'.")
            leaked_info['framework'] = 'Django 3.2.1'
            leaked_info['file_path'] = '/var/www/app/views.py'
            leaked_info['database'] = 'PostgreSQL'
            leaked_info['stack_trace'] = '[Mock Stack Trace Details...]'
            logging.info("Leaked info found: %s", leaked_info)
        else:
            logging.warning("No simulated error pages were triggered.")
        return leaked_info

    def leverage_ssrf_for_internal_scan(self, ssrf_endpoint: str):
        """
        Uses a known SSRF vulnerability to scan the internal network.
        This is a mock implementation.

        Args:
            ssrf_endpoint (str): The vulnerable endpoint URL that can be used for SSRF.

        Returns:
            dict: A dictionary of discovered internal services.
        """
        logging.info("Leveraging SSRF at %s to scan the internal network.", ssrf_endpoint)
        discovered_services = {}
        internal_ips_to_scan = ["10.0.0.5", "169.254.169.254"] # Mock IPs to test

        for ip in internal_ips_to_scan:
            # In a real scenario, you would construct a URL like: {ssrf_endpoint}?url=http://{ip}/
            logging.info("Simulating SSRF request to internal IP: %s", ip)
            if ip == "10.0.0.5":
                discovered_services[ip] = {'service': 'internal-api', 'port': 8080, 'status': 'open'}
                logging.info("Discovered internal service: %s", discovered_services[ip])
            elif ip == "169.254.169.254":
                discovered_services[ip] = {'service': 'aws-metadata', 'status': 'accessible', 'leaked_data': '[Mock AWS IAM Role]'}
                logging.info("Accessed cloud metadata endpoint: %s", discovered_services[ip])
        
        return discovered_services

    def abuse_webhooks_for_recon(self, webhook_registration_url: str, internal_target: str):
        """
        Abuses a webhook registration feature to make the target scan itself.
        This is a mock implementation.

        Args:
            webhook_registration_url (str): The URL where a new webhook can be registered.
            internal_target (str): The internal URL the webhook should point to.

        Returns:
            dict: Information leaked from the webhook response (e.g., timing, error message).
        """
        logging.info("Abusing webhooks to probe internal target: %s", internal_target)
        
        # 1. Register webhook pointing to an internal service
        logging.info("Simulating registration of a webhook at %s pointing to %s.", webhook_registration_url, internal_target)
        
        # 2. Trigger the webhook
        logging.info("Simulating an event that triggers the webhook.")

        # 3. Analyze the (mock) response
        logging.info("Analyzing the response from the webhook trigger.")
        leaked_info = {
            'timing_ms': 150, # A longer time might indicate a valid internal service
            'error_message': 'Connection refused', # This can confirm if a port is closed
            'status': 'Inferred port is closed on the internal target.'
        }
        logging.info("Leaked info from webhook abuse: %s", leaked_info)
        return leaked_info

if __name__ == '__main__':
    target = "http://example.com"
    lotl = LOTLIntelligence(target_url=target)

    # 1. Abuse Error Pages
    print("\n--- Abusing Error Pages ---")
    lotl.abuse_error_pages(paths=['/nonexistent-path-for-debug'])

    # 2. Leverage SSRF
    print("\n--- Leveraging SSRF for Internal Scan ---")
    ssrf_vuln_url = f"{target}/load_image_from_url"
    lotl.leverage_ssrf_for_internal_scan(ssrf_endpoint=ssrf_vuln_url)

    # 3. Abuse Webhooks
    print("\n--- Abusing Webhooks for Recon ---")
    webhook_url = f"{target}/api/v1/webhooks"
    lotl.abuse_webhooks_for_recon(webhook_registration_url=webhook_url, internal_target="http://10.0.0.10:9200")
