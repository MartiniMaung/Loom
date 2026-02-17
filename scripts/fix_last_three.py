import json

with open('data/projects_polished.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix Apollo Server
if 'Apollo Server' in data:
    data['Apollo Server']['capabilities'] = ['graphql', 'server', 'api']

# Fix Hasura
if 'Hasura' in data:
    data['Hasura']['capabilities'] = ['graphql', 'database', 'realtime']

# Fix GraphQL Yoga
if 'GraphQL Yoga' in data:
    data['GraphQL Yoga']['capabilities'] = ['graphql', 'server', 'api']

# Save final version
with open('data/projects_final.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('✅ Fixed Apollo Server, Hasura, and GraphQL Yoga capabilities')
total_with_caps = sum(1 for p in data.values() if p.get('capabilities'))
print(f'✅ Total projects with capabilities: {total_with_caps}')
