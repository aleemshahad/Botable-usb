#!/usr/bin/env python3
"""
Bootable USB Creator
A comprehensive tool for creating bootable USB drives for Windows 10, 11, and other operating systems.
Supports both UEFI and Legacy BIOS modes.
"""

import os
import sys
import subprocess
import json
import threading
from pathlib import Path
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext


class USBDevice:
    """Represents a USB storage device"""
    def __init__(self, device: str, size: str, model: str, mountpoint: str = ""):
        self.device = device
        self.size = size
        self.model = model
        self.mountpoint = mountpoint
    
    def __str__(self):
        return f"{self.device} - {self.model} ({self.size})"


class BootableUSBCreator:
    """Main application class for creating bootable USB drives"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bootable USB Creator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_iso = tk.StringVar()
        self.selected_device = tk.StringVar()
        self.boot_mode = tk.StringVar(value="UEFI")
        self.partition_scheme = tk.StringVar(value="GPT")
        self.file_system = tk.StringVar(value="FAT32")
        self.volume_label = tk.StringVar(value="BOOTABLE_USB")
        
        self.usb_devices: List[USBDevice] = []
        self.is_creating = False
        
        self.setup_ui()
        self.refresh_devices()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Bootable USB Creator", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # ISO Selection Section
        iso_frame = ttk.LabelFrame(main_frame, text="ISO Image Selection", padding="10")
        iso_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        iso_frame.columnconfigure(1, weight=1)
        
        ttk.Label(iso_frame, text="ISO File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        iso_entry = ttk.Entry(iso_frame, textvariable=self.selected_iso, state='readonly')
        iso_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(iso_frame, text="Browse...", command=self.browse_iso)
        browse_btn.grid(row=0, column=2)
        
        # USB Device Selection Section
        device_frame = ttk.LabelFrame(main_frame, text="USB Device Selection", padding="10")
        device_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        device_frame.columnconfigure(1, weight=1)
        
        ttk.Label(device_frame, text="USB Device:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.device_combo = ttk.Combobox(device_frame, textvariable=self.selected_device, 
                                         state='readonly')
        self.device_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        refresh_btn = ttk.Button(device_frame, text="Refresh", command=self.refresh_devices)
        refresh_btn.grid(row=0, column=2)
        
        # Warning label
        warning_label = ttk.Label(device_frame, 
                                 text="⚠️  WARNING: All data on the selected USB device will be erased!",
                                 foreground='red', font=('Arial', 9, 'bold'))
        warning_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Boot Mode
        ttk.Label(config_frame, text="Boot Mode:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        boot_mode_frame = ttk.Frame(config_frame)
        boot_mode_frame.grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(boot_mode_frame, text="UEFI", variable=self.boot_mode, 
                       value="UEFI", command=self.update_partition_scheme).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(boot_mode_frame, text="Legacy BIOS", variable=self.boot_mode, 
                       value="BIOS", command=self.update_partition_scheme).pack(side=tk.LEFT)
        
        # Partition Scheme
        ttk.Label(config_frame, text="Partition Scheme:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        partition_frame = ttk.Frame(config_frame)
        partition_frame.grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(partition_frame, text="GPT", variable=self.partition_scheme, 
                       value="GPT").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(partition_frame, text="MBR", variable=self.partition_scheme, 
                       value="MBR").pack(side=tk.LEFT)
        
        # File System
        ttk.Label(config_frame, text="File System:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        fs_frame = ttk.Frame(config_frame)
        fs_frame.grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(fs_frame, text="FAT32", variable=self.file_system, 
                       value="FAT32").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(fs_frame, text="NTFS", variable=self.file_system, 
                       value="NTFS").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(fs_frame, text="exFAT", variable=self.file_system, 
                       value="exFAT").pack(side=tk.LEFT)
        
        # Volume Label
        ttk.Label(config_frame, text="Volume Label:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        label_entry = ttk.Entry(config_frame, textvariable=self.volume_label)
        label_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Progress status label
        self.progress_label = ttk.Label(progress_frame, text="Ready", font=('Arial', 9))
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Progress bar with percentage
        progress_container = ttk.Frame(progress_frame)
        progress_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_container.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_container, mode='determinate', maximum=100, 
                                            style='green.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.progress_percent = ttk.Label(progress_container, text="0%", width=5)
        self.progress_percent.grid(row=0, column=1)
        
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=10, state='disabled',
                                                  wrap=tk.WORD)
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        progress_frame.rowconfigure(2, weight=1)
        
        # Action Buttons
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.grid(row=5, column=0, pady=(0, 0))
        
        self.create_btn = ttk.Button(self.button_frame, text="Create Bootable USB", 
                                     command=self.create_bootable_usb, style='Accent.TButton')
        self.create_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Finish button (hidden initially)
        self.finish_btn = ttk.Button(self.button_frame, text="✓ Finish", 
                                     command=self.on_finish, style='Success.TButton')
        
        # Configure styles
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', font=('Arial', 10, 'bold'), foreground='green')
        
        # Configure light green progress bar
        style.configure('green.Horizontal.TProgressbar', 
                       troughcolor='#e0e0e0',
                       background='#90EE90',  # Light green
                       lightcolor='#98FB98',
                       darkcolor='#7CCD7C')
    
    def update_partition_scheme(self):
        """Update partition scheme based on boot mode"""
        if self.boot_mode.get() == "UEFI":
            self.partition_scheme.set("GPT")
        else:
            self.partition_scheme.set("MBR")
    
    def on_finish(self):
        """Handle Finish button click - close the application"""
        self.root.quit()
        self.root.destroy()
    
    def show_finish_button(self):
        """Show the Finish button when process is complete"""
        self.finish_btn.pack(side=tk.LEFT, padx=5)
        self.create_btn.config(state='disabled')
    
    def hide_finish_button(self):
        """Hide the Finish button"""
        self.finish_btn.pack_forget()
    
    def update_progress(self, value: int, status: str = ""):
        """Update progress bar and status label"""
        self.progress_bar['value'] = value
        self.progress_percent.config(text=f"{value}%")
        if status:
            self.progress_label.config(text=status)
        self.root.update_idletasks()
    
    def reset_progress(self):
        """Reset progress bar to initial state"""
        self.progress_bar['value'] = 0
        self.progress_percent.config(text="0%")
        self.progress_label.config(text="Ready")
        self.hide_finish_button()
        self.root.update_idletasks()
    
    def log(self, message: str, level: str = "INFO"):
        """Add a message to the log"""
        self.log_text.config(state='normal')
        timestamp = ""
        if level == "ERROR":
            self.log_text.insert(tk.END, f"[ERROR] {message}\n", 'error')
            self.log_text.tag_config('error', foreground='red')
        elif level == "SUCCESS":
            self.log_text.insert(tk.END, f"[SUCCESS] {message}\n", 'success')
            self.log_text.tag_config('success', foreground='green')
        elif level == "WARNING":
            self.log_text.insert(tk.END, f"[WARNING] {message}\n", 'warning')
            self.log_text.tag_config('warning', foreground='orange')
        else:
            self.log_text.insert(tk.END, f"[INFO] {message}\n")
        
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
    
    def browse_iso(self):
        """Open file dialog to select ISO file"""
        filename = filedialog.askopenfilename(
            title="Select ISO File",
            filetypes=[("ISO Files", "*.iso"), ("All Files", "*.*")]
        )
        if filename:
            self.selected_iso.set(filename)
            self.log(f"Selected ISO: {filename}")
            
            # Auto-generate volume label from ISO filename
            iso_name = Path(filename).stem  # Get filename without extension
            # Clean up the name: uppercase, replace spaces/special chars with underscore
            clean_label = ''.join(c if c.isalnum() else '_' for c in iso_name).upper()
            # Limit to 11 characters for FAT32 compatibility
            clean_label = clean_label[:11]
            self.volume_label.set(clean_label)
            self.log(f"Auto-generated volume label: {clean_label}")
    
    def refresh_devices(self):
        """Refresh the list of available USB devices"""
        self.log("Scanning for USB devices...")
        self.usb_devices = self.get_usb_devices()
        
        device_list = [str(device) for device in self.usb_devices]
        self.device_combo['values'] = device_list
        
        if device_list:
            self.device_combo.current(0)
            self.log(f"Found {len(device_list)} USB device(s)")
        else:
            self.log("No USB devices found", "WARNING")
    
    def get_usb_devices(self) -> List[USBDevice]:
        """Get list of USB storage devices"""
        devices = []
        try:
            # Use lsblk to get block devices
            result = subprocess.run(
                ['lsblk', '-J', '-o', 'NAME,SIZE,MODEL,TRAN,TYPE,MOUNTPOINT'],
                capture_output=True, text=True, check=True
            )
            
            data = json.loads(result.stdout)
            
            for device in data.get('blockdevices', []):
                # Filter for USB devices
                if device.get('tran') == 'usb' and device.get('type') == 'disk':
                    dev_path = f"/dev/{device['name']}"
                    size = device.get('size', 'Unknown')
                    model = device.get('model', 'Unknown').strip()
                    mountpoint = device.get('mountpoint', '')
                    
                    devices.append(USBDevice(dev_path, size, model, mountpoint))
        
        except subprocess.CalledProcessError as e:
            self.log(f"Error scanning devices: {e}", "ERROR")
        except json.JSONDecodeError as e:
            self.log(f"Error parsing device information: {e}", "ERROR")
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
        
        return devices
    
    def run_command(self, cmd: List[str], description: str = "") -> bool:
        """Run a shell command and log output"""
        try:
            if description:
                self.log(description)
            
            self.log(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout:
                self.log(result.stdout.strip())
            
            return True
        
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e}", "ERROR")
            if e.stderr:
                self.log(f"Error output: {e.stderr}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
            return False
    
    def unmount_device(self, device: str) -> bool:
        """Unmount all partitions of a device"""
        try:
            # Get all mounted partitions for this device
            result = subprocess.run(
                ['lsblk', '-J', '-o', 'NAME,MOUNTPOINT', device],
                capture_output=True, text=True, check=True
            )
            
            data = json.loads(result.stdout)
            
            for dev in data.get('blockdevices', []):
                for child in dev.get('children', []):
                    mountpoint = child.get('mountpoint')
                    if mountpoint:
                        part_name = child.get('name')
                        self.log(f"Unmounting /dev/{part_name}...")
                        subprocess.run(['sudo', 'umount', f"/dev/{part_name}"], 
                                     capture_output=True, check=False)
            
            return True
        
        except Exception as e:
            self.log(f"Error unmounting device: {e}", "WARNING")
            return False
    
    def copy_with_progress(self, source: str, destination: str) -> bool:
        """Copy files from source to destination with progress tracking (30-90%)"""
        try:
            import re
            import time
            
            # First, get total size to copy
            self.log("Calculating total size...")
            result = subprocess.run(
                ['du', '-sb', source],
                capture_output=True, text=True, check=True
            )
            total_size = int(result.stdout.split()[0])
            self.log(f"Total size to copy: {total_size / (1024**3):.2f} GB")
            
            # Start rsync with progress
            process = subprocess.Popen(
                ['sudo', 'rsync', '-ah', '--info=progress2', f"{source}/", destination],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Monitor progress
            last_update = time.time()
            for line in process.stdout:
                # Parse rsync progress output
                # Format: "1.23G  45%  123.45MB/s    0:00:12"
                match = re.search(r'(\d+)%', line)
                if match:
                    copy_percent = int(match.group(1))
                    # Scale from 30% to 90% (60% range)
                    overall_percent = 30 + int(copy_percent * 0.6)
                    current_time = time.time()
                    # Update UI every 0.5 seconds to avoid overwhelming
                    if current_time - last_update > 0.5:
                        self.update_progress(overall_percent, f"Copying files: {copy_percent}%")
                        last_update = current_time
                
                # Log detailed progress (but not every line to avoid spam)
                if line.strip() and '%' in line:
                    self.log(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.update_progress(90, "File copy complete")
                return True
            else:
                stderr = process.stderr.read()
                self.log(f"Copy failed: {stderr}", "ERROR")
                return False
        
        except Exception as e:
            self.log(f"Error during file copy: {e}", "ERROR")
            return False
    
    def create_bootable_usb(self):
        """Main function to create bootable USB"""
        if self.is_creating:
            messagebox.showwarning("In Progress", "A USB creation is already in progress!")
            return
        
        # Validation
        if not self.selected_iso.get():
            messagebox.showerror("Error", "Please select an ISO file!")
            return
        
        if not os.path.exists(self.selected_iso.get()):
            messagebox.showerror("Error", "Selected ISO file does not exist!")
            return
        
        if not self.selected_device.get():
            messagebox.showerror("Error", "Please select a USB device!")
            return
        
        # Get the actual device path
        device_index = self.device_combo.current()
        if device_index < 0 or device_index >= len(self.usb_devices):
            messagebox.showerror("Error", "Invalid device selection!")
            return
        
        device = self.usb_devices[device_index].device
        
        # Confirmation
        confirm = messagebox.askyesno(
            "Confirm",
            f"This will ERASE ALL DATA on {device}!\n\n"
            f"ISO: {os.path.basename(self.selected_iso.get())}\n"
            f"Device: {self.selected_device.get()}\n"
            f"Boot Mode: {self.boot_mode.get()}\n"
            f"Partition: {self.partition_scheme.get()}\n"
            f"File System: {self.file_system.get()}\n\n"
            "Are you sure you want to continue?"
        )
        
        if not confirm:
            return
        
        # Start creation in a separate thread
        self.is_creating = True
        self.create_btn.config(state='disabled')
        self.reset_progress()
        
        thread = threading.Thread(target=self._create_bootable_usb_thread, args=(device,))
        thread.daemon = True
        thread.start()
    
    def _create_bootable_usb_thread(self, device: str):
        """Thread function for creating bootable USB"""
        try:
            self.log("=" * 50, "INFO")
            self.log("Starting bootable USB creation process...", "INFO")
            self.log("=" * 50, "INFO")
            
            # Step 1: Unmount device (0-5%)
            self.update_progress(0, "Step 1/6: Unmounting device...")
            self.log("\n[Step 1/6] Unmounting device...")
            self.unmount_device(device)
            self.update_progress(5, "Step 1/6: Complete")
            
            # Step 2: Wipe device (5-10%)
            self.update_progress(5, "Step 2/6: Wiping device...")
            self.log("\n[Step 2/6] Wiping device...")
            if not self.run_command(
                ['sudo', 'wipefs', '--all', device],
                "Removing existing file system signatures..."
            ):
                raise Exception("Failed to wipe device")
            self.update_progress(10, "Step 2/6: Complete")
            
            # Step 3: Create partition table (10-20%)
            self.update_progress(10, "Step 3/6: Creating partition table...")
            self.log("\n[Step 3/6] Creating partition table...")
            if self.partition_scheme.get() == "GPT":
                if not self.run_command(
                    ['sudo', 'parted', '-s', device, 'mklabel', 'gpt'],
                    "Creating GPT partition table..."
                ):
                    raise Exception("Failed to create GPT partition table")
                
                # Create EFI partition for UEFI
                if not self.run_command(
                    ['sudo', 'parted', '-s', device, 'mkpart', 'primary', 'fat32', '1MiB', '100%'],
                    "Creating partition..."
                ):
                    raise Exception("Failed to create partition")
                
                if not self.run_command(
                    ['sudo', 'parted', '-s', device, 'set', '1', 'boot', 'on'],
                    "Setting boot flag..."
                ):
                    raise Exception("Failed to set boot flag")
            else:
                # MBR for Legacy BIOS
                if not self.run_command(
                    ['sudo', 'parted', '-s', device, 'mklabel', 'msdos'],
                    "Creating MBR partition table..."
                ):
                    raise Exception("Failed to create MBR partition table")
                
                if not self.run_command(
                    ['sudo', 'parted', '-s', device, 'mkpart', 'primary', 'fat32', '1MiB', '100%'],
                    "Creating partition..."
                ):
                    raise Exception("Failed to create partition")
                
                if not self.run_command(
                    ['sudo', 'parted', '-s', device, 'set', '1', 'boot', 'on'],
                    "Setting boot flag..."
                ):
                    raise Exception("Failed to set boot flag")
            
            # Wait for partition to be recognized
            self.log("Waiting for partition to be recognized...")
            result = subprocess.run(['sudo', 'partprobe', device], capture_output=True, text=True)
            if result.returncode != 0:
                self.log(f"partprobe warning: {result.stderr}", "WARNING")
            import time
            time.sleep(3)  # Increased wait time for Ubuntu
            
            # Determine partition name (handle different device types)
            # NVMe devices: /dev/nvme0n1 -> /dev/nvme0n1p1
            # MMC/SD cards: /dev/mmcblk0 -> /dev/mmcblk0p1
            # Regular USB: /dev/sdb -> /dev/sdb1
            if 'nvme' in device or 'mmcblk' in device or 'loop' in device:
                partition = f"{device}p1"
            else:
                partition = f"{device}1"
            
            # Verify partition exists (retry up to 5 times)
            for retry in range(5):
                if os.path.exists(partition):
                    self.log(f"Partition {partition} detected")
                    break
                self.log(f"Waiting for partition {partition} (attempt {retry + 1}/5)...")
                time.sleep(1)
            else:
                raise Exception(f"Partition {partition} not found after creation. Device may need manual intervention.")
            
            self.update_progress(20, "Step 3/6: Complete")
            
            # Step 4: Format partition (20-30%)
            self.update_progress(20, "Step 4/6: Formatting partition...")
            self.log(f"\n[Step 4/6] Formatting partition {partition}...")
            fs = self.file_system.get()
            label = self.volume_label.get()
            
            if fs == "FAT32":
                if not self.run_command(
                    ['sudo', 'mkfs.vfat', '-F', '32', '-n', label, partition],
                    f"Formatting as FAT32..."
                ):
                    raise Exception("Failed to format partition")
            elif fs == "NTFS":
                if not self.run_command(
                    ['sudo', 'mkfs.ntfs', '-f', '-L', label, partition],
                    f"Formatting as NTFS..."
                ):
                    raise Exception("Failed to format partition")
            elif fs == "exFAT":
                # Try mkfs.exfat first (exfatprogs), fall back to mkexfatfs (exfat-utils)
                exfat_cmd = 'mkfs.exfat' if subprocess.run(['which', 'mkfs.exfat'], capture_output=True).returncode == 0 else 'mkexfatfs'
                if not self.run_command(
                    ['sudo', exfat_cmd, '-n', label, partition],
                    f"Formatting as exFAT..."
                ):
                    raise Exception("Failed to format partition")
            
            self.update_progress(30, "Step 4/6: Complete")
            
            # Step 5: Mount and copy ISO contents (30-90%)
            self.update_progress(30, "Step 5/6: Mounting ISO...")
            self.log("\n[Step 5/6] Copying ISO contents...")
            
            # Create mount points
            iso_mount = "/tmp/bootable_iso_mount"
            usb_mount = "/tmp/bootable_usb_mount"
            
            os.makedirs(iso_mount, exist_ok=True)
            os.makedirs(usb_mount, exist_ok=True)
            
            try:
                # Mount ISO
                if not self.run_command(
                    ['sudo', 'mount', '-o', 'loop', self.selected_iso.get(), iso_mount],
                    "Mounting ISO file..."
                ):
                    raise Exception(f"Failed to mount ISO: {self.selected_iso.get()}")
                
                # Wait a moment before mounting USB
                time.sleep(1)
                
                # Mount USB
                if not self.run_command(
                    ['sudo', 'mount', partition, usb_mount],
                    "Mounting USB partition..."
                ):
                    raise Exception(f"Failed to mount USB partition: {partition}. Ensure partition was formatted correctly.")
                
                # Copy files with progress tracking
                self.log("Copying files (this may take several minutes)...")
                if not self.copy_with_progress(iso_mount, usb_mount):
                    raise Exception("Failed to copy files")
                
            finally:
                # Unmount with retries
                self.log("Unmounting filesystems...")
                for _ in range(3):
                    result = subprocess.run(['sudo', 'umount', iso_mount], capture_output=True, check=False)
                    if result.returncode == 0:
                        break
                    time.sleep(1)
                for _ in range(3):
                    result = subprocess.run(['sudo', 'umount', usb_mount], capture_output=True, check=False)
                    if result.returncode == 0:
                        break
                    time.sleep(1)
            
            # Step 6: Install bootloader (90-95%)
            self.update_progress(90, "Step 6/6: Installing bootloader...")
            self.log("\n[Step 6/6] Installing bootloader...")
            
            if self.boot_mode.get() == "BIOS":
                # Install GRUB for Legacy BIOS
                try:
                    subprocess.run(['sudo', 'mount', partition, usb_mount], 
                                 capture_output=True, check=True)
                    
                    if not self.run_command(
                        ['sudo', 'grub-install', '--target=i386-pc', '--boot-directory=' + usb_mount + '/boot', device],
                        "Installing GRUB bootloader..."
                    ):
                        self.log("GRUB installation failed, but ISO may still be bootable", "WARNING")
                    
                    subprocess.run(['sudo', 'umount', usb_mount], 
                                 capture_output=True, check=False)
                except Exception as e:
                    self.log(f"Bootloader installation warning: {e}", "WARNING")
            else:
                self.log("UEFI mode - bootloader installation not required")
            
            self.update_progress(95, "Step 6/6: Complete")
            
            # Sync and finalize (95-100%)
            self.update_progress(95, "Finalizing: Syncing data to disk...")
            self.log("\nSyncing data to disk...")
            subprocess.run(['sync'], check=False)
            self.update_progress(100, "Complete!")
            
            self.log("=" * 50, "SUCCESS")
            self.log("Bootable USB created successfully!", "SUCCESS")
            self.log("=" * 50, "SUCCESS")
            self.log(f"\nYou can now safely remove the USB device: {device}")
            
            # Show Finish button on successful completion
            self.show_finish_button()
            
            messagebox.showinfo("Success", "Bootable USB created successfully!\n\nClick 'Finish' to close the application.")
        
        except Exception as e:
            self.log(f"\nFailed to create bootable USB: {e}", "ERROR")
            messagebox.showerror("Error", f"Failed to create bootable USB:\n{e}")
            self.create_btn.config(state='normal')
        
        finally:
            self.is_creating = False


def check_dependencies():
    """Check if required system tools are available"""
    required_tools = ['lsblk', 'parted', 'mkfs.vfat', 'rsync', 'wipefs', 'partprobe']
    optional_tools = ['mkfs.ntfs', 'mkfs.exfat', 'grub-install']
    
    missing_required = []
    missing_optional = []
    
    for tool in required_tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            missing_required.append(tool)
    
    for tool in optional_tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            missing_optional.append(tool)
    
    if missing_required:
        print("ERROR: Missing required tools:")
        print("  " + ", ".join(missing_required))
        print("\nPlease install them using your package manager:")
        print("  Ubuntu/Debian: sudo apt install parted dosfstools rsync util-linux")
        print("  Fedora: sudo dnf install parted dosfstools rsync util-linux")
        print("  Arch: sudo pacman -S parted dosfstools rsync util-linux")
        return False
    
    if missing_optional:
        print("WARNING: Missing optional tools (some features may not work):")
        print("  " + ", ".join(missing_optional))
        print("\nTo enable all features, install:")
        print("  Ubuntu/Debian: sudo apt install ntfs-3g exfatprogs grub2-common")
        print("  Fedora: sudo dnf install ntfs-3g exfatprogs grub2-tools")
        print("  Arch: sudo pacman -S ntfs-3g exfatprogs grub")
        print()
    
    return True


def main():
    """Main entry point"""
    print("Bootable USB Creator")
    print("=" * 50)
    
    # Check if running as root
    if os.geteuid() != 0:
        print("NOTE: This application requires sudo privileges for disk operations.")
        print("You will be prompted for your password when needed.\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("Starting GUI...\n")
    
    # Create and run GUI
    root = tk.Tk()
    app = BootableUSBCreator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
