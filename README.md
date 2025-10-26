# Bootable USB Creator

A comprehensive Linux tool for creating bootable USB drives for Windows 10, 11, and other operating systems. Features a modern GUI with support for both UEFI and Legacy BIOS modes.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

## Features

- ✅ **Multi-OS Support**: Create bootable USB for Windows 10, 11, Linux distributions, and other operating systems
- ✅ **UEFI & Legacy BIOS**: Support for both modern UEFI and legacy BIOS boot modes
- ✅ **Multiple Partition Schemes**: GPT and MBR partition table support
- ✅ **File System Options**: FAT32, NTFS, and exFAT formatting
- ✅ **User-Friendly GUI**: Modern Tkinter-based interface with real-time progress logging
- ✅ **Safe Device Detection**: Automatic USB device scanning with detailed information
- ✅ **Bootloader Installation**: Automatic GRUB installation for Legacy BIOS mode
- ✅ **Advanced Progress Tracking**: Real-time light green progress bar with percentage display for each step
- ✅ **Live File Copy Progress**: See actual copy progress with speed and ETA during ISO transfer
- ✅ **Finish Button**: Convenient "Finish" button appears at 100% completion to close the application

## Screenshots

The application provides:
- ISO file selection with file browser
- Automatic USB device detection and refresh
- Configuration options for boot mode, partition scheme, and file system
- **Light green progress bar with percentage display** showing current operation and completion status
- **Finish button** that appears when process completes at 100%
- Real-time progress logging with color-coded messages
- Warning prompts before data erasure

## Requirements

### System Requirements
- Linux operating system (Ubuntu, Debian, Fedora, Arch, etc.)
- Python 3.6 or higher
- Sudo privileges for disk operations

### Required System Tools
```bash
# Ubuntu/Debian
sudo apt install parted dosfstools rsync util-linux python3-tk

# Fedora
sudo dnf install parted dosfstools rsync util-linux python3-tkinter

# Arch Linux
sudo pacman -S parted dosfstools rsync util-linux tk
```

### Optional Tools (for additional features)
```bash
# Ubuntu/Debian
sudo apt install ntfs-3g exfat-utils grub2-common

# Fedora
sudo dnf install ntfs-3g exfat-utils grub2-tools

# Arch Linux
sudo pacman -S ntfs-3g exfat-utils grub
```

## Installation

1. **Clone or download this repository:**
   ```bash
   cd ~/Documents/GitHub
   git clone <repository-url> "Botable usb"
   cd "Botable usb"
   ```

2. **Make the script executable:**
   ```bash
   chmod +x bootable_usb_creator.py
   ```

3. **Verify dependencies:**
   ```bash
   python3 bootable_usb_creator.py
   ```
   The application will check for missing dependencies on startup.

## Usage

### Basic Usage

1. **Launch the application:**
   ```bash
   python3 bootable_usb_creator.py
   ```

2. **Select ISO file:**
   - Click "Browse..." to select your Windows 10/11 or other OS ISO file

3. **Select USB device:**
   - The application automatically detects USB devices
   - Click "Refresh" to rescan for devices
   - Select your target USB drive from the dropdown

4. **Configure settings:**
   - **Boot Mode**: Choose UEFI (modern) or Legacy BIOS (older systems)
   - **Partition Scheme**: GPT (recommended for UEFI) or MBR (for Legacy BIOS)
   - **File System**: FAT32 (universal), NTFS (Windows), or exFAT (large files)
   - **Volume Label**: Custom name for your USB drive

5. **Create bootable USB:**
   - Click "Create Bootable USB"
   - Confirm the warning prompt
   - Wait for the process to complete

### Command Line Alternative

For advanced users who prefer command-line tools, you can also use `dd` directly:

```bash
# WARNING: This will erase all data on the USB drive!
sudo dd if=/path/to/your.iso of=/dev/sdX bs=4M status=progress && sync
```

Replace `/dev/sdX` with your actual USB device (e.g., `/dev/sdb`).

## Configuration Options

### Boot Modes

- **UEFI**: Modern boot mode, recommended for newer computers (2012+)
  - Faster boot times
  - Supports GPT partition tables
  - Required for Secure Boot

- **Legacy BIOS**: Traditional boot mode for older computers
  - Compatible with older hardware
  - Uses MBR partition tables
  - Requires GRUB bootloader installation

### Partition Schemes

- **GPT (GUID Partition Table)**:
  - Modern standard
  - Required for UEFI boot
  - Supports drives larger than 2TB
  - More reliable

