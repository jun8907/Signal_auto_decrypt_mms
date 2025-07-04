import os
import subprocess


APP_PARTS_DIR = "/data/data/org.thoughtcrime.securesms/app_parts/"
LOCAL_MMS_DIR = "mms_files"
LOCAL_EXTRA_DIR = "extracted_files"


EXTRACTION_TARGETS = {
    "preferences": "/data/data/org.thoughtcrime.securesms/shared_prefs/org.thoughtcrime.securesms_preferences.xml",
    "signal_db": "/data/data/org.thoughtcrime.securesms/databases/signal.db",
    "keystore": "/data/misc/keystore/persistent.sqlite"
}

def run_shell_cmd(cmd):
    return subprocess.run(["adb", "shell", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def su_cp(remote_path, local_path):
    print(f"[*] {remote_path} 추출 중...")
    temp_path = f"/sdcard/{os.path.basename(remote_path)}"

    
    run_shell_cmd(f"su -c 'cp {remote_path} {temp_path}'")

    
    subprocess.run(["adb", "pull", temp_path, local_path])

    
    run_shell_cmd(f"rm {temp_path}")

def extract_all_mms():
    os.makedirs(LOCAL_MMS_DIR, exist_ok=True)

    print("[*] .mms 파일 목록 수집 중...")
    result = run_shell_cmd(f"su -c 'ls {APP_PARTS_DIR}'")
    files = result.stdout.strip().split('\n')
    mms_files = [f for f in files if f.endswith(".mms")]

    print(f"[+] 총 {len(mms_files)}개의 .mms 파일 발견됨")

    for filename in mms_files:
        remote_path = os.path.join(APP_PARTS_DIR, filename)
        local_path = os.path.join(LOCAL_MMS_DIR, filename)
        su_cp(remote_path, local_path)

    print("[+] .mms 파일 추출 완료")

def extract_additional_files():
    os.makedirs(LOCAL_EXTRA_DIR, exist_ok=True)

    for key, remote_path in EXTRACTION_TARGETS.items():
        local_path = os.path.join(LOCAL_EXTRA_DIR, os.path.basename(remote_path))
        su_cp(remote_path, local_path)

    print("[+] 설정, DB, keystore 파일 추출 완료")

if __name__ == "__main__":
    extract_all_mms()
    extract_additional_files()
