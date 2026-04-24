#!/usr/bin/env python3
"""Grade all eval outputs for ad-creative skill iteration 1."""
import json
import os
import re

BASE = "/Users/wayne/.claude/skills/ad-creative-workspace/iteration-1"

def grade_json_prompts(path, eval_name):
    """Grade a JSON prompts file."""
    results = {"eval_name": eval_name, "expectations": []}

    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        results["expectations"].append({"text": "Valid JSON output", "passed": False, "evidence": f"File not found or invalid JSON: {path}"})
        return results

    # 1. Valid JSON array
    is_array = isinstance(data, list)
    results["expectations"].append({
        "text": "Valid JSON array format",
        "passed": is_array,
        "evidence": f"Type: {type(data).__name__}, length: {len(data) if is_array else 'N/A'}"
    })

    if not is_array:
        return results

    # 2. Each item has "prompt" key
    has_prompt_keys = all("prompt" in item for item in data)
    results["expectations"].append({
        "text": "All items have 'prompt' key",
        "passed": has_prompt_keys,
        "evidence": f"{sum(1 for item in data if 'prompt' in item)}/{len(data)} items have 'prompt' key"
    })

    # 3. Each item has "ratio" key
    has_ratio_keys = all("ratio" in item for item in data)
    results["expectations"].append({
        "text": "All items have 'ratio' key",
        "passed": has_ratio_keys,
        "evidence": f"{sum(1 for item in data if 'ratio' in item)}/{len(data)} items have 'ratio' key"
    })

    # 4. No leftover [PLACEHOLDERS]
    all_text = json.dumps(data)
    placeholders = re.findall(r'\[[A-Z][A-Z _/]+\]', all_text)
    no_placeholders = len(placeholders) == 0
    results["expectations"].append({
        "text": "No unfilled [PLACEHOLDER] brackets",
        "passed": no_placeholders,
        "evidence": f"Found {len(placeholders)} placeholders" + (f": {placeholders[:5]}" if placeholders else "")
    })

    # 5. Contains hex color codes (brand-specific)
    hex_codes = re.findall(r'#[0-9A-Fa-f]{6}', all_text)
    has_hex = len(hex_codes) > 0
    results["expectations"].append({
        "text": "Contains hex color codes (brand-specific)",
        "passed": has_hex,
        "evidence": f"Found {len(hex_codes)} hex codes: {list(set(hex_codes))[:5]}"
    })

    # 6. Uses correct model (nb2/pro, not flux)
    wrong_models = [item.get("model", "") for item in data if "flux" in item.get("model", "").lower()]
    correct_models = len(wrong_models) == 0
    results["expectations"].append({
        "text": "Uses correct model (nb2/pro, not flux)",
        "passed": correct_models,
        "evidence": f"Wrong model references: {wrong_models}" if wrong_models else "No incorrect model references (uses nb2/pro or omits model key)"
    })

    # 7. Prompts are substantial (>200 chars each)
    substantial = all(len(item.get("prompt", "")) > 200 for item in data)
    lengths = [len(item.get("prompt", "")) for item in data]
    results["expectations"].append({
        "text": "All prompts are substantial (>200 chars)",
        "passed": substantial,
        "evidence": f"Prompt lengths: {lengths}, min: {min(lengths)}"
    })

    return results


def grade_text_prompts(path, eval_name):
    """Grade a plain text prompts file."""
    results = {"eval_name": eval_name, "expectations": []}

    try:
        with open(path) as f:
            text = f.read()
    except FileNotFoundError:
        results["expectations"].append({"text": "File exists", "passed": False, "evidence": f"Not found: {path}"})
        return results

    # 1. Contains numbered sections
    sections = re.findall(r'##\s+\d+\.', text)
    has_sections = len(sections) >= 3
    results["expectations"].append({
        "text": "Contains numbered template sections",
        "passed": has_sections,
        "evidence": f"Found {len(sections)} sections"
    })

    # 2. No leftover [PLACEHOLDERS]
    placeholders = re.findall(r'\[[A-Z][A-Z _/]+\]', text)
    no_placeholders = len(placeholders) == 0
    results["expectations"].append({
        "text": "No unfilled [PLACEHOLDER] brackets",
        "passed": no_placeholders,
        "evidence": f"Found {len(placeholders)} placeholders" + (f": {placeholders[:5]}" if placeholders else "")
    })

    # 3. Contains hex color codes
    hex_codes = re.findall(r'#[0-9A-Fa-f]{6}', text)
    has_hex = len(hex_codes) > 0
    results["expectations"].append({
        "text": "Contains hex color codes (brand-specific)",
        "passed": has_hex,
        "evidence": f"Found {len(hex_codes)} hex codes: {list(set(hex_codes))[:5]}"
    })

    # 4. Contains aspect ratio specs
    ratios = re.findall(r'\d+:\d+\s+aspect ratio', text)
    has_ratios = len(ratios) > 0
    results["expectations"].append({
        "text": "Contains aspect ratio specifications",
        "passed": has_ratios,
        "evidence": f"Found {len(ratios)} ratio specs"
    })

    # 5. Substantial length (>500 chars per section)
    total_len = len(text)
    substantial = total_len > 1500
    results["expectations"].append({
        "text": "Substantial prompt detail (>1500 chars total)",
        "passed": substantial,
        "evidence": f"Total length: {total_len} chars"
    })

    # 6. Contains specific template names
    template_names = ["Us vs Them", "Bold Statement", "Post-It", "Native"]
    found = [t for t in template_names if t.lower() in text.lower()]
    has_templates = len(found) > 0
    results["expectations"].append({
        "text": "References specific ad template formats",
        "passed": has_templates,
        "evidence": f"Found template refs: {found}"
    })

    # 7. Brand name appears multiple times
    brand_count = text.lower().count("gymshark")
    brand_present = brand_count >= 3
    results["expectations"].append({
        "text": "Brand name appears throughout (>=3 times)",
        "passed": brand_present,
        "evidence": f"'Gymshark' appears {brand_count} times"
    })

    return results


