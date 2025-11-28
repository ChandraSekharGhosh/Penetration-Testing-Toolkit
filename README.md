# Penetration-Testing-Toolkit

Company: Codtech IT Solutions<br>
Name: Chandra Sekhar Ghosh<br>
Intern ID: CT04DR1779<br>
Domain: Cybersecury and Ethical Hacking<br>
Duration: 4 weeks<br>
Mentor: Muzammil<br>

A comprehensive, modular penetration testing toolkit written in Python for security professionals, ethical hackers, and students learning cybersecurity.

---

## ⚠️ LEGAL DISCLAIMER<br>

**THIS TOOL IS FOR EDUCATIONAL PURPOSES AND AUTHORIZED TESTING ONLY.**<br>

- **Unauthorized access to computer systems is ILLEGAL**<br>
- Always obtain **written permission** before testing any system<br>
- Use only on systems you own or have explicit authorization to test<br>
- Misuse of this tool may result in criminal prosecution<br>
- The authors are not responsible for any misuse or damage caused by this tool<br>

By using this tool, you agree to use it responsibly and legally.<br>

---

## ✨ Features<br>

### 🔍 Port Scanner<br>
- Multi-threaded TCP port scanning<br>
- Customizable port ranges<br>
- Service detection<br>
- Adjustable timeout and thread count<br>
- Banner grabbing capability<br>

### 🔐 Brute Force Module<br>
- SSH authentication testing<br>
- HTTP form-based authentication<br>
- Wordlist-based password attacks<br>
- Rate limiting to avoid detection<br>
- Real-time progress feedback<br>

### 🛡️ Vulnerability Scanner<br>
- HTTP security headers analysis<br>
- Common vulnerable port detection<br>
- Security misconfigurations identification<br>
- Comprehensive vulnerability reporting<br>

### 🗺️ Network Mapper<br>
- Host discovery via ping sweep<br>
- Network range scanning<br>
- Active host identification<br>
- Fast subnet enumeration<br>

### 🔨 Hash Cracker<br>
- MD5, SHA1, SHA256 hash cracking<br>
- Dictionary-based attacks<br>
- Real-time progress display<br>
- Support for custom wordlists<br>

---

## 📦 Requirements<br>

### System Requirements<br>
- **Operating System:** Linux, macOS, or Windows<br>
- **Python Version:** 3.7 or higher<br>
- **RAM:** Minimum 512MB (2GB recommended for large scans)<br>
- **Network:** Active internet connection (for some modules)<br>

### Python Dependencies<br>
```
requests>=2.28.0
paramiko>=2.11.0
```

---

## 🚀 Installation<br>

### Step 1: Clone the Repository<br>
```bash
# Using HTTPS<br>
git clone https://github.com/ChandraSekharGhosh/Penetration-Testing-Toolkit.git

# OR using SSH
git clone git@github.com:ChandraSekharGhosh/Penetration-Testing-Toolkit.git

# Navigate to directory
cd Penetration-Testing-Toolkit
```

### Step 2: Create Virtual Environment (Recommended)<br>
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies<br>
```bash
# Install required packages
pip install -r requirements.txt

# OR install manually
pip install requests paramiko
```

### Step 4: Verify Installation<br>
```bash
# Check if script runs
python pentest.py --help

# You should see the help menu
```

### Step 5: Make Executable (Linux/macOS)<br>
```bash
chmod +x pentest.py
```

---

## 📖 Usage<br>

### General Syntax<br>
```bash
python pentest.py <module> [options]
```

### Available Modules<br>
- `portscan` - Port scanning module
- `bruteforce` - Authentication brute forcing
- `vulnscan` - Vulnerability scanning
- `netmap` - Network mapping
- `hashcrack` - Password hash cracking

### Getting Help<br>
```bash
# General help
python pentest.py --help

# Module-specific help
python pentest.py portscan --help
python pentest.py bruteforce --help
python pentest.py vulnscan --help
python pentest.py netmap --help
python pentest.py hashcrack --help
```

---

## 🔧 Module Documentation<br>

### 1. Port Scanner<br>

Scan TCP ports on a target system to identify open services.<br>

#### Basic Usage<br>
```bash
python pentest.py portscan -t <target> -p <port_range>
```

#### Options<br>
| Option | Description | Default |
|--------|-------------|---------|
| `-t, --target` | Target IP address or hostname (required) | - |
| `-p, --ports` | Port range to scan (e.g., 1-1000) | - |
| `--threads` | Number of concurrent threads | 100 |

#### Examples<br>
```bash
# Scan common ports on a target
python pentest.py portscan -t 192.168.1.1 -p 1-1000

# Scan specific ports
python pentest.py portscan -t example.com -p 80-443

# Fast scan with more threads
python pentest.py portscan -t 10.0.0.1 -p 1-65535 --threads 500

# Scan all ports (slow)
python pentest.py portscan -t scanme.nmap.org -p 1-65535
```

