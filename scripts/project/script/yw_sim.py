"""
Youthful Wellspring Simulation Module
Replicates the React SPA's PLC/SCADA logic for demo purposes.

To activate: Create a gateway timer script that calls:
    project.script.yw_sim.run_tick("[default]YW_Demo")
every 2 seconds.
"""

import system
from java.util import Date


# === TANK SIMULATION ===

def update_tank_levels(base_path, pump_running, backwash_in_progress):
	"""
	Update all tank levels based on pump state and outlet valve positions.
	Inlet valves fill tanks; outlet valves drain tanks.
	"""
	tank_names = ["Tank_A", "Tank_B", "Tank_C", "Tank_D"]
	
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		
		# Read current state
		level = system.tag.readBlocking([tank_path + "/Level"])[0].value
		inlet_open = system.tag.readBlocking([tank_path + "/InletValve"])[0].value
		outlet_open = system.tag.readBlocking([tank_path + "/OutletValve"])[0].value
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		
		if not enabled:
			continue
		
		# Simulate level changes
		delta = 0.0
		
		# Pump running + inlet valve = filling
		if pump_running and inlet_open and not backwash_in_progress:
			delta += 1.5  # Fill rate per tick
		
		# Outlet valve or backwash = draining
		if outlet_open or backwash_in_progress:
			delta -= 0.8  # Drain rate per tick
		
		# Clamp level
		new_level = max(0.0, min(100.0, level + delta))
		
		# Write back
		system.tag.writeBlocking([tank_path + "/Level"], [new_level])
		
		# Update demand flag
		low_sp = system.tag.readBlocking([tank_path + "/LowSP"])[0].value
		demand = new_level < low_sp
		system.tag.writeBlocking([tank_path + "/Demand"], [demand])


# === VALVE PRIORITY ARBITRATION ===

def update_valve_logic(base_path):
	"""
	Priority-based valve control: open inlet valve for highest-priority tank with demand.
	"""
	tank_names = ["Tank_A", "Tank_B", "Tank_C", "Tank_D"]
	
	# Gather tank states
	tanks = []
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		demand = system.tag.readBlocking([tank_path + "/Demand"])[0].value
		priority = system.tag.readBlocking([tank_path + "/Priority"])[0].value
		level = system.tag.readBlocking([tank_path + "/Level"])[0].value
		high_sp = system.tag.readBlocking([tank_path + "/HighSP"])[0].value
		
		if enabled and demand:
			tanks.append({
				"name": tank_name,
				"path": tank_path,
				"priority": priority,
				"level": level,
				"high_sp": high_sp
			})
	
	# Sort by priority (0 = highest)
	tanks.sort(key=lambda t: t["priority"])
	
	# Close all inlet valves first
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		system.tag.writeBlocking([tank_path + "/InletValve"], [False])
	
	# Open inlet valve for highest-priority tank
	if len(tanks) > 0:
		winner = tanks[0]
		# Only open if not yet at high setpoint
		if winner["level"] < winner["high_sp"]:
			system.tag.writeBlocking([winner["path"] + "/InletValve"], [True])
	
	# Update system-level demand flag
	any_demand = len(tanks) > 0
	system.tag.writeBlocking([base_path + "/System/AnyDemand"], [any_demand])


# === PUMP CONTROL ===

def update_pump(base_path):
	"""
	Pump logic:
	- Auto mode: run if system demand exists
	- Manual mode: follow command
	"""
	mode = system.tag.readBlocking([base_path + "/Pump/Mode"])[0].value
	command = system.tag.readBlocking([base_path + "/Pump/Command"])[0].value
	fault = system.tag.readBlocking([base_path + "/Pump/Fault"])[0].value
	any_demand = system.tag.readBlocking([base_path + "/System/AnyDemand"])[0].value
	fault_action = system.tag.readBlocking([base_path + "/Mode/FaultAction"])[0].value
	
	should_run = False
	
	if mode == "Auto":
		should_run = any_demand
	elif mode == "Manual":
		should_run = command
	
	# Stop on fault if configured
	if fault and fault_action == "Stop":
		should_run = False
	
	# Update running state
	currently_running = system.tag.readBlocking([base_path + "/Pump/Running"])[0].value
	
	if should_run != currently_running:
		system.tag.writeBlocking([base_path + "/Pump/Running"], [should_run])
		
		if should_run:
			# Record start time
			system.tag.writeBlocking([base_path + "/Pump/LastStartTime"], [Date()])
	
	# Increment run hours (tick = 2s = 1/1800 hour)
	if should_run:
		run_hours = system.tag.readBlocking([base_path + "/Pump/RunHours"])[0].value
		system.tag.writeBlocking([base_path + "/Pump/RunHours"], [run_hours + (2.0 / 3600.0)])


# === BACKWASH SEQUENCE ===

BACKWASH_STEPS = [
	{"name": "Drain", "duration": 10},
	{"name": "Rinse", "duration": 10},
	{"name": "Refill", "duration": 10}
]

