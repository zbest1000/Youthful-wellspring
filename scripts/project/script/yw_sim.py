"""
Youthful Wellspring Simulation Module
Replicates the React SPA's PLC/SCADA logic from App.tsx

To activate: Create a gateway timer script that calls:
    project.script.yw_sim.run_tick("[default]YW_Demo")
every 2 seconds (matching React's 2000ms interval).
"""

import system
from java.util import Date


def run_tick(base_path):
	"""
	Main simulation loop matching React App.tsx lines 100-195
	
	Args:
	    base_path: Tag path to demo folder, e.g. "[default]YW_Demo"
	"""
	# Check if simulation is active
	sim_active = system.tag.readBlocking([base_path + "/System/SimulationActive"])[0].value
	if not sim_active:
		return
	
	# Check if initialized
	initialized = system.tag.readBlocking([base_path + "/Config/Initialized"])[0].value
	if not initialized:
		return
	
	# === STEP 1: Calculate Effective Fault (lines 108-112) ===
	mode_tags = {
		"eStop": system.tag.readBlocking([base_path + "/Mode/EStop"])[0].value,
		"pressureFault": system.tag.readBlocking([base_path + "/Mode/PressureFault"])[0].value,
		"flowFault": system.tag.readBlocking([base_path + "/Mode/FlowFault"])[0].value,
		"bypassPFFault": system.tag.readBlocking([base_path + "/Mode/BypassPFFault"])[0].value,
		"autoSelected": system.tag.readBlocking([base_path + "/Mode/AutoSelected"])[0].value,
	}
	
	effective_fault = (
		mode_tags["eStop"] or 
		(mode_tags["pressureFault"] and not mode_tags["bypassPFFault"]) or
		mode_tags["flowFault"]
	)
	system.tag.writeBlocking([base_path + "/Mode/EffectiveFault"], [effective_fault])
	
	
	# === STEP 2: Update Tank Fill Requests (lines 115-124) ===
	tank_names = ["Tank_1", "Tank_2", "Tank_3", "Tank_4"]
	tank_data = []
	
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		
		level_pct = system.tag.readBlocking([tank_path + "/LevelPct"])[0].value
		low_sp = system.tag.readBlocking([tank_path + "/LowSP"])[0].value
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		auto_enable = system.tag.readBlocking([tank_path + "/AutoEnable"])[0].value
		sensor_open = system.tag.readBlocking([tank_path + "/SensorOpen"])[0].value
		priority = system.tag.readBlocking([tank_path + "/Priority"])[0].value
		
		# Compute fill request (matching React logic line 117-121)
		fill_req = (
			enabled and 
			auto_enable and 
			level_pct < low_sp and 
			not sensor_open and
			mode_tags["autoSelected"] and
			not effective_fault
		)
		
		system.tag.writeBlocking([tank_path + "/FillReq"], [fill_req])
		
		tank_data.append({
			"path": tank_path,
			"priority": priority,
			"fillReq": fill_req,
			"levelPct": level_pct
		})
	
	
	# === STEP 3: Priority Arbitration (lines 126-143) ===
	backwash_active = system.tag.readBlocking([base_path + "/Backwash/Active"])[0].value
	
	requesting_tanks = [t for t in tank_data if t["fillReq"]]
	
	if len(requesting_tanks) > 0 and not backwash_active:
		# Sort by priority (1=highest, React line 129)
		requesting_tanks.sort(key=lambda t: t["priority"])
		winner = requesting_tanks[0]
		
		# Set valve commands
		for tank in tank_data:
			valve_cmd = (tank["path"] == winner["path"])
			system.tag.writeBlocking([tank["path"] + "/ValveCmd"], [valve_cmd])
			system.tag.writeBlocking([tank["path"] + "/ValveOutput"], [valve_cmd])
	else:
		# Close all valves
		for tank in tank_data:
			system.tag.writeBlocking([tank["path"] + "/ValveCmd"], [False])
			system.tag.writeBlocking([tank["path"] + "/ValveOutput"], [False])
	
	
	# === STEP 4: Calculate Any Demand (line 146) ===
	any_valve_cmd = any(system.tag.readBlocking([t["path"] + "/ValveCmd"])[0].value for t in tank_data)
	any_demand = any_valve_cmd or backwash_active
	system.tag.writeBlocking([base_path + "/Pump/AnyDemand"], [any_demand])
	
	
	# === STEP 5: Pump Request and Running Logic (lines 149-164) ===
	pump_running = system.tag.readBlocking([base_path + "/Pump/PumpRunning"])[0].value
	asc_min_off_timer = system.tag.readBlocking([base_path + "/Pump/ASCMinOffTimer"])[0].value
	asc_min_run_timer = system.tag.readBlocking([base_path + "/Pump/ASCMinRunTimer"])[0].value
	
	if not effective_fault:
		pump_request = any_demand
		system.tag.writeBlocking([base_path + "/Pump/PumpRequest"], [pump_request])
		
		# Start pump if request and not running and ASC min-off satisfied
		if pump_request and not pump_running:
			if not asc_min_off_timer:
				system.tag.writeBlocking([base_path + "/Pump/PumpRunning"], [True])
		
		# Stop pump if no request and running and ASC min-run satisfied
		elif not pump_request and pump_running:
			if not asc_min_run_timer:
				system.tag.writeBlocking([base_path + "/Pump/PumpRunning"], [False])
	else:
		# Fault active - stop pump
		system.tag.writeBlocking([base_path + "/Pump/PumpRunning"], [False])
		system.tag.writeBlocking([base_path + "/Pump/PumpRequest"], [False])
	
	
	# === STEP 6: Simulate Tank Filling (lines 167-177) ===
	pump_running = system.tag.readBlocking([base_path + "/Pump/PumpRunning"])[0].value
	
	for tank in tank_data:
		valve_cmd = system.tag.readBlocking([tank["path"] + "/ValveCmd"])[0].value
		
		if valve_cmd and pump_running and not effective_fault:
			# Fill tank at 0.3% per tick (React line 170)
			new_level = min(tank["levelPct"] + 0.3, 100.0)
			system.tag.writeBlocking([tank["path"] + "/LevelPct"], [new_level])
			system.tag.writeBlocking([tank["path"] + "/LevelX10"], [int(round(new_level * 10))])
	
	
	# === STEP 7: Backwash Timer (lines 180-188) ===
	backwash_timer_pv = system.tag.readBlocking([base_path + "/Backwash/TimerPV"])[0].value
	backwash_duration = system.tag.readBlocking([base_path + "/Backwash/DurationSetting"])[0].value
	
	if backwash_active and backwash_timer_pv < backwash_duration:
		# Increment timer by 2 seconds (React line 181)
		new_timer_pv = backwash_timer_pv + 2
		system.tag.writeBlocking([base_path + "/Backwash/TimerPV"], [new_timer_pv])
		system.tag.writeBlocking([base_path + "/Backwash/Valve"], [True])
	
	elif backwash_active and backwash_timer_pv >= backwash_duration:
		# Backwash complete (React lines 183-187)
		system.tag.writeBlocking([base_path + "/Backwash/Active"], [False])
		system.tag.writeBlocking([base_path + "/Backwash/Valve"], [False])
		system.tag.writeBlocking([base_path + "/Backwash/TimerPV"], [0])
		system.tag.writeBlocking([base_path + "/Backwash/Start"], [False])
	
	
	# === Update System Timestamp ===
	system.tag.writeBlocking([base_path + "/System/LastUpdate"], [Date()])


