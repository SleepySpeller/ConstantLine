print("Booting up...")
import time
from datetime import datetime
from os import getenv

from NetworkManager import Network
from LogManager import Logs

HOSTNAMES = getenv("HOSTNAMES") # Comma-separated list of hostnames or IP addresses to ping. Must be provided as an environment variable.

if not HOSTNAMES:
    raise ValueError("HOSTNAMES environment variable is not set. Please set it to a comma-separated list of hostnames or IP addresses.")

HOSTNAMES = HOSTNAMES.split(",")

TIMEOUT = getenv("TIMEOUT", 2) # How long to wait for a response from the hostnames

SLEEP_TIME = getenv("SLEEP_TIME", 1.2) # How often to check the network status
SLEEP_TIME_DISCONNECTED = getenv("SLEEP_TIME_DISCONNECTED", 0.5) # How often to check the network status when disconnected

def wait_for_network():
    new_ip = network.get_ip(timeout=SLEEP_TIME_DISCONNECTED)
    while not new_ip:
        new_ip = network.get_ip(timeout=SLEEP_TIME_DISCONNECTED)
        time.sleep(SLEEP_TIME_DISCONNECTED)
        
    return new_ip

network = Network(HOSTNAMES, TIMEOUT)
logs = Logs()

print("Getting the current IP")
current_ip = network.get_ip()
if current_ip and type(current_ip) is not False:
    print("Network is up!")
    logs.log({
        "timestamp": datetime.now().isoformat(),
        "status": "starting",
        "ip": current_ip
    })
    
else:
    print("No IP found (startup), waiting for network connection...")
    logs.log({
        "timestamp": datetime.now().isoformat(),
        "status": "starting - disconnected",
    })
    current_ip = wait_for_network()
    print("Reconnected!")
    logs.log_reconnect(current_ip)


print("Starting main loop...")
while True:
    if not network.ping(timeout=1) and not network.get_ip():
        print("No IP found, waiting for network connection...")
        
        logs.log_disconnect(current_ip)
        
        new_ip = wait_for_network()
        
        print("Reconnected!")
        logs.log_reconnect(new_ip)
            
    time.sleep(SLEEP_TIME)