def update_backwash(base_path):
	"""
	Simple backwash state machine.
	"""
	in_progress = system.tag.readBlocking([base_path + "/Backwash/InProgress"])[0].value
	command = system.tag.readBlocking([base_path + "/Backwash/Command"])[0].value
	step = system.tag.readBlocking([base_path + "/Backwash/Step"])[0].value
	progress = system.tag.readBlocking([base_path + "/Backwash/Progress"])[0].value
	
	if command and not in_progress:
		# Start sequence
		system.tag.writeBlocking([base_path + "/Backwash/InProgress"], [True])
		system.tag.writeBlocking([base_path + "/Backwash/Step"], [BACKWASH_STEPS[0]["name"]])
		system.tag.writeBlocking([base_path + "/Backwash/Progress"], [0.0])
		system.tag.writeBlocking([base_path + "/Backwash/Command"], [False])
	
	if in_progress:
		# Find current step index
		current_idx = None
		for i, s in enumerate(BACKWASH_STEPS):
			if s["name"] == step:
				current_idx = i
				break
		
		if current_idx is None:
			# Reset if invalid
			system.tag.writeBlocking([base_path + "/Backwash/InProgress"], [False])
			system.tag.writeBlocking([base_path + "/Backwash/Step"], ["Idle"])
			return
		
		# Increment progress (each tick = 2s)
		new_progress = progress + (2.0 / BACKWASH_STEPS[current_idx]["duration"]) * 100.0
		
		if new_progress >= 100.0:
			# Move to next step
			if current_idx + 1 < len(BACKWASH_STEPS):
				system.tag.writeBlocking([base_path + "/Backwash/Step"], [BACKWASH_STEPS[current_idx + 1]["name"]])
				system.tag.writeBlocking([base_path + "/Backwash/Progress"], [0.0])
			else:
				# Sequence complete
				system.tag.writeBlocking([base_path + "/Backwash/InProgress"], [False])
				system.tag.writeBlocking([base_path + "/Backwash/Step"], ["Idle"])
				system.tag.writeBlocking([base_path + "/Backwash/Progress"], [0.0])
				system.tag.writeBlocking([base_path + "/Backwash/LastRun"], [Date()])
		else:
			system.tag.writeBlocking([base_path + "/Backwash/Progress"], [new_progress])


# === MAIN TICK ===

def run_tick(base_path):
	"""
	Main simulation loop - call this from a gateway timer every 2 seconds.
	
	Args:
	    base_path: Tag path to the demo folder, e.g. "[default]YW_Demo"
	"""
	# Check if simulation is active
	sim_active = system.tag.readBlocking([base_path + "/System/SimulationActive"])[0].value
	if not sim_active:
		return
	
	# Update backwash first
	update_backwash(base_path)
	
	# Read pump & backwash state
	pump_running = system.tag.readBlocking([base_path + "/Pump/Running"])[0].value
	backwash_in_progress = system.tag.readBlocking([base_path + "/Backwash/InProgress"])[0].value
	
	# Update tank levels
	update_tank_levels(base_path, pump_running, backwash_in_progress)
	
	# Update valve logic
	update_valve_logic(base_path)
	
	# Update pump
	update_pump(base_path)
	
	# Update last update timestamp
	system.tag.writeBlocking([base_path + "/System/LastUpdate"], [Date()])


# === HELPER FUNCTIONS FOR PERSPECTIVE ===

def get_tank_snapshot():
	"""
	Return a Python list of tank dictionaries for display in Perspective tables/repeaters.
	"""
	base_path = "[default]YW_Demo"
	tank_names = ["Tank_A", "Tank_B", "Tank_C", "Tank_D"]
	
	tanks = []
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		name = system.tag.readBlocking([tank_path + "/Name"])[0].value
		level = system.tag.readBlocking([tank_path + "/Level"])[0].value
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		demand = system.tag.readBlocking([tank_path + "/Demand"])[0].value
		
		tanks.append({
			"name": name,
			"level": level,
			"enabled": enabled,
			"demand": demand,
			"path": tank_path
		})
	
	return tanks


def get_diagnostics_data():
	"""
	Return diagnostic data as a dataset for the diagnostics screen.
	"""
	base_path = "[default]YW_Demo"
	
	rows = []
	
	# Pump diagnostics
	pump_running = system.tag.readBlocking([base_path + "/Pump/Running"])[0].value
	pump_fault = system.tag.readBlocking([base_path + "/Pump/Fault"])[0].value
	pump_hours = system.tag.readBlocking([base_path + "/Pump/RunHours"])[0].value
	
	rows.append({
		"component": "Pump",
		"parameter": "Running",
		"value": "Yes" if pump_running else "No",
		"status": "OK" if not pump_fault else "Fault",
		"lastUpdate": str(Date())
	})
	
	rows.append({
		"component": "Pump",
		"parameter": "Run Hours",
		"value": "%.1f hrs" % pump_hours,
		"status": "OK",
		"lastUpdate": str(Date())
	})
	
	# Tank diagnostics
	tank_names = ["Tank_A", "Tank_B", "Tank_C", "Tank_D"]
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		name = system.tag.readBlocking([tank_path + "/Name"])[0].value
		level = system.tag.readBlocking([tank_path + "/Level"])[0].value
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		
		rows.append({
			"component": name,
			"parameter": "Level",
			"value": "%.1f%%" % level,
			"status": "OK" if enabled else "Disabled",
			"lastUpdate": str(Date())
		})
	
	return system.dataset.toDataSet(["component", "parameter", "value", "status", "lastUpdate"], rows)
