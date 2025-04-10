# banking_knowledge_base.py - Domain-specific knowledge for banking/lending
class BankingKnowledgeBase:
    def __init__(self):
        # Banking terms and their meanings
        self.banking_terms = {
            "KYC": "Know Your Customer - verification of client identity",
            "AML": "Anti-Money Laundering",
            "LTV": "Loan-to-Value ratio",
            "DTI": "Debt-to-Income ratio",
            "FICO": "Credit score from Fair Isaac Corporation",
            # More banking terms
        }
        
        # Common banking workflows
        self.workflows = {
            "loan_application": ["application_submission", "verification", "underwriting", "approval", "funding"],
            "account_opening": ["application", "identity_verification", "funding", "activation"],
            # More workflows
        }
        
        # Regulatory requirements
        self.regulations = {
            "USA": ["KYC", "AML", "OFAC", "FCRA", "ECOA", "TILA", "RESPA"],
            "EU": ["GDPR", "PSD2", "MiFID II"],
            # More regulations by region
        }
    
    def enrich_story(self, user_story):
        """Add banking domain context to the user story"""
        # Add relevant banking terms
        enriched = user_story
        
        # Find banking terms in the user story
        terms_found = []
        for term in self.banking_terms:
            if term in user_story:
                terms_found.append({
                    "term": term,
                    "definition": self.banking_terms[term]
                })
        
        # Identify workflow context
        workflow_context = None
        for workflow, steps in self.workflows.items():
            if any(step in user_story.lower() for step in steps):
                workflow_context = {
                    "name": workflow,
                    "steps": steps
                }
                break
        
        # Identify regulatory context
        regulatory_context = []
        for region, regs in self.regulations.items():
            relevant_regs = [reg for reg in regs if reg in user_story]
            if relevant_regs:
                regulatory_context.append({
                    "region": region,
                    "regulations": relevant_regs
                })
        
        # Return enriched context
        return {
            "original_story": user_story,
            "terms": terms_found,
            "workflow": workflow_context,
            "regulations": regulatory_context
        }