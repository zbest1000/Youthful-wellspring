# Click PLC + Modbus Tag Mapping Guide

This document provides detailed mapping between Ignition UDT tags and Click PLC memory addresses via **Modbus TCP** communication.

## Overview

The UDT structure is designed to mirror Click PLC (AutomationDirect) memory organization. The system communicates via **Modbus TCP** protocol.

**Hardware:**
- Click PLC (C0-02DD1-D, C0-04AD, or similar)
- Ethernet port for Modbus TCP
- Tank level sensors (4-20mA analog inputs)
- Valve outputs (digital outputs)
- Pump control (digital output)

---

## Modbus Device Configuration

### Step 1: Configure Click PLC for Modbus TCP

1. **In Click Programming Software:**
   - Go to PLC → Setup → Ethernet
   - Enable Modbus TCP Server
   - Set IP Address (e.g., `192.168.1.100`)
   - Set Port: `502` (default Modbus TCP port)
   - Enable Modbus addressing

2. **Modbus Slave ID:** Typically `1` (default)

### Step 2: Configure Ignition Modbus Driver

1. **Gateway Config** → **OPC UA** → **Device Connections**
2. **Add Device:**
   - **Name:** `ClickPLC`
   - **Device Type:** `Modbus TCP`
   - **Hostname:** `192.168.1.100` (your PLC IP)
   - **Port:** `502`
   - **Unit ID:** `1`
   - **Timeout:** `5000 ms`
   - **Scan Rate:** `1000 ms` (adjust as needed)

3. **Test Connection:** Browse available addresses to verify connectivity

---

## Click PLC Memory Map

### Click PLC Address Types

| Click Type | Modbus Function Code | Modbus Address Range | Description |
|-----------|---------------------|---------------------|-------------|
| **X (Inputs)** | FC02 (Read Discrete Inputs) | 10001-10xxx | Physical digital inputs |
| **Y (Outputs)** | FC01/05 (Read/Write Coils) | 00001-00xxx | Physical digital outputs |
| **C (Control Relays)** | FC01/05 (Read/Write Coils) | 00001-08192 | Internal coils/bits |
| **DS (Data Registers)** | FC03/06 (Read/Write Holding Registers) | 400001-404500 | 16-bit integers |
| **DF (Data Registers Float)** | FC03/06 (Read/Write Holding Registers) | 400001-404500 | 32-bit floats (2 registers) |
| **T (Timers)** | FC01 (Read Coils) | Status bit | Timer done bit |
| **TD (Timer Data)** | FC03 (Read Holding Registers) | Timer accumulator | Timer PV |

---

## Tank Tags Mapping

### Tank 1 - Modbus Register Map

| Ignition UDT Tag | Click Address | Modbus Address | Modbus Type | Data Type | R/W | Description |
|-----------------|---------------|----------------|-------------|-----------|-----|-------------|
| `Tanks/Tank_1/Name` | (HMI Only) | - | - | String | R | Tank identifier |
| `Tanks/Tank_1/CapacityLiters` | (HMI Only) | - | - | Int | R | Tank capacity |
| `Tanks/Tank_1/Contents` | (HMI Only) | - | - | String | R | Contents description |
| **`Tanks/Tank_1/LevelPct`** | **DF1** | **400001-400002** | **Holding Reg (Float)** | Float | R | **Tank level % (0-100)** |
| `Tanks/Tank_1/LevelX10` | DS2401 | 402401 | Holding Reg | Int16 | R | Level * 10 (0-1000) |
| **`Tanks/Tank_1/LowSP`** | **DS1200** | **401200** | **Holding Reg** | Int16 | R/W | **Low SP (0-99)** |
| **`Tanks/Tank_1/HighSP`** | **DS1201** | **401201** | **Holding Reg** | Int16 | R/W | **High SP (1-100)** |
| **`Tanks/Tank_1/Priority`** | **DS1202** | **401202** | **Holding Reg** | Int16 | R/W | **Priority (1-8)** |
| **`Tanks/Tank_1/Enabled`** | **C100** | **00100** | **Coil** | Bool | R/W | **Global enable** |
| `Tanks/Tank_1/AutoEnable` | C101 | 00101 | Coil | Bool | R/W | AUTO enable |
| `Tanks/Tank_1/ManEnable` | C102 | 00102 | Coil | Bool | R/W | MANUAL enable |
| `Tanks/Tank_1/OOS` | C103 | 00103 | Coil | Bool | R/W | Out of Service |
| **`Tanks/Tank_1/FillReq`** | **C140** | **00140** | **Coil** | Bool | R | **Fill request** |
| `Tanks/Tank_1/PreCmd` | C160 | 00160 | Coil | Bool | R | Pre-arbitration |
| **`Tanks/Tank_1/ValveCmd`** | **C161** | **00161** | **Coil** | Bool | R | **Valve command** |
| **`Tanks/Tank_1/ValveOutput`** | **Y002** | **00002** | **Coil** | Bool | R | **Valve output** |
| `Tanks/Tank_1/SensorOpen` | C200 | 00200 | Coil | Bool | R | Sensor fault |

