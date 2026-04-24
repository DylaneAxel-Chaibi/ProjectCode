# The Martian Oxygen Grid

**Difficulty:** Medium  
**Domain:** Optimization  

## The Problem

You are tasked with routing oxygen from generator nodes to sink nodes through a complex pipe network on Mars. Each pipe in the network has a maximum `capacity` (the maximum oxygen flow it can handle per tick) and a `leak_rate` (a value between `0.0` and `1.0` representing the percentage of oxygen lost in transit). 

The simulation runs for a total of **60 ticks**. Your goal is to determine a constant flow plan for each pipe to maximize the score while satisfying survival constraints.

## Input Format

Input is provided as a JSON object via `stdin`.

```json
{
  "nodes": [
    {"id": "A", "type": "generator", "output": 100},
    {"id": "B", "type": "relay"}
  ],
  "pipes": [
    {"from": "A", "to": "B", "capacity": 80, "leak_rate": 0.1}
  ],
  "sinks": [
    {"id": "C", "demand": 60}
  ]
}
```

## Output Format

Output should be a JSON object via `stdout`, detailing the constant flow assigned to each pipe.

```json
{
  "flow_plan": [
    {"pipe": "A->B", "flow": 70}
  ]
}
```

## Scoring Formula

Your solution is evaluated based on the total oxygen successfully delivered to sinks, minus the penalty for oxygen leaked into the Martian atmosphere over the 60 ticks:

```text
Score = sum(oxygen_delivered, t=0..60) - 2 * sum(oxygen_leaked, t=0..60)
```

## Survival Constraint

Mars is unforgiving. Each sink **must** receive at least **80% of its demanded oxygen** after accounting for leakages.

If **any** sink receives less than 80% of its demand in the final delivered flow, your plan fails completely: **Score = 0** regardless of the total oxygen delivered.

## Examples

### Example 1: Direct Connection

**Input:**
```json
{
  "nodes": [
    {"id": "Gen1", "type": "generator", "output": 50}
  ],
  "pipes": [
    {"from": "Gen1", "to": "Sink1", "capacity": 50, "leak_rate": 0.0}
  ],
  "sinks": [
    {"id": "Sink1", "demand": 40}
  ]
}
```

**Output:**
```json
{
  "flow_plan": [
    {"pipe": "Gen1->Sink1", "flow": 50}
  ]
}
```

*Explanation:* With no leakage, all 50 units reach the sink. This perfectly satisfies the >= 80% demand constraint (needs >= 32). Pumping maximum capacity gives the best score since there's no leak penalty.

### Example 2: Leaky Pipe

**Input:**
```json
{
  "nodes": [
    {"id": "G1", "type": "generator", "output": 100}
  ],
  "pipes": [
    {"from": "G1", "to": "S1", "capacity": 100, "leak_rate": 0.2}
  ],
  "sinks": [
    {"id": "S1", "demand": 50}
  ]
}
```

**Output:**
```json
{
  "flow_plan": [
    {"pipe": "G1->S1", "flow": 50}
  ]
}
```

*Explanation:* Pumping 50 results in `50 * 0.2 = 10` leaked. Delivered = `50 - 10 = 40`. The sink gets 40, which is exactly 80% of 50. This satisfies the constraint with minimal leak penalty.

### Example 3: Routing Choice

**Input:**
```json
{
  "nodes": [
    {"id": "G", "type": "generator", "output": 100},
    {"id": "R1", "type": "relay"}
  ],
  "pipes": [
    {"from": "G", "to": "R1", "capacity": 50, "leak_rate": 0.1},
    {"from": "G", "to": "S", "capacity": 60, "leak_rate": 0.5},
    {"from": "R1", "to": "S", "capacity": 50, "leak_rate": 0.0}
  ],
  "sinks": [
    {"id": "S", "demand": 40}
  ]
}
```

**Output:**
```json
{
  "flow_plan": [
    {"pipe": "G->R1", "flow": 40},
    {"pipe": "G->S", "flow": 0},
    {"pipe": "R1->S", "flow": 36}
  ]
}
```

*Explanation:* The direct path `G->S` leaks 50%, carrying a huge penalty. The path through `R1` leaks 10% on the first leg. Pumping 40 to `R1` leaks 4, delivering 36 to `R1`. We then pump 36 from `R1` to `S`. Total delivered is 36, which is > 80% of 40 (32).
