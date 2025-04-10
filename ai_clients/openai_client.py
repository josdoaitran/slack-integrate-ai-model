class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def analyze(self, user_story):
        """Analyze user story using OpenAI models"""
        # In a real implementation, this would use the OpenAI API
        # Here's a placeholder implementation
        
        import openai
        openai.api_key = self.api_key
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """
                    You are a banking domain expert specializing in test case generation.
                    Analyze the following user story from a banking application and extract:
                    1. Core functionality
                    2. Potential edge cases
                    3. Security concerns
                    4. Regulatory compliance requirements
                    Return the analysis in a structured JSON format.
                    """},
                    {"role": "user", "content": f"User story: {user_story}"}
                ],
                response_format={"type": "json_object"}
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Return minimal analysis if API fails
            return {
                "functionality": [{"name": "core function", "description": "Basic functionality"}],
                "edge_cases": [],
                "security_concerns": [],
                "confidence": 0.3
            }
