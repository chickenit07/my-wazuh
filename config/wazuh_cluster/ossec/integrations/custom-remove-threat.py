#!/usr/bin/env python
import json
import sys
import time
import os
from socket import socket, AF_UNIX, SOCK_DGRAM
# Global vars
debug_enabled = True
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert = {}
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")
# Set paths
log_file = '{0}/logs/integrations.log'.format(pwd)
socket_addr = '{0}/queue/alerts/ar'.format(pwd)
def main(args):
    debug("# Starting Remove Threat")
    # Read args
    alert_file_location = args[1]
    debug("# File location")
    debug(alert_file_location)
    # Load alert. Parse JSON object.
    with open(alert_file_location) as alert_file:    
        json_alert = json.load(alert_file)
    debug("# Processing alert")
    debug(json_alert)
    # Send event to AR socket
    msg = "(msg_to_agent) [] NNS {0} remove-threat0 - {1}".format(json_alert["agent"]["id"], json_alert["data"]["virustotal"]["source"]["file"])
    debug("messeage")
    debug(msg)
    send_event(msg)

def debug(msg):
    if debug_enabled:
        msg = "{0}: {1}\n".format(now, msg)
        print(msg)
        f = open(log_file,"a")
        f.write(msg)
        f.close()
def send_event(msg):
    sock = socket(AF_UNIX, SOCK_DGRAM)
    sock.connect(socket_addr)
    sock.send(msg.encode())
    sock.close()
if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 2:
            alertfile=sys.argv[1]
            msg = '{0} {1} 2 {2} 3 {3} 4 {4}'.format(now, sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True
        # Logging the call
        f = open(log_file, 'a')
        f.write(msg +'\n')
        f.close()
        if bad_arguments:
            debug("# Exiting: Bad arguments.")
            sys.exit(0)
        # Main function
        main(sys.argv)
    except Exception as e:
        debug('Error:' + str(e))
        raise
