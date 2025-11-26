#!/usr/bin/env python3
"""
Penetration Testing Toolkit
DISCLAIMER: This tool is for EDUCATIONAL PURPOSES and AUTHORIZED TESTING ONLY.
Unauthorized access to computer systems is illegal. Always obtain proper authorization.
"""

import socket
import threading
import argparse
import sys
import time
import requests
import hashlib
from datetime import datetime
from queue import Queue
import subprocess
import re

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class PortScanner:
    """Port scanning module"""
    
    def __init__(self, target, ports, threads=100):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.open_ports = []
        self.queue = Queue()
        self.lock = threading.Lock()
    
    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    print(f"{Colors.GREEN}[+] Port {port} OPEN - Service: {service}{Colors.END}")
            
            sock.close()
        except socket.gaierror:
            print(f"{Colors.RED}[-] Hostname could not be resolved{Colors.END}")
        except socket.error:
            pass
    
    def worker(self):
        """Worker thread for port scanning"""
        while True:
            port = self.queue.get()
            if port is None:
                break
            self.scan_port(port)
            self.queue.task_done()
    
    def scan(self):
        """Execute port scan"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"PORT SCANNER MODULE")
        print(f"{'='*60}{Colors.END}")
        print(f"Target: {self.target}")
        print(f"Scanning ports: {self.ports[0]}-{self.ports[-1]}")
        print(f"Time: {datetime.now()}\n")
        
        # Start worker threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Add ports to queue
        for port in self.ports:
            self.queue.put(port)
        
        # Wait for completion
        self.queue.join()
        
        # Stop workers
        for _ in range(self.threads):
            self.queue.put(None)
        for t in threads:
            t.join()
        
        print(f"\n{Colors.BLUE}Scan complete. Found {len(self.open_ports)} open ports{Colors.END}")
        return self.open_ports


class BruteForcer:
    """Brute force authentication module"""
    
    def __init__(self, target, username, wordlist, protocol='ssh'):
        self.target = target
        self.username = username
        self.wordlist = wordlist
        self.protocol = protocol.lower()
        self.found = False
    
    def ssh_bruteforce(self, password):
        """SSH brute force attempt"""
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.target, username=self.username, password=password, timeout=3)
            client.close()
            return True
        except:
            return False
    
    def http_bruteforce(self, password, url):
        """HTTP form brute force attempt"""
        try:
            data = {'username': self.username, 'password': password}
            response = requests.post(url, data=data, timeout=5)
            
            # Check for successful login indicators
            if response.status_code == 200 and 'dashboard' in response.url.lower():
                return True
            return False
        except:
            return False
    
    def attack(self):
        """Execute brute force attack"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"BRUTE FORCE MODULE")
        print(f"{'='*60}{Colors.END}")
        print(f"Target: {self.target}")
        print(f"Username: {self.username}")
        print(f"Protocol: {self.protocol}")
        print(f"Wordlist: {self.wordlist}\n")
        
        try:
            with open(self.wordlist, 'r') as f:
                passwords = f.read().splitlines()
        except FileNotFoundError:
            print(f"{Colors.RED}[-] Wordlist not found!{Colors.END}")
            return None
        
        print(f"Loaded {len(passwords)} passwords. Starting attack...\n")
        
        for i, password in enumerate(passwords):
            if self.found:
                break
            
            print(f"[{i+1}/{len(passwords)}] Trying: {password}", end='\r')
            
            success = False
            if self.protocol == 'ssh':
                success = self.ssh_bruteforce(password)
            elif self.protocol == 'http':
                success = self.http_bruteforce(password, self.target)
            
            if success:
                print(f"\n{Colors.GREEN}[+] SUCCESS! Password found: {password}{Colors.END}")
                self.found = True
                return password
            
            time.sleep(0.1)  # Rate limiting
        
        if not self.found:
            print(f"\n{Colors.RED}[-] Password not found in wordlist{Colors.END}")
        return None


