import json
import re

# User provided data
raw_data = """Aceh,	Banda Aceh
Bali,Denpasar
Bangka Belitung Islands,	Pangkal Pinang
Banten,Serang
Bengkulu,Bengkulu
Central Java,	Semarang
Central Kalimantan,Palangka Raya
Central Papua,Nabire
Central Sulawesi,Palu
East Java,Surabaya
East Kalimantan,Samarinda
East Nusa Tenggara,Kupang
Gorontalo,Gorontalo
Highland Papua,Wamena
Special Capital Region of Jakarta,Central Jakarta
Jambi,Jambi
Lampung,Bandar Lampung
Maluku,Ambon
North Kalimantan,	Tanjung Selor
North Maluku,Sofifi
North Sulawesi,Manado
North Sumatra,Medan
Papua	,Jayapura
Riau,Pekanbaru
Riau Islands,	Tanjung Pinang
Southeast Sulawesi,Kendari
South Kalimantan,	Banjarbaru
South Papua,Merauke
South Sulawesi,Makassar
South Sumatra,Palembang
Southwest Papua,	Sorong
West Java,Bandung
West Kalimantan,Pontianak
West Nusa Tenggara,Mataram
West Papua,	Manokwari
West Sulawesi,Mamuju
West Sumatra,Padang
Special Region of Yogyakarta,Yogyakarta"""

# File path
fixture_path = 'peeldb/fixtures/states.json'

def create_slug(text):
    return text.lower().replace(' ', '-')

# Start fresh
data = []
current_pk = 1
new_states = []

lines = raw_data.strip().split('\n')

for line in lines:
    parts = line.split(',')
    if len(parts) >= 1:
        province = parts[0].strip()
        # Handle tab if present in province part (e.g. "Papua\t")
        province = province.replace('\t', '').strip()
        
        slug = create_slug(province)
        
        new_state = {
            "model": "peeldb.state",
            "pk": current_pk,
            "fields": {
                "country": 4,
                "name": province,
                "status": "Enabled",
                "slug": slug
            }
        }
        new_states.append(new_state)
        current_pk += 1

# Replace data with new states
data = new_states

# Write back
with open(fixture_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Successfully added {len(new_states)} Indonesian states to {fixture_path}")
