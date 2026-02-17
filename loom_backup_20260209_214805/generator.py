"""
Manifest Generator - Turns patterns into deployable code.
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Template


class ManifestGenerator:
    """Generates deployment manifests from patterns."""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Template]:
        """Load Jinja2 templates for different manifest types."""
        templates = {}
        
        # Enhanced Docker Compose template
        docker_compose_template = '''
version: '3.8'

services:
{% for component in components %}
  {{ component.name|lower }}:
    {% if component.name == "PostgreSQL" %}
    image: postgres:15
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    {% elif component.name == "Redis" %}
    image: redis:7-alpine
    ports:
      - "6379:6379"
    {% elif component.name == "Django" %}
    build:
      context: .
      dockerfile: Dockerfile.django
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://app_user:app_password@postgresql:5432/app_db
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    depends_on:
      - postgresql
      - minio
    {% elif component.name == "MinIO" %}
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    {% elif component.name == "Keycloak" %}
    image: quay.io/keycloak/keycloak:latest
    command: start-dev
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    ports:
      - "8080:8080"
    {% elif component.name == "Elasticsearch" %}
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    {% endif %}
    restart: unless-stopped
{% endfor %}

volumes:
  postgres_data:
  minio_data:
  elasticsearch_data:
'''
        
        templates["docker_compose"] = Template(docker_compose_template)
        return templates
    
    def generate_from_pattern(self, pattern_dict: Dict[str, Any], output_dir: str = "./loom_output") -> Dict[str, str]:
        """Generate deployment files from a pattern."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        generated_files = {}
        
        # Extract components
        components = pattern_dict.get("components", [])
        
        # 1. Generate docker-compose.yml
        docker_compose = self.templates["docker_compose"].render(
            components=components
        )
        
        docker_compose_path = output_path / "docker-compose.yml"
        docker_compose_path.write_text(docker_compose)
        generated_files["docker_compose"] = str(docker_compose_path)
        
        # 2. Generate simple README
        readme_content = f"# {pattern_dict['name']}\n\nRun: docker-compose up -d\n"
        readme_path = output_path / "README.md"
        readme_path.write_text(readme_content)
        generated_files["readme"] = str(readme_path)
        
        return generated_files
