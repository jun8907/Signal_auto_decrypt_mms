# Signal MMS Decryptor 🔐

복호화되지 않은 Signal .mms 파일을 복호화하는 코드입니다.

## 🔧 코드 설명

- pull.py
- preferences_attachment.py
- preferences_database.py
- persistent.py
- modernkey.py
- descrypt_key.py
- data_random.py
- aes_key.py
- descrypt_mms_files.py

### pull.py
루팅된 Android 디바이스에서 Signal 메신저의 .mms 임시파일 및 복호화에 필요한 핵심 파일들을 자동으로 추출하는 코드입니다.
.mms 임시파일은 mms_files/ 디렉터리에 저장
복호화에 필요한 파일들은 extracted_files/ 디렉터리에 저장

```bash
[실행 결과]
[*] .mms 파일 목록 수집 중...
[+] 총 5개의 .mms 파일 발견됨
[*] /data/data/org.thoughtcrime.securesms/app_parts/part1290661725492059278.mms 추출 중...
/sdcard/part1290661725492059278.mms: 1 file pulled, 0 skipped. 0.9 MB/s (101562 bytes in 0.105s)
[*] /data/data/org.thoughtcrime.securesms/app_parts/part1341555342137450792.mms 추출 중...
/sdcard/part1341555342137450792.mms: 1 file pulled, 0 skipped. 11.8 MB/s (101499 bytes in 0.008s)
[*] /data/data/org.thoughtcrime.securesms/app_parts/part3288898270585642176.mms 추출 중...
/sdcard/part3288898270585642176.mms: 1 file pulled, 0 skipped. 2.6 MB/s (100497 bytes in 0.037s)
[*] /data/data/org.thoughtcrime.securesms/app_parts/part6570248723912832133.mms 추출 중...
/sdcard/part6570248723912832133.mms: 1 file pulled, 0 skipped. 4.2 MB/s (100904 bytes in 0.023s)
[*] /data/data/org.thoughtcrime.securesms/app_parts/part8371684658587393699.mms 추출 중...
/sdcard/part8371684658587393699.mms: 1 file pulled, 0 skipped. 5.4 MB/s (100772 bytes in 0.018s)
[+] .mms 파일 추출 완료
[*] /data/data/org.thoughtcrime.securesms/shared_prefs/org.thoughtcrime.securesms_preferences.xml 추출 중...
/sdcard/org.thoughtcrime.securesms_preferences.xml: 1 file pulled, 0 skipped. 0.1 MB/s (2142 bytes in 0.020s)     
[*] /data/data/org.thoughtcrime.securesms/databases/signal.db 추출 중...
/sdcard/signal.db: 1 file pulled, 0 skipped. 17.9 MB/s (3219456 bytes in 0.172s)
[*] /data/misc/keystore/persistent.sqlite 추출 중...
/sdcard/persistent.sqlite: 1 file pulled, 0 skipped. 10.1 MB/s (139264 bytes in 0.013s)
[+] 설정, DB, keystore 파일 추출 완료

### preferences_attachment, database.py
Signal 메신저의 /share_pref/org.thoughtcrime.securesms_preferences.xml 파일에서 SQLCipher에 사용된 패스프레이즈를 추출
- data (hex)
- input (hex)
- GCM Tag (hex)
- iv (base64)

```bash
[실행 결과]
[+] data (hex)       : 7d7db165c6054cb75bee9c5f98c9ef94e694a17231b0e8145a4c5e31b71cb1bb1cd5fd259b07db76d62b7f8238af4ea4
[+] ciphertext (hex) : 7d7db165c6054cb75bee9c5f98c9ef94e694a17231b0e8145a4c5e31b71cb1bb
[+] GCM tag (hex)    : 1cd5fd259b07db76d62b7f8238af4ea4
[+] iv (base64)      : bfOgEB/EMhcm8rOh

[DEBUG] 원본 값: {"data":"TRrne31FUkeP3Oz5e9Zb0MBeqjJ41LrmJwcoeqRaeCq/W8x8Zq7xlKK0c11UxcOCrYG8ruMozbSO8IIMKhUKtKZ2kyeaJ8ALwUY7eVhl5HR9CSfaRff7m0ANThnNoEb4s6yrJoSPL5tJP0wXmSVXdCL8igY2THa5","iv":"lYnYAg0sCNKCH0Dg"}
[+] data (base64): TRrne31FUkeP3Oz5e9Zb0MBeqjJ41LrmJwcoeqRaeCq/W8x8Zq7xlKK0c11UxcOCrYG8ruMozbSO8IIMKhUKtKZ2kyeaJ8ALwUY7eVhl5HR9CSfaRff7m0ANThnNoEb4s6yrJoSPL5tJP0wXmSVXdCL8igY2THa5
[+] iv   (base64): lYnYAg0sCNKCH0Dg
[+] data (decoded, hex): 4d1ae77b7d4552478fdcecf97bd65bd0c05eaa3278d4bae62707287aa45a782abf5bcc7c66aef194a2b4735d54c5c382ad81bcaee328cdb48ef0820c2a150ab4a67693279a27c00bc1463b795865e4747d0927da45f7fb9b400d4e19cda046f8b3acab26848f2f9b493f4c179925577422fc8a06364c76b9
[+] GCM Tag (hex): 493f4c179925577422fc8a06364c76b9
[+] Ciphertext (input, hex): 4d1ae77b7d4552478fdcecf97bd65bd0c05eaa3278d4bae62707287aa45a782abf5bcc7c66aef194a2b4735d54c5c382ad81bcaee328cdb48ef0820c2a150ab4a67693279a27c00bc1463b795865e4747d0927da45f7fb9b400d4e19cda046f8b3acab26848f2f9b

## 🧪 사용법

```bash
python pull.py
python decrypt_mms_files.py
