import json
from pathlib import Path

ROOT_DIR = Path('.')

with open(ROOT_DIR / 'data' / 'troubleshooting-labs.json', 'r', encoding='utf-8') as f:
    labs = json.load(f)
with open(ROOT_DIR / 'data' / 'commands.json', 'r', encoding='utf-8') as f:
    cmds = json.load(f)
cmd_ids = {c['id'] for c in cmds}

print(f"Total labs: {len(labs)}")
all_lab_ids = set()

for lab in labs:
    lid = lab['id']
    title = lab['title']
    assert lid not in all_lab_ids, f"Duplicate lab ID: {lid}"
    all_lab_ids.add(lid)
    
    print(f"\nLab: {lid} - {title}")
    
    # Terminal diagnosis & explanation
    diag = lab.get('finalDiagnosis')
    assert diag is not None, f"Lab {lid} missing finalDiagnosis"
    assert diag.get('title'), f"Lab {lid} missing diagnosis title"
    assert diag.get('rootCause'), f"Lab {lid} missing diagnosis rootCause/explanation"
    assert diag.get('evidenceSummary'), f"Lab {lid} missing diagnosis evidenceSummary"
    assert diag.get('recommendedRemediation'), f"Lab {lid} missing diagnosis recommendedRemediation"
    assert diag.get('verificationSteps'), f"Lab {lid} missing diagnosis verificationSteps"
    
    # Decision points graph
    pts = lab.get('decisionPoints', [])
    assert len(pts) >= 3, f"Lab {lid} has fewer than 3 decision points"
    
    dp_ids = set()
    next_targets = set()
    initial_id = lab.get('initialStepId')
    assert initial_id == pts[0]['id'], f"initialStepId mismatch in {lid}"
    
    for pt in pts:
        pid = pt['id']
        assert pid not in dp_ids, f"Duplicate decision point ID {pid} in {lid}"
        dp_ids.add(pid)
        
        # Supporting evidence exists
        assert pt.get('evidence'), f"Decision point {pid} missing evidence in {lid}"
        assert len(pt['evidence'].strip()) > 10, f"Decision point {pid} evidence too brief in {lid}"
        
        # Options
        opts = pt.get('options', [])
        assert len(opts) >= 2, f"Decision point {pid} has fewer than 2 options"
        opt_ids = set()
        for opt in opts:
            oid = opt['id']
            assert oid not in opt_ids, f"Duplicate option ID {oid} in {pid}"
            opt_ids.add(oid)
            nxt = opt['nextStepId']
            next_targets.add(nxt)
            
    # Check that all next targets exist or are 'diagnosis' (terminal)
    valid_targets = dp_ids | {'diagnosis'}
    for t in next_targets:
        assert t in valid_targets, f"Target '{t}' not in valid targets in {lid}"
        
    # Check orphan nodes (nodes not referenced by any option, except initialStepId)
    orphans = dp_ids - next_targets - {initial_id}
    assert len(orphans) == 0, f"Orphan decision points in {lid}: {orphans}"
    
    # Graph reachability to terminal 'diagnosis'
    adj = {}
    for pt in pts:
        adj[pt['id']] = [opt['nextStepId'] for opt in pt.get('options', [])]
        
    def can_reach_terminal(curr, visited):
        if curr == 'diagnosis':
            return True
        if curr in visited:
            return False
        visited.add(curr)
        for nxt in adj.get(curr, []):
            if can_reach_terminal(nxt, visited.copy()):
                return True
        return False
        
    for pid in dp_ids:
        assert can_reach_terminal(pid, set()), f"Decision point {pid} cannot reach terminal diagnosis in {lid}"
        
    print(f"  Graph validated: {len(dp_ids)} decision points, 0 orphans, all reach 'diagnosis'.")
    
    # Check relatedCommands references against commands.json
    rel_cmds = diag.get('relatedCommands', [])
    invalid_cmds = [c for c in rel_cmds if c not in cmd_ids]
    assert len(invalid_cmds) == 0, f"Invalid related commands in {lid}: {invalid_cmds}"
    print(f"  Related commands: {rel_cmds} (all verified in commands.json)")

print("\nALL 6 LAB GRAPHS & COMMAND REFERENCES VALIDATED SUCCESSFULLY!")
