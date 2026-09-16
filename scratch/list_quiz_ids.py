import json

with open('data/quizzes.json', 'r', encoding='utf-8') as f:
    quizzes = json.load(f)

for idx, q in enumerate(quizzes, 1):
    print(f"[{idx}] ID: '{q.get('id')}', Title: '{q.get('title')}', Category: '{q.get('category')}', Questions: {len(q.get('questions', []))}")
