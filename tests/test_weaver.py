"""
Tests for weaver.py - Pattern weaving and scoring
"""
import pytest
from src.loom.core import CapabilityType
from src.loom.weaver import PatternWeaver, Pattern, calculate_weighted_score

class TestWeightedScoreCalculation:
    """Test the multi-objective scoring function"""
    
    def test_calculate_weighted_score_basic(self, sample_projects):
        """Test basic weighted score calculation"""
        components = [sample_projects[0]]  # FastAPI
        weights = {'security': 1.0, 'cost': 0, 'complexity': 0, 'maturity': 0, 'license_risk': 0}
        
        score = calculate_weighted_score(components, weights)
        assert score == pytest.approx(0.85)  # FastAPI security_score
    
    def test_calculate_weighted_score_multiple(self, sample_projects):
        """Test weighted score with multiple components"""
        components = [sample_projects[0], sample_projects[2]]  # FastAPI + PostgreSQL
        weights = {'security': 0.5, 'cost': 0.5, 'complexity': 0, 'maturity': 0, 'license_risk': 0}
        
        # FastAPI: security=0.85, cost=0.4
        # PostgreSQL: security=0.82, cost=0.3
        # Expected: average of (0.5*0.85 + 0.5*(1-0.4)) and (0.5*0.82 + 0.5*(1-0.3))
        score = calculate_weighted_score(components, weights)
        expected = ((0.5*0.85 + 0.5*0.6) + (0.5*0.82 + 0.5*0.7)) / 2
        assert score == pytest.approx(expected)
    
    def test_default_weights(self, sample_projects):
        """Test that default weights are used when none provided"""
        components = [sample_projects[0]]  # FastAPI
        score = calculate_weighted_score(components, {})
        # Default: security=0.4, cost=0.15, complexity=0.15, maturity=0.2, license_risk=0.1
        # FastAPI: sec=0.85, cost=0.4, complexity=0.3, maturity=0.9, license_risk=0.2
        expected = (0.4*0.85 + 0.15*(1-0.4) + 0.15*(1-0.3) + 0.2*0.9 + 0.1*(1-0.2))
        assert score == pytest.approx(expected)
    
    def test_empty_components(self):
        """Test with empty component list"""
        score = calculate_weighted_score([], {})
        assert score == 0.0

class TestPatternWeaver:
    """Test the PatternWeaver class"""
    
    def test_weaver_initialization(self, test_graph, sample_intent):
        """Test weaver initialization"""
        weaver = PatternWeaver(test_graph, sample_intent)
        assert weaver.graph == test_graph
        assert weaver.intent == sample_intent
        assert weaver.patterns == []
   
    def test_weave_for_intent(self, test_graph, sample_intent):
        """Test weaving patterns for an intent"""
        weaver = PatternWeaver(test_graph, sample_intent)
        patterns = weaver.weave_for_intent(sample_intent)

        assert len(patterns) > 0
        for pattern in patterns:
            assert isinstance(pattern, Pattern)
            # Print debug info
            print(f"\nPattern: {pattern.name}")
            print(f"Components: {[(c[0].name, c[1]) for c in pattern.components]}")
            components = [c[0].name for c in pattern.components]
            assert any('FastAPI' in comp or 'Django' in comp for comp in components)
            assert any('PostgreSQL' in comp or 'MySQL' in comp for comp in components)       
    def test_get_all_patterns(self, test_graph, sample_intent):
        """Test getting all patterns as dictionaries"""
        weaver = PatternWeaver(test_graph, sample_intent)
        weaver.weave_for_intent(sample_intent)
        
        patterns_dict = weaver.get_all_patterns()
        assert len(patterns_dict) > 0
        
        # Check structure of first pattern
        pattern = patterns_dict[0]
        assert "name" in pattern
        assert "description" in pattern
        assert "components" in pattern
        assert "confidence" in pattern
        assert "complexity" in pattern
    
    def test_weave_with_weights(self, test_graph, sample_intent, sample_weights):
        """Test weaving with custom weights"""
        weaver = PatternWeaver(test_graph, sample_intent)
        patterns = weaver.weave_for_intent(sample_intent)
        
        # Apply weights
        for pattern in patterns:
            pattern.calculate_metrics(sample_weights)
        
        # Get patterns with weights
        patterns_dict = weaver.get_all_patterns(sample_weights)
        
        # Check that confidence scores are different with weights
        default_dict = weaver.get_all_patterns()
        assert patterns_dict[0]["confidence"] != default_dict[0]["confidence"]

class TestPattern:
    """Test the Pattern class"""
    
    def test_pattern_creation(self, sample_projects):
        """Test basic pattern creation"""
        pattern = Pattern(
            name="Test Pattern",
            description="A test pattern"
        )
        pattern.add_component(sample_projects[0], "API")
        pattern.add_component(sample_projects[2], "Database")
        
        assert pattern.name == "Test Pattern"
        assert len(pattern.components) == 2
        assert pattern.components[0][0].name == "FastAPI"
        assert pattern.components[0][1] == "API"
    
    def test_pattern_metrics_without_components(self):
        """Test metrics calculation with no components"""
        pattern = Pattern("Empty", "No components")
        pattern.calculate_metrics()
        assert pattern.confidence == 0.0
        assert pattern.complexity == 0.0
    
    def test_pattern_metrics_with_components(self, sample_projects):
        """Test metrics calculation with components"""
        pattern = Pattern("Test", "With components")
        pattern.add_component(sample_projects[0], "API")  # FastAPI
        pattern.add_component(sample_projects[2], "DB")   # PostgreSQL
        
        pattern.calculate_metrics()
        
        # Should have positive confidence
        assert pattern.confidence > 0
        assert pattern.complexity > 0
    
    def test_pattern_to_dict(self, test_graph, sample_projects):
        """Test converting pattern to dictionary"""
        pattern = Pattern("Dict Test", "Testing to_dict")
        pattern.add_component(sample_projects[0], "API")
        pattern.add_component(sample_projects[2], "Database")
        
        pattern_dict = pattern.to_dict(test_graph)
        
        assert pattern_dict["name"] == "Dict Test"
        assert len(pattern_dict["components"]) == 2
        assert "confidence" in pattern_dict
        assert "complexity" in pattern_dict