- **MBR (Master Boot Record)**:
  - Legacy standard
  - Required for Legacy BIOS boot
  - Limited to 2TB drives
  - Maximum 4 primary partitions

### File Systems

- **FAT32**:
  - Universal compatibility
  - Works with UEFI and BIOS
  - File size limit: 4GB
  - Recommended for most use cases

- **NTFS**:
  - Windows native file system
  - No file size limits
  - May have compatibility issues with UEFI
  - Requires ntfs-3g package

- **exFAT**:
  - Modern file system
  - No file size limits
  - Good compatibility
  - Requires exfat-utils package

## Creating Windows 10/11 Bootable USB

### For Modern Computers (UEFI)

1. Download Windows 10/11 ISO from Microsoft
2. Select the ISO in the application
3. Configure:
   - Boot Mode: **UEFI**
   - Partition Scheme: **GPT**
   - File System: **FAT32** (recommended) or **NTFS**
4. Create bootable USB

### For Older Computers (Legacy BIOS)

1. Download Windows 10/11 ISO from Microsoft
2. Select the ISO in the application
3. Configure:
   - Boot Mode: **Legacy BIOS**
   - Partition Scheme: **MBR**
   - File System: **FAT32** or **NTFS**
4. Create bootable USB

## Troubleshooting

### USB Device Not Detected

- Ensure the USB drive is properly connected
- Click the "Refresh" button
- Try a different USB port
- Check if the device is mounted: `lsblk`

### Permission Denied Errors

- The application requires sudo privileges
- You will be prompted for your password
- Ensure your user is in the `sudo` group

### ISO File Not Bootable

- Verify the ISO file is not corrupted (check MD5/SHA256)
- Ensure you downloaded the correct ISO for your target system
- Try a different boot mode (UEFI vs Legacy BIOS)

### GRUB Installation Failed

- This is a warning, not an error
- The USB may still be bootable
- Install grub2-common package for full support

### Boot Fails on Target Computer

- Check BIOS/UEFI settings on the target computer
- Ensure boot mode matches (UEFI vs Legacy)
- Disable Secure Boot if using Legacy BIOS mode
- Try changing the boot order in BIOS

### Large ISO Files (>4GB) with FAT32

- FAT32 has a 4GB file size limit
- If your ISO contains files larger than 4GB:
  - Use NTFS file system instead
  - Or use exFAT if supported

## Safety Features

- ⚠️ **Warning prompts** before erasing data
- 🔍 **Device verification** to prevent accidental formatting
- 📝 **Detailed logging** of all operations
- 🔒 **Sudo authentication** for privileged operations

## Technical Details

### Process Overview

1. **Device Preparation**
   - Unmount all partitions
   - Wipe existing file system signatures

2. **Partitioning**
   - Create GPT or MBR partition table
   - Create primary partition
   - Set boot flag

3. **Formatting**
   - Format partition with selected file system
   - Apply volume label

4. **ISO Transfer**
   - Mount ISO file
   - Copy all contents to USB
   - Preserve file attributes

5. **Bootloader Installation** (Legacy BIOS only)
   - Install GRUB to MBR
   - Configure boot directory

6. **Finalization**
   - Sync data to disk
   - Unmount all filesystems

### Supported Operating Systems

- ✅ Windows 10 (all editions)
- ✅ Windows 11 (all editions)
- ✅ Ubuntu and derivatives
- ✅ Debian
- ✅ Fedora
- ✅ CentOS/RHEL
- ✅ Arch Linux
- ✅ Linux Mint
- ✅ Pop!_OS
- ✅ Any ISO-based operating system

## FAQ

**Q: Can I create a bootable USB for macOS?**
A: This tool is designed for Windows and Linux ISOs. macOS requires special handling and is not currently supported.

**Q: Will this work on Windows or macOS host systems?**
A: No, this is a Linux-only tool. For Windows, use Rufus. For macOS, use balenaEtcher or dd.

**Q: How long does it take to create a bootable USB?**
A: Typically 5-15 minutes depending on ISO size and USB speed. Windows 11 ISOs are around 5GB.

**Q: Can I use the USB drive for storage after?**
A: Yes, you can reformat it. However, while it's bootable, it's dedicated to that purpose.

**Q: Is this safe to use?**
A: Yes, but always double-check the selected device before confirming. The tool includes multiple safety prompts.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

⚠️ **WARNING**: Creating a bootable USB will ERASE ALL DATA on the selected device. Always backup important data before proceeding. The authors are not responsible for any data loss.

## Credits

Developed with ❤️ for the Linux community.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Consult the troubleshooting section

---

**Note**: Always download operating system ISOs from official sources to ensure authenticity and security.
