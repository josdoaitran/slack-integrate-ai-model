# model_orchestrator.py - Handles orchestration between different AI models
class ModelOrchestrator:
    def __init__(self, openai_client, gemini_client, claude_client):
        self.openai_client = openai_client
        self.gemini_client = gemini_client
        self.claude_client = claude_client
        
    def analyze_story(self, user_story):
        """
        Analyze the user story using the appropriate AI model(s)
        Strategy: Use primary model first, fall back to others if needed
        """
        try:
            # First try Claude for deep contextual understanding
            analysis = self.claude_client.analyze(user_story)
            
            # If Claude's confidence is low, try OpenAI
            if analysis.get('confidence', 0) < 0.7:
                openai_analysis = self.openai_client.analyze(user_story)
                
                # Merge analyses, with preference to high-confidence elements
                analysis = self.merge_analyses(analysis, openai_analysis)
                
            # For specialized banking terms, also use Gemini
            gemini_analysis = self.gemini_client.analyze_domain_specific(user_story)
            if gemini_analysis.get('domain_terms'):
                analysis['domain_terms'] = gemini_analysis.get('domain_terms')
                
            return analysis
            
        except Exception as e:
            # Fallback strategy
            print(f"Error in primary analysis: {e}")
            try:
                return self.openai_client.analyze(user_story)
            except:
                return self.gemini_client.analyze(user_story)
                
    def merge_analyses(self, analysis1, analysis2):
        """Merge analyses from different models, prioritizing high-confidence elements"""
        merged = {}
        
        for key in set(analysis1.keys()).union(analysis2.keys()):
            if key in analysis1 and key in analysis2:
                conf1 = analysis1.get('confidence', {}).get(key, 0.5)
                conf2 = analysis2.get('confidence', {}).get(key, 0.5)
                
                merged[key] = analysis1[key] if conf1 > conf2 else analysis2[key]
            elif key in analysis1:
                merged[key] = analysis1[key]
            else:
                merged[key] = analysis2[key]
                
        return merged