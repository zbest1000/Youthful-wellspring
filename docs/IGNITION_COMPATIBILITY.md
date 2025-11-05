# Ignition 8.3 Compatibility Guide

This document addresses compatibility considerations for importing Youthful Wellspring assets into Ignition 8.3.

## ⚠️ Important Compatibility Notes

### Tag Import Format

**Current Format:** The UDT definitions are provided in simplified JSON format.

**Ignition 8.3 Support:**
- ✅ **JSON Import** - Ignition 8.3+ supports JSON tag import via Tag Browser
- ✅ **XML Import** - Also supports traditional XML format
- ⚠️ **Manual Verification Required** - After import, verify all UDT structures in Designer

**Import Process:**
1. Tag Browser → Right-click provider → **Import Tags** → **JSON**
2. Select `tags/YouthfulWellspringUDTs.json`
3. Review import preview
4. Click **Import**
5. **Verify:** Check that all UDT definitions appear with correct data types

**Known Limitations:**
- Some metadata (tag groups, documentation fields) may not import
- Alarm configurations must be added manually after import
- Tag history settings must be configured separately

### Perspective View Format

**Current Format:** Views are in Perspective JSON export format.

**Ignition 8.3 Compatibility:**
- ✅ **JSON Views** - Ignition 8.3 Perspective supports JSON view import/export
- ⚠️ **Component Properties** - Some property names may differ between versions
- ⚠️ **Binding Syntax** - Expression bindings may need adjustment

**Import Process:**
1. Designer → Perspective → Views
2. Right-click folder → **Import View**
3. Select JSON file
4. Review any import warnings
5. **Test in Preview Mode** before deploying

**Common Issues to Check:**
- **Custom properties** on root container may need manual verification
- **Event scripts** (onActionPerformed) - verify script syntax
- **Bindings** - test all tag bindings and expressions
- **Style classes** - verify classes are applied correctly

### Style Classes

**Current Format:** `perspective/style/style.json`

**Ignition 8.3 Reality:**
- ❌ **No style.json import** - Ignition doesn't import style classes from JSON
- ✅ **Manual Creation Required** - Style classes must be created in Theme Editor
- ✅ **CSS Alternative** - Can use custom CSS in Theme

**Workaround - Option 1: Create Style Classes Manually**

In Designer → Perspective → Themes → [Your Theme] → Style Classes:

1. Click **Add Style Class**
2. For each class in `style.json`, create manually:
   ```
   Class Name: card
   Properties:
     backgroundColor: #1e293b
     border: 1px solid #334155
     borderRadius: 8px
     padding: 16px
     boxShadow: 0 4px 6px rgba(0,0,0,0.3)
   ```

3. Repeat for all classes (see style.json for complete list)

**Workaround - Option 2: Use Custom Theme CSS**

1. Designer → Perspective → Themes → [Your Theme]
2. Click **CSS** tab
3. Copy entire contents of `perspective/style/style.css`
4. Paste into Theme CSS editor
5. Save theme

**Note:** Views reference style classes (e.g., `"classes": "card"`). These must exist in your theme.

### Python Script Compatibility

**Current Format:** Python 2.7/Jython compatible script

**Ignition 8.3 Script Functions:**
- ✅ `system.tag.readBlocking()` - Standard tag read
- ✅ `system.tag.writeBlocking()` - Standard tag write
- ✅ `system.dataset.toDataSet()` - Dataset creation
- ✅ `java.util.Date()` - Date/time

**Compatibility:** ✅ **Fully Compatible** - All system functions used are standard Ignition API

**Import Process:**
1. Designer → Scripting → Project Library
2. Right-click → New Script
3. Name: `yw_sim`
4. Copy/paste contents of `scripts/project/script/yw_sim.py`
5. **Test:** Run in Script Console: `project.script.yw_sim.run_tick("[default]YW_Demo")`

### Modbus Device Configuration

**Ignition 8.3 Modbus Driver:**
- ✅ **Built-in Module** - Modbus TCP/RTU driver included
- ✅ **Address Syntax** - `[Device]HR400001`, `[Device]C00100`, `[Device]DI10001`
- ✅ **Data Types** - Float4, Int2, Boolean supported

