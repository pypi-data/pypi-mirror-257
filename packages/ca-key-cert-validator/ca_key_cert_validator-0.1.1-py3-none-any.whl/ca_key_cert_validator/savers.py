from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def private_key_to_bytes(private_key: rsa.RSAPrivateKey) -> bytes:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )


def private_key_to_bytes_with_password(private_key: rsa.RSAPrivateKey, password: bytes) -> bytes:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )


def private_key_to_pem(private_key: rsa.RSAPrivateKey, filename: str) -> None:
    with open(filename, 'wb') as f:
        f.write(private_key_to_bytes(private_key))


def certificate_to_bytes(certificate) -> bytes:
    return certificate.public_bytes(serialization.Encoding.PEM)


def certificate_to_pem(certificate, filename: str) -> None:
    with open(filename, 'wb') as f:
        f.write(certificate_to_bytes(certificate))
