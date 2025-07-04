import base64, hmac, hashlib
from descrypt_key import get_sqlcipher_key
from modernkey import get_modernkey_base64
from data_random import get_data_randoms

def derive_aes_key(modern_key_bytes, data_random_bytes):
    return hmac.new(modern_key_bytes, data_random_bytes, hashlib.sha256).digest()

if __name__ == "__main__":
    modernkey_b64 = get_modernkey_base64(
        "extracted_files/persistent.sqlite",
        "extracted_files/org.thoughtcrime.securesms_preferences.xml"
    )
    if not modernkey_b64:
        print("[!] modernKey 추출 실패")
        exit(1)


    modernkey_b64 += "=" * ((4 - len(modernkey_b64) % 4) % 4)
    modernkey_bytes = base64.b64decode(modernkey_b64)

    sqlcipher_key = get_sqlcipher_key()
    if not sqlcipher_key:
        print("[!] SQLCipher 키 복호화 실패")
        exit(1)

    data_random_list = get_data_randoms(
        "extracted_files/signal.db",
        sqlcipher_key,
        "mms_files"
    )

    print(f"[+] 총 {len(data_random_list)}개 .mms 파일의 AES 키:")
    for filename, data_random in data_random_list:
        aes_key = derive_aes_key(modernkey_bytes, data_random)
        print(f" - {filename} → AES Key: {aes_key.hex()}")
