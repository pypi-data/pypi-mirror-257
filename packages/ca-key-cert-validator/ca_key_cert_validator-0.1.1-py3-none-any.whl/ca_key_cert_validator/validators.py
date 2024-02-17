from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from .sctructures import PrivateKey, Certificate
from .loaders import load_key_from_bytes, load_cert_from_bytes
from .savers import private_key_to_bytes, private_key_to_bytes_with_password, certificate_to_bytes
from . import expections


def validate_key(key: rsa.RSAPrivateKey, password: bytes = None) -> PrivateKey:
    return PrivateKey(
        key=key,
        key_identifier=x509.SubjectKeyIdentifier.from_public_key(key.public_key()).key_identifier.hex(),
        key_type='RSA',
        key_size=key.key_size,
        data=private_key_to_bytes(key) if not password else private_key_to_bytes_with_password(
            key,
            password
        ),
        password=password
    )


def validate_key_from_bytes(data: bytes, password: bytes = None) -> PrivateKey:
    return validate_key(
        load_key_from_bytes(data, password),
        password
    )


def validate_certificate_ca_constraint(certificate: x509.Certificate) -> None:
    if not certificate.extensions.get_extension_for_class(x509.BasicConstraints).value.ca:
        raise expections.CertificateIsNotCAValidationError()


def validate_certificate(
        certificate: x509.Certificate,
        key: rsa.RSAPrivateKey
) -> Certificate:
    # match the certificate with the key comparing public keys
    if certificate.public_key() != key.public_key():
        raise expections.CertificateNotMatchKeyValidationError()

    # validate certificate signature with the key
    try:
        key.public_key().verify(
            signature=certificate.signature,
            data=certificate.tbs_certificate_bytes,
            padding=padding.PKCS1v15(),
            algorithm=certificate.signature_hash_algorithm
        )
    except InvalidSignature:
        raise expections.CertificateSignatureValidationError()

    validate_certificate_ca_constraint(certificate)

    return Certificate(
        certificate=certificate,
        data=certificate_to_bytes(certificate),
        subject=str(certificate.subject),
        issuer=str(certificate.issuer),
        not_valid_before=certificate.not_valid_before,
        not_valid_after=certificate.not_valid_after,
        serial_number=certificate.serial_number,
        subject_key_identifier=x509.SubjectKeyIdentifier.from_public_key(
            certificate.public_key()
        ).key_identifier.hex(),
        authority_key_identifier=x509.AuthorityKeyIdentifier.from_issuer_public_key(
            certificate.public_key()
        ).key_identifier.hex()
    )


def validate_certificate_from_bytes(data: bytes, key: rsa.RSAPrivateKey) -> Certificate:
    return validate_certificate(
        load_cert_from_bytes(data),
        key
    )
