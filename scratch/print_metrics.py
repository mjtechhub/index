import json

with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f).get('categories', [])

print("TOTAL CATEGORIES:", len(topics))
total_topics = 0
total_pub = 0
total_plan = 0
total_beg = 0
total_int = 0
total_adv = 0

with open('scratch/metrics_utf8.txt', 'w', encoding='utf-8') as out_f:
    for cat in topics:
        cid = cat['id']
        cname = cat['name']
        out_f.write(f"\n### {cname} (`{cid}`)\n")
        cat_b = cat_i = cat_a = 0
        cat_pub = cat_plan = 0
        for sec in cat.get('sections', []):
            s_b = sum(1 for t in sec['subtopics'] if t['level'] == 'Beginner')
            s_i = sum(1 for t in sec['subtopics'] if t['level'] == 'Intermediate')
            s_a = sum(1 for t in sec['subtopics'] if t['level'] == 'Advanced')
            s_pub = sum(1 for t in sec['subtopics'] if t.get('status') == 'published')
            s_plan = sum(1 for t in sec['subtopics'] if t.get('status') == 'planned')
            cat_b += s_b; cat_i += s_i; cat_a += s_a
            cat_pub += s_pub; cat_plan += s_plan
            sname = sec['name']
            tot = len(sec['subtopics'])
            out_f.write(f"- **{sname}**: {tot} topics ({s_pub} Published, {s_plan} Planned) — Beginner: {s_b}, Intermediate: {s_i}, Advanced: {s_a}\n")
        out_f.write(f"**Category Total**: {len(cat['sections'])} sections, {cat_pub+cat_plan} topics ({cat_pub} Published, {cat_plan} Planned) [Beginner: {cat_b}, Intermediate: {cat_i}, Advanced: {cat_a}]\n")
        total_topics += (cat_pub + cat_plan)
        total_pub += cat_pub
        total_plan += cat_plan
        total_beg += cat_b
        total_int += cat_i
        total_adv += cat_a

    out_f.write(f"\nMASTER TOTAL: 6 categories, 60 sections, {total_topics} topics ({total_pub} published, {total_plan} planned) [Beg: {total_beg}, Int: {total_int}, Adv: {total_adv}]\n")
