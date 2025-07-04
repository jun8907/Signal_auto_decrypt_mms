# modernkey.py
import base64
import json
from Crypto.Cipher import AES
from preferences_attachment import extract_pref_attachment_secret
from persistent import extract_all_signalsecret_keys

def decrypt_modernkey(persistent_db_path, xml_path):
    modern_key_b64 = get_modernkey_base64(persistent_db_path, xml_path)
    if modern_key_b64:
        print(f"[+] modernKey (base64): {modern_key_b64}")
    else:
        print("[!] modernKey 복호화 실패")

def get_modernkey_base64(persistent_db_path, xml_path):
    keys = extract_all_signalsecret_keys(persistent_db_path)
    if len(keys) < 2:
        print("[!] 복호화 키가 부족합니다.")
        return None

    data_base64, iv_base64 = extract_pref_attachment_secret(xml_path)
    if not data_base64 or not iv_base64:
        print("[!] preferences 정보 추출 실패")
        return None

    data_bytes = base64.b64decode(data_base64)
    iv_bytes = base64.b64decode(iv_base64)
    ciphertext = data_bytes[:-16]
    tag = data_bytes[-16:]

    for i, key in enumerate(keys):
        try:
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv_bytes)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            modern_key_b64 = json.loads(plaintext.decode())["modernKey"]
            return modern_key_b64
        except Exception as e:
            continue

    return None

if __name__ == "__main__":
    decrypt_modernkey("extracted_files/persistent.sqlite", "extracted_files/org.thoughtcrime.securesms_preferences.xml")
