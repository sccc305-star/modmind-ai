function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    document.getElementById('resultContainer').style.display = 'none';
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultContainer').style.display = 'none';
}

function showResult(text) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('result').innerHTML = formatResult(text);
}

function formatResult(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

function copyResult() {
    const result = document.getElementById('result').innerText;
    navigator.clipboard.writeText(result);
    const btn = document.querySelector('.copy-btn');
    btn.innerHTML = '✅ Copied!';
    setTimeout(() => { btn.innerHTML = '📋 Copy'; }, 2000);
}

async function checkPost() {
    const rules = document.getElementById('communityRules').value;
    const post = document.getElementById('postContent').value;

    if (!rules || !post) {
        alert('Please enter both rules and post content!');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/check-post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rules: rules, post: post })
        });
        const data = await response.json();
        showResult(data.result);
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert('Something went wrong! Please try again.');
    }
}

async function scanComment() {
    const comment = document.getElementById('commentContent').value;

    if (!comment) {
        alert('Please enter a comment!');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/scan-comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comment: comment })
        });
        const data = await response.json();
        showResult(data.result);
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert('Something went wrong! Please try again.');
    }
}

async function suggestAction() {
    const situation = document.getElementById('situationContent').value;

    if (!situation) {
        alert('Please describe the situation!');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/suggest-action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ situation: situation })
        });
        const data = await response.json();
        showResult(data.result);
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert('Something went wrong! Please try again.');
    }
}