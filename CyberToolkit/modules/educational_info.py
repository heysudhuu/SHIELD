def get_port_scanning_info():
    return {
        "title": "Port Scanning Fundamentals",
        "description": "Port scanning is a reconnaissance technique used to identify open doors (ports) on a network host. These open ports correspond to active network services.",
        "types": [
            {
                "name": "TCP Connect Scan",
                "mechanism": "Completes the full three-way handshake (SYN -> SYN-ACK -> ACK). The connection is fully established and then closed.",
                "pros_cons": "Highly accurate and doesn't require administrative privileges. However, it is very noisy and easily logged by firewalls and Intrusion Detection Systems (IDS)."
            },
            {
                "name": "TCP SYN Scan (Half-Open)",
                "mechanism": "Sends a SYN packet. If a SYN-ACK is received, the port is open, and the scanner immediately sends a RST packet to tear down the connection before it completes.",
                "pros_cons": "Fast and stealthier than a full TCP Connect scan, but requires administrator/root privileges on most systems."
            },
            {
                "name": "UDP Scan",
                "mechanism": "Sends a UDP packet to the target port. If no response is received, the port is assumed open/filtered. If an ICMP Destination Unreachable packet is returned, the port is closed.",
                "pros_cons": "Slower and less reliable due to UDP being connectionless, but crucial for finding services like DNS, DHCP, and SNMP."
            }
        ],
        "defensive_strategies": [
            "Configure host firewalls (Windows Defender Firewall, iptables) to drop traffic to unused ports.",
            "Use Intrusion Prevention Systems (IPS) or Intrusion Detection Systems (IDS) like Snort or Zeek to detect rapid port sweeps.",
            "Minimize your network footprint by disabling unnecessary services."
        ]
    }

def get_network_scanning_info():
    return {
        "title": "Network host Discovery",
        "description": "Network scanning is used to discover active hosts (laptops, mobile devices, servers) within a specific network range (e.g., an IP subnet).",
        "methods": [
            {
                "name": "ARP Scanning",
                "mechanism": "Sends ARP (Address Resolution Protocol) requests for every IP in the subnet. If a device is active, it responds with its MAC address.",
                "suitability": "Extremely fast and accurate for local subnets (Layer 2), but cannot traverse routers."
            },
            {
                "name": "ICMP Sweep (Ping Sweep)",
                "mechanism": "Sends ICMP Echo Requests (pings) to a range of IP addresses. Active devices return ICMP Echo Replies.",
                "suitability": "Works across subnets (Layer 3), but many modern operating systems (like Windows by default) block ICMP requests, making sweeps incomplete."
            }
        ],
        "defensive_strategies": [
            "Enable firewall rules to block incoming ICMP Echo Requests if ping sweeps are a concern.",
            "Implement MAC filtering and 802.1X Network Access Control (NAC) to prevent unauthorized devices from connecting to the network physical/wireless layer.",
            "Segment networks using VLANs to limit host discovery scope."
        ]
    }

def get_vulnerability_catalog():
    return [
        {
            "port": "21",
            "service": "FTP (File Transfer Protocol)",
            "risk": "Transmission of credentials and file contents in plain text. Vulnerable to sniffing. Often configured with anonymous login enabled.",
            "remediation": "Disable anonymous logins. Upgrade to SFTP (SSH File Transfer Protocol) or FTPS (FTP over SSL/TLS)."
        },
        {
            "port": "22",
            "service": "SSH (Secure Shell)",
            "risk": "Brute-force password guessing. Weak cipher suites or outdated daemon versions can lead to remote command execution.",
            "remediation": "Disable password authentication and enforce SSH key pairs. Restrict SSH access to specific IPs. Install Fail2ban to block brute-force attempts."
        },
        {
            "port": "23",
            "service": "Telnet",
            "risk": "All traffic, including logins and command executions, is sent in cleartext.",
            "remediation": "Disable Telnet entirely. Use SSH instead."
        },
        {
            "port": "80",
            "service": "HTTP (Web Server)",
            "risk": "Data transmitted in cleartext. Vulnerable to interception of session cookies and login tokens.",
            "remediation": "Configure SSL/TLS (HTTPS) on port 443 and redirect all HTTP traffic to HTTPS using permanent redirects (HTTP 301)."
        },
        {
            "port": "445",
            "service": "SMB (Server Message Block)",
            "risk": "High-risk protocol. Vulnerable to critical exploits (like EternalBlue - MS17-010). Can allow unauthorized network file sharing access.",
            "remediation": "Never expose port 445 directly to the internet. Disable SMBv1. Require packet signing (SMB Signing) and restrict SMB access using firewalls."
        }
    ]
