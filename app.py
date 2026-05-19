from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')

def ask_ai(prompt):
   MODELS = [
    "openrouter/owl-alpha",
    "mistralai/mistral-nemo",
    "arcee-ai/trinity-large-thinking:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "google/gemma-3-27b-it:free",
]
    
    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }),
                timeout=30
            )
            result = response.json()
            if 'choices' in result:
                answer = result['choices'][0]['message']['content']
                if answer and len(answer) > 10:
                    return answer
        except:
            continue
    
    return "Service busy, please try again!"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-post', methods=['POST'])
def check_post():
    data = request.get_json()
    post = data['post']
    rules = data['rules']
    
    prompt = f"""
    You are a Reddit moderator AI assistant.
    
    Community Rules:
    {rules}
    
    Post to check:
    {post}
    
    Analyze this post and provide:
    1. Rule Violation: Yes/No
    2. Which rule is violated (if any)
    3. Toxicity Level: Low/Medium/High
    4. Recommended Action: Approve/Remove/Warn/Ban
    5. Reason for action
    6. Suggested reply to user (if needed)
    
    Be precise and helpful.
    """
    
    result = ask_ai(prompt)
    return jsonify({'result': result})

@app.route('/scan-comment', methods=['POST'])
def scan_comment():
    data = request.get_json()
    comment = data['comment']
    
    prompt = f"""
    You are a Reddit content moderator AI.
    
    Analyze this comment:
    "{comment}"
    
    Provide:
    1. Toxic: Yes/No
    2. Toxicity Type: (Hate Speech/Spam/Harassment/Safe)
    3. Severity: Low/Medium/High
    4. Action: Keep/Remove/Warn User
    5. Reason
    
    Be precise and concise.
    """
    
    result = ask_ai(prompt)
    return jsonify({'result': result})

@app.route('/suggest-action', methods=['POST'])
def suggest_action():
    data = request.get_json()
    situation = data['situation']
    
    prompt = f"""
    You are an experienced Reddit moderator AI assistant.
    
    Situation: {situation}
    
    Suggest the best moderation action:
    1. Recommended Action
    2. Reason
    3. Message to send to user
    4. Future prevention tips
    
    Be helpful and fair.
    """
    
    result = ask_ai(prompt)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)