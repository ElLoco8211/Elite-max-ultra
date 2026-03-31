import time
import subprocess

while True:
    print("🚀 Scan in corso...")
    
    subprocess.run(["python", "main.py"])
    
    print("⏳ Attendo 5 minuti...\n")
    time.sleep(300)