class VulnerabilityScanner:
    """Basic vulnerability scanning module"""
    
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
    
    def check_http_headers(self):
        """Check for security headers"""
        print(f"\n{Colors.YELLOW}[*] Checking HTTP security headers...{Colors.END}")
        
        try:
            response = requests.get(f"http://{self.target}", timeout=5)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME sniffing protection',
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-XSS-Protection': 'XSS protection'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    vuln = f"Missing {description} ({header})"
                    self.vulnerabilities.append(vuln)
                    print(f"{Colors.RED}[-] {vuln}{Colors.END}")
                else:
                    print(f"{Colors.GREEN}[+] {description} present{Colors.END}")
        except:
            print(f"{Colors.RED}[-] Could not connect to HTTP service{Colors.END}")
    
    def check_common_ports(self):
        """Check for commonly vulnerable ports"""
        print(f"\n{Colors.YELLOW}[*] Checking for vulnerable ports...{Colors.END}")
        
        vulnerable_ports = {
            21: 'FTP (plaintext)',
            23: 'Telnet (plaintext)',
            25: 'SMTP (potential relay)',
            445: 'SMB (EternalBlue)',
            3389: 'RDP (brute force target)',
            5900: 'VNC (weak auth)'
        }
        
        for port, desc in vulnerable_ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                vuln = f"Port {port} open - {desc}"
                self.vulnerabilities.append(vuln)
                print(f"{Colors.RED}[-] {vuln}{Colors.END}")
            sock.close()
    
    def scan(self):
        """Execute vulnerability scan"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"VULNERABILITY SCANNER MODULE")
        print(f"{'='*60}{Colors.END}")
        print(f"Target: {self.target}\n")
        
        self.check_http_headers()
        self.check_common_ports()
        
        print(f"\n{Colors.BLUE}Found {len(self.vulnerabilities)} potential vulnerabilities{Colors.END}")
        return self.vulnerabilities


class NetworkMapper:
    """Network mapping and host discovery module"""
    
    def __init__(self, network):
        self.network = network
        self.active_hosts = []
    
    def ping_sweep(self):
        """Perform ping sweep to discover active hosts"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"NETWORK MAPPER MODULE")
        print(f"{'='*60}{Colors.END}")
        print(f"Network: {self.network}\n")
        print(f"{Colors.YELLOW}[*] Performing ping sweep...{Colors.END}\n")
        
        base_ip = '.'.join(self.network.split('.')[:-1])
        
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            
            try:
                # Platform-specific ping command
                param = '-n' if sys.platform.startswith('win') else '-c'
                command = ['ping', param, '1', '-W', '1', ip]
                
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if result.returncode == 0:
                    self.active_hosts.append(ip)
                    print(f"{Colors.GREEN}[+] Host found: {ip}{Colors.END}")
            except:
                pass
        
        print(f"\n{Colors.BLUE}Found {len(self.active_hosts)} active hosts{Colors.END}")
        return self.active_hosts


