import json
from collections import Counter

with open('data/projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('PROJECT REFINEMENT ANALYSIS')
print('='*50)

# Count projects with issues
total = len(data)
no_caps = sum(1 for p in data.values() if not p.get('capabilities'))
zero_pop = sum(1 for p in data.values() if p.get('popularity_score', 0) == 0)
default_maturity = sum(1 for p in data.values() if p.get('maturity_score', 0) == 0.5)

print(f'\n📊 Total projects: {total}')
print(f'❌ No capabilities: {no_caps} ({no_caps/total*100:.1f}%)')
print(f'📉 Zero popularity: {zero_pop} ({zero_pop/total*100:.1f}%)')
print(f'⏳ Default maturity: {default_maturity} ({default_maturity/total*100:.1f}%)')

# Show examples of problematic projects
print('\n📋 Projects needing attention:')
problem_projects = []
for name, p in data.items():
    if not p.get('capabilities'):
        problem_projects.append((name, p.get('description', '')[:50]))

for name, desc in problem_projects[:10]:
    print(f'  • {name}: {desc}')

# Count by license type
licenses = Counter(p.get('license', 'Unknown') for p in data.values())
print('\n📜 License distribution:')
for license, count in licenses.most_common(5):
    print(f'  • {license}: {count}')

# Save problematic projects list
with open('data/to_refine.json', 'w') as f:
    json.dump([name for name, _ in problem_projects], f, indent=2)

print(f'\n💾 Saved {len(problem_projects)} projects to refine to data/to_refine.json')
