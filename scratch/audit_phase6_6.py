import json

with open("data/commands.json", "r", encoding="utf-8") as f:
    cmds = json.load(f)
print("=== EXISTING COMMANDS (Total: {}) ===".format(len(cmds)))
for i, c in enumerate(cmds):
    print("{}. [{}] {} ({}) - warning: {}".format(i+1, c.get("category"), c.get("command"), c.get("platform"), c.get("warnings")))

with open("data/quizzes.json", "r", encoding="utf-8") as f:
    quizzes = json.load(f)
print("\n=== EXISTING QUIZZES (Total: {}) ===".format(len(quizzes)))
for q in quizzes:
    print("- {}: {} ({} questions)".format(q.get("id"), q.get("title"), len(q.get("questions", []))))
    for qi, qitem in enumerate(q.get("questions", [])):
        print("    Q{}: {} (Ans: {})".format(qi+1, qitem.get("question")[:50], qitem.get("correctIndex")))

with open("data/resources.json", "r", encoding="utf-8") as f:
    res = json.load(f)
print("\n=== EXISTING RESOURCES (Total: {}) ===".format(len(res)))
for r in res:
    print("- {}: [{}] {} ({}) -> {}".format(r.get("id"), r.get("category"), r.get("title"), r.get("type"), r.get("url")))
