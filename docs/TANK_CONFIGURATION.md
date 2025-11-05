# Tank Configuration Guide

This document explains how to configure the Youthful Wellspring system to handle 1-8 tanks dynamically.

## Overview

The system supports a configurable number of tanks from 1 to 8. The number of active tanks is controlled by the `Config/TankCount` tag, which defaults to 4 tanks.

## Configuration Steps

### 1. Set Tank Count

Navigate to the `Config/TankCount` tag and set the value between 1 and 8:

```
Tag Path: [default]YW_Demo/Config/TankCount
Valid Range: 1-8
Default Value: 4
```

### 2. Enable/Disable Tank Instances

For each tank you want to use, set its `Enabled` flag:

**Tanks 1-4 (Default)**
- Enabled by default
- Already configured with typical setpoints

**Tanks 5-8 (Optional)**
- Disabled by default (Enabled = false)
- Must be enabled manually if using more than 4 tanks

Example paths:
```
[default]YW_Demo/Tanks/Tank_5/Enabled = true
[default]YW_Demo/Tanks/Tank_6/Enabled = true
[default]YW_Demo/Tanks/Tank_7/Enabled = true
[default]YW_Demo/Tanks/Tank_8/Enabled = true
```

### 3. Configure Tank Parameters

For each enabled tank, configure the following parameters:

| Parameter | Tag Path | Description | Default |
|-----------|----------|-------------|---------|
| **Name** | `Tank_X/Name` | Display name | "Tank X" |
| **LowSP** | `Tank_X/LowSP` | Low setpoint (%) | 40.0 |
| **HighSP** | `Tank_X/HighSP` | High setpoint (%) | 95.0 |
| **Priority** | `Tank_X/Priority` | Fill priority (1=highest) | X |
| **Enabled** | `Tank_X/Enabled` | Global enable | true/false |
| **AutoEnable** | `Tank_X/AutoEnable` | AUTO mode enable | true |

## How It Works

### Simulation Script

The simulation script (`yw_sim.py`) dynamically reads the `TankCount` configuration at each execution and only processes tanks 1 through the configured count:

```python
# Read configured tank count (1-8)
tank_count = system.tag.readBlocking([base_path + "/Config/TankCount"])[0].value
tank_count = max(1, min(8, tank_count))  # Clamp to valid range

# Generate tank names based on configuration
tank_names = ["Tank_" + str(i) for i in range(1, tank_count + 1)]
```

This means:
- If `TankCount = 1`, only `Tank_1` is processed
- If `TankCount = 4`, tanks 1-4 are processed (default)
- If `TankCount = 8`, all 8 tanks are processed

### Priority Arbitration

The priority arbitration system works with any number of tanks:
- All enabled tanks with fill requests are considered
- Tanks are sorted by priority (1 = highest priority)
- The tank with the lowest priority number wins the fill request
- Only one tank can fill at a time (unless backwash is active)

## Use Cases

### Single Tank System (TankCount = 1)
- Simplest configuration
- Only Tank_1 is monitored and controlled
- No priority arbitration needed
- Pump runs whenever Tank_1 needs filling

### Standard System (TankCount = 4)
- Default configuration
- Balances complexity and capability
- Suitable for most installations

### Large System (TankCount = 8)
- Maximum configuration
- Requires additional PLC I/O
- All 8 analog inputs and 8 valve outputs must be wired
- Priority arbitration ensures optimal filling sequence

## PLC Integration Notes

When integrating with a real PLC (Click PLC or other), ensure:

1. **Analog Inputs**: Configure one 4-20mA input per tank
   - X001-X008 for Tanks 1-8
   - Scale to DF1-DF8 (0-100%)

2. **Digital Outputs**: Configure one output per tank valve
   - Y002-Y009 for Tank 1-8 valves
   - Plus Y001 for pump contactor

3. **Memory Allocation**:
   - Holding Registers: DS1200-1272 for tank parameters
   - Coils: C100-C168 for tank control flags
   - See `PLC_MAPPING.md` for complete address map

## Changing Configuration at Runtime

The system supports changing `TankCount` while running:

1. **Increasing Tank Count** (e.g., 4 → 6):
   - Set `Config/TankCount = 6`
   - Enable tanks 5 and 6: `Tank_5/Enabled = true`, `Tank_6/Enabled = true`
   - System will start processing new tanks on next simulation tick

2. **Decreasing Tank Count** (e.g., 6 → 4):
   - Set `Config/TankCount = 4`
   - System stops processing tanks 5-8 immediately
   - Valves for disabled tanks are closed
   - Tank levels remain at current values

## Verification Checklist

After configuration changes:

- [ ] Verify `Config/TankCount` is set correctly (1-8)
- [ ] Verify each tank 1-N has `Enabled = true`
- [ ] Verify tanks N+1 through 8 have `Enabled = false` (optional)
- [ ] Check that tank priorities are unique (1-8, 1=highest)
- [ ] Verify simulation script processes correct number of tanks
- [ ] Test priority arbitration with multiple low tanks
- [ ] Confirm only configured tanks appear in diagnostics
- [ ] Verify pump responds to demand from any enabled tank

## Helper Functions

All helper functions automatically respect the `TankCount` configuration:

### `get_tank_snapshot()`
Returns a list of tank dictionaries for the configured number of tanks.

```python
tanks = project.script.yw_sim.get_tank_snapshot("[default]YW_Demo")
# Returns only tanks 1 through TankCount
```

### `get_diagnostics_data()`
Returns diagnostic data for all configured tanks.

```python
diagnostics = project.script.yw_sim.get_diagnostics_data("[default]YW_Demo")
# Includes only tanks 1 through TankCount
```

## Limitations

1. **Maximum 8 Tanks**: The system is designed for up to 8 tanks due to:
   - PLC register address allocation
   - Available Click PLC I/O
   - Typical small-to-medium water system requirements

2. **Tank Instances Must Exist**: All 8 tank UDT instances must be present in the tag structure, even if not all are enabled.

3. **Sequential Naming**: Tanks must be numbered sequentially (Tank_1, Tank_2, etc.). Gaps are not supported.

## Troubleshooting

### Tanks Not Processing
- Check `Config/TankCount` value
- Verify `Tank_X/Enabled = true` for tanks 1 through TankCount
- Check simulation script is running (gateway timer active)

### Wrong Tanks Processing
- Verify `Config/TankCount` matches desired configuration
- Check that tank instances Tank_1 through Tank_N exist

### Priority Arbitration Issues
- Ensure each tank has unique priority (1-8)
- Lower priority number = higher priority (1 = highest)
- Check that `Tank_X/AutoEnable = true` for all enabled tanks

## Example Configurations

### 2-Tank System
```
Config/TankCount = 2
Tank_1/Enabled = true, Priority = 1
Tank_2/Enabled = true, Priority = 2
Tank_3/Enabled = false
Tank_4-8/Enabled = false
```

### 6-Tank System
```
Config/TankCount = 6
Tank_1/Enabled = true, Priority = 1
Tank_2/Enabled = true, Priority = 2
Tank_3/Enabled = true, Priority = 3
Tank_4/Enabled = true, Priority = 4
Tank_5/Enabled = true, Priority = 5
Tank_6/Enabled = true, Priority = 6
Tank_7-8/Enabled = false
```

## Support

For questions or issues with tank configuration:
- Review `PLC_MAPPING.md` for PLC integration details
- Check `REACT_ALIGNMENT.md` for simulation logic details
- See `IGNITION_COMPATIBILITY.md` for Ignition-specific requirements
