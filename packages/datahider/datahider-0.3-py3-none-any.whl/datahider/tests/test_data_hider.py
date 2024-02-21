import base64
import boto3
import pytest
import uuid
import re
from datahider import DataHider

@pytest.fixture
def random_key_name():
    random_id = str(uuid.uuid4())
    return f"data_hider_test_{random_id}"


def test_encrypt_data_returns_base64_without_exception(random_key_name):
    data_hider_instance = DataHider(keyname=random_key_name, session=boto3.Session())
    data_to_encrypt = {"user": "John Doe", "age": 25, "city": "Example City"}

    def is_base64(original: str) -> bool:
        raw_data: bytes = base64.urlsafe_b64decode(original)
        re_encoded: str = base64.urlsafe_b64encode(raw_data).decode("utf-8")

        print(f"\nOriginal\n {original}\nEncoded:\n {re_encoded}")

        return re_encoded == original

    try:
        encrypted = data_hider_instance.encrypt_and_base64(data_to_encrypt)
        assert isinstance(encrypted, str)
        if not is_base64(encrypted):
            pytest.fail(f"Output was not base64 encoded: {encrypted}")

    except Exception as e:
        pytest.fail(f"Encrypting data raised an exception: {e}")


def test_decrypt_returns_equal_data(random_key_name):
    data_hider_instance = DataHider(keyname=random_key_name, session=boto3.Session())
    data_to_encrypt = {"user": "John Doe", "age": 25, "city": "Example City"}

    encrypted_data_base64 = data_hider_instance.encrypt_and_base64(data_to_encrypt)

    try:
        decrypted_data = data_hider_instance.decrypt_base64_blob(encrypted_data_base64)
        assert decrypted_data == data_to_encrypt
    except Exception as e:
        pytest.fail(f"Decrypting data raised an exception: {e}")


def test_remove_key_without_exception(random_key_name):
    data_hider_instance = DataHider(keyname=random_key_name, session=boto3.Session())

    try:
        data_hider_instance.dangerous_remove_key_you_will_lose_data()
    except Exception as e:
        pytest.fail(f"Removing the key raised an exception: {e}")


def test_remake_key_fails(random_key_name):
    with pytest.raises(Exception, match=re.escape("An error occurred (InvalidRequestException) when calling the GetSecretValue operation: You can't perform this operation on the secret because it was marked for deletion.")):

        data_hider_instance = DataHider(keyname=random_key_name, session=boto3.Session())

        data_hider_instance.dangerous_remove_key_you_will_lose_data()

        # Remake the key
        data_hider_instance2 = DataHider(keyname=random_key_name)