### Tank 2-8 Modbus Addresses

| Tank | LevelPct (DF) | LowSP (DS) | HighSP (DS) | Priority (DS) | Enabled (C) | FillReq (C) | ValveCmd (C) | ValveOutput (Y) |
|------|---------------|------------|-------------|---------------|-------------|-------------|--------------|-----------------|
| **Tank_1** | 400001-400002 | 401200 | 401201 | 401202 | 00100 | 00140 | 00161 | 00002 |
| **Tank_2** | 400003-400004 | 401210 | 401211 | 401212 | 00104 | 00141 | 00162 | 00003 |
| **Tank_3** | 400005-400006 | 401220 | 401221 | 401222 | 00108 | 00142 | 00163 | 00004 |
| **Tank_4** | 400007-400008 | 401230 | 401231 | 401232 | 00112 | 00143 | 00164 | 00005 |
| **Tank_5** | 400009-400010 | 401240 | 401241 | 401242 | 00116 | 00144 | 00165 | 00006 |
| **Tank_6** | 400011-400012 | 401250 | 401251 | 401252 | 00120 | 00145 | 00166 | 00007 |
| **Tank_7** | 400013-400014 | 401260 | 401261 | 401262 | 00124 | 00146 | 00167 | 00008 |
| **Tank_8** | 400015-400016 | 401270 | 401271 | 401272 | 00128 | 00147 | 00168 | 00009 |

---

## Pump Tags Mapping

| Ignition UDT Tag | Click Address | Modbus Address | Modbus Type | Data Type | R/W | Description |
|-----------------|---------------|----------------|-------------|-----------|-----|-------------|
| **`Pump/AnyDemand`** | **C040** | **00040** | **Coil** | Bool | R | **Any demand** |
| **`Pump/PumpRequest`** | **C060** | **00060** | **Coil** | Bool | R | **Pump request** |
| **`Pump/PumpRunning`** | **Y001** | **00001** | **Coil** | Bool | R | **Pump output** |
| `Pump/PumpAvailable` | (Computed) | - | - | Bool | R | Computed |
| `Pump/ASCMinOffTimer` | T2 | 00002 (status) | Coil | Bool | R | ASC Min-OFF timer |
| `Pump/ASCMinOffPV` | TD2 | 400012 | Holding Reg | Int16 | R | Min-OFF PV (sec) |
| `Pump/ASCMinRunTimer` | T1 | 00001 (status) | Coil | Bool | R | ASC Min-RUN timer |
| `Pump/ASCMinRunPV` | TD1 | 400011 | Holding Reg | Int16 | R | Min-RUN PV (sec) |
| **`Pump/ASCMinOffSetting`** | **DS101** | **400101** | **Holding Reg** | Int16 | R/W | **Min-OFF (sec)** |
| **`Pump/ASCMinRunSetting`** | **DS102** | **400102** | **Holding Reg** | Int16 | R/W | **Min-RUN (sec)** |

---

## Mode Tags Mapping

