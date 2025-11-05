# PLC Tag Mapping Guide

This document provides detailed mapping between Ignition UDT tags and PLC memory addresses for connecting Youthful Wellspring to a real control system.

## Overview

The UDT structure is designed to mirror typical PLC tag organization (based on Click PLC conventions). Adapt the addresses below to match your specific PLC brand and memory layout.

---

## Tag Provider Configuration

### OPC UA Connection Setup

1. **Gateway Config** → **OPC UA** → **Connections**
2. **Add New Connection:**
   - Name: `ProductionPLC`
   - Endpoint URL: `opc.tcp://[PLC_IP]:4840` (adjust for your PLC)
   - Security: Configure as needed
   - Identity: Username/password or anonymous

---

## Tank Tags Mapping

### Tank 1 (Repeat for Tank_2, Tank_3, Tank_4)

| Ignition UDT Tag | PLC Address | Data Type | R/W | Description |
|-----------------|-------------|-----------|-----|-------------|
| `Tanks/Tank_1/Name` | (HMI Only) | String | R | Tank identifier - not in PLC |
| `Tanks/Tank_1/CapacityLiters` | (HMI Only) | Int | R | Tank capacity - not in PLC |
| `Tanks/Tank_1/Contents` | (HMI Only) | String | R | Contents description - not in PLC |
| **`Tanks/Tank_1/LevelPct`** | **DF1** | Float | R | **Tank level percentage (0-100)** |
| `Tanks/Tank_1/LevelX10` | DS2401 | Int | R | Level * 10 (0-1000) |
| **`Tanks/Tank_1/LowSP`** | **DS1200** | Float | R/W | **Low setpoint (%)** |
| **`Tanks/Tank_1/HighSP`** | **DS1201** | Float | R/W | **High setpoint (%)** |
| **`Tanks/Tank_1/Priority`** | **DS1202** | Int | R/W | **Priority (1-8, 1=highest)** |
| **`Tanks/Tank_1/Enabled`** | **C100** | Bool | R/W | **Global enable coil** |
| `Tanks/Tank_1/AutoEnable` | C101 (custom) | Bool | R/W | AUTO_en_TK1 |
| `Tanks/Tank_1/ManEnable` | C102 (custom) | Bool | R/W | MAN_en_TK1 |
| `Tanks/Tank_1/OOS` | C103 (custom) | Bool | R/W | Out of Service flag |
| **`Tanks/Tank_1/FillReq`** | **C140** | Bool | R | **Computed fill request** |
| `Tanks/Tank_1/PreCmd` | C160 | Bool | R | Pre-arbitration intent |
| **`Tanks/Tank_1/ValveCmd`** | **C161** | Bool | R | **Winning valve command** |
| **`Tanks/Tank_1/ValveOutput`** | **Y002** | Bool | R | **Actual valve output** |
| `Tanks/Tank_1/SensorOpen` | C200 | Bool | R | Level sensor open fault |
| `Tanks/Tank_1/ValveHWPresent` | (HMI Only) | Bool | R | Hardware present check |
| `Tanks/Tank_1/MinOpenTimer` | T200 | Bool | R | Min open timer active |
| `Tanks/Tank_1/MinOpenPV` | TD200 | Int | R | Min open timer PV |

### Tank 2-4 Address Increments

| Tank | Level | LowSP | HighSP | Priority | Enabled | FillReq | ValveCmd | ValveOutput |
|------|-------|-------|--------|----------|---------|---------|----------|-------------|
| Tank_2 | DF2 | DS1210 | DS1211 | DS1212 | C104 | C141 | C162 | Y003 |
| Tank_3 | DF3 | DS1220 | DS1221 | DS1222 | C108 | C142 | C163 | Y004 |
| Tank_4 | DF4 | DS1230 | DS1231 | DS1232 | C112 | C143 | C164 | Y005 |

---

## Pump Tags Mapping