def check_brand_dna(eval_dir, eval_name):
    """Check if brand DNA document exists and is substantial."""
    dna_path = os.path.join(eval_dir, "brand-dna.md")
    research_path = os.path.join(eval_dir, "brand-research.md")

    path = dna_path if os.path.exists(dna_path) else research_path
    exists = os.path.exists(path)

    result = {
        "text": "Brand research/DNA document exists",
        "passed": exists,
        "evidence": f"Found at {path}" if exists else "No brand-dna.md or brand-research.md"
    }

    if exists:
        with open(path) as f:
            content = f.read()
        is_structured = any(k in content.upper() for k in ["VISUAL SYSTEM", "BRAND OVERVIEW", "PHOTOGRAPHY", "COLOR"])
        return result, {
            "text": "Brand document has structured sections",
            "passed": is_structured,
            "evidence": f"Length: {len(content)} chars, structured: {is_structured}"
        }
    return result, None


# Grade all evals
all_grades = {}

# Eval 1: Aloha
for variant in ["with_skill", "without_skill"]:
    key = f"eval-1-aloha-{variant}"
    output_dir = f"{BASE}/eval-1-aloha/{variant}/outputs"
    grades = grade_json_prompts(f"{output_dir}/prompts.json", key)
    dna_result, dna_struct = check_brand_dna(output_dir, key)
    grades["expectations"].insert(0, dna_result)
    if dna_struct:
        grades["expectations"].insert(1, dna_struct)
    all_grades[key] = grades

    # Save grading.json
    grade_dir = f"{BASE}/eval-1-aloha/{variant}"
    with open(f"{grade_dir}/grading.json", 'w') as f:
        json.dump(grades, f, indent=2)

# Eval 2: Gymshark
for variant in ["with_skill", "without_skill"]:
    key = f"eval-2-gymshark-{variant}"
    output_dir = f"{BASE}/eval-2-gymshark/{variant}/outputs"
    if variant == "with_skill":
        grades = grade_text_prompts(f"{output_dir}/prompts.txt", key)
    else:
        grades = grade_text_prompts(f"{output_dir}/prompts.txt", key)
    dna_result, dna_struct = check_brand_dna(output_dir, key)
    grades["expectations"].insert(0, dna_result)
    if dna_struct:
        grades["expectations"].insert(1, dna_struct)
    all_grades[key] = grades

    grade_dir = f"{BASE}/eval-2-gymshark/{variant}"
    with open(f"{grade_dir}/grading.json", 'w') as f:
        json.dump(grades, f, indent=2)

# Eval 3: Grind
for variant in ["with_skill", "without_skill"]:
    key = f"eval-3-grind-{variant}"
    output_dir = f"{BASE}/eval-3-grind/{variant}/outputs"
    grades = grade_json_prompts(f"{output_dir}/prompts.json", key)
    dna_result, dna_struct = check_brand_dna(output_dir, key)
    grades["expectations"].insert(0, dna_result)
    if dna_struct:
        grades["expectations"].insert(1, dna_struct)
    all_grades[key] = grades

    grade_dir = f"{BASE}/eval-3-grind/{variant}"
    with open(f"{grade_dir}/grading.json", 'w') as f:
        json.dump(grades, f, indent=2)

# Print summary
print("=" * 60)
print("GRADING SUMMARY")
print("=" * 60)
for key, grades in all_grades.items():
    passed = sum(1 for e in grades["expectations"] if e["passed"])
    total = len(grades["expectations"])
    print(f"\n{key}: {passed}/{total} passed")
    for e in grades["expectations"]:
        status = "PASS" if e["passed"] else "FAIL"
        print(f"  [{status}] {e['text']}")
        if not e["passed"]:
            print(f"         {e['evidence']}")
