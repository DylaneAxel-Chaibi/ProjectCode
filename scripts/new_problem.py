import argparse
import os

def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Scaffold a new problem.")
    parser.add_argument("--slug", required=True, help="Problem slug (e.g., mini-shell)")
    parser.add_argument("--domain", required=True, help="Problem domain (e.g., Systems)")
    parser.add_argument("--difficulty", required=True, help="Problem difficulty (e.g., Hard)")
    
    args = parser.parse_args()
    
    slug = args.slug
    title = slug.replace("-", " ").title()
    
    # 1. problems/slug/problem.md
    md_content = f"""# {title}

**Difficulty:** {args.difficulty}  
**Domain:** {args.domain}  

## The Problem

Write your problem statement here.

## Input Format

```json
{{}}
```

## Output Format

```json
{{}}
```

## Examples

### Example 1

**Input:**
```json
{{}}
```

**Output:**
```json
{{}}
```
"""
    create_file(os.path.join("problems", slug, "problem.md"), md_content)
    
    # 2. problems/slug/scorer.py
    scorer_content = """def score(solution_output: dict, expected: dict, input_data: dict) -> dict:
    # TODO: Implement scoring logic
    # Return format: {"score": int, "max": int, "breakdown": {...}}
    return {"score": 0, "max": 100, "reason": "Not implemented"}
"""
    create_file(os.path.join("problems", slug, "scorer.py"), scorer_content)
    
    # 3. problems/slug/validator.py
    validator_content = """def validate(input_data: dict) -> bool:
    # TODO: Implement input validation logic
    return True
"""
    create_file(os.path.join("problems", slug, "validator.py"), validator_content)
    
    # 4. problems/slug/test_cases/.gitkeep
    create_file(os.path.join("problems", slug, "test_cases", ".gitkeep"), "")
    
    # 5. solutions/slug/main.py
    main_content = """import sys
import json

def main():
    input_data = json.loads(sys.stdin.read())
    
    # TODO: Implement solution
    output_data = {}
    
    print(json.dumps(output_data))

if __name__ == "__main__":
    main()
"""
    create_file(os.path.join("solutions", slug, "main.py"), main_content)
    
    # 6. solutions/slug/Makefile
    makefile_content = """run:
\tpython main.py
"""
    create_file(os.path.join("solutions", slug, "Makefile"), makefile_content)
    
    print(f"Problem '{slug}' scaffolded.")
    print(f"Edit problems/{slug}/problem.md to write the statement.")

if __name__ == "__main__":
    main()
