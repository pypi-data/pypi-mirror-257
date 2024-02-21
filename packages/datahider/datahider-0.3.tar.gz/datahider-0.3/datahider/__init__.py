import json
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

class DataHider:
    def __init__(self, keyname: str, session: boto3.Session):
        """
        Creates a new DataHider. Immediately loads the private key and caches it.
        :param keyname: The name of the key stored in AWS secrets manager
        """
        self.secrets_manager: BaseClient = session.client("secretsmanager")
        self.keyname = keyname

        # Helper function always returns a valid encryption key (or else it throws)
        # Defined as a nested function because python does not have a `private` keyword
        def get_key_or_create_if_not_exists(name: str) -> bytes:
            try:
                # Attempt to get the existing key
                key: str = self.secrets_manager.get_secret_value(SecretId=name)['SecretString']
                return key.encode() # return as `bytes`
            except ClientError as e:
                # If key is not found, generate a random key and store it

                # Boto3 exceptions are dynamically generated. This won't work:
                # except ResourceNotFoundException as e:
                # therefore, this manual workaround is required.
                if 'ResourceNotFoundException' == e.__class__.__name__:
                    key: bytes = Fernet.generate_key()
                    self.secrets_manager.create_secret(Name=name, SecretString=key.decode('utf-8'))
                    return key
                else:
                    raise e

        self.crypto = Fernet(get_key_or_create_if_not_exists(keyname))

    def dangerous_remove_key_you_will_lose_data(self):
        """Remove the key from secrets manager"""
        self.secrets_manager.delete_secret(SecretId=self.keyname)

    def encrypt_and_base64(self, data: any) -> str:
        """
        Encrypts the given data and base64 encodes that encrypted blob.
        :param data: The data to be encrypted
        :return: base64 encoded, encrypted data
        """

        # serialize the data into a string
        serialized_data: str = json.dumps(data)

        # encode: tell python to interpret the string as an array of bytes
        serialized_bytes: bytes = serialized_data.encode()

        # encrypt: encrypt the data (Fernet outputs base64)
        encrypted_data: bytes = self.crypto.encrypt(serialized_bytes)

        # decode: tell python to interpret the array of bytes as utf8
        return encrypted_data.decode('utf-8')  # tell python that the bytes are utf8

    def decrypt_base64_blob(self, encrypted_string_base64: str) -> any:
        """
        Decrypts the base64 encoded encrypted data
        :param encrypted_string_base64: The base64 encoded, encrypted data
        :return: The decrypted data
        """

        # encode: tell python to interpret the string as array of bytes
        encrypted_bytes: bytes = encrypted_string_base64.encode()

        # decrypt: decrypt the data
        decrypted_bytes: bytes = self.crypto.decrypt(encrypted_bytes)

        # decode: tell python to interpret the array of bytes as utf8
        serialized_data: str = decrypted_bytes.decode('utf-8')
        data = json.loads(serialized_data)
        return data
