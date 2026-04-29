import requests
import json
import os
import time
from datetime import datetime

# Configuration
DATA_DIR = "data/districts"
API_BASE = "https://gramawardsachivalayam.ap.gov.in/GSWSDASHBOARD/api/GSWSWeb"
ATTENDANCE_API = "https://gramawardsachivalayam.ap.gov.in/attendanceReports/api/report/volunteerDetailsLevel1"
DELAY = 0.8  # 800ms delay between requests to be safe

def get_maps():
    print("📡 Building District/Mandal ID Maps...")
    dist_map = {}
    mandal_map = {}

    try:
        # Get Districts
        r = requests.post(f"{API_BASE}/LoadDashboardDistricts", json={"TYPE": "1"}, timeout=30)
        dists = r.json().get('DataList', [])
        for d in dists:
            d_name = d['DISTRICT_NAME']
            d_code = d['LGD_DIST_CODE']
            dist_map[d_name] = d_code

            # Get Mandals for this district
            time.sleep(1)
            rm = requests.post(f"{API_BASE}/LoadDashboardDistricts", json={"TYPE": "2", "DISTRICT": d_code}, timeout=30)
            mandals = rm.json().get('DataList', [])
            for m in mandals:
                m_name = m['MANDAL_NAME']
                m_code = m['LGD_MANDAL_CODE']
                # Store as (DistrictName, MandalName) -> MandalCode
                mandal_map[(d_name, m_name)] = m_code
        
        print(f"✅ Map built: {len(dist_map)} districts, {len(mandal_map)} mandals.")
        return dist_map, mandal_map
    except Exception as e:
        print(f"❌ Error building maps: {e}")
        return None, None

def sync():
    dist_map, mandal_map = get_maps()
    if not dist_map: return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json') and len(f) == 8] # 101.json etc
    total_files = len(files)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    for idx, filename in enumerate(files):
        filepath = os.path.join(DATA_DIR, filename)
        print(f"\n📂 Processing {filename} ({idx+1}/{total_files})...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            district_data = json.load(f)
        
        updated_count = 0
        for sec_code, sec_info in district_data.items():
            d_name = sec_info.get('district')
            m_name = sec_info.get('mandal')
            
            d_id = dist_map.get(d_name)
            m_id = mandal_map.get((d_name, m_name))
            
            if not d_id or not m_id:
                print(f"  ⚠️  Skipping {sec_code} (Missing ID mapping for {d_name}/{m_name})")
                continue
            
            try:
                time.sleep(DELAY)
                payload = {
                    "type": "5",
                    "districtId": str(d_id),
                    "mandalId": str(m_id),
                    "secId": str(sec_code),
                    "date": date_str
                }
                
                resp = requests.post(ATTENDANCE_API, json=payload, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
                result = resp.json().get('result', [])
                if not isinstance(result, list): result = [result] if result else []
                
                # Filter out nulls
                staff = [s for s in result if s]
                
                if staff:
                    # Update staff array
                    sec_info['staff'] = [
                        {"name": s.get('EMP_NAME') or s.get('NAME'), "designation": s.get('DESIGNATION')}
                        for s in staff
                    ]
                    updated_count += 1
                    print(".", end="", flush=True)
                else:
                    print("o", end="", flush=True)
                    
            except Exception as e:
                print("x", end="", flush=True)
        
        # Save updated district file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(district_data, f, ensure_ascii=False)
        print(f"\n✅ Updated {updated_count} secretariats in {filename}")

if __name__ == "__main__":
    sync()
