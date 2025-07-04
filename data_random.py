# data_random.py
from sqlcipher3 import dbapi2 as sqlcipher
import os
from descrypt_key import get_sqlcipher_key

def extract_data_random_for_mms(encrypted_db_path, key_plaintext, mms_folder):
    results = get_data_randoms(encrypted_db_path, key_plaintext, mms_folder)
    for filename, data_random in results:
        print(f"[+] {filename} → data_random (hex): {data_random.hex()}")
    print(f"[+] 매칭된 mms 파일 수: {len(results)}")

def get_data_randoms(encrypted_db_path, key_plaintext, mms_folder):
    try:
        conn = sqlcipher.connect(encrypted_db_path)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA key = '{key_plaintext}';")
        cursor.execute("PRAGMA cipher_page_size = 4096;")
        cursor.execute("PRAGMA kdf_iter = 1;")
        cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1;")
        cursor.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1;")
        cursor.execute("SELECT count(*) FROM sqlite_master;")

        mms_filenames = set(os.listdir(mms_folder))
        cursor.execute("SELECT data_file, data_random FROM attachment WHERE data_random IS NOT NULL")
        rows = cursor.fetchall()

        matched = []
        for data_file_path, data_random in rows:
            db_filename = os.path.basename(data_file_path)
            if db_filename in mms_filenames:
                matched.append((db_filename, data_random))

        conn.close()
        return matched

    except Exception as e:
        print(f"[!] 오류 발생: {e}")
        return []

if __name__ == "__main__":
    sqlcipher_plaintext_key = get_sqlcipher_key()
    if sqlcipher_plaintext_key is None:
        print("[!] SQLCipher 키 복호화 실패, 프로그램 종료")
        exit(1)

    mms_dir = "mms_files"
    encrypted_db = "extracted_files/signal.db"
    extract_data_random_for_mms(encrypted_db, sqlcipher_plaintext_key, mms_dir)
