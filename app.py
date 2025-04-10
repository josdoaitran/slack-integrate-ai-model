# app.py - Main Flask Application
from flask import Flask, request, jsonify
import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Import AI model clients
from ai_clients.openai_client import OpenAIClient
from ai_clients.gemini_client import GeminiClient
from ai_clients.claude_client import ClaudeClient
from test_generator import TestCaseGenerator
from model_orchestrator import ModelOrchestrator
from banking_knowledge_base import BankingKnowledgeBase

# Initialize Flask app
app = Flask(__name__)

# Initialize Slack app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
handler = SlackRequestHandler(slack_app)

# Initialize AI clients
openai_client = OpenAIClient(api_key=os.environ.get("OPENAI_API_KEY"))
gemini_client = GeminiClient(api_key=os.environ.get("GEMINI_API_KEY"))
claude_client = ClaudeClient(api_key=os.environ.get("CLAUDE_API_KEY"))

# Initialize knowledge base, orchestrator and test generator
knowledge_base = BankingKnowledgeBase()
model_orchestrator = ModelOrchestrator(
    openai_client=openai_client,
    gemini_client=gemini_client,
    claude_client=claude_client
)
test_generator = TestCaseGenerator(knowledge_base)

@slack_app.command("/generate-tests")
def handle_generate_tests_command(ack, command, respond):
    """Handler for /generate-tests slash command"""
    ack()
    respond("Processing your request...")
    
    user_story = command['text']
    if not user_story:
        respond("Please provide a user story with the command. Example: `/generate-tests As a loan officer, I want to approve qualified loan applications quickly.`")
        return
    
    # Generate the test cases
    results = process_user_story(user_story)
    
    # Format and send response
    formatted_response = format_test_cases(results)
    respond(formatted_response)

def process_user_story(user_story):
    """Process the user story to generate test cases"""
    # Enrich user story with banking domain knowledge
    enriched_story = knowledge_base.enrich_story(user_story)
    
    # Get AI analysis from orchestrator
    ai_analysis = model_orchestrator.analyze_story(enriched_story)
    
    # Generate test cases based on analysis
    test_cases = test_generator.generate_test_cases(ai_analysis)
    
    return test_cases

def format_test_cases(test_cases):
    """Format test cases for Slack response"""
    response = "📋 *Generated Test Cases*\n\n"
    
    for i, test in enumerate(test_cases, 1):
        response += f"*Test Case {i}: {test['title']}*\n"
        response += f"*Description:* {test['description']}\n"
        response += "*Steps:*\n"
        
        for j, step in enumerate(test['steps'], 1):
            response += f"{j}. {step}\n"
            
        response += f"*Expected Result:* {test['expected_result']}\n"
        response += f"*Test Type:* {test['type']}\n\n"
    
    return response

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Endpoint for Slack events"""
    return handler.handle(request)

if __name__ == "__main__":
    app.run(port=3000)