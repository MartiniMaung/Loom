from loom.graph import SemanticGraph
g = SemanticGraph()
ory = g.projects.get("Ory_Kratos")
if ory:
    print(f"Project name: '{ory.name}'")
    print(f"Type: {type(ory.name)}")
else:
    print("Ory_Kratos not found")
