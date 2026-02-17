import json

# Load the data
with open('data/projects_architectural.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define capabilities for each project
capability_map = {
    # Web Frameworks
    'Django': ['web_framework', 'authentication', 'database'],
    'Flask': ['web_framework'],
    'Express': ['web_framework', 'api_gateway'],
    'Rails': ['web_framework', 'database', 'authentication'],
    'Spring Boot': ['web_framework', 'authentication', 'database'],
    
    # Databases
    'PostgreSQL': ['database', 'storage'],
    'MySQL': ['database', 'storage'],
    'MongoDB': ['database', 'storage', 'vector_db'],
    'Elasticsearch': ['search', 'database', 'analytics'],
    
    # Message Queues
    'RabbitMQ': ['message_queue', 'message_broker'],
    'Apache Kafka': ['message_queue', 'streaming', 'event_bus'],
    
    # Monitoring
    'Prometheus': ['monitoring', 'metrics'],
    'Grafana': ['monitoring', 'visualization'],
    'Jaeger': ['tracing', 'monitoring'],
    'Logstash': ['logging', 'etl'],
    
    # Authentication
    'Keycloak': ['authentication', 'authorization', 'identity'],
    'Ory Kratos': ['authentication', 'identity'],
    
    # Infrastructure
    'Redis': ['cache', 'database', 'message_queue'],
    'Terraform': ['infrastructure', 'iac'],
    'Ansible': ['infrastructure', 'automation', 'iac'],
    
    # Languages/Runtimes
    'Node.js': ['runtime', 'javascript'],
    'Deno': ['runtime', 'javascript', 'typescript'],
    'Python': ['runtime', 'language'],
    'Java': ['runtime', 'language'],
}

# Update projects
updated = 0
for name, proj in data.items():
    if name in capability_map:
        proj['capabilities'] = capability_map[name]
        updated += 1
    else:
        # Keep existing capabilities if any
        proj['capabilities'] = proj.get('capabilities', [])

print(f'Updated {updated} projects with capabilities')

# Save back
with open('data/projects_architectural.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('✅ Saved updated data')