| Ignition UDT Tag | Click Address | Modbus Address | Modbus Type | Data Type | R/W | Description |
|-----------------|---------------|----------------|-------------|-----------|-----|-------------|
| **`Mode/AutoSelected`** | **X021** | **10021** | **Discrete Input** | Bool | R | **AUTO selector** |
| `Mode/ManualSelected` | X022 | 10022 | Discrete Input | Bool | R | MANUAL selector |
| `Mode/SystemStopped` | X023 | 10023 | Discrete Input | Bool | R | STOPPED selector |
| **`Mode/EStop`** | **X001** | **10001** | **Discrete Input** | Bool | R | **E-Stop input** |
| **`Mode/PressureFault`** | **X002** | **10002** | **Discrete Input** | Bool | R | **Pressure fault** |
| **`Mode/FlowFault`** | **X003** | **10003** | **Discrete Input** | Bool | R | **Flow fault** |
| `Mode/EffectiveFault` | (Computed) | - | - | Bool | R | Computed fault |
| **`Mode/BypassPFFault`** | **C020** | **00020** | **Coil** | Bool | R/W | **Fault bypass** |

---

## Backwash Tags Mapping

| Ignition UDT Tag | Click Address | Modbus Address | Modbus Type | Data Type | R/W | Description |
|-----------------|---------------|----------------|-------------|-----------|-----|-------------|
| **`Backwash/Start`** | **C030** | **00030** | **Coil** | Bool | W | **Start command** |
| **`Backwash/Active`** | **C031** | **00031** | **Coil** | Bool | R | **Sequence active** |
| **`Backwash/Valve`** | **Y010** | **00010** | **Coil** | Bool | R | **Valve output** |
| **`Backwash/DurationSetting`** | **DS103** | **400103** | **Holding Reg** | Int16 | R/W | **Duration (sec)** |
| `Backwash/TimerPV` | TD10 | 400020 | Holding Reg | Int16 | R | Timer PV |
| `Backwash/HWTrigger` | X004 | 10004 | Discrete Input | Bool | R | HW trigger |

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

## Click PLC Programming Notes

### Analog Input Scaling (Tank Levels)

Tank level sensors (4-20mA) must be scaled to 0-100% in Click PLC:

**Click PLC Ladder Logic:**
```
Analog Input X001 (4-20mA) → Scale to DF1 (0.0-100.0)

Using SCALE instruction:
  Input: X001 (raw counts 0-4000)
  Input Min: 800 (4mA = 800 counts)
  Input Max: 4000 (20mA = 4000 counts)
  Output Min: 0.0
  Output Max: 100.0
  Output: DF1
```

Repeat for Tank 2-8 (as configured):
- X002 → DF2
- X003 → DF3
- X004 → DF4
- X005 → DF5 (if Tank 5 enabled)
- X006 → DF6 (if Tank 6 enabled)
- X007 → DF7 (if Tank 7 enabled)
- X008 → DF8 (if Tank 8 enabled)

### Modbus TCP Configuration in Click PLC

1. **Enable Modbus TCP Server:**
   - Click Programming Software → PLC → Setup
   - Ethernet tab → Enable Modbus TCP/IP Slave
   - Set IP Address: `192.168.1.100`
   - Port: `502`
   - Unit ID: `1`

2. **Memory Allocation:**
   - Ensure sufficient memory for data registers (DS1-DS4500)
   - Reserve C1-C200 for control logic
   - Reserve Y1-Y10 for outputs

3. **Watchdog Timer (Optional):**
   - Implement Modbus communication watchdog
   - If no Modbus read/write for 10 seconds, fault system
   - Use timer to monitor last Modbus activity

### PLC Program Structure

**Scan Order:**
1. Read analog inputs → Scale to DF1-DF4
2. Read digital inputs (X001-X023) → Mode, faults
3. **Tank Control Logic:**
   - Calculate fill requests (C140-C143)
   - Priority arbitration → Valve commands (C161-C164)
   - Map valve commands to outputs (Y002-Y005)
4. **Pump Control Logic:**
   - Aggregate demand (C040)
   - Anti-short-cycle timers (T1, T2)
   - Pump output (Y001)
5. **Backwash Logic:**
   - Monitor start command (C030)
   - Timer control (T10)
   - Valve output (Y010)
6. Write outputs
7. Update status registers for HMI

### Wiring Diagram Reference

