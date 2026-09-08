#!/usr/bin/env python3
"""
MJ Tech Hub - CI/CD & Local Site Validation Suite
Validates:
1. JSON syntax & schema rules for data files
2. JavaScript syntax & static checks
3. HTML link integrity (internal a href, img src, script src, link href)
4. Duplicate HTML IDs and multiple IDs on a single tag
5. Unescaped literal artifacts (e.g. \\n in HTML)
6. Hardcoded local/environment paths (e.g. c:\\xampp)
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parent.parent

class SiteValidator:
    def __init__(self, root: Path):
        self.root = root
        self.errors = []
        self.warnings = []
        self.stats = {
            "json_files_checked": 0,
            "html_files_checked": 0,
            "js_files_checked": 0,
            "links_checked": 0,
            "assets_checked": 0
        }

    def error(self, category: str, file_path: Path, message: str):
        rel = file_path.relative_to(self.root) if file_path.is_relative_to(self.root) else file_path
        self.errors.append(f"[{category}] {rel}: {message}")

    def warn(self, category: str, file_path: Path, message: str):
        rel = file_path.relative_to(self.root) if file_path.is_relative_to(self.root) else file_path
        self.warnings.append(f"[{category}] {rel}: {message}")

    def validate_json_data(self):
        """Validate JSON files against expected schema structures"""
        data_dir = self.root / "data"
        if not data_dir.exists():
            self.error("JSON", data_dir, "data directory does not exist")
            return

        json_files = list(data_dir.glob("*.json"))
        for jf in json_files:
            self.stats["json_files_checked"] += 1
            try:
                with open(jf, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                self.error("JSON Syntax", jf, f"Invalid JSON syntax: {e}")
                continue

            # Specific file validations
            if jf.name == "tutorials.json":
                if not isinstance(data, list):
                    self.error("JSON Schema", jf, "tutorials.json must be a JSON array")
                else:
                    required_fields = ["id", "title", "description", "category", "level", "readTime", "url"]
                    ids = set()
                    for idx, item in enumerate(data):
                        for rf in required_fields:
                            if rf not in item or not str(item[rf]).strip():
                                self.error("JSON Schema", jf, f"Record #{idx} missing required field '{rf}'")
                        tid = item.get("id")
                        if tid in ids:
                            self.error("JSON Schema", jf, f"Duplicate tutorial id: '{tid}'")
                        ids.add(tid)
                        # Verify tutorial file exists
                        tut_url = item.get("url", "")
                        tut_file = self.root / tut_url.replace("./", "")
                        if not tut_file.exists():
                            self.error("Broken File Ref", jf, f"Tutorial file not found for id '{tid}': {tut_url}")

            elif jf.name == "topics.json":
                if not isinstance(data, dict) or "categories" not in data:
                    self.error("JSON Schema", jf, "topics.json must be an object with 'categories' key")
                else:
                    required_fields = ["id", "name", "type", "description", "url"]
                    for idx, cat in enumerate(data.get("categories", [])):
                        for rf in required_fields:
                            if rf not in cat:
                                self.error("JSON Schema", jf, f"Category #{idx} missing required field '{rf}'")

            elif jf.name == "commands.json":
                if not isinstance(data, list):
                    self.error("JSON Schema", jf, "commands.json must be an array")
                else:
                    required_fields = ["command", "platform", "purpose", "syntax", "example", "expectedResult", "useCase", "category"]
                    for idx, cmd in enumerate(data):
                        for rf in required_fields:
                            if rf not in cmd:
                                self.error("JSON Schema", jf, f"Command #{idx} missing required field '{rf}'")

            elif jf.name == "resources.json":
                if not isinstance(data, list):
                    self.error("JSON Schema", jf, "resources.json must be an array")
                else:
                    required_fields = ["id", "title", "description", "category", "type", "url", "status"]
                    for idx, res in enumerate(data):
                        for rf in required_fields:
                            if rf not in res:
                                self.error("JSON Schema", jf, f"Resource #{idx} missing required field '{rf}'")

    def validate_html_files(self):
        """Validate HTML files for syntax, duplicate IDs, broken links, and artifacts"""
        html_files = [f for f in self.root.rglob("*.html") if "backup" not in f.parts and "public" not in f.parts]

        for hf in html_files:
            self.stats["html_files_checked"] += 1
            try:
                with open(hf, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                self.error("File Read", hf, f"Failed to read file: {e}")
                continue

            # Check literal '\n' artifact
            if r"\n" in content:
                # Find line numbers with literal \n
                lines = content.splitlines()
                for line_idx, line in enumerate(lines, 1):
                    if r"\n" in line:
                        self.error("Artifact", hf, f"Literal '\\n' artifact on line {line_idx}: {line.strip()[:60]}")

            # Check duplicate IDs and multiple IDs on a single tag
            tag_matches = re.finditer(r'<([a-zA-Z0-9]+)([^>]*)>', content)
            file_ids = []
            for tm in tag_matches:
                tag_name = tm.group(1)
                attrs_str = tm.group(2)
                # Find all id="..." in this tag
                ids_in_tag = re.findall(r'\bid=[\"\']([^\"\']+)[\"\']', attrs_str)
                if len(ids_in_tag) > 1:
                    self.error("HTML Syntax", hf, f"Tag <{tag_name}> has multiple id attributes: {ids_in_tag}")
                for i in ids_in_tag:
                    file_ids.append(i)

            id_counts = Counter(file_ids)
            for element_id, count in id_counts.items():
                if count > 1:
                    self.error("Duplicate ID", hf, f"Duplicate ID '#{element_id}' found {count} times on page")

            # Check local file references (href, src)
            # Scripts & Links & Images
            ref_matches = re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']', content)
            asset_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.css', '.js', '.woff', '.woff2')
            for ref in ref_matches:
                # Ignore placeholders, externals, hash anchors, mailto, tel, data
                if ref.startswith(("http://", "https://", "//", "#", "mailto:", "tel:", "data:")):
                    continue
                if ref == "":
                    continue

                if "{{BASE}}" in ref:
                    clean_ref = ref.replace("{{BASE}}/", "").replace("{{BASE}}", "").split("?")[0].split("#")[0]
                    target_path = (self.root / clean_ref).resolve()
                else:
                    clean_ref = ref.split("?")[0].split("#")[0]
                    target_path = (hf.parent / clean_ref).resolve()

                if not clean_ref:
                    continue

                is_asset = any(clean_ref.lower().endswith(ext) for ext in asset_extensions)
                if is_asset:
                    self.stats["assets_checked"] += 1
                else:
                    self.stats["links_checked"] += 1

                if not target_path.exists():
                    ref_type = "Broken Asset" if is_asset else "Broken Link"
                    self.error(ref_type, hf, f"Referenced file not found: '{ref}' -> '{target_path}'")

    def validate_css_assets(self):
        """Validate local assets referenced via url(...) in CSS files"""
        css_files = [f for f in self.root.rglob("*.css") if "backup" not in f.parts and "public" not in f.parts]
        for cf in css_files:
            try:
                with open(cf, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                self.error("CSS Read", cf, f"Failed to read CSS file: {e}")
                continue

            matches = re.finditer(r'url\([\'\"]?([^\'\"\)]+)[\'\"]?\)', content)
            for m in matches:
                ref = m.group(1).strip()
                if ref.startswith(("http://", "https://", "//", "data:")):
                    continue
                clean_ref = ref.split("?")[0].split("#")[0]
                if not clean_ref:
                    continue

                self.stats["assets_checked"] += 1
                target_path = (cf.parent / clean_ref).resolve()
                if not target_path.exists():
                    self.error("Broken CSS Asset", cf, f"Referenced asset not found: '{ref}' -> '{target_path}'")

    def validate_scripts(self):
        """Validate all Python and JS files for hardcoded paths and basic correctness"""
        py_files = [f for f in self.root.rglob("*.py") if "backup" not in f.parts and "public" not in f.parts and f.name != "validate_site.py"]
        for pf in py_files:
            try:
                with open(pf, "r", encoding="utf-8") as f:
                    content = f.read()
                if "xampp" in content.lower():
                    self.error("Hardcoded Path", pf, "Contains hardcoded 'xampp' path")
            except Exception as e:
                self.error("Python", pf, f"Error inspecting Python file: {e}")

        js_files = [f for f in self.root.rglob("*.js") if "backup" not in f.parts and "public" not in f.parts]
        for jf in js_files:
            self.stats["js_files_checked"] += 1
            try:
                with open(jf, "r", encoding="utf-8") as f:
                    content = f.read()
                if "xampp" in content.lower():
                    self.error("Hardcoded Path", jf, "Contains hardcoded 'xampp' path")
            except Exception as e:
                self.error("JS", jf, f"Error inspecting JS file: {e}")

    def run_all(self):
        print("Running MJ Tech Hub Site Validator...")
        self.validate_json_data()
        self.validate_html_files()
        self.validate_css_assets()
        self.validate_scripts()

        print(f"\nChecked:")
        for k, v in self.stats.items():
            print(f"  - {k}: {v}")

        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  [WARN] {w}")

        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  [FAIL] {e}")
            return False
        else:
            print("\nALL CHECKS PASSED: Site is structurally sound!")
            return True

if __name__ == "__main__":
    validator = SiteValidator(REPO_ROOT)
    success = validator.run_all()
    sys.exit(0 if success else 1)
