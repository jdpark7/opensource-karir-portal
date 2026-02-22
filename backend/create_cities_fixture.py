import json
import re

# User provided data (same as states)
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
fixture_path = 'peeldb/fixtures/cities.json'

def create_slug(text):
    return text.lower().replace(' ', '-')

# Start fresh
data = []
current_pk = 1

lines = raw_data.strip().split('\n')

for i, line in enumerate(lines, start=1):
    parts = line.split(',')
    if len(parts) >= 2:
        # Province is parts[0], City is parts[1]
        city_name = parts[1].strip()
        
        # Handle tab if present
        city_name = city_name.replace('\t', '').strip()
        
        slug = create_slug(city_name)
        
        # pk and state are same as line number (1-based index)
        # assuming states were created in the exact same order
        state_pk = i 
        
        new_city = {
            "model": "peeldb.city",
            "pk": current_pk,
            "fields": {
                "name": city_name,
                "state": state_pk,
                "status": "Enabled",
                "slug": slug
            }
        }
        data.append(new_city)
        current_pk += 1

# Write to file
with open(fixture_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Successfully created {len(data)} Indonesian cities in {fixture_path}")
