import json

with open('data/projects_architectural.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('ARCHITECTURAL PROJECTS (24)')
print('='*50)

# Group by type
categories = {
    'Web Frameworks': [],
    'Databases': [],
    'Message Queues': [],
    'Infrastructure': [],
    'Monitoring': [],
    'Authentication': [],
    'Other': []
}

for name, proj in data.items():
    caps = proj.get('capabilities', [])
    if 'web_framework' in caps:
        categories['Web Frameworks'].append(name)
    elif 'database' in caps:
        categories['Databases'].append(name)
    elif 'message_queue' in caps:
        categories['Message Queues'].append(name)
    elif 'cache' in caps or 'container' in caps:
        categories['Infrastructure'].append(name)
    elif 'monitoring' in caps:
        categories['Monitoring'].append(name)
    elif 'authentication' in caps:
        categories['Authentication'].append(name)
    else:
        categories['Other'].append(name)

for cat, projects in categories.items():
    if projects:
        print(f'\n{cat}:')
        for p in sorted(projects):
            print(f'  • {p}')

print('\n' + '='*50)
print('SAMPLE PROJECT (full data):')
import random
sample_name = random.choice(list(data.keys()))
print(json.dumps({sample_name: data[sample_name]}, indent=2))
