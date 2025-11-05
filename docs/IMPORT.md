# Youthful Wellspring - Ignition Import Guide

This document explains how to import and configure the Youthful Wellspring Ignition 8.3 project assets.

## Prerequisites

- Ignition 8.3+ Gateway with Perspective module
- Designer Launcher installed
- Basic understanding of Ignition tag browser and Perspective views

## Import Order

Follow these steps in order to ensure proper dependencies:

### 1. Import UDT Definitions

**File:** `tags/YouthfulWellspringUDTs.json`

1. Open **Designer** and connect to your gateway
2. Navigate to **Tag Browser**
3. Right-click on the root folder (or desired parent folder)
4. Select **Import Tags** → **JSON**
5. Browse to `tags/YouthfulWellspringUDTs.json`
6. Click **Import**
7. Verify that the following UDTs appear:
   - `YW_Tank`
   - `YW_Pump`
   - `YW_Mode`
   - `YW_Backwash`
   - `YW_System`

### 2. Import Demo Tag Instances

**File:** `tags/YouthfulWellspringSimInstances.json`

1. In **Tag Browser**, right-click on `[default]` provider (or your preferred provider)
2. Select **Import Tags** → **JSON**
3. Browse to `tags/YouthfulWellspringSimInstances.json`
4. Click **Import**
5. Verify the `YW_Demo` folder structure:
   ```
   [default]YW_Demo/
   ├── System
   ├── Mode
   ├── Pump
   ├── Backwash
   └── Tanks/
       ├── Tank_A
       ├── Tank_B
       ├── Tank_C
       └── Tank_D
   ```

### 3. Import Python Simulation Script

**File:** `scripts/project/script/yw_sim.py`

1. In **Designer**, open **Scripting** → **Project Library**
2. Create a new script module named `yw_sim` (if not already present)
3. Copy the entire contents of `scripts/project/script/yw_sim.py`
4. Paste into the script module editor
5. Click **Save**
6. Test by running in the **Script Console**:
   ```python
   project.script.yw_sim.run_tick("[default]YW_Demo")
   ```

### 4. Import Style Classes

**File:** `perspective/style/style.json`

1. In **Designer**, navigate to **Perspective** → **Styles**
2. Right-click on **Style Classes**
3. Select **Import** (or manually add each class from the JSON)
4. Load `perspective/style/style.json`

**Optional:** If your project supports custom CSS:

**File:** `perspective/style/style.css`

1. Navigate to **Project** → **Resources**
2. Create a folder named `css` (if not present)
3. Upload `perspective/style/style.css`
4. Reference in your theme configuration

### 5. Import Perspective Views

**Directory:** `perspective/views/`

Import views in this order to resolve dependencies:

#### A. Component Views (Reusable)

1. Navigate to **Perspective** → **Views**
2. Create a folder structure: `YouthfulWellspring/components/`
3. Import each component view:
   - Right-click `components/` folder → **Import View**
   - Import `perspective/views/components/TankCard.json`
   - Import `perspective/views/components/StatusCard.json`

#### B. Popup Views

1. Create folder: `YouthfulWellspring/popups/`
2. Import:
   - `perspective/views/popups/TankFaceplate.json`

#### C. Screen Views

1. Create folder: `YouthfulWellspring/screens/`
2. Import each screen view:
   - `perspective/views/screens/overview.json`
   - `perspective/views/screens/pump.json`
   - `perspective/views/screens/alarms.json`
   - `perspective/views/screens/trends.json`
   - `perspective/views/screens/diagnostics.json`
   - `perspective/views/screens/config.json`
   - `perspective/views/screens/settings.json`

#### D. Main Shell View

1. Create folder: `YouthfulWellspring/main/`
2. Import:
   - `perspective/views/main/Shell.json`

### 6. Configure Gateway Timer Script (Required for Simulation)

To enable the simulation logic:

1. Navigate to **Gateway** → **Config** → **Scripting** → **Timer Scripts**
2. Click **Add Timer Script**
3. Configure:
   - **Name:** `YW Simulation Tick`
   - **Script:**
     ```python
     project.script.yw_sim.run_tick("[default]YW_Demo")
     ```
   - **Execution Mode:** `Fixed Rate`
   - **Interval:** `2000 ms` (2 seconds)
   - **Enabled:** `True`
4. Click **Save**

> **Note:** Disable this timer when connecting to a real PLC. The simulation will automatically stop if `System/SimulationActive` tag is set to `False`.

