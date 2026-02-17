from loom.auditor import PatternAuditor
from loom.graph import SemanticGraph
import json

g = SemanticGraph()
auditor = PatternAuditor(g)

# Load the evolved pattern directly
with open("cms_v3_evolved.json", "r", encoding="utf-8-sig") as f:
    pattern_data = json.load(f)

print("Pattern components:")
for comp in pattern_data.get("components", []):
    print(f"  - {comp['name']} as {comp.get('role', 'Unknown')}")
    # Check if this is loaded as authentication
    proj = g.projects.get(comp["name"])
    if proj:
        caps = [c.value for c in proj.capabilities]
        print(f"    Capabilities: {caps}")
        print(f"    Has authentication: {'authentication' in caps}")

# Now run the audit check manually
print("\nRunning authentication check manually:")
pattern = auditor._load_pattern("cms_v3_evolved.json")
has_auth = False
for project, _ in pattern.components:
    caps = [cap.value for cap in project.capabilities]
    if "authentication" in caps:
        print(f"Found authentication in: {project.name}")
        has_auth = True

print(f"Pattern has authentication: {has_auth}")