| Ignition UDT Tag | PLC Address | Data Type | R/W | Description |
|-----------------|-------------|-----------|-----|-------------|
| **`Pump/AnyDemand`** | **C040** | Bool | R | **Any tank or backwash request** |
| **`Pump/PumpRequest`** | **C060** | Bool | R | **Pump request coil** |
| **`Pump/PumpRunning`** | **Y001** (mirror C040) | Bool | R | **Pump output status** |
| `Pump/PumpAvailable` | (Computed) | Bool | R | Computed in PLC/HMI |
| `Pump/ASCMinOffTimer` | T2 | Bool | R | Anti-Short-Cycle Min-OFF timer |
| `Pump/ASCMinOffPV` | TD2 | Int | R | Min-OFF timer present value (seconds) |
| `Pump/ASCMinRunTimer` | T1 | Bool | R | Anti-Short-Cycle Min-RUN timer |
| `Pump/ASCMinRunPV` | TD1 | Int | R | Min-RUN timer present value (seconds) |
| **`Pump/ASCMinOffSetting`** | **DS101** | Int | R/W | **Min-OFF duration (seconds)** |
| **`Pump/ASCMinRunSetting`** | **DS102** | Int | R/W | **Min-RUN duration (seconds)** |

---

## Mode Tags Mapping

| Ignition UDT Tag | PLC Address | Data Type | R/W | Description |
|-----------------|-------------|-----------|-----|-------------|
| **`Mode/AutoSelected`** | **X021** | Bool | R | **AUTO mode selector switch** |
| `Mode/ManualSelected` | X022 | Bool | R | MANUAL mode selector switch |
| `Mode/SystemStopped` | X023 | Bool | R | SYSTEM STOPPED selector |
| **`Mode/EStop`** | **X001** | Bool | R | **Emergency Stop input** |
| **`Mode/PressureFault`** | **X002** | Bool | R | **Pressure fault input** |
| **`Mode/FlowFault`** | **X003** | Bool | R | **Flow fault input** |
| `Mode/EffectiveFault` | (Computed) | Bool | R | Computed from E-Stop + faults |
| **`Mode/BypassPFFault`** | **C020** | Bool | R/W | **Pressure/Flow fault bypass (HMI toggle)** |

---

## Backwash Tags Mapping

| Ignition UDT Tag | PLC Address | Data Type | R/W | Description |
|-----------------|-------------|-----------|-----|-------------|
| **`Backwash/Start`** | **C030** | Bool | W | **Backwash start command (HMI button)** |
| **`Backwash/Active`** | **C031** | Bool | R | **Backwash sequence active** |
| **`Backwash/Valve`** | **Y010** | Bool | R | **Backwash valve output** |
| **`Backwash/DurationSetting`** | **DS103** | Int | R/W | **Backwash duration (seconds)** |
| `Backwash/TimerPV` | TD10 | Int | R | Backwash timer present value |
| `Backwash/HWTrigger` | X004 | Bool | R | Hardware trigger switch (optional) |

---

## System Config Tags

| Ignition UDT Tag | PLC Address | Data Type | R/W | Description |
|-----------------|-------------|-----------|-----|-------------|
| `Config/TankCount` | (HMI Only) | Int | R | Number of tanks (1-8) - not in PLC |
| `Config/SiteName` | (HMI Only) | String | R | Site name - not in PLC |
| `Config/Location` | (HMI Only) | String | R | Site location - not in PLC |
| `Config/Initialized` | (HMI Only) | Bool | R/W | System initialization flag - not in PLC |

---

## System Info Tags

| Ignition UDT Tag | PLC Address | Data Type | R/W | Description |
|-----------------|-------------|-----------|-----|-------------|
| `System/SolarPower` | (External) | Float | R | Solar power generation (W) - if available |
| `System/BatteryLevel` | (External) | Float | R | Battery level (%) - if available |
| `System/PLCRunning` | (Computed) | Bool | R | PLC communication status |
| `System/ScanTime` | (PLC System) | Float | R | PLC scan time (ms) |
| `System/CommStatus` | (Computed) | Bool | R | OPC connection status |
| `System/SimulationActive` | (HMI Only) | Bool | R/W | Simulation mode flag - not in PLC |
| `System/LastUpdate` | (HMI Only) | DateTime | R | Last update timestamp - not in PLC |