**Known Modbus Considerations:**
- Float registers (DF) use 2 Modbus registers (e.g., DF1 = HR400001-400002)
- Ensure "Reverse String Bytes" and "Reverse Register Bytes" match PLC byte order
- Coil addressing: Y002 maps to Modbus coil 2 (address 00002)
- Discrete Input addressing: X021 maps to DI address 10021

### Component Type Verification

All component types used are standard Ignition 8.3 Perspective components:

| Component | Type String | Status |
|-----------|-------------|--------|
| Flex Container | `ia.container.flex` | ✅ Standard |
| View Container | `ia.container.view` | ✅ Standard |
| Label | `ia.display.label` | ✅ Standard |
| Button | `ia.input.button` | ✅ Standard |
| Dropdown | `ia.input.dropdown` | ✅ Standard |
| Toggle | `ia.input.toggle` | ✅ Standard |
| Numeric Entry | `ia.input.numericentry` | ✅ Standard |
| Table | `ia.display.table` | ✅ Standard |
| Tank (Level) | `ia.display.tank` | ✅ Standard |
| Time Series Chart | `ia.chart.timeseries` | ✅ Standard |
| Alarm Status Table | `ia.display.alarmstatustable` | ✅ Standard |

**All components are standard - no custom modules required.**

### Binding Syntax

**Expression Bindings:**
```json
{
  "type": "expr",
  "config": {
    "expression": "{[default]YW_Demo/Pump/PumpRunning}"
  }
}
```
✅ **Compatible** - Standard Ignition 8.3 expression binding syntax

**Tag Bindings:**
```json
{
  "type": "tag",
  "config": {
    "tagPath": "[default]YW_Demo/Pump/PumpRunning",
    "bidirectional": true
  }
}
```
✅ **Compatible** - Standard bidirectional tag binding

**Property Bindings:**
```json
{
  "type": "property",
  "config": {
    "path": "view.params.tankPath"
  }
}
```
✅ **Compatible** - Standard property reference

### Script Syntax in Events

**Button Click Example:**
```python
system.tag.writeBlocking(['[default]YW_Demo/Pump/Command'], [True])
```
✅ **Compatible** - Standard Jython 2.7 syntax

**Navigation Example:**
```python
self.parent.parent.parent.custom.currentScreen = 'overview'
```
✅ **Compatible** - Standard property write

### Version-Specific Features

**Minimum Requirements:**
- Ignition **8.3.0** or higher
- Perspective Module license
- Modbus Driver (included in standard gateway)

**Recommended Version:**
- Ignition **8.1.25+** for optimal Perspective performance
- Ignition **8.1.30+** for latest Perspective bug fixes

**Features Used:**
- ✅ Perspective Views (8.0+)
- ✅ Style Classes (8.0+)
- ✅ Flex Containers (8.0+)
- ✅ Custom Properties (8.0+)
- ✅ Bidirectional Bindings (8.0+)
- ✅ Modbus TCP Driver (all versions)

**No Advanced Features Used:**
- ❌ No Perspective Templates (8.1.10+)
- ❌ No Symbol Factory (8.1.17+)
- ❌ No Markdown Component (8.1.19+)
- ❌ No Perspective Workstation SSO (8.1.20+)

## 🔧 Post-Import Checklist

After importing all assets, verify:

### 1. Tag Structure
- [ ] All UDT definitions imported successfully
- [ ] UDT instances created under `[default]YW_Demo`
- [ ] All tags have correct data types
- [ ] Memory tags have default values

### 2. Perspective Views
- [ ] All views imported without errors
- [ ] No missing component warnings in Designer
- [ ] Preview mode shows layouts correctly
- [ ] All bindings have valid tag paths

### 3. Style Classes
- [ ] Style classes created in Theme Editor (or CSS added)
- [ ] Test a view and verify styling appears
- [ ] Check card backgrounds, badges, buttons render correctly

