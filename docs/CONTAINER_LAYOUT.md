# Container Layout Documentation

This document provides a detailed breakdown of the Perspective view structure and container layouts used in the Youthful Wellspring project.

## Design Philosophy

The project follows a **Tailwind CSS-inspired component architecture** adapted for Ignition Perspective:

- **Flex containers** for responsive layouts
- **Reusable embedded views** for consistent UI components
- **Style classes** for consistent theming
- **Bidirectional tag bindings** for real-time data updates
- **Popup views** for detailed interactions

## View Hierarchy

```
YouthfulWellspring/
├── main/
│   └── Shell.json                 (Root container with navigation)
├── screens/
│   ├── overview.json              (Dashboard grid)
│   ├── pump.json                  (Pump control panel)
│   ├── alarms.json                (Alarm table)
│   ├── trends.json                (Historical charts)
│   ├── diagnostics.json           (System diagnostics table)
│   ├── config.json                (Configuration settings)
│   └── settings.json              (User settings)
├── components/
│   ├── TankCard.json              (Reusable tank display)
│   └── StatusCard.json            (Reusable status widget)
└── popups/
    └── TankFaceplate.json         (Tank detail editor)
```

---

## Main Shell Layout

**Path:** `YouthfulWellspring/main/Shell.json`

### Container Structure

```
root (Flex Column)
├── HeaderBar (Flex Row) [basis: 60px]
│   ├── Logo (Label) [basis: 200px]
│   ├── NavButtons (Flex Row) [grow: 1]
│   │   ├── OverviewBtn (Button)
│   │   ├── PumpBtn (Button)
│   │   ├── AlarmsBtn (Button)
│   │   ├── TrendsBtn (Button)
│   │   ├── DiagnosticsBtn (Button)
│   │   ├── ConfigBtn (Button)
│   │   └── SettingsBtn (Button)
│   └── AlarmIndicator (Label) [basis: 150px]
└── ContentArea (Flex Column) [grow: 1]
    └── ViewLoader (Embedded View)
```

### Key Properties

- **currentScreen** (custom property): String value controlling which screen is displayed
- **ViewLoader binding:** Dynamic path based on `currentScreen`
  ```
  'YouthfulWellspring/screens/' + {view.custom.currentScreen}
  ```

### Navigation Pattern

Each button writes to `view.custom.currentScreen`:
```python
self.parent.parent.parent.custom.currentScreen = 'overview'
```

---

## Screen: Overview

**Path:** `YouthfulWellspring/screens/overview.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
├── StatusCards (Flex Row) [basis: 200px]
│   ├── PumpStatusCard (Embedded View) [grow: 1]
│   ├── ModeCard (Embedded View) [grow: 1]
│   ├── BackwashCard (Embedded View) [grow: 1]
│   └── DemandCard (Embedded View) [grow: 1]
└── TankGrid (Flex Row, wrap) [grow: 1]
    ├── Tank_A (Embedded View) [basis: calc(50% - 8px)]
    ├── Tank_B (Embedded View) [basis: calc(50% - 8px)]
    ├── Tank_C (Embedded View) [basis: calc(50% - 8px)]
    └── Tank_D (Embedded View) [basis: calc(50% - 8px)]
```

### Layout Notes

- **StatusCards:** 4 equal-width cards (grow: 1) displaying system status
- **TankGrid:** 2x2 responsive grid using flex wrap
- **Gap styling:** 16px gap between cards

---

## Screen: Pump Control

**Path:** `YouthfulWellspring/screens/pump.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
└── PumpControlPanel (Flex Column) [basis: 400px]
    ├── RunningIndicator (Label)
    ├── ModeSelector (Flex Row)
    │   ├── AutoMode (Button)
    │   └── ManualMode (Button)
    ├── ManualControls (Flex Row) [visible: mode == 'Manual']
    │   ├── StartBtn (Button)
    │   └── StopBtn (Button)
    └── PumpStats (Flex Grid, 2 columns)
        ├── RunHoursLabel + RunHoursValue
        └── FaultLabel + FaultValue
```

### Key Bindings

- **RunningIndicator text:**
  ```
  tag: [default]YW_Demo/Pump/Running
  format: value ? '🟢 RUNNING' : '🔴 STOPPED'
  ```
- **ManualControls visibility:**
  ```
  expression: {[default]YW_Demo/Pump/Mode} = 'Manual'
  ```

### Button Actions

- **START button:**
  ```python
  system.tag.writeBlocking(['[default]YW_Demo/Pump/Command'], [True])
  ```
- **STOP button:**
  ```python
  system.tag.writeBlocking(['[default]YW_Demo/Pump/Command'], [False])
  ```

---

## Screen: Alarms

**Path:** `YouthfulWellspring/screens/alarms.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
└── AlarmTable (AlarmStatusTable) [grow: 1]
```

### Table Configuration

- **Component type:** `ia.display.alarmstatustable`
- **Filter:** Active Unacked + Active Acked alarms
- **Columns:**
  - Priority (icon, 80px)
  - Name (300px)
  - Label (400px)
  - Active Time (200px)
  - Value (150px)

