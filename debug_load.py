import json
from src.loom.evolver import PatternEvolver
from src.loom.graph import SemanticGraph

graph = SemanticGraph()
evolver = PatternEvolver(graph)

try:
    pattern = evolver.load_pattern("test_evolution.json")
    print("✅ Load successful!")
    print(f"Pattern name: {pattern.name}")
    print(f"Components loaded: {len(pattern.components)}")
except Exception as e:
    print(f"❌ Load failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
