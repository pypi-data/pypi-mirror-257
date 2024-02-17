from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa


@dataclass
class PrivateKey:
    key: rsa.RSAPrivateKey
    key_identifier: str
    key_type: str
    key_size: int
    data: bytes
    password: Optional[bytes] = None


@dataclass
class Certificate:
    certificate: x509.Certificate
    data: bytes
    subject: str
    issuer: str
    subject_key_identifier: str
    authority_key_identifier: str
    not_valid_before: datetime
    not_valid_after: datetime
    serial_number: int
