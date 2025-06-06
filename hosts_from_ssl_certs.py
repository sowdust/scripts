"""
    This script takes a file with a list of ip addresses
    and prints out the alternative names and common names 
    found in their SSL certificates

"""


import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID



input_file = ''
port = 443

def get_certificate(ip, port):
    # Create SSL context with verification disabled
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((ip, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=ip) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
    return der_cert

def parse_certificate(der_cert):
    cert = x509.load_der_x509_certificate(der_cert, default_backend())

    # Extract Common Name (CN)
    cn = None
    for attribute in cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME):
        cn = attribute.value

    # Extract Subject Alternative Names (SAN)
    try:
        san_extension = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        dns_names = san_extension.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        dns_names = []

    return cn, dns_names

if __name__ == "__main__":
    #ip_address = input("Enter IP address: ").strip()
    #port = int(input("Enter port: ").strip())


    with open(input_file, 'r') as file:
        for host in file.readlines():
            ip_address = host.strip()

            try:
                der_cert = get_certificate(ip_address, port)
                cn, san_dns = parse_certificate(der_cert)

                print(f"{cn}")

                #print("[+] Subject Alternative Names (DNS):")
                if san_dns:
                    for dns in san_dns:
                        print(f"{dns}")
                else:
                    print("    (None)")

            except Exception as e:
                print(f"[!] Error: {e}")