class HashCracker:
    """Password hash cracking module"""
    
    def __init__(self, hash_value, wordlist, hash_type='md5'):
        self.hash_value = hash_value.lower()
        self.wordlist = wordlist
        self.hash_type = hash_type.lower()
    
    def crack(self):
        """Attempt to crack the hash"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"HASH CRACKER MODULE")
        print(f"{'='*60}{Colors.END}")
        print(f"Hash: {self.hash_value}")
        print(f"Type: {self.hash_type}")
        print(f"Wordlist: {self.wordlist}\n")
        
        try:
            with open(self.wordlist, 'r') as f:
                passwords = f.read().splitlines()
        except FileNotFoundError:
            print(f"{Colors.RED}[-] Wordlist not found!{Colors.END}")
            return None
        
        print(f"Loaded {len(passwords)} passwords. Cracking...\n")
        
        for i, password in enumerate(passwords):
            if self.hash_type == 'md5':
                test_hash = hashlib.md5(password.encode()).hexdigest()
            elif self.hash_type == 'sha1':
                test_hash = hashlib.sha1(password.encode()).hexdigest()
            elif self.hash_type == 'sha256':
                test_hash = hashlib.sha256(password.encode()).hexdigest()
            else:
                print(f"{Colors.RED}[-] Unsupported hash type{Colors.END}")
                return None
            
            print(f"[{i+1}/{len(passwords)}] Testing: {password}", end='\r')
            
            if test_hash == self.hash_value:
                print(f"\n{Colors.GREEN}[+] Hash cracked! Password: {password}{Colors.END}")
                return password
        
        print(f"\n{Colors.RED}[-] Hash not cracked{Colors.END}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Penetration Testing Toolkit - For AUTHORIZED testing only',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Port Scan:        python pentest.py portscan -t 192.168.1.1 -p 1-1000
  Brute Force:      python pentest.py bruteforce -t 192.168.1.1 -u admin -w wordlist.txt
  Vulnerability:    python pentest.py vulnscan -t example.com
  Network Map:      python pentest.py netmap -n 192.168.1.0
  Hash Crack:       python pentest.py hashcrack -H 5f4dcc3b5aa765d61d8327deb882cf99 -w wordlist.txt
        """
    )
    
    subparsers = parser.add_subparsers(dest='module', help='Module to use')
    
    # Port Scanner
    port_parser = subparsers.add_parser('portscan', help='Port scanning module')
    port_parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    port_parser.add_argument('-p', '--ports', default='1-1000', help='Port range (e.g., 1-1000)')
    port_parser.add_argument('--threads', type=int, default=100, help='Number of threads')
    
    # Brute Forcer
    brute_parser = subparsers.add_parser('bruteforce', help='Brute force module')
    brute_parser.add_argument('-t', '--target', required=True, help='Target IP or URL')
    brute_parser.add_argument('-u', '--username', required=True, help='Username')
    brute_parser.add_argument('-w', '--wordlist', required=True, help='Password wordlist')
    brute_parser.add_argument('--protocol', default='ssh', choices=['ssh', 'http'], help='Protocol')
    
    # Vulnerability Scanner
    vuln_parser = subparsers.add_parser('vulnscan', help='Vulnerability scanning module')
    vuln_parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    
    # Network Mapper
    net_parser = subparsers.add_parser('netmap', help='Network mapping module')
    net_parser.add_argument('-n', '--network', required=True, help='Network (e.g., 192.168.1.0)')
    
    # Hash Cracker
    hash_parser = subparsers.add_parser('hashcrack', help='Hash cracking module')
    hash_parser.add_argument('-H', '--hash', required=True, help='Hash to crack')
    hash_parser.add_argument('-w', '--wordlist', required=True, help='Password wordlist')
    hash_parser.add_argument('--type', default='md5', choices=['md5', 'sha1', 'sha256'], help='Hash type')
    
    args = parser.parse_args()
    
    if not args.module:
        parser.print_help()
        return
    
    print(f"{Colors.BOLD}{Colors.RED}")
    print("="*60)
    print("  PENETRATION TESTING TOOLKIT")
    print("  FOR AUTHORIZED USE ONLY")
    print("="*60)
    print(f"{Colors.END}")
    
    # Execute selected module
    if args.module == 'portscan':
        start, end = map(int, args.ports.split('-'))
        ports = range(start, end + 1)
        scanner = PortScanner(args.target, ports, args.threads)
        scanner.scan()
    
    elif args.module == 'bruteforce':
        bruter = BruteForcer(args.target, args.username, args.wordlist, args.protocol)
        bruter.attack()
    
    elif args.module == 'vulnscan':
        scanner = VulnerabilityScanner(args.target)
        scanner.scan()
    
    elif args.module == 'netmap':
        mapper = NetworkMapper(args.network)
        mapper.ping_sweep()
    
    elif args.module == 'hashcrack':
        cracker = HashCracker(args.hash, args.wordlist, args.type)
        cracker.crack()


if __name__ == '__main__':
    main()