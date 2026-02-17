import json
from src.loom.evolver import PatternEvolver
from src.loom.graph import SemanticGraph

graph = SemanticGraph()
evolver = PatternEvolver(graph)

# Test security upgrade suggestions
print("Testing security upgrade suggestions:")
test_cases = [
    ("FastAPI", "web_framework"),
    ("MySQL", "database"),
    ("RabbitMQ", "message_queue"),
    ("Django", "web_framework")  # Should not be upgraded
]

for project_name, role in test_cases:
    project = graph.projects.get(project_name)
    if project:
        upgrade = evolver._suggest_security_upgrade(project, role)
        if upgrade:
            print(f"  {project_name} (security: {project.security_score}) -> {upgrade.name} (security: {upgrade.security_score})")
        else:
            print(f"  {project_name}: No upgrade suggested (security: {project.security_score})")
    else:
        print(f"  {project_name}: Not found in graph")

print("\nSecurity scores in graph:")
for name in ["FastAPI", "Django", "MySQL", "PostgreSQL", "RabbitMQ", "Apache_Kafka"]:
    proj = graph.projects.get(name)
    if proj:
        print(f"  {name}: {proj.security_score}")
