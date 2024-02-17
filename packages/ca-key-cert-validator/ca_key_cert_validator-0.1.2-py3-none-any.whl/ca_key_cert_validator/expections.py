
class ValidationError(Exception):
    MESSAGE = 'Validation error'

    def __init__(self, message=None):
        self.message = message or self.MESSAGE
        super().__init__(self.message)


class KeyValidationError(ValidationError):
    MESSAGE = 'Key validation error'


class KeyIncorrectPasswordValidationError(KeyValidationError):
    MESSAGE = 'Key incorrect password'


class KeyInvalidFormatValidationError(KeyValidationError):
    MESSAGE = 'Key invalid format'


class KeyIsNotEncryptedValidationError(KeyValidationError):
    MESSAGE = 'Password was given but private key is not encrypted'


class KeyIsEncryptedValidationError(KeyValidationError):
    MESSAGE = 'Password was not given but private key is encrypted'


class CertificateValidationError(ValidationError):
    MESSAGE = 'Certificate validation error'


class CertificateInvalidFormatValidationError(CertificateValidationError):
    MESSAGE = 'Certificate invalid format'


class CertificateNotMatchKeyValidationError(CertificateValidationError):
    MESSAGE = 'Certificate does not match key'


class CertificateSignatureValidationError(CertificateValidationError):
    MESSAGE = 'Certificate signature validation error'


class CertificateIsNotCAValidationError(CertificateValidationError):
    MESSAGE = 'Certificate is not CA'