# === HELPER FUNCTIONS FOR PERSPECTIVE ===

def get_tank_snapshot(base_path="[default]YW_Demo"):
	"""
	Return a Python list of tank dictionaries for display in Perspective tables/repeaters.
	Matches React's tank structure.
	"""
	tank_names = ["Tank_1", "Tank_2", "Tank_3", "Tank_4"]
	
	tanks = []
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		
		name = system.tag.readBlocking([tank_path + "/Name"])[0].value
		level_pct = system.tag.readBlocking([tank_path + "/LevelPct"])[0].value
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		fill_req = system.tag.readBlocking([tank_path + "/FillReq"])[0].value
		valve_cmd = system.tag.readBlocking([tank_path + "/ValveCmd"])[0].value
		priority = system.tag.readBlocking([tank_path + "/Priority"])[0].value
		
		tanks.append({
			"name": name,
			"levelPct": level_pct,
			"enabled": enabled,
			"fillReq": fill_req,
			"valveCmd": valve_cmd,
			"priority": priority,
			"path": tank_path
		})
	
	return tanks


def get_diagnostics_data(base_path="[default]YW_Demo"):
	"""
	Return diagnostic data as a dataset for the diagnostics screen.
	"""
	rows = []
	
	# Pump diagnostics
	pump_running = system.tag.readBlocking([base_path + "/Pump/PumpRunning"])[0].value
	pump_request = system.tag.readBlocking([base_path + "/Pump/PumpRequest"])[0].value
	any_demand = system.tag.readBlocking([base_path + "/Pump/AnyDemand"])[0].value
	asc_min_off = system.tag.readBlocking([base_path + "/Pump/ASCMinOffTimer"])[0].value
	asc_min_run = system.tag.readBlocking([base_path + "/Pump/ASCMinRunTimer"])[0].value
	
	rows.append({
		"component": "Pump",
		"parameter": "Running",
		"value": "Yes" if pump_running else "No",
		"status": "Running" if pump_running else "Stopped",
		"lastUpdate": str(Date())
	})
	
	rows.append({
		"component": "Pump",
		"parameter": "Request",
		"value": "Yes" if pump_request else "No",
		"status": "OK",
		"lastUpdate": str(Date())
	})
	
	rows.append({
		"component": "Pump",
		"parameter": "Any Demand",
		"value": "Yes" if any_demand else "No",
		"status": "OK",
		"lastUpdate": str(Date())
	})
	
	# Mode diagnostics
	auto_selected = system.tag.readBlocking([base_path + "/Mode/AutoSelected"])[0].value
	effective_fault = system.tag.readBlocking([base_path + "/Mode/EffectiveFault"])[0].value
	
	rows.append({
		"component": "Mode",
		"parameter": "Control Mode",
		"value": "AUTO" if auto_selected else "MANUAL",
		"status": "OK",
		"lastUpdate": str(Date())
	})
	
	rows.append({
		"component": "Mode",
		"parameter": "Effective Fault",
		"value": "FAULT" if effective_fault else "OK",
		"status": "Fault" if effective_fault else "OK",
		"lastUpdate": str(Date())
	})
	
	# Tank diagnostics
	tank_names = ["Tank_1", "Tank_2", "Tank_3", "Tank_4"]
	for tank_name in tank_names:
		tank_path = base_path + "/Tanks/" + tank_name
		name = system.tag.readBlocking([tank_path + "/Name"])[0].value
		level_pct = system.tag.readBlocking([tank_path + "/LevelPct"])[0].value
		enabled = system.tag.readBlocking([tank_path + "/Enabled"])[0].value
		fill_req = system.tag.readBlocking([tank_path + "/FillReq"])[0].value
		
		rows.append({
			"component": name,
			"parameter": "Level",
			"value": "%.1f%%" % level_pct,
			"status": "Filling" if fill_req else ("OK" if enabled else "Disabled"),
			"lastUpdate": str(Date())
		})
	
	# Backwash diagnostics
	backwash_active = system.tag.readBlocking([base_path + "/Backwash/Active"])[0].value
	backwash_timer_pv = system.tag.readBlocking([base_path + "/Backwash/TimerPV"])[0].value
	
	rows.append({
		"component": "Backwash",
		"parameter": "Active",
		"value": "Yes (%ds)" % backwash_timer_pv if backwash_active else "No",
		"status": "Active" if backwash_active else "Idle",
		"lastUpdate": str(Date())
	})
	
	return system.dataset.toDataSet(
		["component", "parameter", "value", "status", "lastUpdate"], 
		rows
	)


def get_pump_status_summary(base_path="[default]YW_Demo"):
	"""
	Return a summary dict for pump status cards.
	"""
	return {
		"running": system.tag.readBlocking([base_path + "/Pump/PumpRunning"])[0].value,
		"request": system.tag.readBlocking([base_path + "/Pump/PumpRequest"])[0].value,
		"anyDemand": system.tag.readBlocking([base_path + "/Pump/AnyDemand"])[0].value,
		"available": system.tag.readBlocking([base_path + "/Pump/PumpAvailable"])[0].value,
		"ascMinOffActive": system.tag.readBlocking([base_path + "/Pump/ASCMinOffTimer"])[0].value,
		"ascMinRunActive": system.tag.readBlocking([base_path + "/Pump/ASCMinRunTimer"])[0].value,
	}
