# Visual Features Guide

## Progress Bar

### Light Green Color Scheme
The progress bar uses a pleasant light green color (#90EE90) that provides excellent visual feedback:
- **Background**: Light green (#90EE90)
- **Light shade**: Pale green (#98FB98)
- **Dark shade**: Medium sea green (#7CCD7C)
- **Trough**: Light gray (#e0e0e0)

### Progress Stages
The progress bar fills from 0% to 100% as the bootable USB is created:

```
0%   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  0%   Ready
5%   ██━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  5%   Step 1/6: Unmounting device...
10%  ███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  10%  Step 2/6: Wiping device...
20%  ██████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  20%  Step 3/6: Creating partition table...
30%  ██████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  30%  Step 4/6: Formatting partition...
50%  ████████████████━━━━━━━━━━━━━━━━━━━━━━━  50%  Copying files: 33%
90%  ████████████████████████████████━━━━━━━━  90%  Step 6/6: Installing bootloader...
100% ████████████████████████████████████████  100% Complete!
```

## Finish Button

### When It Appears
The **✓ Finish** button automatically appears when:
- The bootable USB creation process completes successfully
- Progress bar reaches 100%
- All steps are completed without errors

### Button Behavior
- **Text**: "✓ Finish" (with checkmark)
- **Color**: Green text to indicate success
- **Action**: Closes the application when clicked
- **Location**: Appears next to the "Exit" button in the button bar

### User Flow
1. User clicks "Create Bootable USB"
2. Progress bar fills from 0% to 100% (light green)
3. Success message appears: "Bootable USB created successfully!"
4. **✓ Finish** button appears
5. User clicks "Finish" to close the application

## Visual States

### Before Starting
- Progress bar: 0%, light gray trough
- Status: "Ready"
- Buttons: "Create Bootable USB" and "Exit" visible

### During Creation
- Progress bar: 0-100%, filling with light green
- Status: Shows current step (e.g., "Step 3/6: Creating partition table...")
- Buttons: "Create Bootable USB" disabled, "Exit" visible

### After Completion (Success)
- Progress bar: 100%, fully filled with light green
- Status: "Complete!"
- Buttons: "Create Bootable USB" disabled, "Exit" visible, **"✓ Finish" appears**

### After Completion (Error)
- Progress bar: Stopped at error point
- Status: Shows last successful step
- Buttons: "Create Bootable USB" enabled (can retry), "Exit" visible

## Color Psychology

The light green color was chosen because:
- ✅ **Positive Association**: Green universally represents success, completion, and "go"
- ✅ **Easy on Eyes**: Light green is pleasant and not harsh
- ✅ **Progress Indication**: Clear visual feedback of advancement
- ✅ **Professional**: Modern and clean appearance

## Accessibility

- High contrast between progress bar and trough
- Clear percentage text display
- Status label provides text-based progress information
- Color-coded log messages (green for success, red for errors, orange for warnings)
