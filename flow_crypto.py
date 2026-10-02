import base64
import json
import os

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


PRIVATE_KEY_PATH = os.path.join(
    os.path.dirname(__file__),
    "flow_private.pem"
)


def load_private_key():
    """
    Load the encrypted PKCS#1 RSA private key.
    """

    passphrase = os.getenv("FLOW_PASSPHRASE")

    if not passphrase:
        raise RuntimeError(
            "FLOW_PASSPHRASE environment variable is missing"
        )

    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key_data = key_file.read()

    return RSA.import_key(
        private_key_data,
        passphrase=passphrase
    )


def decrypt_request(
    encrypted_aes_key,
    encrypted_flow_data,
    initial_vector
):
    """
    Decrypt a WhatsApp Flow request.

    Returns:
        decrypted_body
        aes_key
        iv
    """

    # -----------------------------------------
    # LOAD RSA PRIVATE KEY
    # -----------------------------------------

    private_key = load_private_key()

    # -----------------------------------------
    # DECODE ENCRYPTED AES KEY
    # -----------------------------------------

    encrypted_aes_key_bytes = base64.b64decode(
        encrypted_aes_key
    )

    # -----------------------------------------
    # RSA-OAEP / SHA-256
    # -----------------------------------------

    rsa_cipher = PKCS1_OAEP.new(
        private_key,
        hashAlgo=SHA256
    )

    aes_key = rsa_cipher.decrypt(
        encrypted_aes_key_bytes
    )

    # -----------------------------------------
    # DECODE FLOW DATA
    # -----------------------------------------

    encrypted_flow_data_bytes = base64.b64decode(
        encrypted_flow_data
    )

    iv = base64.b64decode(
        initial_vector
    )

    # -----------------------------------------
    # AES-GCM
    # -----------------------------------------

    aes_cipher = AES.new(
        aes_key,
        AES.MODE_GCM,
        nonce=iv
    )

    # Last 16 bytes = authentication tag
    ciphertext = encrypted_flow_data_bytes[:-16]
    auth_tag = encrypted_flow_data_bytes[-16:]

    decrypted_data = aes_cipher.decrypt_and_verify(
        ciphertext,
        auth_tag
    )

    decrypted_body = json.loads(
        decrypted_data.decode("utf-8")
    )

    return decrypted_body, aes_key, iv


def encrypt_response(
    response_data,
    aes_key,
    iv
):
    """
    Encrypt the response sent back to WhatsApp.

    Meta's Flow endpoint protocol uses
    a bitwise-flipped IV for the response.
    """

    response_json = json.dumps(
        response_data,
        separators=(",", ":")
    ).encode("utf-8")

    # -----------------------------------------
    # FLIP IV
    # -----------------------------------------

    flipped_iv = bytes(
        byte ^ 0xFF
        for byte in iv
    )

    # -----------------------------------------
    # AES-GCM
    # -----------------------------------------

    aes_cipher = AES.new(
        aes_key,
        AES.MODE_GCM,
        nonce=flipped_iv
    )

    encrypted_data, auth_tag = (
        aes_cipher.encrypt_and_digest(
            response_json
        )
    )

    encrypted_payload = (
        encrypted_data + auth_tag
    )

    # -----------------------------------------
    # BASE64 RESPONSE
    # -----------------------------------------

    return base64.b64encode(
        encrypted_payload
    ).decode("utf-8")