---

## Screen: Trends

**Path:** `YouthfulWellspring/screens/trends.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
└── TrendChart (TimeSeriesChart) [grow: 1]
```

### Chart Configuration

- **Component type:** `ia.chart.timeseries`
- **Pens:**
  - Tank A Level (blue, #3b82f6)
  - Tank B Level (green, #10b981)
  - Tank C Level (orange, #f59e0b)
  - Tank D Level (purple, #8b5cf6)
- **Time range:** Last 1 hour
- **Data source:** Tag history for each tank's `Level` tag

---

## Screen: Diagnostics

**Path:** `YouthfulWellspring/screens/diagnostics.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
└── DiagnosticsTable (Table) [grow: 1]
```

### Table Configuration

- **Data source:** Expression binding to script function
  ```
  project.script.yw_sim.get_diagnostics_data()
  ```
- **Columns:**
  - Component (200px)
  - Parameter (200px)
  - Value (150px)
  - Status (100px, badge render)
  - Last Update (200px)

---

## Screen: Config

**Path:** `YouthfulWellspring/screens/config.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
└── ConfigPanel (Flex Column) [basis: 400px]
    ├── SystemMode (Flex Row)
    │   ├── Label
    │   └── ModeDropdown (Dropdown)
    ├── FaultAction (Flex Row)
    │   ├── Label
    │   └── FaultDropdown (Dropdown)
    └── InitializeBtn (Button)
```

### Dropdown Bindings

- **ModeDropdown:**
  ```
  tag: [default]YW_Demo/Mode/Selector (bidirectional)
  options: [{value: 'Auto', label: 'Automatic'}, {value: 'Manual', label: 'Manual'}]
  ```
- **FaultDropdown:**
  ```
  tag: [default]YW_Demo/Mode/FaultAction (bidirectional)
  options: [{value: 'Continue', label: 'Continue Operation'}, {value: 'Stop', label: 'Stop on Fault'}]
  ```

---

## Screen: Settings

**Path:** `YouthfulWellspring/screens/settings.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 60px]
└── SettingsPanel (Flex Column) [basis: 500px]
    ├── UserInfo (Label)
    ├── ThemeToggle (Flex Row)
    │   ├── Label
    │   └── ThemeOptions (Dropdown)
    ├── SimulationToggle (Flex Row)
    │   ├── Label
    │   └── SimToggle (Toggle)
    └── InfoText (Label)
```

### Key Bindings

- **SimToggle:**
  ```
  tag: [default]YW_Demo/System/SimulationActive (bidirectional)
  ```

---

## Component: TankCard

**Path:** `YouthfulWellspring/components/TankCard.json`

### Container Structure

```
root (Flex Column) [clickable]
├── Header (Label) [basis: 40px]
└── Body (Flex Row) [grow: 1]
    ├── TankVisual (Tank component) [basis: 120px]
    └── Details (Flex Column) [grow: 1]
        ├── Level (Label)
        ├── LowSP (Label)
        ├── HighSP (Label)
        ├── Status (Label, badge)
        └── ValveStatus (Label)
```

### Parameters

- **tankPath:** Tag path to tank UDT instance (e.g., `[default]YW_Demo/Tanks/Tank_A`)

### Click Action

Opens the `TankFaceplate` popup:
```python
system.perspective.openPopup('TankFaceplate', {'tankPath': self.view.params.tankPath})
```

### Key Bindings

- **TankVisual value:**
  ```
  expression: '{' + {view.params.tankPath} + '/Level}'
  ```
- **Status badge:**
  ```
  text: if({...}/Demand, '🔽 DEMAND', '✓ OK')
  style: if({...}/Demand, {classes: 'badge-warning'}, {classes: 'badge-success'})
  ```

---

## Component: StatusCard

**Path:** `YouthfulWellspring/components/StatusCard.json`

### Container Structure

```
root (Flex Column)
├── Title (Label) [basis: 40px]
└── ValueDisplay (Label) [grow: 1]
```

### Parameters

- **title:** Display title (e.g., "Pump Status")
- **tagPath:** Base tag path (e.g., `[default]YW_Demo/Pump`)
- **valueKey:** Tag member to display (e.g., `Running`)
- **icon:** Icon name (not yet implemented)

### Key Bindings

- **ValueDisplay:**
  ```
  expression: toString('{' + {view.params.tagPath} + '/' + {view.params.valueKey} + '}'}')
  ```

---

## Popup: TankFaceplate

**Path:** `YouthfulWellspring/popups/TankFaceplate.json`

### Container Structure

```
root (Flex Column)
├── Header (Label) [basis: 60px]
├── TankVisual (Flex Column) [basis: 200px]
│   ├── LevelDisplay (Label)
│   └── TankLevel (Tank component)
├── SetpointEditors (Flex Column) [basis: 200px]
│   ├── LowSP (Flex Row)
│   │   ├── Label
│   │   └── Input (NumericEntry)
│   ├── HighSP (Flex Row)
│   │   ├── Label
│   │   └── Input (NumericEntry)
│   └── Priority (Flex Row)
│       ├── Label
│       └── Input (NumericEntry)
└── Actions (Flex Row) [basis: 60px]
    └── CloseBtn (Button)
```

### Parameters

- **tankPath:** Tag path to tank UDT instance

### Editable Bindings

All numeric entry fields use **bidirectional** bindings:
```
expression: '{' + {view.params.tankPath} + '/LowSP}' (bidirectional: true)
```

### Close Action

```python
system.perspective.closePopup(self.view.id)
```

---

## Style Classes Reference

All views reference style classes defined in `perspective/style/style.json`:

### Layout Classes

- **`card`**: Base card styling (background, border, shadow)
- **`card-title`**: Card header text
- **`tank-card`**: Tank-specific card with hover effects

### Typography

- **`screen-title`**: Large screen headers
- **`label-primary`**: Primary text labels
- **`label-secondary`**: Secondary/muted labels
- **`label-muted`**: Very light labels
- **`value-display`**: Data value text
- **`value-large`**: Large data values

### Buttons

- **`nav-button`**: Top navigation buttons
- **`button-primary`**: Primary action buttons (blue)
- **`button-secondary`**: Secondary actions (gray)
- **`button-success`**: Positive actions (green, e.g., START)
- **`button-critical`**: Negative actions (red, e.g., STOP)

### Badges

- **`badge-success`**: Green status badge
- **`badge-warning`**: Orange/yellow status badge
- **`badge-critical`**: Red status badge

---

## Responsive Behavior

### Breakpoints

While Perspective doesn't have built-in breakpoints like CSS, the layouts adapt using:

- **Flex grow/shrink:** Components expand to fill available space
- **Basis percentages:** `calc(50% - 8px)` for 2-column grids
- **Wrap containers:** TankGrid wraps to single column on narrow screens

### Recommendations for Mobile

- Use **Perspective's breakpoint system** to swap layouts at smaller widths
- Consider creating alternate "mobile" views for key screens
- Adjust `basis` values for single-column layouts on phones

---

## Data Flow Patterns

### Tag Bindings

All views use **direct tag bindings** or **expression bindings** referencing tags:

```json
{
  "binding": {
    "type": "tag",
    "config": {
      "tagPath": "[default]YW_Demo/Pump/Running"
    }
  }
}
```

### Bidirectional Bindings

For user-editable controls (dropdowns, numeric entry):

```json
{
  "binding": {
    "type": "tag",
    "config": {
      "tagPath": "[default]YW_Demo/Mode/Selector",
      "bidirectional": true
    }
  }
}
```

### Script-Based Data

For complex data (like diagnostics table):

```json
{
  "binding": {
    "type": "expr",
    "config": {
      "expression": "project.script.yw_sim.get_diagnostics_data()"
    }
  }
}
```

---

## Extending the Layout

### Adding a New Screen

1. Create a new view JSON file in `perspective/views/screens/`
2. Follow the container pattern:
   ```
   root (Flex Column)
   ├── Title (Label) [basis: 60px]
   └── ContentArea [grow: 1]
   ```
3. Add a navigation button to `Shell.json`:
   ```python
   self.parent.parent.parent.custom.currentScreen = 'yourscreen'
   ```

### Adding a New Component

1. Create view in `perspective/views/components/`
2. Define **params** for reusability (e.g., `tagPath`, `title`)
3. Use **expression bindings** to reference params:
   ```
   '{' + {view.params.tagPath} + '/Level}'
   ```
4. Embed in screen views using `ia.container.view`

---

## Best Practices

1. **Use flex containers** for all layouts (avoid absolute positioning)
2. **Define basis sizes** for fixed-height sections (headers, footers)
3. **Use `grow: 1`** for content areas that should expand
4. **Apply style classes** consistently (avoid inline styles)
5. **Parameterize embedded views** for reusability
6. **Use bidirectional bindings** for user inputs
7. **Keep view depth shallow** (max 3-4 levels deep)
8. **Test on multiple resolutions** (1920x1080, 1280x800, tablet, mobile)

---

## Troubleshooting Layout Issues

### Content Not Filling Space

- Check parent container has `grow: 1` or explicit basis
- Verify root container is `Flex Column` or `Flex Row`

### Components Overlapping

- Ensure all siblings have proper `basis` or `grow` values
- Check for conflicting absolute positions

### Bindings Not Updating

- Verify tag paths are correct (case-sensitive!)
- Check binding type (tag vs. expression vs. property)
- Use **Preview Mode** to test bindings

### Style Classes Not Applying

- Confirm class names match `style.json` exactly
- Check for typos in `"classes": "..."` property
- Clear browser cache if styles don't update

---

## Summary

The Youthful Wellspring layout architecture prioritizes:

- **Modularity:** Reusable components via embedded views
- **Responsiveness:** Flex-based layouts that adapt to screen size
- **Maintainability:** Consistent patterns across all screens
- **Performance:** Direct tag bindings with minimal scripting

For further details on specific components, refer to the JSON files in `perspective/views/`.
