# Signal_auto_descrypt_mms 🔐

복호화되지 않은 Signal .mms 파일을 복호화하는 코드입니다.

<br><br>

## 🧪 사용법

```bash
git clone https://github.com/jun8907/Signal_auto_descrypt_mms.git
cd Signal_auto_descrypt_mms
python pull.py
python decrypt_mms_files.py
```

<br><br>

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
<br><br>
### pull.py

루팅된 Android 디바이스에서 Signal 메신저의 .mms 임시파일 및 복호화에 필요한 핵심 파일들을 자동으로 추출하는 코드입니다.
.mms 임시파일은 `mms_files/` 디렉터리에 저장
복호화에 필요한 파일들은 `extracted_files/` 디렉터리에 저장

```python
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
```

### preferences_attachment, database.py

Signal 메신저의 /share_pref/org.thoughtcrime.securesms_preferences.xml 파일에서 SQLCipher에 사용된 패스프레이즈를 추출
- `data (hex)`
- `input (hex)`
- `GCM Tag (hex)`
- `iv (base64)`

```python
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
```

### persistent.py

Android 기기에서 추출한 Signal 메신저의 `persistent.sqlite` 키스토어 DB에서 `SignalSecret` alias에 해당하는 복호화 키(16바이트)를 자동으로 추출하는 코드입니다.

```python
[실행 결과]
[+] SignalSecret #1 id: 7284520658499830241
    → 추출된 복호화 키 (16바이트 hex): d1ccc1ae4d0e3a5ef0b1074794e076b7
[+] SignalSecret #2 id: 6456924783388765775
    → 추출된 복호화 키 (16바이트 hex): d843d662011f92d82c69659c4311904f
```

### modernkey.py

Signal 메신저의 설정 파일과 키 저장소를 이용하여, 첨부파일(.mms 등) 복호화에 사용되는 `modernKey` 값을 자동으로 복호화하고 출력

```python
[실행 결과]
[+] modernKey (base64): HQO/GTzksS8QwavfHEsHUFCzQeAadbAI3vFEERRNkQQ
```

### data_random

Signal 메신저 데이터베이스(signal.db)에서 첨부파일 복호화에 필요한 `data_random` 값을 추출합니다. 추출된 `data_random`은 `modernKey`와 함께 HMAC-SHA256을 이용해 AES 복호화 키를 생성하는 데 사용됩니다.

```python
[실행 결과]
[*] SignalSecret #1 복호화 시도 중...

[*] SignalSecret #2 복호화 시도 중...
[+] 복호화 성공! SQLCipher Key (hex): 9a177c5296dedc24cf72cd563c39d3234e616f4ab2c596696ed27411d65fde94
[+] part1290661725492059278.mms → data_random (hex): 46e90c13603a4de1c4f6cfaa4f0779000e8ab32c131e85409b75e9655f1e698f
[+] part3288898270585642176.mms → data_random (hex): 53c69075ce255f1260a31d7297c6dda88cfa2b1dd87dc07522c1c724d908c4dc
[+] part1341555342137450792.mms → data_random (hex): f5c03eb1245fbbcb7926127a94f403e583bc9f93a140e862847b7244a0b8c393
[+] part8371684658587393699.mms → data_random (hex): 2158157cafcfa52e463160da8173631786ea5e699b485bdacacbf4e4768c7ddb
[+] part6570248723912832133.mms → data_random (hex): 85e5761071da3b8b2211d1a218ba58b1c45857f1cc081534d3e744d1e44a9ccd
[+] 매칭된 mms 파일 수: 5
```

### aes_key.py

Signal 메신저에서 전송된 .mms 임시파일을 복호화하기 위한 AES 키 ****를 자동으로 파생합니다.

modernKey, data_random, 그리고 HMAC-SHA256 알고리즘을 통해 각 파일에 대응되는 256비트 AES 키를 생성합니다.

```python
[실행 결과]
[+] 총 5개 .mms 파일의 AES 키:
 - part1290661725492059278.mms → AES Key: 7030973f5dfc4dec52d547ed3ce68cc0c0168a70c08b83c8bb8476904576304a        
 - part3288898270585642176.mms → AES Key: 6a75f6f119a149afc939e4c86f1516806e0de5fb92b83bf5a79d2a8e8e548543        
 - part1341555342137450792.mms → AES Key: f579509c5f94f30da8fcec830dee69d5162b110930197dce2aa20a3a0c07855d        
 - part8371684658587393699.mms → AES Key: 0550d123e5c488704b005cbc3a8b25ea34edbc19038d5bf7a1cf750dd9edc3ab        
 - part6570248723912832133.mms → AES Key: 6b65b8362775873002770e3fb94c3fb9a493aa17113cc85f73607e368f29c3cb
```

### descrypt_mms_files.py

Signal 메신저의 암호화된 `.mms` 첨부파일을 자동으로 복호화하여 원본 이미지 파일(.jpg)로 복원해주는 코드입니다.

복원된 원본 이미지 파일은 des_mms_files/ 디렉터리에 저장

```python
[실행 결과]
[+] 총 5개 .mms 파일 복호화 중...
[+] part1290661725492059278.mms → 복호화 완료 → des_mms_files\part1290661725492059278.mms.jpg
[+] part3288898270585642176.mms → 복호화 완료 → des_mms_files\part3288898270585642176.mms.jpg
[+] part1341555342137450792.mms → 복호화 완료 → des_mms_files\part1341555342137450792.mms.jpg
[+] part8371684658587393699.mms → 복호화 완료 → des_mms_files\part8371684658587393699.mms.jpg
[+] part6570248723912832133.mms → 복호화 완료 → des_mms_files\part6570248723912832133.mms.jpg
```