**Analog Inputs (4-20mA):**
- X001: Tank 1 Level Sensor
- X002: Tank 2 Level Sensor
- X003: Tank 3 Level Sensor
- X004: Tank 4 Level Sensor
- X005: Tank 5 Level Sensor (optional)
- X006: Tank 6 Level Sensor (optional)
- X007: Tank 7 Level Sensor (optional)
- X008: Tank 8 Level Sensor (optional)

**Digital Inputs:**
- X001: E-Stop (NC contact)
- X002: Pressure Switch (NO contact)
- X003: Flow Switch (NO contact)
- X021: Auto Mode Selector
- X022: Manual Mode Selector
- X023: System Stop Selector

**Digital Outputs:**
- Y001: Pump Contactor
- Y002: Tank 1 Inlet Valve
- Y003: Tank 2 Inlet Valve
- Y004: Tank 3 Inlet Valve
- Y005: Tank 4 Inlet Valve
- Y006: Tank 5 Inlet Valve (optional)
- Y007: Tank 6 Inlet Valve (optional)
- Y008: Tank 7 Inlet Valve (optional)
- Y009: Tank 8 Inlet Valve (optional)
- Y010: Backwash Valve

---

## Ignition Tag Configuration Examples

### Method 1: Direct Modbus Addressing (Recommended)

In Ignition Tag Browser, configure each tag:

**Tank 1 Level (Float):**
```
Tag Name: LevelPct
Value Source: OPC
OPC Server: Ignition OPC UA Server
OPC Item Path: [ClickPLC]HR400001
Data Type: Float (32-bit, 2 registers)
Scan Class: Direct/1000ms
```

**Tank 1 Low Setpoint (Int):**
```
Tag Name: LowSP
Value Source: OPC
OPC Server: Ignition OPC UA Server
OPC Item Path: [ClickPLC]HR401200
Data Type: Int2
Scan Class: Default/5000ms
```

**Tank 1 Valve Output (Bool):**
```
Tag Name: ValveOutput
Value Source: OPC
OPC Server: Ignition OPC UA Server
OPC Item Path: [ClickPLC]C00002
Data Type: Boolean
Scan Class: Direct/500ms
```

**Pump Output (Bool):**
```
Tag Name: PumpRunning
Value Source: OPC
OPC Server: Ignition OPC UA Server
OPC Item Path: [ClickPLC]C00001
Data Type: Boolean
Scan Class: Direct/500ms
```

**Mode Selector Input (Bool):**
```
Tag Name: AutoSelected
Value Source: OPC
OPC Server: Ignition OPC UA Server
OPC Item Path: [ClickPLC]DI10021
Data Type: Boolean
Scan Class: Direct/250ms
```

### Method 2: Using Address Shortcuts

Ignition Modbus driver syntax:
- **Holding Registers (DS/DF):** `[Device]HR400001` (400001 = register 1)
- **Coils (C/Y):** `[Device]C00100` (coil 100)
- **Discrete Inputs (X):** `[Device]DI10001` (input 1)
- **Input Registers:** `[Device]IR300001` (if used)

### Method 3: Bulk Import with CSV

Create a CSV file for bulk tag import:

```csv
TagPath,OPCItemPath,DataType,ScanClass
[default]YW_Demo/Tanks/Tank_1/LevelPct,[ClickPLC]HR400001,Float4,Direct
[default]YW_Demo/Tanks/Tank_1/LowSP,[ClickPLC]HR401200,Int2,Default
[default]YW_Demo/Tanks/Tank_1/HighSP,[ClickPLC]HR401201,Int2,Default
[default]YW_Demo/Tanks/Tank_1/Priority,[ClickPLC]HR401202,Int2,Default
[default]YW_Demo/Tanks/Tank_1/Enabled,[ClickPLC]C00100,Boolean,Direct
[default]YW_Demo/Tanks/Tank_1/ValveOutput,[ClickPLC]C00002,Boolean,Direct
[default]YW_Demo/Pump/PumpRunning,[ClickPLC]C00001,Boolean,Direct
[default]YW_Demo/Mode/AutoSelected,[ClickPLC]DI10021,Boolean,Direct
[default]YW_Demo/Mode/EStop,[ClickPLC]DI10001,Boolean,Direct
```

Import via: Tag Browser → Import Tags → CSV

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