#### Output Example<br>
```
============================================================
PORT SCANNER MODULE
============================================================
Target: 192.168.1.1
Scanning ports: 1-1000
Time: 2025-11-26 10:30:45

[+] Port 22 OPEN - Service: ssh
[+] Port 80 OPEN - Service: http
[+] Port 443 OPEN - Service: https

Scan complete. Found 3 open ports
```

---

### 2. Brute Force Module<br>

Attempt to authenticate using a wordlist of passwords.

#### Basic Usage<br>
```bash
python pentest.py bruteforce -t <target> -u <username> -w <wordlist> --protocol <protocol>
```

#### Options<br>
| Option | Description | Default |
|--------|-------------|---------|
| `-t, --target` | Target IP/URL (required) | - |
| `-u, --username` | Username to test (required) | - |
| `-w, --wordlist` | Path to password wordlist (required) | - |
| `--protocol` | Protocol to use (ssh/http) | ssh |

#### Examples<br>
```bash
# SSH brute force
python pentest.py bruteforce -t 192.168.1.100 -u admin -w passwords.txt --protocol ssh

# HTTP form brute force
python pentest.py bruteforce -t http://example.com/login -u admin -w rockyou.txt --protocol http

# Using custom wordlist
python pentest.py bruteforce -t 10.0.0.5 -u root -w /usr/share/wordlists/common.txt
```

#### Creating a Wordlist<br>
```bash
# Simple wordlist
echo -e "password\nadmin\n123456\nletmein" > wordlist.txt

# Download rockyou.txt (popular wordlist)
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

#### Output Example<br>
```
============================================================
BRUTE FORCE MODULE
============================================================
Target: 192.168.1.100
Username: admin
Protocol: ssh
Wordlist: passwords.txt

Loaded 1000 passwords. Starting attack...

[543/1000] Trying: password123

[+] SUCCESS! Password found: admin2024
```

---

### 3. Vulnerability Scanner<br>

Scan for common security vulnerabilities and misconfigurations.

#### Basic Usage<br>
```bash
python pentest.py vulnscan -t <target>
```

#### Options
| Option | Description | Default |
|--------|-------------|---------|
| `-t, --target` | Target IP or hostname (required) | - |

#### Examples
```bash
# Basic vulnerability scan
python pentest.py vulnscan -t example.com

# Scan local server
python pentest.py vulnscan -t 127.0.0.1

# Scan IP address
python pentest.py vulnscan -t 192.168.1.1
```

#### What It Checks
- ✅ HTTP security headers (X-Frame-Options, CSP, HSTS, etc.)
- ✅ Commonly vulnerable ports (FTP, Telnet, SMB, etc.)
- ✅ Missing security configurations
- ✅ Potential attack vectors

#### Output Example
```
============================================================
VULNERABILITY SCANNER MODULE
============================================================
Target: example.com

[*] Checking HTTP security headers...
[+] X-Frame-Options present
[-] Missing MIME sniffing protection (X-Content-Type-Options)
[-] Missing HSTS (Strict-Transport-Security)

[*] Checking for vulnerable ports...
[-] Port 21 open - FTP (plaintext)
[-] Port 23 open - Telnet (plaintext)

Found 4 potential vulnerabilities
```

---

### 4. Network Mapper

Discover active hosts on a network subnet.

#### Basic Usage
```bash
python pentest.py netmap -n <network>
```

#### Options
| Option | Description | Default |
|--------|-------------|---------|
| `-n, --network` | Network address (e.g., 192.168.1.0) (required) | - |

#### Examples
```bash
# Scan home network
python pentest.py netmap -n 192.168.1.0

# Scan office network
python pentest.py netmap -n 10.0.0.0

# Scan different subnet
python pentest.py netmap -n 172.16.0.0
```

#### Output Example
```
============================================================
NETWORK MAPPER MODULE
============================================================
Network: 192.168.1.0

[*] Performing ping sweep...

[+] Host found: 192.168.1.1
[+] Host found: 192.168.1.10
[+] Host found: 192.168.1.15
[+] Host found: 192.168.1.100

Found 4 active hosts
```

---

### 5. Hash Cracker

Crack password hashes using dictionary attacks.

#### Basic Usage
```bash
python pentest.py hashcrack -H <hash> -w <wordlist> --type <hash_type>
```

#### Options
| Option | Description | Default |
|--------|-------------|---------|
| `-H, --hash` | Hash to crack (required) | - |
| `-w, --wordlist` | Path to wordlist (required) | - |
| `--type` | Hash type (md5/sha1/sha256) | md5 |

#### Examples
```bash
# Crack MD5 hash
python pentest.py hashcrack -H 5f4dcc3b5aa765d61d8327deb882cf99 -w wordlist.txt --type md5

