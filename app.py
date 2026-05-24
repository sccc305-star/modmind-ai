from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }),
            timeout=30
        )
        result = response.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
    except:
        pass
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
@app.route('/bulk-scan', methods=['POST'])
def bulk_scan():
    data = request.get_json()
    comments = data['comments']
    
    prompt = f"""
    You are a Reddit content moderator AI.
    
    Analyze these comments one by one:
    {comments}
    
    For each comment provide:
    Comment #: [number]
    Toxic: Yes/No
    Type: (Hate Speech/Spam/Harassment/Safe)
    Action: Keep/Remove/Warn
    
    Be precise and concise.
    """
    
    result = ask_ai(prompt)
    return jsonify({'result': result})

@app.route('/mod-report', methods=['POST'])
def mod_report():
    data = request.get_json()
    community = data['community']
    actions = data['actions']
    
    prompt = f"""
    You are a Reddit moderation AI assistant.
    
    Community: {community}
    Recent Actions: {actions}
    
    Generate a professional weekly moderation report with:
    1. Executive Summary
    2. Total Actions Taken
    3. Most Common Violations
    4. Community Health Score (1-10)
    5. Recommendations for next week
    6. Trends to watch
    
    Be professional and detailed.
    """
    
    result = ask_ai(prompt)
    return jsonify({'result': result})
if __name__ == '__main__':
    app.run(debug=True)