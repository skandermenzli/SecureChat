from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


def gen_key(id):
    # Generate our key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Write our key to disk for safe keeping
    file  = "key-"+id+".pem"
    with open(file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
        ))
    return key


def gen_cer_req(id):
    key = gen_key(id)
    # Generate a CSR
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"TU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Tunis"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"CUN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"INSAT"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"INSAT"),
    ])).add_extension(
        x509.SubjectAlternativeName([
            # Describe what sites we want this certificate for.
            x509.DNSName(u"mySecureChat.com")
        ]),
        critical=False,
        # Sign the CSR with our private key.
    ).sign(key, hashes.SHA256())
    # Write our CSR out to disk.
    file = "csr-"+id+".pem"
    with open(file, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

