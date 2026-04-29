import requests, json, os

API_KEY = "36491518b58b42cfbffa854fde92f134"
BASE_URL = "https://api.vswsonline.ap.gov.in/reports/api/CSPServiceDashboard"

DIST_MAP = {
    "ANANTAPUR": "19", "CHITTOOR": "23", "EAST GODAVARI": "04", "GUNTUR": "07",
    "KRISHNA": "06", "KURNOOL": "13", "NELLORE": "09", "PRAKASAM": "08",
    "SRIKAKULAM": "01", "VISAKHAPATNAM": "03", "VIZIANAGARAM": "02", "WEST GODAVARI": "05",
    "KADAPA": "11", "ANAKAPALLI": "21", "ALLURI SITHARAMA RAJU": "20",
    "BAPATLA": "17", "ELURU": "15", "KAKINADA": "14", "KONASEEMA": "16",
    "NANDYAL": "25", "NTR": "18", "PALNADU": "24", "PARVATHIPURAM MANYAM": "22",
    "SRI SATHYA SAI": "26", "TIRUPATI": "07"
}

def sync():
    os.makedirs("data/districts", exist_ok=True)
    dists = requests.get(f"{BASE_URL}/GetDistrict", headers={"ApiKey": API_KEY}).json().get('result', [])
    
    for d in dists:
        d_id = d.get('DistrictCode')
        d_name = d.get('DistrictName', 'UNKNOWN').upper()
        print(f"Syncing {d_name} ({d_id})...")
        
        # Pull staff count and details for the whole district in one go!
        staff_data = requests.get(f"{BASE_URL}/GetCSPStaffDetails?DistrictCode={d_id}", headers={"ApiKey": API_KEY}).json().get('result', [])
        
        grouped = {}
        for s in staff_data:
            code = str(s.get('SecretariatCode', ''))
            if not code: continue
            if code not in grouped:
                grouped[code] = {
                    "secCode": code, "secName": s.get('SecretariatName'),
                    "district": d_name, "staff": []
                }
            grouped[code]["staff"].append({"name": s.get('EmployeeName'), "designation": s.get('Designation')})
            
        with open(f"data/districts/{d_id}.json", "w", encoding='utf-8') as f:
            json.dump(grouped, f, indent=2)

if __name__ == "__main__":
    sync()
