#!/usr/bin/env python3
"""
Fetch OSS Projects for Loom Knowledge Graph
Expands dataset from 23 to 100+ projects using GitHub API
"""

import json
import time
import os
from pathlib import Path
import requests
from tqdm import tqdm

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')  # Optional but recommended
DATA_FILE = Path('data/projects.json')
OUTPUT_FILE = Path('data/projects_expanded.json')

# Base set of known-good projects (preserve existing data)
CORE_PROJECTS = [
    "FastAPI", "Django", "Flask", "Express", "Spring Boot", "Rails",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "RabbitMQ", "Apache Kafka", "Nginx", "Apache HTTP Server",
    "Keycloak", "Ory Kratos", "Prometheus", "Grafana", "Jaeger",
    "Kubernetes", "Docker", "Terraform", "Ansible",
    "React", "Vue.js", "Angular", "Node.js", "Deno",
    "Apache Spark", "Apache Flink", "Apache Airflow",
    "Elasticsearch", "Logstash", "Kibana"  # ELK Stack
]

# Categories to help with capability mapping
CAPABILITY_KEYWORDS = {
    "web_framework": ["framework", "web", "http", "rest", "api"],
    "database": ["database", "db", "sql", "nosql", "persistence"],
    "message_queue": ["queue", "message", "broker", "streaming"],
    "cache": ["cache", "caching", "redis"],
    "authentication": ["auth", "oauth", "identity", "sso", "jwt"],
    "monitoring": ["monitor", "metric", "observability", "logging"],
    "container": ["container", "docker", "kubernetes"],
    "infrastructure": ["infrastructure", "iac", "provision"],
    "frontend": ["frontend", "ui", "react", "vue", "angular"],
    "backend": ["backend", "server", "api"],
    "big_data": ["big data", "spark", "hadoop", "data processing"],
    "cicd": ["ci/cd", "pipeline", "automation"]
}

# Default security scores (0.0-1.0) - will be refined later
DEFAULT_SECURITY_SCORE = 0.7

def fetch_github_projects(query="stars:>10000", limit=200):
    """Fetch popular GitHub projects"""
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    url = "https://api.github.com/search/repositories"
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 100
    }
    
    projects = []
    
    for page in range(1, 4):  # Fetch up to 3 pages
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 403:
            print("Rate limit exceeded. Add GITHUB_TOKEN or try later.")
            break
            
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('items', []):
            projects.append({
                'name': item['name'],
                'full_name': item['full_name'],
                'description': item['description'] or '',
                'stars': item['stargazers_count'],
                'language': item['language'],
                'license': item['license']['name'] if item.get('license') else 'Unknown'
            })
        
        if len(data.get('items', [])) < 100:
            break
        
        time.sleep(0.5)  # Avoid rate limiting
    
    return projects

def infer_capabilities(name, description, language=None):
    """Infer project capabilities from name and description"""
    capabilities = []
    text = f"{name} {description}".lower()
    
    for cap, keywords in CAPABILITY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            capabilities.append(cap)
    
    # Language-based inference
    if language:
        if language.lower() in ['javascript', 'typescript', 'python', 'java', 'go', 'rust']:
            if 'web' in text or 'framework' in text:
                capabilities.append('web_framework')
    
    return list(set(capabilities))  # Remove duplicates

def calculate_initial_score(projects):
    """Calculate initial security scores based on project attributes"""
    scored = []
    
    for p in projects:
        # Base score
        score = 0.7
        
        # Adjust based on stars (popularity ≠ security, but indicates maintenance)
        stars = p.get('stars', 0)
        if stars > 50000:
            score += 0.1
        elif stars > 20000:
            score += 0.05
        elif stars < 1000:
            score -= 0.1
        
        # Language-based adjustments (some languages have better security defaults)
        lang = p.get('language')
        if lang and isinstance(lang, str):
            lang = lang.lower()
            if lang in ['rust', 'go']:
                score += 0.1
            elif lang in ['c', 'c++']:
                score -= 0.05
        
        # Clamp to 0.0-1.0
        p['security_score'] = max(0.1, min(1.0, round(score, 2)))
        
        # Add placeholder fields for future objectives
        p['cost'] = 0.5  # Placeholder
        p['operational_complexity'] = 0.5  # Placeholder
        p['ecosystem_maturity'] = min(1.0, stars / 100000) if stars else 0.5
        p['license_risk'] = 0.3 if p.get('license') in ['MIT', 'Apache-2.0', 'BSD'] else 0.6
        
        scored.append(p)
    
    return scored

def merge_with_existing(existing_file, new_projects):
    """Merge new projects with existing ones, preserving existing data"""
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8-sig') as f:
            existing = json.load(f)
        
        # Create lookup by name
        existing_dict = {p['name']: p for p in existing if isinstance(p, dict)}
        
        # Update or add new projects
        for p in new_projects:
            name = p['name']
            if name in existing_dict:
                # Preserve existing fields but update with new data
                existing_dict[name].update(p)
            else:
                existing_dict[name] = p
        
        return list(existing_dict.values())
    else:
        return new_projects

def main():
    print("🚀 Fetching OSS projects for Loom knowledge graph...")
    
    # Step 1: Fetch from GitHub
    print("📡 Fetching from GitHub API...")
    github_projects = fetch_github_projects()
    print(f"   Found {len(github_projects)} projects")
    
    # Step 2: Add core projects if missing
    print("📋 Adding core projects...")
    core_projects_data = []
    for name in CORE_PROJECTS:
        if not any(p['name'] == name for p in github_projects):
            core_projects_data.append({
                'name': name,
                'description': f"{name} - Popular OSS project",
                'stars': 10000,
                'language': 'Unknown',
                'license': 'Open Source'
            })
    
    all_new = github_projects + core_projects_data
    
    # Step 3: Infer capabilities
    print("🔍 Inferring capabilities...")
    for p in tqdm(all_new):
        p['capabilities'] = infer_capabilities(
            p['name'], 
            p.get('description', ''),
            p.get('language')
        )
    
    # Step 4: Calculate initial scores
    print("📊 Calculating initial scores...")
    all_new = calculate_initial_score(all_new)
    
    # Step 5: Merge with existing
    print("🔄 Merging with existing data...")
    merged = merge_with_existing(DATA_FILE, all_new)
    
    # Step 6: Save
    print(f"💾 Saving {len(merged)} projects to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Done!")
    print(f"   Total projects: {len(merged)}")
    print(f"   New projects added: {len(merged) - 23}")
    print(f"\nNext: Review {OUTPUT_FILE} manually to refine capabilities and scores")

if __name__ == "__main__":
    main()