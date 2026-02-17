from loom.graph import SemanticGraph
g = SemanticGraph()
ory = g.projects.get("Ory_Kratos")
if ory:
    caps = [c.value for c in ory.capabilities]
    print(f"Ory_Kratos capabilities: {caps}")
    print(f"Ory_Kratos has authentication: {'authentication' in caps}")
    print(f"Ory_Kratos security_score: {ory.security_score}")
else:
    print("Ory_Kratos not found")
