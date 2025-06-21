from ping3 import ping
import random
import requests

class Network:
    def __init__(self, hostnames: list[str], timeout: int = 2):
        self.hostnames = hostnames
        self.timeout = timeout
    
    def get_random_hostname(self) -> str:
        return random.choice(self.hostnames)
    
    def ping(self, address: str = None, timeout: int = None) -> int:
        """Ping a given address or a random hostname from the list.

        Args:
            address (str, optional): Address to ping. Defaults to a random hostname from the list.
            timeout (int, optional): Time limit until the packets timeout. Defaults to the Network's passed timeout.

        Returns:
            int: Latency in milliseconds if the ping is successful.
        """
        if not address: address = self.get_random_hostname()
        if not timeout: timeout = self.timeout
        
        return ping(address, timeout=timeout) # If you're seeing a PermissionError here, the user doesn't have the permission to send raw packets. Check https://github.com/alessandromaggio/pythonping/issues/27#issuecomment-811620352 or run the script with sudo.

    def get_ip(self, timeout: int = None, retry_timeout: int = 1, retry_attempts: int = 3) -> (str | bool):
        """
        Get the public IP address of the machine.
        
        :param timeout: Timeout for the request in seconds. Default is None, which uses the Network's passed timeout.
        :param retry_timeout: Timeout for retrying the request in seconds if rate limited. Default is 0.5 seconds.
        :param retry_attempts: Number of retry attempts if the request fails due to rate limiting. Default is 3.
        :return: The public IP address as a string, True if the request fails due to rate limiting, or False on other errors.
        """
        
        if timeout is None: timeout = self.timeout
        
        try:
            response = requests.get("https://api.ipify.org", timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError:
            i = 0
            
            while response.status_code == 429 or response.status_code == 503:
                response = requests.get("https://api.ipify.org", timeout=retry_timeout)
                i += 1
                if i > retry_attempts:
                    return True
                
            return response.text
        except Exception:
            return False