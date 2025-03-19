import tkinter as tk
from tkinter import ttk
import webview
import json
import os

class FlashcardAPI:
    def __init__(self):
        self.cards = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'emia4110.txt')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    question, answer = line.strip().split('\t')
                    self.cards.append({
                        'question': question,
                        'answer': answer
                    })
    
    def get_cards(self):
        return {
            'cards': self.cards,
            'total_cards': len(self.cards)
        }

def get_html_content():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OCES2003 Midterm Review Flash Cards</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {
            font-family: 'Courier New', monospace;
            margin: 20px;
            background-color: #f0f0f0;
            background-image: 
                linear-gradient(rgba(200, 200, 200, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(200, 200, 200, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        #card {
            background: #F2F6FA;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            min-height: 200px;
            cursor: pointer;
            margin-bottom: 20px;
            font-size: 17px;
            line-height: 1.5;
            color: #162029;
            position: relative;
        }
        .flip-indicator {
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: #666;
            font-style: italic;
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        button {
            font-family: 'Courier New', monospace;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #162029;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #8ACC24;
        }
        button.random-button {
            background-color: #FC6B3C;
        }
        button.random-button:hover {
            background-color: #E55B2F;
        }
        .counter {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div id="card" onclick="toggleCard()">
        <div id="content"></div>
        <div class="flip-indicator">Click to flip</div>
    </div>
    <div class="controls">
        <button onclick="previousCard()">Previous</button>
        <span class="counter">Card <span id="current">1</span> of <span id="total">0</span></span>
        <div class="button-group">
            <button onclick="nextCard()">Next</button>
            <button class="random-button" onclick="randomCard()">Random</button>
        </div>
    </div>

    <script>
        let currentIndex = 0;
        let showingAnswer = false;
        let cards = [];
        
        function updateContent() {
            if (!cards || cards.length === 0) {
                document.getElementById('content').innerHTML = 'No cards available';
                return;
            }

            const card = cards[currentIndex];
            const content = showingAnswer ? card.answer : card.question;
            
            let lines = content.split('<br>');
            let processedLines = lines.map(line => {
                if (line.includes('(a)')) {
                    const [before, after] = line.split('(a)', 2);
                    return `<strong>${before}</strong>(a)${after}`;
                }
                return line;
            });
            
            document.getElementById('content').innerHTML = processedLines.join('<br>');
            document.getElementById('current').textContent = currentIndex + 1;
            document.getElementById('total').textContent = cards.length;
            
            if (typeof MathJax !== 'undefined') {
                MathJax.typesetPromise().catch(err => {
                    console.log('MathJax error:', err);
                });
            }
        }

        function toggleCard() {
            showingAnswer = !showingAnswer;
            updateContent();
        }

        function previousCard() {
            currentIndex = (currentIndex - 1 + cards.length) % cards.length;
            showingAnswer = false;
            updateContent();
        }

        function nextCard() {
            currentIndex = (currentIndex + 1) % cards.length;
            showingAnswer = false;
            updateContent();
        }

        function randomCard() {
            const oldIndex = currentIndex;
            while (currentIndex === oldIndex && cards.length > 1) {
                currentIndex = Math.floor(Math.random() * cards.length);
            }
            showingAnswer = false;
            updateContent();
        }
    </script>
</body>
</html>
"""

def main():
    api = FlashcardAPI()
    
    window = webview.create_window(
        'OCES2003 Midterm Review Flash Cards',
        html=get_html_content(),
        js_api=api
    )
    
    def on_loaded():
        cards_data = api.get_cards()
        window.evaluate_js(f"""
            cards = {json.dumps(cards_data['cards'])};
            updateContent();
        """)
    
    window.events.loaded += on_loaded
    webview.start(debug=True)

if __name__ == '__main__':
    main()