# Crack SHA1 hash
python pentest.py hashcrack -H 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8 -w rockyou.txt --type sha1

# Crack SHA256 hash
python pentest.py hashcrack -H 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 -w common.txt --type sha256
```

#### Hash Examples
```bash
# MD5 hash of "password"
5f4dcc3b5aa765d61d8327deb882cf99

# SHA1 hash of "password"
5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8

# SHA256 hash of "password"
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

#### Output Example
```
============================================================
HASH CRACKER MODULE
============================================================
Hash: 5f4dcc3b5aa765d61d8327deb882cf99
Type: md5
Wordlist: wordlist.txt

Loaded 10000 passwords. Cracking...

[2543/10000] Testing: sunshine

[+] Hash cracked! Password: password
```

---

## 💡 Complete Examples

### Example 1: Full Security Assessment
```bash
# Step 1: Discover hosts
python pentest.py netmap -n 192.168.1.0

# Step 2: Scan open ports on discovered host
python pentest.py portscan -t 192.168.1.100 -p 1-10000

# Step 3: Check for vulnerabilities
python pentest.py vulnscan -t 192.168.1.100

# Step 4: Attempt SSH authentication (if port 22 is open)
python pentest.py bruteforce -t 192.168.1.100 -u admin -w wordlist.txt
```

### Example 2: Web Application Testing
```bash
# Check web server security
python pentest.py vulnscan -t example.com

# Scan web ports
python pentest.py portscan -t example.com -p 80,443,8080,8443

# Test login form
python pentest.py bruteforce -t http://example.com/login -u admin -w passwords.txt --protocol http
```

### Example 3: Password Recovery
```bash
# Crack a password hash from database dump
python pentest.py hashcrack -H a94a8fe5ccb19ba61c4c0873d391e987982fbbd3 -w rockyou.txt --type sha1
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue: "Module not found" error
```bash
# Solution: Install dependencies
pip install -r requirements.txt
pip install requests paramiko
```

#### Issue: Permission denied on Linux/macOS
```bash
# Solution: Make script executable
chmod +x pentest.py

# OR run with python3 explicitly
python3 pentest.py portscan -t 192.168.1.1 -p 80
```

#### Issue: "Connection refused" during port scan
**Cause:** Target system is blocking connections or firewall is active
**Solution:** 
- Verify target is reachable: `ping <target>`
- Check if you have authorization to scan
- Try scanning with fewer threads: `--threads 10`

#### Issue: SSH brute force not working
**Cause:** paramiko not installed or SSH service blocking
**Solution:**
```bash
# Install paramiko
pip install paramiko

# Check if SSH is accessible
telnet <target> 22
```

#### Issue: Wordlist not found
```bash
# Solution: Use absolute path
python pentest.py bruteforce -t 192.168.1.1 -u admin -w /home/user/wordlists/rockyou.txt
```

#### Issue: Rate limiting / Timeout errors
**Cause:** Target system is rate limiting requests
**Solution:** Add delays between attempts (modify code or use slower wordlist)

---

## 🔒 Security Best Practices

### 1. Always Get Authorization
- Obtain written permission before testing
- Document your scope and limitations
- Never test production systems without approval

### 2. Use Responsibly
- Start with non-invasive scans
- Avoid denial-of-service attacks
- Be aware of rate limiting
- Don't disrupt normal operations

### 3. Protect Your Results
- Encrypt your findings
- Share reports securely
- Follow responsible disclosure practices

### 4. Stay Legal
- Know your local laws
- Understand computer fraud laws
- Get proper certifications (CEH, OSCP)

---

## 📚 Learning Resources

### Recommended Reading
- **Books:**
  - "The Web Application Hacker's Handbook" by Dafydd Stuttard
  - "Metasploit: The Penetration Tester's Guide" by David Kennedy
  - "Black Hat Python" by Justin Seitz

### Online Platforms
- **Practice Labs:**
  - HackTheBox (https://www.hackthebox.eu/)
  - TryHackMe (https://tryhackme.com/)
  - PentesterLab (https://pentesterlab.com/)
  
### Certifications
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- CompTIA Security+

---

## 🙏 Acknowledgments

- Thanks to the open-source security community
- Inspired by tools like Nmap, Metasploit, and Burp Suite
- Special thanks to all contributors

---

## ⭐ Star This Repository

If you found this tool helpful, please consider giving it a star! It helps others discover the project.

---

**Remember: With great power comes great responsibility. Use ethically!** 🛡️
