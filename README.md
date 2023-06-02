# Tiny-DNS-Server
A small DNS server written in Python to do forward and reverse lookups from the /etc/hosts file and return results.

Originally by HowCode.org written for a Windows Domain PC.
https://github.com/howCodeORG/howDNS

Heavily modified by Timothy Perkins for Linux.

Requirements:
    python3
    python_hosts ("sudo pip3 install python-hosts")
        -by Jon Hadfield (https://github.com/jonhadfield/python-hosts)
    bcolors.py (make sure it's in your scripts directory)
        -by Neil Marcum
    run as root ("sudo python3 dns.py") since it runs on a <1024 port number

Limitations:
    For any host not found in the /etc/hosts file, it correctly returns "Not Found", but has extra bytes at the end.

Notes:
    Variable names are capitalized exactly as they are in IETF's RFC for DNS (RFC 1035).
    https://www.ietf.org/rfc/rfc1035.txt
    
Warning: This is probably vulnerable to all sorts of attack. DO NOT expose it to the Internet!
