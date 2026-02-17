import json

# Load the 119 project dataset
with open('data/projects_119_final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('ADDING CAPABILITIES TO 119 PROJECTS')
print('='*50)

# Comprehensive capability mapping
capability_map = {
    # Languages
    'Python': ['language', 'runtime', 'scripting'],
    'Java': ['language', 'runtime', 'jvm'],
    'Go': ['language', 'runtime', 'compiled'],
    'Rust': ['language', 'runtime', 'systems'],
    'TypeScript': ['language', 'javascript', 'typed'],
    'PHP': ['language', 'web', 'scripting'],
    'Ruby': ['language', 'web', 'scripting'],
    'C#': ['language', 'dotnet', 'compiled'],
    'Swift': ['language', 'ios', 'compiled'],
    'Kotlin': ['language', 'jvm', 'android'],
    'Scala': ['language', 'jvm', 'functional'],
    'Node.js': ['runtime', 'javascript', 'server'],
    'Deno': ['runtime', 'javascript', 'typescript'],
    
    # Web Frameworks
    'Django': ['web_framework', 'python', 'fullstack'],
    'Flask': ['web_framework', 'python', 'micro'],
    'Express': ['web_framework', 'nodejs', 'api'],
    'Spring Boot': ['web_framework', 'java', 'microservice'],
    'Rails': ['web_framework', 'ruby', 'fullstack'],
    'Laravel': ['web_framework', 'php', 'fullstack'],
    'Symfony': ['web_framework', 'php', 'enterprise'],
    'ASP.NET Core': ['web_framework', 'dotnet', 'cross_platform'],
    'Phoenix': ['web_framework', 'elixir', 'realtime'],
    'Play Framework': ['web_framework', 'scala', 'reactive'],
    
    # Databases
    'PostgreSQL': ['database', 'relational', 'sql'],
    'MySQL': ['database', 'relational', 'sql'],
    'MariaDB': ['database', 'relational', 'sql'],
    'SQLite': ['database', 'embedded', 'sql'],
    'MongoDB': ['database', 'nosql', 'document'],
    'Redis': ['database', 'cache', 'key_value'],
    'Elasticsearch': ['database', 'search', 'analytics'],
    'Cassandra': ['database', 'nosql', 'wide_column'],
    'CouchDB': ['database', 'nosql', 'document'],
    'Neo4j': ['database', 'graph', 'nosql'],
    'InfluxDB': ['database', 'timeseries', 'metrics'],
    'ClickHouse': ['database', 'olap', 'columnar'],
    'CockroachDB': ['database', 'distributed', 'sql'],
    'TiDB': ['database', 'distributed', 'sql'],
    'DynamoDB': ['database', 'nosql', 'aws'],
    'Firebase': ['database', 'nosql', 'realtime'],
    'Supabase': ['database', 'postgres', 'backend'],
    'PlanetScale': ['database', 'mysql', 'serverless'],
    
    # Message Queues
    'RabbitMQ': ['message_queue', 'amqp', 'broker'],
    'Apache Kafka': ['message_queue', 'streaming', 'event_bus'],
    'NATS': ['message_queue', 'lightweight', 'cloud'],
    'ZeroMQ': ['message_queue', 'library', 'distributed'],
    'ActiveMQ': ['message_queue', 'jms', 'broker'],
    'Pulsar': ['message_queue', 'streaming', 'multi_tenant'],
    
    # API Gateways
    'Kong': ['api_gateway', 'reverse_proxy', 'nginx'],
    'Apache APISIX': ['api_gateway', 'reverse_proxy', 'dynamic'],
    'Traefik': ['reverse_proxy', 'load_balancer', 'kubernetes'],
    'HAProxy': ['load_balancer', 'reverse_proxy', 'tcp'],
    'Envoy': ['proxy', 'service_mesh', 'edge'],
    
    # Service Mesh
    'Istio': ['service_mesh', 'traffic_management', 'security'],
    'Linkerd': ['service_mesh', 'observability', 'kubernetes'],
    'Consul': ['service_discovery', 'service_mesh', 'kv_store'],
    
    # Container/Orchestration
    'Docker': ['container', 'runtime', 'image'],
    'Kubernetes': ['orchestration', 'containers', 'scheduling'],
    'Podman': ['container', 'runtime', 'daemonless'],
    'OpenShift': ['paas', 'kubernetes', 'enterprise'],
    
    # CI/CD
    'Jenkins': ['ci_cd', 'automation', 'pipeline'],
    'GitLab CI': ['ci_cd', 'git', 'automation'],
    'GitHub Actions': ['ci_cd', 'automation', 'workflow'],
    'ArgoCD': ['gitops', 'cd', 'kubernetes'],
    'Spinnaker': ['cd', 'multicloud', 'pipeline'],
    
    # Monitoring
    'Prometheus': ['monitoring', 'metrics', 'timeseries'],
    'Grafana': ['visualization', 'dashboard', 'metrics'],
    'Jaeger': ['tracing', 'distributed', 'observability'],
    'Logstash': ['logging', 'etl', 'pipeline'],
    'Datadog': ['monitoring', 'saas', 'apm'],
    'New Relic': ['apm', 'monitoring', 'saas'],
    'Elastic APM': ['apm', 'monitoring', 'elastic'],
    'Loki': ['logging', 'grafana', 'prometheus'],
    'Sentry': ['error_tracking', 'monitoring', 'debug'],
    'Checkmk': ['monitoring', 'infrastructure', 'alerting'],
    'Zabbix': ['monitoring', 'infrastructure', 'alerting'],
    'Nagios': ['monitoring', 'infrastructure', 'legacy'],
    'OpenTelemetry': ['observability', 'tracing', 'metrics'],
    
    # Service Discovery
    'Eureka': ['service_discovery', 'netflix', 'java'],
    'ZooKeeper': ['coordination', 'distributed', 'kv_store'],
    'etcd': ['kv_store', 'distributed', 'raft'],
    
    # API Documentation
    'Swagger': ['api_docs', 'openapi', 'documentation'],
    'Redoc': ['api_docs', 'openapi', 'ui'],
    'Postman': ['api_client', 'testing', 'collection'],
    'Insomnia': ['api_client', 'testing', 'graphql'],
    
    # Testing Tools
    'Selenium': ['testing', 'browser', 'automation'],
    'Cypress': ['testing', 'e2e', 'frontend'],
    'Playwright': ['testing', 'e2e', 'cross_browser'],
    'Jest': ['testing', 'javascript', 'unit'],
    'PyTest': ['testing', 'python', 'unit'],
    'JUnit': ['testing', 'java', 'unit'],
    'TestNG': ['testing', 'java', 'integration'],
    'Mocha': ['testing', 'javascript', 'node'],
    
    # Build Tools
    'Maven': ['build', 'java', 'dependency'],
    'Gradle': ['build', 'java', 'kotlin'],
    'Webpack': ['bundler', 'javascript', 'module'],
    'Vite': ['bundler', 'javascript', 'dev_server'],
    'esbuild': ['bundler', 'javascript', 'performance'],
    
    # Infrastructure as Code
    'Terraform': ['iac', 'provisioning', 'cloud'],
    'Ansible': ['iac', 'configuration', 'automation'],
    'Puppet': ['configuration', 'management', 'declarative'],
    'Chef': ['configuration', 'management', 'ruby'],
    'SaltStack': ['configuration', 'automation', 'remote_execution'],
    'CloudFormation': ['iac', 'aws', 'infrastructure'],
    'CDK': ['iac', 'aws', 'programmable'],
    
    # Security
    'Keycloak': ['authentication', 'authorization', 'sso'],
    'Ory Kratos': ['authentication', 'identity', 'api'],
    'Vault': ['secrets', 'encryption', 'security'],
    'Sealed Secrets': ['secrets', 'kubernetes', 'encryption'],
    'OpenSSL': ['crypto', 'ssl', 'certificates'],
    'Let\'s Encrypt': ['certificates', 'ssl', 'automation'],
    'Certbot': ['certificates', 'letsencrypt', 'automation'],
    'Trivy': ['security', 'scanning', 'vulnerability'],
    'SonarQube': ['code_quality', 'static_analysis', 'security'],
    
    # Object Storage
    'MinIO': ['storage', 's3', 'object'],
    'Ceph': ['storage', 'distributed', 'object'],
    'SeaweedFS': ['storage', 'distributed', 'fast'],
}

updated = 0
for name, proj in data.items():
    if name in capability_map:
        proj['capabilities'] = capability_map[name]
        updated += 1
        print(f'✅ {name}: {capability_map[name]}')
    else:
        print(f'⚠️  {name}: No capability mapping')
        proj['capabilities'] = ['unknown']

print(f'\n📊 Updated {updated} projects with capabilities')
print(f'📊 Total projects: {len(data)}')

# Save final dataset
with open('data/projects_119_final.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('✅ Final dataset saved to data/projects_119_final.json')
