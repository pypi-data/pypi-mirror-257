from typing import BinaryIO

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.hazmat.backends import default_backend

from . import expections


def load_key_from_bytes(data: bytes, password: bytes = None) -> PrivateKeyTypes:
    try:
        return serialization.load_pem_private_key(
            data,
            password,
            default_backend()
        )
    except ValueError as ve:
        if ve.args[0] == 'Bad decrypt. Incorrect password?':
            raise expections.KeyIncorrectPasswordValidationError()
        if ve.args[0].startswith('Could not deserialize key data'):
            raise expections.KeyInvalidFormatValidationError()
        raise expections.KeyValidationError(ve.args[0])
    except TypeError as te:
        if te.args[0] == 'Password was given but private key is not encrypted.':
            raise expections.KeyIsNotEncryptedValidationError()
        if te.args[0] == 'Password was not given but private key is encrypted':
            raise expections.KeyIsEncryptedValidationError()
        raise expections.KeyValidationError(te.args[0])


def load_key_from_file_descriptor(f: BinaryIO, password: bytes = None) -> PrivateKeyTypes:
    return load_key_from_bytes(
        f.read(),
        password
    )


def load_key_from_file(filename: str, password: bytes = None) -> PrivateKeyTypes:
    with open(filename, mode='rb') as f:
        return load_key_from_file_descriptor(f, password)


def load_cert_from_bytes(data: bytes) -> x509.Certificate:
    try:
        return x509.load_pem_x509_certificate(data, default_backend())
    except ValueError as ve:
        if ve.args[0].startswith('Unable to load PEM file'):
            raise expections.CertificateInvalidFormatValidationError()
        raise expections.CertificateValidationError(ve.args[0])


def load_cert_from_file_descriptor(f: BinaryIO) -> x509.Certificate:
    return load_cert_from_bytes(f.read())
