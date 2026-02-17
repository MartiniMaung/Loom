import json

with open('data/projects_architectural.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('VERIFYING CAPABILITIES')
print('='*50)

# Check each project
all_good = True
for name, proj in data.items():
    caps = proj.get('capabilities', [])
    if not caps:
        print(f'❌ {name}: NO CAPABILITIES')
        all_good = False
    else:
        print(f'✅ {name}: {caps}')

print('\n' + '='*50)
print(f'All projects have capabilities: {all_good}')

# Show sample
print('\nSAMPLE PROJECT:')
import random
sample_name = random.choice(list(data.keys()))
print(json.dumps({sample_name: data[sample_name]}, indent=2))