---

## PLC-Specific Notes

### Click PLC (AutomationDirect)
- Address format: `C100`, `DF1`, `DS1200`, `X001`, `Y001`, `T1`, `TD1`
- Coils: C1-C2000
- Data registers: DS1-DS4500
- Timers: T1-T500

### Allen-Bradley CompactLogix/ControlLogix
- Tag-based addressing: `Program:MainProgram.Tank1_Level`
- Use tag names instead of addresses
- Map to UDT structure in PLC for consistency

### Siemens S7-1200/1500
- Address format: `DB1.DBD0` (Data Block)
- Use symbolic names in TIA Portal
- Map OPC UA tags to DB structure

### Modbus RTU/TCP
- Register addresses: 40001+
- Coils: 00001+
- Map holding registers to floats/ints, coils to bools

---

## Example OPC Tag Path Configuration

### For Click PLC via Modbus

```
Tank 1 Level:
  OPC Path: ns=2;s=Channel1.Device1.DF1
  Data Type: Float
  Scan Class: 1 second

Tank 1 Low Setpoint:
  OPC Path: ns=2;s=Channel1.Device1.DS1200
  Data Type: Float
  Scan Class: 5 seconds

Tank 1 Valve Output:
  OPC Path: ns=2;s=Channel1.Device1.Y002
  Data Type: Boolean
  Scan Class: 500 ms
```

### For Allen-Bradley via EtherNet/IP

```
Tank 1 Level:
  OPC Path: [ControllerName]Program:MainProgram.Tank1_LevelPct
  Data Type: Real
  Scan Class: 1 second
```

---

## Tag Update Rates

Recommended scan classes for optimal performance:

| Tag Group | Scan Rate | Notes |
|-----------|-----------|-------|
| Tank Levels (LevelPct) | 1 second | Fast enough for display updates |
| Valve Outputs (ValveCmd, ValveOutput) | 500 ms | Critical for control feedback |
| Pump Status (PumpRunning) | 500 ms | Critical for control feedback |
| Setpoints (LowSP, HighSP, Priority) | 5 seconds | Infrequent changes |
| Digital Inputs (EStop, Faults) | 250 ms | Safety-critical |
| Timers (ASC, Backwash) | 1 second | Display only |

---

## Import Process for Production

1. **Import UDTs** as memory tags initially (for structure)
2. **Edit tag instances** one-by-one to change `valueSource` from `memory` to `opc`
3. **Set OPC Item Path** for each tag
4. **Test read/write** on individual tags before enabling full system
5. **Disable simulation** by setting `System/SimulationActive` = False
6. **Delete gateway timer script** (no longer needed)

---

## Verification Checklist

After mapping all tags:

- [ ] Tank levels display live PLC values
- [ ] Valve commands write to PLC outputs
- [ ] Pump responds to demand signals
- [ ] Mode selector switches read from PLC
- [ ] E-Stop and faults trigger in HMI when PLC faults
- [ ] Setpoints can be changed from HMI and persist in PLC
- [ ] Backwash command writes to PLC
- [ ] All alarms trigger correctly
- [ ] Tag history records data
- [ ] No binding errors in Designer

---

## Support

For PLC-specific addressing questions:
- Click PLC: AutomationDirect support documentation
- Allen-Bradley: Rockwell TechConnect
- Siemens: TIA Portal help files
- Modbus: Modbus.org specification

For Ignition OPC configuration:
- Inductive University: OPC UA courses
- Ignition User Manual: OPC UA connections
- Ignition Forum: community.inductiveautomation.com