### 7. Create Perspective Session

1. Navigate to **Perspective** → **Sessions**
2. Create a new session or page
3. Set the **Primary View** to:
   ```
   YouthfulWellspring/main/Shell
   ```
4. Configure page settings (title, size, etc.)
5. Save and launch the session

## Post-Import Configuration

### Enable Tag History (Optional)

To populate the **Trends** screen with historical data:

1. In **Tag Browser**, navigate to each tank's `Level` tag:
   - `[default]YW_Demo/Tanks/Tank_A/Level`
   - `[default]YW_Demo/Tanks/Tank_B/Level`
   - `[default]YW_Demo/Tanks/Tank_C/Level`
   - `[default]YW_Demo/Tanks/Tank_D/Level`
2. Right-click → **Edit Tag**
3. Go to **History** tab
4. Enable **Historical**
5. Set **Storage Provider** to your configured historian
6. Set **Sample Mode** to `On Change` or `Periodic` (e.g., 5 seconds)
7. Click **OK**

### Configure Alarm Pipelines (Optional)

For the **Alarms** screen to display custom alarms:

1. Configure alarm setpoints on tank `Level` tags
2. Example alarm configuration:
   - **Low-Low Alarm:** Level < 10%
   - **High-High Alarm:** Level > 95%
3. Assign to an alarm pipeline

### Wire the "Mark Initialized" Button (Config Screen)

The **Config** screen has an "Initialize" button that writes to `System/Initialized`. If you need additional logic:

1. Open `YouthfulWellspring/screens/config` view
2. Find the `InitializeBtn` component
3. Edit the `onActionPerformed` script to add custom logic:
   ```python
   # Example: Reset all tank levels
   system.tag.writeBlocking(['[default]YW_Demo/System/Initialized'], [True])
   system.tag.writeBlocking([
       '[default]YW_Demo/Tanks/Tank_A/Level',
       '[default]YW_Demo/Tanks/Tank_B/Level',
       '[default]YW_Demo/Tanks/Tank_C/Level',
       '[default]YW_Demo/Tanks/Tank_D/Level'
   ], [50.0, 50.0, 50.0, 50.0])
   system.perspective.print('System Initialized - All tanks reset to 50%')
   ```

## Testing the Import

1. **Launch the Perspective Session** in a browser or Workstation client
2. **Verify Navigation:** Click through all tabs (Overview, Pump Control, Alarms, Trends, Diagnostics, Config, Settings)
3. **Check Tank Cards:** Tank levels should be updating every 2 seconds (if simulation is active)
4. **Test Pump Control:**
   - Switch to **Manual Mode**
   - Click **START** → pump should run
   - Click **STOP** → pump should stop
   - Switch back to **Auto Mode** → pump should run if any tank has demand
5. **Test Tank Faceplate:** Click on a tank card → popup should appear with editable setpoints
6. **Check Trends:** Historical data should populate if tag history is enabled
7. **Verify Diagnostics:** Table should show pump and tank status

## Troubleshooting

### Issue: Views not displaying correctly

- **Check tag paths:** Ensure all bindings reference `[default]YW_Demo` (or your custom tag provider)
- **Verify UDT import:** Ensure all UDT definitions imported successfully

### Issue: Simulation not running

- **Check timer script:** Ensure gateway timer is enabled and running every 2 seconds
- **Check tag value:** Verify `[default]YW_Demo/System/SimulationActive` is `True`
- **Check logs:** Review gateway logs for script errors

### Issue: Style classes not applying

- **Verify import:** Ensure style classes imported into Perspective → Styles
- **Check view styles:** Verify components reference class names correctly (e.g., `"classes": "card"`)

### Issue: Tank faceplate popup not opening

- **Check popup path:** Ensure popup view path is `YouthfulWellspring/popups/TankFaceplate`
- **Verify script syntax:** Check the `onActionPerformed` script in `TankCard` component

## Next Steps

- **Connect to Real PLC:** Replace tag bindings with OPC tags from your PLC
- **Customize Alarming:** Configure alarm pipelines and notifications
- **Add Security:** Implement role-based access control for operator/engineer views
- **Extend Functionality:** Add reports, data logging, or additional screens

## Support

For questions or issues, refer to:
- `docs/CONTAINER_LAYOUT.md` for view structure details
- Ignition User Manual: https://docs.inductiveautomation.com/
- Ignition Forum: https://forum.inductiveautomation.com/
