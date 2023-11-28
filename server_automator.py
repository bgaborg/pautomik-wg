import configparser
import subprocess
import logging
import logging.handlers
import re
import sys
import os


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
config = configparser.ConfigParser()
config.read('settings.ini')
if not 'domain' in config['duckdns']:
    raise Exception("No domain set in settings.ini")
if not 'token' in config['duckdns']:
    raise Exception("No token set in settings.ini")
ductdns_domain = config['duckdns']['domain']
duckdns_token = config['duckdns']['token']


logger = logging.getLogger('pivpn_automator')
logger.setLevel(logging.INFO)
fh = logging.handlers.RotatingFileHandler('/var/log/pivpn_automator.log', maxBytes=1000000, backupCount=5)
fh.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)


def update_duckdns():
    logger.info(f"Running duckdns update for domain: {ductdns_domain}")
    # get ipv4 address
    #ipv4_addr = subprocess.check_output(['curl', '-s', 'https://api.ipify.org']).decode('utf-8').strip()
    # get ipv6 address
    ipv6_addr = subprocess.check_output(['curl', '-s', 'https://api6.ipify.org']).decode('utf-8').strip()
    #command = ['bash', '-c', f'echo url="https://www.duckdns.org/update?domains={ductdns_domain}&token={duckdns_token}&ip={ipv4_addr}&ipv6={ipv6_addr}&verbose=true" | curl -k -K -']
    command = ['bash', '-c', f'echo url="https://www.duckdns.org/update?domains={ductdns_domain}&token={duckdns_token}&ipv6={ipv6_addr}&verbose=true" | curl -k -K -']
    output = subprocess.check_output(command, universal_newlines=True)
    logger.info(f"Output: {output}")

def main():
    update_duckdns()

if __name__ == "__main__":
    main()
