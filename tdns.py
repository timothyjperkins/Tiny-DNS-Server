"""
Originally by HowCode.org written for a Windows Domain PC.
https://github.com/howCodeORG/howDNS

Heavily modified by Timothy Perkins for Linux.

Requirements:
    python3
    python_hosts ("sudo pip3 install python-hosts")
        -by Jon Hadfield (https://github.com/jonhadfield/python-hosts)
    bcolors.py (make sure it's in your scripts directory)
        -by Neil Marcum
    run as root ("sudo python3 tdns.py") since it runs on a <1024 port number

Limitations:
    For any host not found in the /etc/hosts file, it correctly returns "Not Found", but has extra bytes at the end.

Notes:
    Variable names are capitalized exactly as they are in IETF's RFC for DNS (RFC 1035).
    https://www.ietf.org/rfc/rfc1035.txt

"""

import socket
import os
from python_hosts import Hosts
from bcolors import bcolors

port = 53
ip = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

os.system('clear')
print("\nDNS Server started on", bcolors.OKBLUE, ip, ":", port, bcolors.NORMAL)

hosts = Hosts(path='/etc/hosts')
count = len(hosts.entries)
print("Imported", bcolors.OKBLUE, count, bcolors.NORMAL, "entries from the hosts file.\n")
print(" Requested -> Returned\n")


# Variables are named exactly as they are in the IETF RFC 1035
# https://www.ietf.org/rfc/rfc1035.txt
def getflags():

    QR = '1'

    OPCODE = '0000'

    AA = '1'

    TC = '0'

    RD = '0'

    # Byte 2

    RA = '0'

    Z = '000'

    if found is True:
        RCODE = '0000'
    else:
        RCODE = '0011'

    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')


def getquestiondomain(data):

    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            x += 1
            if x == expectedlength:
                domainparts.append(domainstring)
                domainstring = ''
                state = 0
                x = 0
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            state = 1
            expectedlength = byte
        y += 1

    questiontype = data[y:y+2]

    return domainparts, questiontype


def buildquestion(hostsname, rectype):
    qbytes = b''

    length = len(hostsname)
    qbytes += bytes([length])

    for char in hostsname:
        qbytes += ord(char).to_bytes(1, byteorder='big')

    qbytes += b'\x00'

    if rectype == 'A':
        qbytes += (1).to_bytes(2, byteorder='big')

    qbytes += (1).to_bytes(2, byteorder='big')

    return qbytes


def rectobytes(hostname, rectype, recttl, recval):

    # Turn on message compression on the response (c0 0c).
    rbytes = b'\xc0\x0c'

    # DNS Type (binary 01)
    if rectype == 'A':
        rbytes = rbytes + bytes([0]) + bytes([1])

    # DNS Class (binary 01)
    rbytes = rbytes + bytes([0]) + bytes([1])

    # Four byte Time-to-Live
    rbytes += int(recttl).to_bytes(4, byteorder='big')

    if rectype == 'A':
        rbytes = rbytes + bytes([0]) + bytes([4])

        # Split the IP address into its four parts
        for part in recval.split('.'):
            rbytes += bytes([int(part)])

    return rbytes


def buildresponse(addresstosend):

    # Transaction ID
    TransID = int.from_bytes(data[:2], byteorder='big')
    TransactionID = TransID.to_bytes(2, byteorder='big')

    # Get the flags
    Flags = getflags()

    # Question Count
    QDCOUNT = b'\x00\x01'

    # Answer Count
    if found is True:
        ANCOUNT = (1).to_bytes(2, byteorder='big')
    else:
        ANCOUNT = (0).to_bytes(2, byteorder='big')

    # Nameserver Count
    NSCOUNT = (0).to_bytes(2, byteorder='big')

    # Additonal Count
    ARCOUNT = (0).to_bytes(2, byteorder='big')

    dnsheader = TransactionID+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT

    # Create DNS body
    dnsbody = b''

    # Get answer for query
    dnsquestion = buildquestion(outputhost, "A")

    # If the host is found, return the response
    # dnsbody += rectobytes(host_to_send_back, record_type, record_ttl, record_value)
    if found is True:
        dnsbody += rectobytes(outputhost, "A", "600", addresstosend)

    return dnsheader + dnsquestion + dnsbody


def gethost(outputhost):

    global found
    found = False

    # Block to test if the received hostname is in the /etc/hosts file
    for entry in hosts.entries:
        if entry.names[0] == outputhost:
            found = True
            print(bcolors.OKGREEN, outputhost, "->", entry.address, bcolors.NORMAL)
            return entry.address

    if found is False:
        print(bcolors.FAIL, outputhost, "-> Not Found", bcolors.NORMAL)
        return "127.0.0.1"


try:
    while 1:
        data, address = sock.recvfrom(512)

        testing = data[13:].decode('utf-8')
        outputhost = testing.replace("\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00", "")

        addresstosend = gethost(outputhost)

        r = buildresponse(addresstosend)

        sock.sendto(r, address)
except(KeyboardInterrupt, SystemExit):
    print("\b\bExiting")
