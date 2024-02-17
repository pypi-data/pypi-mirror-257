import httpx
import hashlib
import random
import time
import base64



from argon2 import PasswordHasher



def calculate_password_hash(data):
    ph = PasswordHasher()
    hash = ph.hash(data)
    return hash


def generate_cnonce():
    return ''.join(random.choices('abcdef0123456789', k=16))


def create_initial_request(url):
    response = httpx.get(url)
    www_authenticate_header = response.headers.get('WWW-Authenticate', '')
    # Extract necessary information from WWW-Authenticate header
    realm = www_authenticate_header.split('realm="')[1].split('"')[0]
    nonce = www_authenticate_header.split('nonce="')[1].split('"')[0]
    return realm, nonce


def create_follow_up_request(url, realm, nonce):
    username = "svc-digestupdates"
    password = "your-password"  # Replace with the actual password
    uri = "/path/to/resource"
    cnonce = generate_cnonce()
    nc = "00000001"
    qop = "auth"
    algorithm = "SHA256"
    algorithm = "SHA256"

    # Calculate the hash of A1, A2, and the final response
    A1 = f"{username}:{realm}:{password}"
    A2 = f"GET:{uri}"

    response = calculate_password_hash(f"{calculate_password_hash(A1)}:{nonce}:{nc}:{cnonce}:{qop}:{calculate_password_hash(A2)}")

    # Construct the Authorization header
    authorization_header = (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", '
        f'cnonce="{cnonce}", nc={nc}, qop={qop}, response="{response}", algorithm={algorithm}'
    )

    headers = {'Authorization': authorization_header}
    response = httpx.get(url, headers=headers)

    return response


if __name__ == "__main__":
    realm, nonce = create_initial_request()
    response = create_follow_up_request(realm, nonce)

    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)