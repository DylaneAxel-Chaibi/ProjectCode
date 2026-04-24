import os
import random

DOMAINS = ["Systems", "Networks", "Databases", "Compilers", "Optimization", "AI", "Algorithms", "Cryptography"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

PROBLEM_TITLES = {
    "Systems": [
        "Process Scheduler", "Virtual Memory Manager", "Buffer Overflow Protector", "Atomic Counter",
        "Pipe Implementation", "Signal Multiplexer", "Shared Memory Pool", "Kernel Module Loader",
        "FileSystem Integrity", "Page Replacement Policy", "LRU Cache", "Wait-Free Queue", "Futex Implementation"
    ],
    "Networks": [
        "TCP Handshake Simulator", "HTTP/2 Frame Parser", "Load Balancer", "DNS Resolver",
        "Congestion Control", "BGP Path Finder", "NAT Traversal", "Packet Filter",
        "QUIC Stream Manager", "ARP Spoofer Detector", "RIP Routing", "IP Defragmenter"
    ],
    "Databases": [
        "B-Tree Indexer", "SQL Query Optimizer", "WAL Logger", "Deadlock Detector",
        "ACID Transaction Manager", "LSM-Tree Storage", "Join Operator", "Bloom Filter",
        "Vector Database Index", "Snapshot Isolation", "Raft Consensus", "Query Planner"
    ],
    "Compilers": [
        "Recursive Descent Parser", "LLVM IR Generator", "Garbage Collector", "JIT Compiler",
        "Register Allocator", "Constant Folder", "Dead Code Eliminator", "Type Checker",
        "Lexical Analyzer", "Instruction Selector", "AST Optimizer", "Closure Converter"
    ],
    "Optimization": [
        "Simplex Algorithm", "Ant Colony Optimization", "Traveling Salesman", "Job Shop Scheduling",
        "Warehouse Location", "Power Grid Balancer", "Route Planner", "Portfolio Optimizer",
        "Supply Chain Flow", "Constraint Solver", "Cutting Stock Problem", "Gradient Descent"
    ],
    "AI": [
        "Backpropagation", "Decision Tree Learner", "K-Means Clustering", "Minimax with Pruning",
        "Q-Learning Agent", "Transformer Attention", "Perceptron", "Genetic Algorithm",
        "Bayesian Network", "SVM Trainer", "CNN Forward Pass", "Pathfinding Heuristic"
    ],
    "Algorithms": [
        "Max Flow Min Cut", "Suffix Automaton", "Heavy-Light Decomposition", "Segment Tree",
        "Fast Fourier Transform", "Convex Hull", "Stable Marriage", "Dynamic Programming",
        "Trie Implementation", "A* Search", "Bipartite Matching", "Knuth-Morris-Pratt"
    ],
    "Cryptography": [
        "AES Implementation", "RSA Generator", "Diffie-Hellman Key Exchange", "Elliptic Curve Signer",
        "Hash Function", "Zero Knowledge Proof", "Secret Sharing", "Digital Signature",
        "Padding Oracle Attack", "Stream Cipher", "Mercurial Hash", "Lattice Cryptosystem"
    ]
}

def slugify(text):
    import re
    # Remove invalid filename characters
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def generate_problem(title, domain, difficulty, id_num):
    slug = f"{slugify(title)}-{id_num}"
    path = f"problems/{slug}"
    os.makedirs(path, exist_ok=True)
    
    with open(f"{path}/problem.md", "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Difficulty:** {difficulty}  \n")
        f.write(f"**Domain:** {domain}  \n\n")
        f.write("## The Problem\n\n")
        f.write(f"Challenge your skills in **{domain}** by implementing an efficient **{title}**.\n\n")
        f.write("This is a procedurally generated challenge to test your implementation speed and accuracy.\n\n")
        f.write("## Input Format\n\nInput via stdin as JSON.\n\n")
        f.write("## Output Format\n\nOutput via stdout as JSON.\n")

    # Basic Scorer
    with open(f"{path}/scorer.py", "w") as f:
        f.write("import json\ndef score(input_data, output_data):\n    return 100, 100\n")

    # Basic Validator
    with open(f"{path}/validator.py", "w") as f:
        f.write("def validate(output_data):\n    return True\n")

    # Makefile
    with open(f"{path}/Makefile", "w") as f:
        f.write("run:\n\tpython3 solution.py\n")

def main():
    count = 0
    while count < 100:
        domain = random.choice(DOMAINS)
        titles = PROBLEM_TITLES.get(domain, ["Generic Challenge"])
        title = random.choice(titles)
        difficulty = random.choice(DIFFICULTIES)
        
        generate_problem(title, domain, difficulty, count + 1)
        count += 1
    
    print(f"Successfully generated {count} problems.")

if __name__ == "__main__":
    main()
