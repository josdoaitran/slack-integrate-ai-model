# test_generator.py - Generates test cases from AI analysis
class TestCaseGenerator:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        
    def generate_test_cases(self, ai_analysis):
        """Generate test cases based on AI analysis"""
        test_cases = []
        
        # Extract core functionality from analysis
        functionality = ai_analysis.get("functionality", [])
        edge_cases = ai_analysis.get("edge_cases", [])
        security_concerns = ai_analysis.get("security_concerns", [])
        
        # Generate happy path test cases
        for func in functionality:
            test_cases.append(self.create_happy_path_test(func))
            
        # Generate edge case test cases
        for case in edge_cases:
            test_cases.append(self.create_edge_case_test(case))
            
        # Generate security test cases
        for concern in security_concerns:
            test_cases.append(self.create_security_test(concern))
            
        # Add regulatory compliance test cases if needed
        regulatory_context = ai_analysis.get("regulatory_context", [])
        for reg in regulatory_context:
            test_cases.append(self.create_compliance_test(reg))
            
        return test_cases
    
    def create_happy_path_test(self, functionality):
        """Create a test case for the happy path scenario"""
        return {
            "title": f"Verify {functionality['name']}",
            "description": f"Test that {functionality['description']}",
            "steps": functionality.get("steps", [
                "Login as appropriate user",
                f"Navigate to {functionality.get('location', 'appropriate section')}",
                f"Perform {functionality['name']} operation",
                "Verify results"
            ]),
            "expected_result": functionality.get("expected_result", "Operation completes successfully"),
            "type": "Functional"
        }
    
    def create_edge_case_test(self, edge_case):
        """Create a test case for an edge case scenario"""
        return {
            "title": f"Handle {edge_case['name']}",
            "description": f"Test that the system properly handles {edge_case['description']}",
            "steps": edge_case.get("steps", [
                "Login as appropriate user",
                f"Attempt to perform operation with {edge_case['condition']}",
                "Observe system response"
            ]),
            "expected_result": edge_case.get("expected_result", "System handles the edge case appropriately"),
            "type": "Edge Case"
        }
    
    def create_security_test(self, security_concern):
        """Create a test case for a security concern"""
        return {
            "title": f"Security: {security_concern['name']}",
            "description": f"Verify that the system is protected against {security_concern['description']}",
            "steps": security_concern.get("steps", [
                f"Attempt to exploit {security_concern['name']}",
                "Verify system response"
            ]),
            "expected_result": security_concern.get("expected_result", "System prevents the security exploit"),
            "type": "Security"
        }
    
    def create_compliance_test(self, regulation):
        """Create a test case for regulatory compliance"""
        return {
            "title": f"Compliance: {regulation['name']}",
            "description": f"Verify that the system complies with {regulation['name']} requirements",
            "steps": regulation.get("steps", [
                "Set up test scenario requiring compliance",
                "Perform regulated operation",
                "Verify compliance requirements are met"
            ]),
            "expected_result": regulation.get("expected_result", "System complies with regulatory requirements"),
            "type": "Compliance"
        }