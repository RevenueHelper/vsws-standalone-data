import os
import shutil

base_path = r"D:\Government orders"

folders = {
    "1. General_Service_Rules": ["Maternity", "Leave", "Increment", "Child Care", "compensatory", "Relief", "Service-Charge"],
    "2. GSWS_Admin": ["GSWS", "Probation", "110-2019", "217-2019", "02_GSWS", "GAD-MS100", "gad_ms156"],
    "3. PR_and_RD": ["PRandRD", "Panchayat_Sec", "Digital_Asst", "Engineering_Asst", "panchayati-raj"],
    "4. Revenue_Dept": ["Revenue", "VRO", "Surveyor", "Ward_Revenue", "house sites", "REV_MS", "REV-MS", "ccla"],
    "5. Agriculture_and_Allied": ["Horticulture", "Sericulture", "Fisheries", "Animal_Husbandry", "Agriculture"],
    "6. Health_and_Welfare": ["ANM", "WelfareandEducation", "TW-Job-chart", "WEAs-service", "HMF-MS83", "G.O.Ms.No. 153"],
    "7. Home_and_Police": ["Home", "Mahila", "Police"],
    "8. MA_and_UD_Ward": ["MAandUD", "Ward_Secretariats"]
}

# Create folders
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Move files
files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]

for file in files:
    moved = False
    lower_file = file.lower()
    for folder, keywords in folders.items():
        for kw in keywords:
            if kw.lower() in lower_file:
                shutil.move(os.path.join(base_path, file), os.path.join(base_path, folder, file))
                moved = True
                break
        if moved:
            break

print("Organization Complete!")
