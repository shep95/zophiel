import logging
import requests

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpSecManager:
    """
    Manages operational security for the Zohar Toolkit, including anonymized connections.
    When Ghost Mode is enabled, all network traffic from the toolkit's modules
    should be routed through the session object provided by this manager.
    """

    def __init__(self, ghost_mode_enabled: bool = False):
        """
        Initializes the OpSecManager.

        Args:
            ghost_mode_enabled (bool): If True, enables Ghost Mode, which routes traffic through Tor.
        """
        self.ghost_mode_enabled = ghost_mode_enabled
        self.session = requests.Session()

        if self.ghost_mode_enabled:
            logging.warning("GHOST MODE ENABLED. All traffic will be routed through the Tor network.")
            logging.info("Tor proxy must be running on socks5://127.0.0.1:9050 for Ghost Mode to work.")
            # Configure the session to use the default Tor SOCKS proxy
            self.session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
        else:
            logging.info("Ghost Mode is disabled. Traffic will be sent directly.")

    def get_session(self) -> requests.Session:
        """
        Returns the configured requests session object.
        Modules should use this session for all HTTP/HTTPS requests to respect Ghost Mode.

        Returns:
            requests.Session: The session object, configured for Tor if Ghost Mode is active.
        """
        return self.session

    def check_anonymity(self) -> dict:
        """
        Checks the current public IP address to verify anonymity.
        Uses the managed session, so the check itself is performed over Tor if enabled.

        Returns:
            dict: A dictionary containing the IP address and other location details.
        """
        try:
            logging.info("Checking current public IP address...")
            response = self.session.get("https://ipinfo.io/json", timeout=10)
            response.raise_for_status()
            ip_info = response.json()
            logging.info("Current IP: %s (%s, %s)", ip_info.get('ip'), ip_info.get('city'), ip_info.get('country'))
            return ip_info
        except requests.exceptions.RequestException as e:
            logging.error("Could not check IP address. Is Tor running? Error: %s", e)
            return {'error': str(e)}

if __name__ == '__main__':
    # Example of how to use the OpSecManager

    # --- Scenario 1: Ghost Mode OFF ---
    print("--- Initializing with Ghost Mode OFF ---")
    opsec_manager_off = OpSecManager(ghost_mode_enabled=False)
    opsec_manager_off.check_anonymity()

    # --- Scenario 2: Ghost Mode ON ---
    # NOTE: This requires a running Tor proxy on port 9050.
    # You can start one with the Tor Browser or by running `tor` as a service.
    print("\n--- Initializing with Ghost Mode ON ---")
    opsec_manager_on = OpSecManager(ghost_mode_enabled=True)
    opsec_manager_on.check_anonymity()

    # How other modules would use it:
    # session = opsec_manager_on.get_session()
    # response = session.get("http://example.com")
    # print(f"\nRequest sent through the managed session. Response status: {response.status_code}")
