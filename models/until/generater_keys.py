import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from ..config import private_path, public_path


def generate_keys(private_key_path=private_path, public_key_path=public_path):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serialize private key
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Generate public key from private key
    public_key = private_key.public_key()
    
    # Serialize public key
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write private key to file
    with open(private_key_path, 'wb') as f:
        f.write(private_key_pem)
    
    # Write public key to file
    with open(public_key_path, 'wb') as f:
        f.write(public_key_pem)
def load_key(key_path):
    if os.path.exists(key_path):
        with open(key_path, 'rb') as f:
            return f.read()
    return None

def get_keys(private_key_path=private_path, public_key_path=public_path):
    try:
        private_key_pem = load_key(private_key_path)
        public_key_pem = load_key(public_key_path)
        
        if private_key_pem is None or public_key_pem is None:
            private_key_pem, public_key_pem = generate_keys()
        # print(private_path,)
        # print(public_key_pem)
        return private_key_pem, public_key_pem
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
    
if __name__ == "__main__":
    private_key, public_key =get_keys()
    print(private_key)
    print(public_key)