from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

private_path = r"D:\LLM_application\llm_flask\models\keys\private_key.pem"
public_path = r"D:\LLM_application\llm_flask\models\keys\public_key.pem"

def generate_keys(private_key_path=private_path, public_key_path=public_path):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key = private_key.public_key()
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open(private_key_path, 'wb') as f:
        f.write(private_key_pem)
    
    with open(public_key_path, 'wb') as f:
        f.write(public_key_pem)

def load_private_key(private_key_path=private_path):
    with open(private_key_path, 'rb') as f:
        return f.read()

def load_public_key(public_key_path=public_path):
    with open(public_key_path, 'rb') as f:
        return f.read()
    
if __name__ == "__main__":
    private_path = r"D:\LLM_application\llm_flask\models\keys\private_key.pem"
    public_path = r"D:\LLM_application\llm_flask\models\keys\public_key.pem"
    generate_keys(private_key_path=private_path, public_key_path=public_path)

    print(load_private_key(private_key_path=private_path))
    print(load_public_key(public_key_path=public_path))