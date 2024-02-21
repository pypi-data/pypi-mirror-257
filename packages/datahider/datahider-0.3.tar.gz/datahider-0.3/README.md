# DataHider

A small Facade over Fernet and Boto3.

## What for

- Turn data into a string that is
  - Encrypted, meaning it can't be tampered with
  - URL safe base 64, meaning you can use it anywhere, anyway
    - It may still have ending `=`s
- Decode above such strings back into data.
- Without having to manually bother with encryption keys.

## "Data"?

Anything accepted by `json.loads`. Which means any composition according to this recursive definition: 

Data is
- Dictionary of str -> Data
- List of Data
- Tuple of Data
- Bool
- Number
- String
- None

## How not to use

### Pittfall 1: AWS marks secrets for deletion and locks them

Creating a key and then deleting it results in the keyname being "locked" by AWS:

botocore.errorfactory.InvalidRequestException: An error occurred (InvalidRequestException) when calling the GetSecretValue operation: You can't perform this operation on the secret because it was marked for deletion.

AWS Secrets Manager Secrets have a default retention (recovery window) period of 30 days after deletion to give you the chance to recover it - in case it was deleted by mistake or you change your mind. So even if it shows on the AWS console as deleted, it still exists in AWS's API records.

### Pittfall 2: private keys are cached

So maybe you set the secret retention time to 0.

**If you do that** there's something else you need to take into account.

Each DataHider object caches the encryption key. This presents susceptibility to the following scenario:

- make instance **A** with keyname **N** (which will generate a new key **K**)
- make instance **B** with keyname **N**
- delete the key using **B**
   - **A** will still encrypt and decrypt without errors as the private key is cached. But any other instance will not be able to decrypt what comes out of **A**.
- make instance **C** with keyname **N** (which will generate a new key **L**)
   - **A** will "speak a different language" compared to instance **C**:
   - **A** uses **K**, but **C** uses **L**, despite both agreeing on the key name **N**.
    
In this scenario, data loss occurs when messages encrypted by **A** are attempted to be decrypted by **C**, and vice versa.


## How to use

You need to be logged in on AWS. The encryption key is stored in AWS secrets manager.

**Example 1:** Creating an instance of DataHider

If the key already exists, it will use the existing key. If not, it will generate a new key.

```py
from datahider import DataHider

data_hider_instance = DataHider(keyname="your_key_name")
```

**Example 2:** Encrypting and Base64 Encoding Data

```py
data_to_encrypt = {"user": "John Doe", "age": 25, "city": "Example City"}
encrypted_data_base64 = data_hider_instance.encrypt_and_base64(data_to_encrypt)
print(f"Encrypted and Base64 encoded data: {encrypted_data_base64}")
```

**Example 3:** Decrypting Base64 Encoded Data

```python
decrypted_data = data_hider_instance.decrypt_base64_blob(encrypted_data_base64)
print(f"Decrypted data: {decrypted_data}")
```

**Example 4:** Removing the Key (Use with caution!)

This will delete the key from Secrets Manager. You will lose access to data encrypted with this key.

```python
remover = data_hider_instance.dangerous_remove_key_you_will_lose_data()
```

### Note: Make sure to handle exceptions appropriately in a production environment.

DataHider does not catch exceptions it can't handle. It does not define new exception classes.

## Copyright

This code is the intellectual property of Nova Technology B.V.

Unauthorized reproduction is prohibited.