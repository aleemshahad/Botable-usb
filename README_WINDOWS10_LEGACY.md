# Creating Windows 10 Bootable USB - Legacy BIOS Mode

## ✅ Your System is Ready!

All required tools are installed on your Ubuntu system:
- ✓ parted (partition management)
- ✓ mkfs.ntfs (NTFS formatting)
- ✓ rsync (file copying)
- ✓ grub-install (bootloader)

## 📋 Steps to Create Windows 10 Legacy Bootable USB

### 1. **Launch the Application**
```bash
cd /home/aleem/Documents/GitHub/Botable-usb
python3 bootable_usb_creator.py
```

### 2. **Configure Settings**
- **Boot Mode**: Select **Legacy BIOS**
- **Partition Scheme**: Select **MBR** (auto-selected with Legacy BIOS)
- **File System**: Select **NTFS**
- **Volume Label**: Use default or customize (e.g., "WIN10_USB")

### 3. **Select Your Files**
- Click **Browse** and select your Windows 10 ISO file
- Select your USB device from the dropdown (e.g., `/dev/sdb - 14.6GB`)
- Click **Refresh** if your USB isn't showing

### 4. **Create Bootable USB**
- Click **Create Bootable USB**
- Confirm the warning (all data will be erased!)
- Enter your sudo password when prompted
- Wait for the process to complete (may take 5-15 minutes)

## 🔧 What Was Fixed

1. **NTFS Formatting**: Changed from `-f` to `-Q` flag for proper quick format
2. **Partition Type**: Now correctly creates NTFS partition type in MBR
3. **Windows Bootloader**: Detects Windows ISO and uses `bootmgr` instead of GRUB
4. **Boot Flag**: Properly sets the boot flag on MBR partition

## ⚠️ Important Notes

### Before Creating:
- **Backup your USB data** - everything will be erased!
- **Unmount the USB** if it's currently mounted (the app will do this automatically)
- Your USB is currently at: `/dev/sdb` (14.6GB)

### For Windows 10 Legacy Boot:
- NTFS is **required** for files larger than 4GB (like `install.wim`)
- MBR partition scheme is **required** for Legacy BIOS
- The bootable USB will work on older computers without UEFI

### After Creation:
- Safely eject the USB
- Boot your target computer
- Enter BIOS/Boot menu (usually F12, F2, or Del key)
- Select the USB drive
- Choose "Legacy" or "CSM" boot mode in BIOS if available

## 🐛 Troubleshooting

### If USB doesn't boot:
1. **Check BIOS settings**:
   - Enable Legacy/CSM boot mode
   - Disable Secure Boot
   - Set USB as first boot device

2. **Verify partition**:
   ```bash
   sudo fdisk -l /dev/sdb
   ```
   Should show:
   - Disk label type: dos (MBR)
   - Partition 1 marked as bootable (*)
   - Type: HPFS/NTFS/exFAT

3. **Check bootmgr**:
   ```bash
   sudo mount /dev/sdb1 /mnt
   ls /mnt/bootmgr
   ls /mnt/sources/boot.wim
   sudo umount /mnt
   ```

### Common Issues:
- **"Partition not found"**: Wait longer after partition creation (increased to 3 seconds)
- **"Mount failed"**: USB may still be mounted - unmount manually first
- **"Permission denied"**: Make sure to enter sudo password when prompted

## 🎯 Quick Command Reference

```bash
# Check USB devices
lsblk -o NAME,SIZE,TYPE,TRAN,MOUNTPOINT

# Check partition table
sudo fdisk -l /dev/sdb

# Manually unmount if needed
sudo umount /dev/sdb1

# Run the application
python3 bootable_usb_creator.py
```

## ✨ Success Indicators

When the process completes successfully, you should see:
- Progress bar at 100%
- "Bootable USB created successfully!" message
- Green "✓ Finish" button appears
- Log shows "Windows bootloader (bootmgr) already copied from ISO"

Your Windows 10 Legacy bootable USB is now ready to use!
