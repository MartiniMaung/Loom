import json

# Load current data
with open('data/projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define architectural components (actual tech stack items)
architectural_projects = {
    # Web Frameworks
    'FastAPI', 'Django', 'Flask', 'Express', 'Spring Boot', 'Rails',
    'Laravel', 'ASP.NET Core', 'Phoenix', 'Actix-web',
    
    # Databases
    'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
    'Cassandra', 'CouchDB', 'DynamoDB', 'Neo4j', 'InfluxDB',
    'ClickHouse', 'TimescaleDB', 'MariaDB', 'SQLite',
    
    # Message Queues
    'RabbitMQ', 'Apache Kafka', 'ActiveMQ', 'NATS', 'ZeroMQ',
    
    # API Gateways / Proxies
    'NGINX', 'Apache HTTP Server', 'Traefik', 'HAProxy', 'Envoy',
    'Kong', 'Apache APISIX',
    
    # Authentication
    'Keycloak', 'Ory Kratos', 'Auth0', 'Okta', 'CAS',
    
    # Monitoring
    'Prometheus', 'Grafana', 'Jaeger', 'Zipkin', 'Datadog',
    'New Relic', 'Elastic APM',
    
    # Container & Orchestration
    'Docker', 'Kubernetes', 'Podman', 'containerd', 'OpenShift',
    
    # Service Mesh
    'Istio', 'Linkerd', 'Consul',
    
    # Infrastructure as Code
    'Terraform', 'Ansible', 'Pulumi', 'CloudFormation',
    
    # CI/CD
    'Jenkins', 'GitLab CI', 'GitHub Actions', 'ArgoCD', 'Spinnaker',
    
    # Logging
    'Logstash', 'Fluentd', 'Vector', 'Loki',
    
    # Storage
    'MinIO', 'Ceph', 'SeaweedFS',
    
    # Search
    'Elasticsearch', 'Solr', 'Meilisearch', 'Algolia',
    
    # GraphQL
    'Apollo Server', 'GraphQL Yoga', 'Hasura',
    
    # Testing
    'Selenium', 'Cypress', 'Jest', 'PyTest', 'JUnit',
    
    # Languages/Runtimes
    'Node.js', 'Deno', 'Python', 'Java', 'Go', 'Rust',
}

# Filter projects
filtered = {}
for name, proj in data.items():
    if name in architectural_projects:
        filtered[name] = proj

print(f'Original: {len(data)} projects')
print(f'Filtered: {len(filtered)} architectural projects')
print(f'Removed: {len(data) - len(filtered)} documentation/learning projects')

# Save filtered list
with open('data/projects_architectural.json', 'w', encoding='utf-8') as f:
    json.dump(filtered, f, indent=2)

print('\n✅ Saved architectural projects to data/projects_architectural.json')
