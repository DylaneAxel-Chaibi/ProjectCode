# ProjectCode

ProjectCode is an offline coding challenge and algorithmic assessment platform designed to track problem-solving progression. It features a robust Python-based scoring engine that validates submissions against custom constraints, timeouts, and edge cases, enabling advanced optimization problem sets like graph routing and resource management.

The platform includes an interactive Next.js dashboard that seamlessly integrates with GitHub Actions. As you solve challenges and push your code, an automated pipeline grades your solution, updates the persistent scoreboard, and deploys a modernized Skill Tree UI to GitHub Pages to visualize your learning path.

## Repository Structure

```text
ProjectCode/
├── .github/workflows/   # CI/CD pipelines for auto-grading and Pages deployment
├── problems/            # Problem definitions, Python scorers, and JSON test cases
├── results/             # Persistent JSON datastore (scores.json) for historical submissions
├── runner/              # Core Python grading orchestrator and subprocess isolation logic
├── scripts/             # Developer utilities (e.g., problem scaffolding scripts)
├── solutions/           # User-submitted algorithmic implementations and Makefiles
└── web/                 # Next.js interactive dashboard and React component library
```

## How to Add a New Problem

To quickly scaffold a new challenge, run the included CLI utility:

```bash
python scripts/new_problem.py --slug "your-problem" --domain "Algorithms" --difficulty "Medium"
```

1. Edit the generated `problems/your-problem/problem.md` to finalize the statement.
2. Implement the grading logic in `problems/your-problem/scorer.py`.
3. Add your standard `.json` testing constraints into `problems/your-problem/test_cases/`.

## How to Submit a Solution

1. Navigate to the generated directory for the problem: `solutions/{slug}/`
2. Write your implementation logic in `main.py` (or your preferred language, modifying the `Makefile`).
3. Commit and push your changes to the `main` branch. 
4. The `.github/workflows/grade.yml` GitHub Actions pipeline will automatically intercept the push, run your code against the test cases, and append your score to `results/scores.json`.

## Viewing Results

Once the auto-grader completes its run, the `.github/workflows/deploy.yml` pipeline automatically triggers. It statically builds the Next.js frontend with your latest scores and deploys it.

You can view your real-time Skill Tree and submission history by visiting your GitHub Pages URL (e.g., `https://<your-username>.github.io/projectcode`).

## Local Development

To run the Next.js dashboard locally and view your offline scores:

```bash
cd web
npm install
npm run dev
```

Open `http://localhost:3000` to access the interactive dashboard.
