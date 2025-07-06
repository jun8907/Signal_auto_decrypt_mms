import os
import base64, hmac, hashlib
from Crypto.Cipher import AES
from descrypt_key import get_sqlcipher_key
from modernkey import get_modernkey_base64
from data_random import get_data_randoms
import magic  

def derive_aes_key(modern_key_bytes, data_random_bytes):
    return hmac.new(modern_key_bytes, data_random_bytes, hashlib.sha256).digest()

def decrypt_mms_file(input_path, key):
    iv = b"\x00" * 16
    cipher = AES.new(key, AES.MODE_CTR, initial_value=iv, nonce=b"")

    with open(input_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def get_file_extension(decrypted_data):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(decrypted_data)

    ext_map = {
    'image/jpeg': '.jpg',
    'application/pdf': '.pdf',
    'application/zip': '.zip',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/x-hwp': '.hwp',
    'text/plain': '.txt',    
    'video/mp4': '.mp4',
    'video/quicktime': '.mov'
    }

    return ext_map.get(mime_type, '.bin')  

if __name__ == "__main__":
    modernkey_b64 = get_modernkey_base64(
        "extracted_files/persistent.sqlite",
        "extracted_files/org.thoughtcrime.securesms_preferences.xml"
    )
    if not modernkey_b64:
        print("[!] ModernKey 추출 실패")
        exit(1)

    modernkey_b64 += "=" * ((4 - len(modernkey_b64) % 4) % 4)
    modernkey_bytes = base64.b64decode(modernkey_b64)

    sqlcipher_key = get_sqlcipher_key()
    if not sqlcipher_key:
        print("[!] SQLCipher 키 복호화 실패")
        exit(1)

    mms_dir = "mms_files"
    des_dir = "des_mms_files"
    os.makedirs(des_dir, exist_ok=True)

    data_random_list = get_data_randoms("extracted_files/signal.db", sqlcipher_key, mms_dir)

    print(f"[+] 총 {len(data_random_list)}개 .mms 파일 복호화 중...")

    for filename, data_random in data_random_list:
        input_path = os.path.join(mms_dir, filename)
        derived_key = derive_aes_key(modernkey_bytes, data_random)
        decrypted_data = decrypt_mms_file(input_path, derived_key)

        extension = get_file_extension(decrypted_data)
        output_path = os.path.join(des_dir, filename + extension)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        print(f"[+] {filename} → 복호화 완료 → {output_path}")
