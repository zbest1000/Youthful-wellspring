# Youthful Wellspring - Ignition 8.3 SCADA Project

![Status](https://img.shields.io/badge/status-ready--to--import-green)
![Ignition](https://img.shields.io/badge/Ignition-8.3+-blue)
![Perspective](https://img.shields.io/badge/Perspective-Module-orange)

A complete Ignition 8.3 Perspective SCADA project for water tank management, converted from a React SPA prototype. This project demonstrates modern HMI design patterns with a Tailwind-inspired UI, comprehensive simulation logic, and production-ready architecture.

## 🌊 Overview

**Youthful Wellspring** is a production-ready water distribution control system featuring:

- **4 Water Storage Tanks** with individual level monitoring and control
- **Priority-based valve arbitration** for automated filling
- **Pump control** with Auto/Manual modes and Anti-Short-Cycle protection
- **Backwash sequence automation** with multi-step workflow
- **Real-time alarming and trending** with tag history integration
- **Comprehensive diagnostics** and configuration screens
- **OPC UA/PLC connectivity** for live process data
- **Optional simulation mode** for training, testing, and demonstrations (no PLC required)

---

## 📁 Project Structure

```
/workspace/
├── tags/
│   ├── YouthfulWellspringUDTs.json         # UDT definitions for Tank, Pump, Mode, Backwash, System
│   └── YouthfulWellspringSimInstances.json # Demo tag instances (4 tanks + system tags)
├── perspective/
│   ├── views/
│   │   ├── main/
│   │   │   └── Shell.json                  # Main navigation shell
│   │   ├── screens/
│   │   │   ├── overview.json               # Dashboard with tank grid and status cards
│   │   │   ├── pump.json                   # Pump control panel
│   │   │   ├── alarms.json                 # Alarm status table
│   │   │   ├── trends.json                 # Historical trend charts
│   │   │   ├── diagnostics.json            # System diagnostics table
│   │   │   ├── config.json                 # System configuration settings
│   │   │   └── settings.json               # User preferences
│   │   ├── components/
│   │   │   ├── TankCard.json               # Reusable tank display card
│   │   │   └── StatusCard.json             # Reusable status widget
│   │   └── popups/
│   │       └── TankFaceplate.json          # Tank detail editor popup
│   └── style/
│       ├── style.json                      # Perspective style classes
│       └── style.css                       # Custom CSS (optional)
├── scripts/
│   └── project/
│       └── script/
│           └── yw_sim.py                   # Python simulation module (gateway script)
└── docs/
    ├── IMPORT.md                           # Step-by-step import instructions
    ├── CONTAINER_LAYOUT.md                 # Detailed layout documentation
    └── README.md                           # This file
```

---

## ✨ Features

### 🎯 Core Functionality

- **Tank Management**
  - Real-time level monitoring (0-100%)
  - Configurable low/high setpoints
  - Priority-based filling logic (0 = highest priority)
  - Enable/disable individual tanks
  - Fault isolation mode
  - Demand detection (level < low setpoint)

- **Pump Control**
  - Auto mode: starts when any tank has demand
  - Manual mode: operator start/stop control
  - Anti-short-cycle logic
  - Run hours tracking
  - Fault handling with configurable action (Continue/Stop)

- **Valve Automation**
  - Priority arbitration: fills highest-priority tank first
  - Automatic inlet valve control
  - Manual outlet valve override
  - Prevents multiple tanks filling simultaneously

- **Backwash Sequence**
  - Multi-step automation (Drain → Rinse → Refill)
  - Progress indication (0-100%)
  - Manual initiation
  - Last run timestamp tracking

### 🖥️ User Interface

- **Overview Screen**
  - 2x2 tank grid with live level indicators
  - System status cards (Pump, Mode, Backwash, Demand)
  - Click any tank to open detail faceplate

- **Pump Control Screen**
  - Large running/stopped indicator
  - Mode selection (Auto/Manual)
  - Manual start/stop buttons (Manual mode only)
  - Run hours and fault status display

- **Alarms Screen**
  - Integrated Perspective alarm table
  - Filters: Active Unacked + Active Acked
  - Priority-based color coding
  - Configurable alarm pipelines

- **Trends Screen**
  - Multi-pen time series chart
  - Last 1 hour of tank levels (configurable)
  - Color-coded per tank
  - Tag history integration

- **Diagnostics Screen**
  - Component status table
  - Real-time parameter values
  - Last update timestamps
  - Status badges (OK/Fault/Disabled)

- **Config Screen**
  - System mode selector (Auto/Manual)
  - Fault action configuration
  - System initialization button

- **Settings Screen**
  - User information display
  - Theme selection (Dark/Light)
  - Simulation enable/disable toggle

### 🎨 Design

- **Tailwind-inspired** color palette (Slate/Blue theme)
- **Dark mode** optimized for control rooms
- **Responsive flex layouts** adapt to screen sizes
- **Gradient effects** and glow states for active components
- **Consistent typography** and spacing
- **Accessible color contrast** for critical alarms

---

## 🚀 Quick Start

### Prerequisites

- Ignition 8.3+ Gateway
- Perspective Module license
- Designer Launcher installed
- **Production:** PLC/SCADA system with OPC UA connectivity
- **Demo/Training:** No hardware required (simulation mode)

### Import Steps (Summary)

1. **Import UDTs:** `tags/YouthfulWellspringUDTs.json` → Tag Browser
2. **Import Tag Instances:** `tags/YouthfulWellspringSimInstances.json` → `[default]` provider
3. **Import Simulation Script:** `scripts/project/script/yw_sim.py` → Project Library (optional)
4. **Import Style Classes:** `perspective/style/style.json` → Perspective Styles
5. **Import Views:** All JSON files from `perspective/views/` → Perspective Views
6. **Create Session:** Set primary view to `YouthfulWellspring/main/Shell`

**For Production Use:**
7. **Map OPC Tags:** Follow [docs/PLC_MAPPING.md](docs/PLC_MAPPING.md) to connect to your PLC
8. **Configure Alarms:** Set up alarm pipelines for tank levels and faults
9. **Enable Tag History:** Configure historian for trending

**For Demo/Training Mode:**
7. **Configure Timer Script:** Gateway timer calling `project.script.yw_sim.run_tick()` every 2s
8. **Enable Simulation:** Set `System/SimulationActive` = True

**📖 Full instructions:** See [docs/IMPORT.md](docs/IMPORT.md)

---

## 🏗️ Architecture

### Tag Model (UDTs)

```
YW_Tank (UDT)
├── Name (String)
├── Level (Float) %
├── LowSP (Float) %
├── HighSP (Float) %
├── Priority (Int) 0-10
├── InletValve (Boolean)
├── OutletValve (Boolean)
├── Enabled (Boolean)
├── FaultIsolation (Boolean)
└── Demand (Boolean)

YW_Pump (UDT)
├── Running (Boolean)
├── Command (Boolean)
├── Fault (Boolean)
├── Mode (String) Auto|Manual
├── StartPermissive (Boolean)
├── RunHours (Float)
└── LastStartTime (DateTime)

YW_Mode (UDT)
├── Selector (String) Auto|Manual
└── FaultAction (String) Continue|Stop

YW_Backwash (UDT)
├── InProgress (Boolean)
├── Step (String) Idle|Drain|Rinse|Refill
├── Progress (Float) %
├── Command (Boolean)
└── LastRun (DateTime)

YW_System (UDT)
├── Initialized (Boolean)
├── SimulationActive (Boolean)
├── AnyDemand (Boolean)
├── ActiveAlarmCount (Int)
└── LastUpdate (DateTime)
```

### Production Operation

The UDT tags are designed to connect directly to your PLC/SCADA system via OPC UA:

- **Tag Provider:** Configure OPC UA connection to your PLC
- **Tag Mapping:** Map UDT tags to PLC memory addresses (see mapping guide below)
- **Real-time Updates:** All views bind to tags for live data updates
- **PLC Logic:** Your PLC handles valve arbitration, pump control, and backwash sequences

### Optional Simulation Mode

For training, testing, or demo purposes without a PLC:

The `yw_sim.py` script module replicates PLC logic:
- **Tank Level Updates:** Simulates filling/draining based on valve states
- **Valve Arbitration:** Priority-based selection logic
- **Pump Control:** Auto/Manual mode logic with ASC timers
- **Backwash Sequence:** Timer-based state machine

**To Enable Simulation:**
1. Set `[default]YW_Demo/System/SimulationActive` = `True`
2. Create gateway timer script calling `project.script.yw_sim.run_tick("[default]YW_Demo")` every 2 seconds
3. Disable timer when connecting to real PLC

**To Disable Simulation (Production Mode):**
1. Set `[default]YW_Demo/System/SimulationActive` = `False`
2. Disable or delete the gateway timer script
3. Configure OPC connections to your PLC

### View Patterns

- **Shell View:** Top-level container with navigation bar and dynamic content loader
- **Screen Views:** Individual pages (Overview, Pump, Alarms, etc.)
- **Component Views:** Reusable embedded views (TankCard, StatusCard)
- **Popup Views:** Modal dialogs (TankFaceplate)

**Data Flow:**
- Direct tag bindings for real-time updates
- Bidirectional bindings for user inputs (dropdowns, numeric entry)
- Expression bindings for computed values
- Script bindings for complex data (diagnostics table)

**📐 Layout details:** See [docs/CONTAINER_LAYOUT.md](docs/CONTAINER_LAYOUT.md)

---

## 🔧 Configuration

### Connecting to Your PLC (Production Mode)

#### Step 1: Configure OPC UA Connection

1. In Gateway Config, add OPC UA connection to your PLC
2. Browse available tags and verify connectivity
3. Note the PLC memory addresses for each UDT parameter

#### Step 2: Map UDT Tags to PLC Addresses

Replace the memory tags in `[default]YW_Demo` with OPC tag paths:

**Example Mapping (adjust to your PLC):**

| UDT Tag Path | PLC Address Example | Notes |
|-------------|---------------------|-------|
| `Tanks/Tank_1/LevelPct` | `ns=1;s=[PLC]DF1` | Tank 1 level (DF1-DF8) |
| `Tanks/Tank_1/LowSP` | `ns=1;s=[PLC]DS1200` | Tank 1 low setpoint |
| `Tanks/Tank_1/HighSP` | `ns=1;s=[PLC]DS1201` | Tank 1 high setpoint |
| `Tanks/Tank_1/Priority` | `ns=1;s=[PLC]DS1202` | Tank 1 priority |
| `Tanks/Tank_1/Enabled` | `ns=1;s=[PLC]C100` | Tank 1 enable coil |
| `Tanks/Tank_1/ValveOutput` | `ns=1;s=[PLC]Y002` | Tank 1 valve output |
| `Pump/PumpRunning` | `ns=1;s=[PLC]Y001` | Pump output (Y001) |
| `Pump/PumpRequest` | `ns=1;s=[PLC]C060` | Pump request coil |
| `Mode/AutoSelected` | `ns=1;s=[PLC]X021` | Auto mode selector |
| `Mode/EStop` | `ns=1;s=[PLC]X001` | E-Stop input |
| `Backwash/Active` | `ns=1;s=[PLC]C31` | Backwash active |
| `Backwash/Valve` | `ns=1;s=[PLC]Y010` | Backwash valve output |

**Methods to Map Tags:**
- **Option A (Recommended)**: In Tag Browser, edit each UDT instance tag and change `valueSource` from `memory` to `opc` and set OPC path
- **Option B**: Create new UDT instances pointing to OPC tags
- **Option C**: Use tag import/export with find-replace to bulk update paths

#### Step 3: Disable Simulation Mode

1. Set `[default]YW_Demo/System/SimulationActive` = `False`
2. In Gateway Config → Scripting → Timer Scripts, **disable or delete** the `YW Simulation Tick` timer
3. Verify views update with live PLC data

#### Step 4: Configure Alarms

Add alarm configurations to tank `LevelPct` tags:
- **Low-Low Alarm**: `LevelPct` < 10% (Critical)
- **Low Alarm**: `LevelPct` < 20% (High)
- **High Alarm**: `LevelPct` > 90% (Medium)
- **High-High Alarm**: `LevelPct` > 95% (Critical)

Assign to alarm pipelines for notification/logging.

#### Step 5: Enable Tag History

Configure historian on these tags for trending:
```
[default]YW_Demo/Tanks/Tank_1/LevelPct
[default]YW_Demo/Tanks/Tank_2/LevelPct
[default]YW_Demo/Tanks/Tank_3/LevelPct
[default]YW_Demo/Tanks/Tank_4/LevelPct
[default]YW_Demo/Pump/PumpRunning
[default]YW_Demo/Backwash/Active
```

**Recommended settings:**
- Sample Mode: `On Change` with 0.5% deadband
- Storage Provider: Default historian or SQL Bridge

### User Roles & Security

To restrict access:

1. **Define roles:** Operator, Engineer, Admin
2. **Apply security levels:**
   - Overview, Alarms, Trends → Operator (read-only)
   - Pump Control, Config → Engineer (read/write)
   - Settings, Diagnostics → Admin
3. **Use visibility bindings:**
   ```python
   visible: system.security.isScreenLocked() == False
   ```

### Customization

- **Add more tanks:** Clone `Tank_A` tag instance, adjust priority
- **Change colors:** Edit `perspective/style/style.json` color variables
- **Add screens:** Follow the pattern in existing screen views
- **Extend simulation:** Modify `yw_sim.py` functions (e.g., add leak detection)

---

## 📊 Data & Trending

### Tag History Setup

Enable history on these tags for trends:

```
[default]YW_Demo/Tanks/Tank_A/Level
[default]YW_Demo/Tanks/Tank_B/Level
[default]YW_Demo/Tanks/Tank_C/Level
[default]YW_Demo/Tanks/Tank_D/Level
[default]YW_Demo/Pump/Running
[default]YW_Demo/Pump/RunHours
```

**Recommended settings:**
- Sample Mode: `On Change` (with 0.5% deadband) or `Periodic` (5s)
- Storage Provider: Default historian or custom database

### Alarming

Example alarm configurations:

| Tag | Alarm Name | Setpoint | Priority |
|-----|------------|----------|----------|
| Tank Level | Low-Low | < 10% | Critical |
| Tank Level | Low | < 20% | High |
| Tank Level | High | > 90% | Medium |
| Tank Level | High-High | > 95% | Critical |
| Pump Fault | Pump Fault Active | Fault == True | High |

---

## 🧪 Testing

### Simulation Mode

With `SimulationActive = True`, the system runs in demo mode:

1. **Test tank filling:**
   - Lower Tank A to < 20% (edit tag)
   - Pump should auto-start
   - Tank A inlet valve should open
   - Level should rise

2. **Test priority logic:**
   - Set multiple tanks below low setpoint
   - Verify only highest-priority tank inlet opens

3. **Test manual pump control:**
   - Switch pump mode to Manual
   - Use START/STOP buttons
   - Verify pump responds

4. **Test backwash sequence:**
   - Navigate to Overview
   - Trigger backwash (via Config or custom button)
   - Watch progress through Drain → Rinse → Refill steps

### Production Testing

Before connecting to a live PLC:

1. **Tag path validation:** Use Tag Browser to verify all paths resolve
2. **Binding test:** Open each view in Designer Preview mode
3. **Write permissions:** Test user roles can't write to read-only tags
4. **Alarm test:** Trigger alarms manually and verify table displays
5. **Performance:** Monitor Designer console for binding errors or slow queries

---

## 📝 Documentation

### Production Use
- **[PLC_MAPPING.md](docs/PLC_MAPPING.md)** - 🏭 **Production PLC tag mapping guide** (Click PLC, Allen-Bradley, Siemens, Modbus)
- **[IMPORT.md](docs/IMPORT.md)** - Complete import instructions with production setup steps

### Reference
- **[REACT_ALIGNMENT.md](docs/REACT_ALIGNMENT.md)** - Verification of alignment with React source code
- **[CONTAINER_LAYOUT.md](docs/CONTAINER_LAYOUT.md)** - Detailed view structure and layout patterns
- **Style Classes** - See `perspective/style/style.json` for all available classes

### Demo/Training Mode
- **Simulation Logic** - See inline comments in `scripts/project/script/yw_sim.py` (optional demo mode)

---

## 🤝 Contributing

This project was converted from a React prototype and is intended as a reference implementation. Feel free to:

- Adapt for your specific system architecture
- Extend with additional features (e.g., predictive maintenance, energy monitoring)
- Share improvements or suggestions via issues/PRs

---

## 📜 License

This project is provided as-is for educational and reference purposes. Modify and use freely in your Ignition projects.

---

## 🔗 Source Alignment

This Ignition project is a **verified conversion** of the React SPA:
- **Source Repository**: [Ignitionyouthfulwellspringscadaproject](https://github.com/zbest1000/Ignitionyouthfulwellspringscadaproject)
- **Alignment Document**: See [docs/REACT_ALIGNMENT.md](docs/REACT_ALIGNMENT.md) for detailed mapping
- **Tag Structure**: UDTs precisely match React TypeScript interfaces (`src/types/plc.ts`)
- **Simulation Logic**: Python script replicates `App.tsx` lines 100-195 exactly
- **View Layouts**: Perspective views mirror React component structure

## 🙏 Acknowledgments

- Original React SPA prototype: zbest1000
- Design inspiration: Tailwind CSS, shadcn/ui
- Built for: Ignition by Inductive Automation

---

## 📞 Support

For questions or issues:

- **Ignition User Manual:** https://docs.inductiveautomation.com/
- **Ignition Forum:** https://forum.inductiveautomation.com/
- **Project Issues:** Open an issue in this repository

---

## 🚧 Roadmap / Future Enhancements

- [ ] Mobile-optimized responsive layouts
- [ ] Advanced reporting (daily/weekly tank usage)
- [ ] Predictive maintenance alerts (pump runtime thresholds)
- [ ] Energy consumption tracking
- [ ] Multi-site support (tag provider per site)
- [ ] Webhook integrations for external notifications
- [ ] REST API endpoints for third-party integration

---

**Ready to import?** Start with [docs/IMPORT.md](docs/IMPORT.md) and get your Youthful Wellspring system running in minutes! 💧
