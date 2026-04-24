def score(solution_output: dict, expected: dict, input_data: dict) -> dict:
    if not isinstance(solution_output, dict):
        return {"score": 0, "max": 100, "reason": "Invalid output format"}
        
    flow_plan = solution_output.get("flow_plan", [])
    if not isinstance(flow_plan, list):
        return {"score": 0, "max": 100, "reason": "Invalid flow_plan format"}

    # Extract user assigned flows
    assigned_flows = {item["pipe"]: max(0, float(item.get("flow", 0))) for item in flow_plan if isinstance(item, dict) and "pipe" in item}
    
    # Parse network from input_data
    pipes = {}
    for p in input_data.get("pipes", []):
        pipe_id = f"{p['from']}->{p['to']}"
        pipes[pipe_id] = p
        
    sinks = {s["id"]: s["demand"] for s in input_data.get("sinks", [])}
    
    # Tracking per tick
    sink_received_per_tick = {s_id: 0.0 for s_id in sinks}
    total_leaked_per_tick = 0.0
    
    for pipe_id, p in pipes.items():
        flow = assigned_flows.get(pipe_id, 0.0)
        
        # Enforce physical pipe capacity constraint
        capacity = float(p.get("capacity", float('inf')))
        flow = min(flow, capacity)
        
        leak_rate = float(p.get("leak_rate", 0.0))
        
        # Calculate delivery and leakage
        delivered = flow * (1 - leak_rate)
        leaked = flow * leak_rate
        
        total_leaked_per_tick += leaked
        
        # If this pipe connects to a sink, add to its received total
        if p["to"] in sinks:
            sink_received_per_tick[p["to"]] += delivered
            
    ticks = 60
    total_leaked = total_leaked_per_tick * ticks
    
    # Check survival constraint
    for s_id, demand in sinks.items():
        total_demand = demand * ticks
        received = sink_received_per_tick[s_id] * ticks
        
        if received < 0.8 * total_demand:
            return {
                "score": 0, 
                "max": 100, 
                "reason": "survival_violation",
                "breakdown": {
                    "sink": s_id,
                    "received": received,
                    "required": 0.8 * total_demand
                }
            }
            
    # Calculate final score
    total_delivered = sum(sink_received_per_tick.values()) * ticks
    raw_score = total_delivered - 2 * total_leaked
    
    # Normalize to 0-100 range based on a theoretical maximum
    theoretical_max = sum(sinks.values()) * ticks
    
    if theoretical_max > 0:
        normalized_score = (raw_score / theoretical_max) * 100
    else:
        normalized_score = 0
        
    final_score = max(0, min(100, int(normalized_score)))
    
    return {
        "score": final_score,
        "max": 100,
        "breakdown": {
            "raw_score": raw_score,
            "total_delivered": total_delivered,
            "total_leaked": total_leaked,
            "theoretical_max": theoretical_max
        }
    }

