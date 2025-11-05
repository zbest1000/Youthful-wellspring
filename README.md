# Youthful Wellspring - Ignition 8.3 SCADA Project

![Status](https://img.shields.io/badge/status-ready--to--import-green)
![Ignition](https://img.shields.io/badge/Ignition-8.3+-blue)
![Perspective](https://img.shields.io/badge/Perspective-Module-orange)

A complete Ignition 8.3 Perspective SCADA project for water tank management, converted from a React SPA prototype. This project demonstrates modern HMI design patterns with a Tailwind-inspired UI, comprehensive simulation logic, and production-ready architecture.

## 🌊 Overview

**Youthful Wellspring** is a water distribution control system featuring:

- **4 Water Storage Tanks** with individual level monitoring and control
- **Priority-based valve arbitration** for automated filling
- **Pump control** with Auto/Manual modes
- **Backwash sequence automation** with multi-step workflow
- **Real-time alarming and trending**
- **Comprehensive diagnostics** and configuration screens
- **Simulation mode** for training and testing (no PLC required)

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

### Import Steps (Summary)

1. **Import UDTs:** `tags/YouthfulWellspringUDTs.json` → Tag Browser
2. **Import Tag Instances:** `tags/YouthfulWellspringSimInstances.json` → `[default]` provider
3. **Import Simulation Script:** `scripts/project/script/yw_sim.py` → Project Library
4. **Import Style Classes:** `perspective/style/style.json` → Perspective Styles
5. **Import Views:** All JSON files from `perspective/views/` → Perspective Views
6. **Configure Timer Script:** Gateway timer to call `project.script.yw_sim.run_tick("[default]YW_Demo")` every 2s
7. **Create Session:** Set primary view to `YouthfulWellspring/main/Shell`

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

### Simulation Logic

The `yw_sim.py` script module replicates PLC logic:

- **Tank Level Updates:** Fills when pump runs + inlet valve open, drains when outlet open
- **Valve Arbitration:** Priority-based selection of which tank gets inlet flow
- **Pump Control:** Auto mode uses demand detection; Manual mode uses operator commands
- **Backwash Sequence:** Step-based state machine with progress tracking
- **Diagnostics:** Snapshot functions for Perspective table bindings

**Gateway Timer Script:**
```python
project.script.yw_sim.run_tick("[default]YW_Demo")
```
**Interval:** 2000ms (2 seconds)

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

### Connecting to a Real PLC

1. **Map tags to OPC tags:**
   - Replace `[default]YW_Demo` memory tags with OPC UA tags from your PLC
   - Update all view bindings to reference new tag paths

2. **Disable simulation:**
   - Set `[default]YW_Demo/System/SimulationActive` to `False`, or
   - Disable the gateway timer script

3. **Configure alarms:**
   - Add alarm configurations to tank `Level` tags (Low-Low, High-High)
   - Assign to alarm pipelines

4. **Enable tag history:**
   - Configure historian on tank `Level` tags
   - Set sample mode (On Change or Periodic)

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

- **[IMPORT.md](docs/IMPORT.md)** - Complete import instructions with troubleshooting
- **[CONTAINER_LAYOUT.md](docs/CONTAINER_LAYOUT.md)** - Detailed view structure and layout patterns
- **Style Classes** - See `perspective/style/style.json` for all available classes
- **Simulation Logic** - See inline comments in `scripts/project/script/yw_sim.py`

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
