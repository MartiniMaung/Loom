import json
import requests
import time
from typing import Dict, Optional

# GitHub repo mapping for each project
github_repos = {
    'Django': 'django/django',
    'Flask': 'pallets/flask',
    'Express': 'expressjs/express',
    'Spring Boot': 'spring-projects/spring-boot',
    'Rails': 'rails/rails',
    'PostgreSQL': 'postgres/postgres',
    'MySQL': 'mysql/mysql-server',
    'MongoDB': 'mongodb/mongo',
    'Redis': 'redis/redis',
    'Elasticsearch': 'elastic/elasticsearch',
    'RabbitMQ': 'rabbitmq/rabbitmq-server',
    'Apache Kafka': 'apache/kafka',
    'Keycloak': 'keycloak/keycloak',
    'Ory Kratos': 'ory/kratos',
    'Prometheus': 'prometheus/prometheus',
    'Grafana': 'grafana/grafana',
    'Jaeger': 'jaegertracing/jaeger',
    'Terraform': 'hashicorp/terraform',
    'Ansible': 'ansible/ansible',
    'Node.js': 'nodejs/node',
    'Deno': 'denoland/deno',
    'Python': 'python/cpython',
    'Java': 'openjdk/jdk',
    'Logstash': 'elastic/logstash',
}

def get_stars(repo: str) -> Optional[int]:
    """Fetch star count from GitHub API"""
    url = f"https://api.github.com/repos/{repo}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['stargazers_count']
        else:
            print(f"  ⚠️  Failed to fetch {repo}: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ Error fetching {repo}: {e}")
        return None

def stars_to_popularity(stars: Optional[int]) -> float:
    """Convert star count to popularity score (0-1)"""
    if not stars:
        return 0.3  # Default for unfetchable
    
    # Log scale: 0 stars = 0.1, 100k+ stars = 1.0
    if stars >= 100000:
        return 1.0
    elif stars >= 50000:
        return 0.95
    elif stars >= 20000:
        return 0.9
    elif stars >= 10000:
        return 0.85
    elif stars >= 5000:
        return 0.8
    elif stars >= 1000:
        return 0.7
    elif stars >= 500:
        return 0.6
    elif stars >= 100:
        return 0.5
    else:
        return max(0.1, stars / 1000)  # Scale for low-star projects

# Load the data
with open('data/projects_architectural.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('FETCHING GITHUB STARS')
print('='*50)

for name, proj in data.items():
    if name in github_repos:
        repo = github_repos[name]
        print(f'\n📦 {name}: {repo}')
        stars = get_stars(repo)
        popularity = stars_to_popularity(stars)
        proj['popularity_score'] = popularity
        stars_display = f"{stars:,}" if stars else "N/A"
        print(f'   ⭐ Stars: {stars_display} → Popularity: {popularity:.2f}')
        time.sleep(1)  # Rate limiting

    else:
        print(f'\n📦 {name}: No GitHub repo mapped')
        proj['popularity_score'] = 0.5  # Default

# Save updated data
with open('data/projects_architectural.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('\n✅ Updated popularity scores saved')
