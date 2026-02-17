import json
with open('data/projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Data type: {type(data)}')

if isinstance(data, dict):
    print(f'Total projects: {len(data)}')
    print('\nFirst 5 projects:')
    items = list(data.items())[:5]
    for name, proj in items:
        print(f"  • {name}: {proj.get('capabilities', [])}")
    
    print('\nSample of full data:')
    import random
    sample_name = random.choice(list(data.keys()))
    print(json.dumps({sample_name: data[sample_name]}, indent=2))
else:
    print(f'Total projects: {len(data)}')
    print('\nFirst 5 projects:')
    for p in data[:5]:
        print(f"  • {p.get('name')}: {p.get('capabilities', [])}")
    
    print('\nSample of full data:')
    import random
    sample = random.choice(data)
    print(json.dumps(sample, indent=2))
