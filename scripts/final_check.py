import json
import random

with open('data/projects_architectural.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('FINAL QUALITY CHECK')
print('='*50)

print(f'Total projects: {len(data)}')

# Show 3 random projects
for i in range(3):
    name = random.choice(list(data.keys()))
    proj = data[name]
    print(f'\n📦 {name}:')
    print(f'  Capabilities: {proj.get("capabilities", [])}')
    print(f'  Popularity: {proj.get("popularity_score", 0):.2f}')
    print(f'  Maturity: {proj.get("maturity_score", 0):.2f}')
    print(f'  Security: {proj.get("security_score", 0):.2f}')
