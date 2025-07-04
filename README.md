# Signal MMS Decryptor 🔐

📷 복호화되지 않은 Signal .mms 파일을 modernKey + data_random 기반으로 복호화하는 도구입니다.

## 🔧 기능

- Signal의 `persistent.sqlite` + `preferences.xml`로부터 modernKey 복호화
- signal.db에서 .mms 파일에 대응하는 `data_random` 추출
- modernKey + data_random → AES 키 생성 (HMAC-SHA256)
- AES-CTR 모드로 `.mms` 복호화 후 `.jpg` 저장

## 🧪 사용법

```bash
python decrypt_mms_files.py
