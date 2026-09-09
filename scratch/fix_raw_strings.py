from pathlib import Path

content_dir = Path('scripts/content')
for p in content_dir.glob('*.py'):
    text = p.read_text(encoding='utf-8')
    # replace "html": """ with "html": r""" where not already raw
    import re
    new_text = re.sub(r'"html":\s*"""', '"html": r"""', text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        print(f"Updated raw strings in {p.name}")
print("Done fixing raw strings.")
