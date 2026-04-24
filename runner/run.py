import argparse
import datetime
import glob
import importlib.util
import json
import os
import subprocess
import sys

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def run():
    parser = argparse.ArgumentParser(description="Run a solution against test cases.")
    parser.add_argument("--problem", required=True, help="Problem slug (e.g., martian-oxygen)")
    parser.add_argument("--solution", required=True, help="Path to solution folder")
    args = parser.parse_args()

    problem_dir = os.path.join("problems", args.problem)
    test_cases_dir = os.path.join(problem_dir, "test_cases")
    scorer_path = os.path.join(problem_dir, "scorer.py")
    
    # Load the problem-specific scorer dynamically
    scorer = load_module_from_path("scorer", scorer_path)

    # Find all input JSON files
    input_files = sorted(glob.glob(os.path.join(test_cases_dir, "case_*_input.json")))
    
    test_results = []
    total_score = 0
    max_score = 0

    for input_file in input_files:
        # Extract the case ID like "case_01"
        basename = os.path.basename(input_file)
        case_id = basename.replace("_input.json", "")
        expected_file = os.path.join(test_cases_dir, f"{case_id}_expected.json")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = f.read()
            
        with open(expected_file, 'r', encoding='utf-8') as f:
            expected_data = f.read()

        stderr_output = ""
        actual_output = ""
        case_score = 0
        case_max = 0

        # Run solution using make -s run (silent mode to avoid Makefile echo)
        try:
            process = subprocess.run(
                ["make", "-s", "run"],
                cwd=args.solution,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=10
            )
            actual_output = process.stdout
            stderr_output = process.stderr if process.stderr else ""
            
            if process.returncode != 0:
                case_score = 0
                case_max = 100
            else:
                try:
                    out_dict = json.loads(actual_output)
                    exp_dict = json.loads(expected_data)
                    inp_dict = json.loads(input_data)
                    score_result = scorer.score(out_dict, exp_dict, inp_dict)
                    case_score = score_result.get("score", 0)
                    case_max = score_result.get("max", 100)
                    if "reason" in score_result:
                        stderr_output += f"\nReason: {score_result['reason']}"
                except json.JSONDecodeError:
                    case_score = 0
                    case_max = 100
                    stderr_output += "\nInvalid JSON output from solution."
                except Exception as e:
                    case_score = 0
                    case_max = 100
                    stderr_output = f"SCORER ERROR: {str(e)}"
                    
        except subprocess.TimeoutExpired:
            stderr_output = "TIMEOUT after 10s"
            case_score = 0
            case_max = 100
        except Exception as e:
            stderr_output = f"RUNNER ERROR: {str(e)}"
            case_score = 0
            case_max = 100
            
        test_results.append({
            "id": case_id,
            "score": case_score,
            "max": case_max,
            "stderr": stderr_output.strip()
        })
        total_score += case_score
        max_score += case_max

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    result = {
        "problem": args.problem,
        "timestamp": timestamp,
        "total_score": total_score,
        "max_score": max_score,
        "test_cases": test_results
    }
    
    scores_file = os.path.join("results", "scores.json")
    os.makedirs(os.path.dirname(scores_file), exist_ok=True)
    
    if os.path.exists(scores_file):
        with open(scores_file, 'r', encoding='utf-8') as f:
            try:
                scores = json.load(f)
            except json.JSONDecodeError:
                scores = []
    else:
        scores = []
        
    scores.append(result)
    
    with open(scores_file, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2)

if __name__ == "__main__":
    run()
