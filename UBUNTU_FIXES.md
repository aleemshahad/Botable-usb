# Ubuntu Compatibility Fixes

## Changes Made

### 1. **Improved Partition Naming Logic**
- **Issue**: The original code didn't handle NVMe and MMC/SD card devices correctly
- **Fix**: Added proper detection for different device types:
  - NVMe devices: `/dev/nvme0n1` → `/dev/nvme0n1p1`
  - MMC/SD cards: `/dev/mmcblk0` → `/dev/mmcblk0p1`
  - Regular USB: `/dev/sdb` → `/dev/sdb1`
  - Loop devices: `/dev/loop0` → `/dev/loop0p1`

### 2. **Partition Detection with Retry Logic**
- **Issue**: Ubuntu sometimes takes longer to recognize new partitions
- **Fix**: 
  - Increased wait time from 2 to 3 seconds after `partprobe`
  - Added retry loop (up to 5 attempts) to verify partition exists
  - Better error messages if partition not found

### 3. **exFAT Compatibility**
- **Issue**: Ubuntu uses `exfatprogs` package instead of older `exfat-utils`
- **Fix**: 
  - Auto-detect which exFAT tool is available (`mkfs.exfat` or `mkexfatfs`)
  - Updated installation instructions to use `exfatprogs`

### 4. **Enhanced Error Handling**
- Added better error messages for mount failures
- Added retry logic for unmounting filesystems (3 attempts)
- Added 1-second delay before mounting USB partition
- More descriptive error messages with device paths

### 5. **Dependency Check Improvements**
- Added `partprobe` to required tools list
- Updated package names for Ubuntu 25.10:
  - `exfat-utils` → `exfatprogs`
  - More accurate package recommendations

### 6. **Auto-Generated Volume Labels**
- **New Feature**: Automatically generates volume label from ISO filename
- Cleans filename (uppercase, replaces special chars with underscores)
- Limits to 11 characters for FAT32 compatibility
- User can still manually edit the label

## Testing Recommendations

1. **Test with different device types**:
   - Standard USB drives
   - NVMe devices (if available)
   - SD cards via card reader

2. **Test with different ISOs**:
   - Ubuntu Desktop ISO
   - Windows 10/11 ISO
   - Other Linux distributions

3. **Test different configurations**:
   - UEFI + GPT + FAT32
   - Legacy BIOS + MBR + FAT32
   - NTFS for large ISOs (>4GB files)

## Known Limitations

- GRUB installation for Legacy BIOS may fail on some systems (non-critical)
- exFAT support requires optional package installation
- NTFS support requires `ntfs-3g` package

## Installation for Ubuntu 25.10

```bash
# Required packages
sudo apt install python3-tk parted dosfstools rsync util-linux

# Optional packages (recommended)
sudo apt install ntfs-3g exfatprogs grub2-common
```
