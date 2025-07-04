import xml.etree.ElementTree as ET
import json
import base64

def extract_pref_attachment_secret(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for elem in root.findall("string"):
        if elem.attrib.get("name") == "pref_attachment_encrypted_secret":
            raw_value = elem.text.strip()
            print(f"[DEBUG] 원본 값: {raw_value}")

            try:
                json_data = json.loads(raw_value)
                data_base64 = json_data["data"]
                iv_base64 = json_data["iv"]
            except Exception as e:
                print(f"[!] JSON 파싱 오류: {e}")
                return None, None

            print(f"[+] data (base64): {data_base64}")
            print(f"[+] iv   (base64): {iv_base64}")

            try:
                data_bytes = base64.b64decode(data_base64)
                print(f"[+] data (decoded, hex): {data_bytes.hex()}")

                if len(data_bytes) <= 16:
                    print("[!] data 길이가 너무 짧아 GCM tag 분리 불가")
                    return data_base64, iv_base64

                gcm_tag = data_bytes[-16:]
                ciphertext = data_bytes[:-16]

                print(f"[+] GCM Tag (hex): {gcm_tag.hex()}")
                print(f"[+] Ciphertext (input, hex): {ciphertext.hex()}")

            except Exception as e:
                print(f"[!] base64 디코딩 오류 (data): {e}")

            return data_base64, iv_base64

    print("[!] pref_attachment_encrypted_secret 항목을 찾을 수 없습니다.")
    return None, None

if __name__ == "__main__":
    xml_file = "extracted_files/org.thoughtcrime.securesms_preferences.xml"
    extract_pref_attachment_secret(xml_file)
