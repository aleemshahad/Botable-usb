# Quick Start Guide

Get your bootable USB created in 5 minutes!

## Prerequisites

Install required system tools:

```bash
# Ubuntu/Debian
sudo apt install python3-tk parted dosfstools rsync util-linux

# Optional (for NTFS and exFAT support):
sudo apt install ntfs-3g exfatprogs grub2-common

# Fedora
sudo dnf install python3-tkinter parted dosfstools rsync util-linux
sudo dnf install ntfs-3g exfatprogs grub2-tools  # Optional

# Arch Linux
sudo pacman -S tk parted dosfstools rsync util-linux
sudo pacman -S ntfs-3g exfatprogs grub  # Optional
```

## Steps

### 1. Make the script executable
```bash
chmod +x bootable_usb_creator.py
```

### 2. Run the application
```bash
python3 bootable_usb_creator.py
```

### 3. Create your bootable USB

1. **Click "Browse..."** and select your ISO file (e.g., Windows 10/11 ISO)
2. **Select your USB device** from the dropdown (it auto-detects USB drives)
3. **Choose settings:**
   - For modern computers (2012+): UEFI + GPT + FAT32
   - For older computers: Legacy BIOS + MBR + FAT32
4. **Click "Create Bootable USB"**
5. **Confirm** the warning (all data will be erased!)
6. **Wait** for completion (5-15 minutes)

## Common Configurations

### Windows 10/11 (Modern PC)
- Boot Mode: **UEFI**
- Partition: **GPT**
- File System: **FAT32**

### Windows 10/11 (Old PC)
- Boot Mode: **Legacy BIOS**
- Partition: **MBR**
- File System: **FAT32**

### Linux Distributions
- Boot Mode: **UEFI** (or Legacy BIOS for older hardware)
- Partition: **GPT** (or MBR for Legacy)
- File System: **FAT32**

## Tips

- ✅ Use FAT32 for maximum compatibility
- ✅ Use NTFS if your ISO has files larger than 4GB
- ✅ Always verify the USB device before confirming
- ✅ Safely eject the USB after creation completes

## Troubleshooting

**USB not detected?**
- Click "Refresh" button
- Try a different USB port
- Ensure USB is properly connected

**Permission errors?**
- Enter your sudo password when prompted
- Ensure you're in the sudo group

**Need help?**
- Check the full README.md for detailed documentation
- Look at the application logs for error messages

---

That's it! Your bootable USB is ready to use. 🎉
