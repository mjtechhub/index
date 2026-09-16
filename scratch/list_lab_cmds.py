import json

labs = json.load(open('data/troubleshooting-labs.json', encoding='utf-8'))
cmds = {c['id'] for c in json.load(open('data/commands.json', encoding='utf-8'))}

for lab in labs:
    rel = lab['finalDiagnosis'].get('relatedCommands', [])
    invalid = [c for c in rel if c not in cmds]
    print(f"{lab['id']}: all={rel}, invalid={invalid}")
