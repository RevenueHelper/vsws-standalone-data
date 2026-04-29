"""
FINAL CORRECT SPLITTER — Uses real 3-digit district prefixes (101-113)
Splits ap_staff_full_backup.json into 101.json, 102.json... 113.json
Each file is a flat dict: { secCode: { secCode, secName, district, mandal, staff[] } }
"""
import json
import os

BACKUP_FILE = r'D:\android apps\vsws_standalone\ap_staff_full_backup.json'
OUTPUT_DIR  = r'D:\android apps\VSWS_HELPER\github_hub\data\districts'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading backup file... (this may take 30 seconds)")
with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total secretariats in backup: {len(data)}")

# Group by 3-digit prefix
buckets = {}
for secCode, entry in data.items():
    prefix = secCode[:3]
    if prefix not in buckets:
        buckets[prefix] = {}
    # Only keep useful keys for the app
    buckets[prefix][secCode] = {
        "secCode":   entry.get("secCode", secCode),
        "secName":   entry.get("secName", ""),
        "district":  entry.get("district", ""),
        "mandal":    entry.get("mandal", ""),
        "staff":     entry.get("staff", [])
    }

print(f"\n=== Splitting into {len(buckets)} files ===")
for prefix in sorted(buckets.keys()):
    count = len(buckets[prefix])
    out_file = os.path.join(OUTPUT_DIR, f"{prefix}.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(buckets[prefix], f, ensure_ascii=False)
    file_size_kb = os.path.getsize(out_file) // 1024
    print(f"  {prefix}.json -> {count} secretariats, {file_size_kb} KB")

print("\n✅ DONE! All files written to:", OUTPUT_DIR)
print("Upload ONLY the 3-digit named files (101.json to 113.json) to GitHub.")
print("Delete the old 01.json - 26.json files from GitHub first!")