### 4. Scripts
- [ ] `yw_sim` script module created
- [ ] No syntax errors in Script Console
- [ ] Test `project.script.yw_sim.run_tick()` manually

### 5. Modbus Connection
- [ ] Modbus device configured in Gateway
- [ ] Connection status shows "Connected"
- [ ] Can browse tags from PLC
- [ ] Read/write test on a single tag successful

### 6. Session Configuration
- [ ] Perspective session/page created
- [ ] Primary view set to `YouthfulWellspring/main/Shell`
- [ ] Session launches without errors
- [ ] Navigation works between screens

## 🐛 Troubleshooting Common Issues

### Issue: Tags fail to import

**Symptoms:** Import preview shows errors, or tags missing after import

**Solutions:**
1. Verify JSON is valid: `python -m json.tool tags/YouthfulWellspringUDTs.json`
2. Import UDT definitions first, then instances
3. Check tag provider has write permissions
4. Try importing as XML instead (export from another gateway)

### Issue: Views don't display correctly

**Symptoms:** Components missing, layout broken, binding errors

**Solutions:**
1. Check Designer console for binding errors
2. Verify tag paths exist and are correct format
3. Test in Preview Mode before deploying to session
4. Check style classes exist in theme
5. Verify custom properties on root container

### Issue: Style classes not applied

**Symptoms:** Views render but have no styling/colors

**Solutions:**
1. Create style classes manually in Theme Editor
2. OR add CSS to Theme CSS tab
3. Verify class names match exactly (case-sensitive)
4. Clear browser cache and refresh session

### Issue: Scripts don't run

**Symptoms:** Gateway timer errors, script console errors

**Solutions:**
1. Check Jython syntax (Python 2.7 compatible only)
2. Verify `system.tag` functions use correct tag provider
3. Check tag paths in script match actual tag structure
4. Test script manually in Script Console first

### Issue: Modbus connection fails

**Symptoms:** Device shows "Faulted", can't read tags

**Solutions:**
1. Verify Click PLC IP address and port 502
2. Check Modbus TCP enabled in Click PLC setup
3. Ping PLC from Ignition server: `ping 192.168.1.100`
4. Verify Unit ID matches (typically 1)
5. Check firewall allows port 502
6. Use Modbus diagnostic tools to verify PLC responds

### Issue: Bindings show "Bad_NotFound"

**Symptoms:** Tags show red icon, values display "Bad_NotFound"

**Solutions:**
1. Verify tag path spelling and case
2. Check tag provider name `[default]` vs `[ProviderName]`
3. Ensure tags are enabled (not disabled)
4. For OPC tags, verify OPC connection is good
5. Check tag security/permissions

## 📞 Support Resources

**Ignition Documentation:**
- Tag JSON Import: https://docs.inductiveautomation.com/docs/8.1/appendix/tag-json-import
- Perspective Views: https://docs.inductiveautomation.com/docs/8.1/perspective/view-design
- Modbus Driver: https://docs.inductiveautomation.com/docs/8.1/appendix/modules/modbus-driver-module

**Inductive Automation:**
- Forum: https://forum.inductiveautomation.com/
- Support: support@inductiveautomation.com
- Training: https://inductiveuniversity.com/

**Youthful Wellspring Project:**
- GitHub: https://github.com/zbest1000/Youthful-wellspring
- Issues: Open issue on GitHub repository

---

## ✅ Summary

**Overall Compatibility: ✅ GOOD**

The Youthful Wellspring project is compatible with Ignition 8.3, with these considerations:

✅ **Fully Compatible:**
- Tag UDT structure (JSON import supported)
- Perspective view JSON format
- Python script syntax
- Modbus device configuration
- All component types
- Binding syntax

⚠️ **Manual Steps Required:**
- Style classes must be created manually or via CSS
- Alarm configurations added post-import
- Tag history enabled separately
- Modbus tag mapping requires editing each tag

❌ **Not Supported:**
- Direct style.json import (workaround provided)

**Recommendation:** Import and test in a development gateway first before deploying to production.
