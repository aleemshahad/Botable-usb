# Changelog

All notable changes to the Bootable USB Creator project will be documented in this file.

## [1.2.0] - 2025-10-26

### Added
- **Light Green Progress Bar**: Progress bar now displays in a pleasant light green color (#90EE90)
- **Finish Button**: A "✓ Finish" button appears when the process completes at 100%
  - Clicking the Finish button closes the application
  - Button is styled in green to indicate successful completion
  - Only appears after successful completion
- **Enhanced User Experience**: Success dialog now prompts user to click Finish button

### Changed
- Progress bar color changed from default blue to light green for better visual feedback
- Create button is disabled after successful completion (Finish button replaces it)
- Success message updated to inform user about the Finish button

## [1.1.0] - 2025-10-26

### Added
- **Advanced Progress Bar**: Replaced indeterminate progress bar with determinate progress bar showing actual percentage (0-100%)
- **Step-by-Step Progress Tracking**: Progress bar now shows completion percentage for each of the 6 steps:
  - Step 1: Unmounting device (0-5%)
  - Step 2: Wiping device (5-10%)
  - Step 3: Creating partition table (10-20%)
  - Step 4: Formatting partition (20-30%)
  - Step 5: Copying ISO contents (30-90%)
  - Step 6: Installing bootloader (90-95%)
  - Finalization: Syncing data (95-100%)
- **Live File Copy Progress**: Real-time progress tracking during ISO file copy with rsync
- **Progress Status Label**: Shows current operation status above the progress bar
- **Percentage Display**: Shows exact percentage next to the progress bar

### Changed
- Progress bar mode changed from `indeterminate` to `determinate`
- File copying now uses `copy_with_progress()` method for better progress tracking
- Progress updates are throttled to every 0.5 seconds to avoid UI overwhelming
- UEFI mode now explicitly logs that bootloader installation is not required

### Technical Details
- Added `update_progress(value, status)` method to update progress bar and status label
- Added `reset_progress()` method to reset progress bar to initial state
- Added `copy_with_progress(source, destination)` method for file copying with progress tracking
- Progress bar scales file copy progress (0-100%) to overall progress (30-90%)
- Uses rsync's `--info=progress2` flag for progress information

## [1.0.0] - 2025-10-25

### Initial Release
- Multi-OS bootable USB creation support
- UEFI and Legacy BIOS boot modes
- GPT and MBR partition schemes
- FAT32, NTFS, and exFAT file systems
- Modern GUI with Tkinter
- Automatic USB device detection
- Real-time logging with color-coded messages
- Safety features and confirmation prompts
- Comprehensive documentation
