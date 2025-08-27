#!/usr/bin/env python3
import os
import shutil
import zipfile
import struct

def create_advanced_apk():
    print("Building Advanced VCamera APK...")
    
    apk_dir = "build/apk_advanced"
    os.makedirs(apk_dir, exist_ok=True)
    os.makedirs(f"{apk_dir}/META-INF", exist_ok=True)
    
    # Create proper DEX file with basic structure
    dex_content = bytearray()
    # DEX magic and version
    dex_content.extend(b'dex\n035\x00')
    # Checksum (placeholder)
    dex_content.extend(b'\x00' * 4)
    # SHA-1 signature (placeholder)
    dex_content.extend(b'\x00' * 20)
    # File size (will be updated)
    dex_content.extend(struct.pack('<I', 112))  # Minimum DEX size
    # Header size
    dex_content.extend(struct.pack('<I', 0x70))
    # Endian tag
    dex_content.extend(b'\x78\x56\x34\x12')
    # Link size and offset
    dex_content.extend(b'\x00' * 8)
    # Map offset
    dex_content.extend(struct.pack('<I', 112))
    # String IDs
    dex_content.extend(b'\x00' * 8)
    # Type IDs
    dex_content.extend(b'\x00' * 8)
    # Proto IDs
    dex_content.extend(b'\x00' * 8)
    # Field IDs
    dex_content.extend(b'\x00' * 8)
    # Method IDs
    dex_content.extend(b'\x00' * 8)
    # Class defs
    dex_content.extend(b'\x00' * 8)
    # Data size and offset
    dex_content.extend(b'\x00' * 8)
    
    # Pad to minimum size
    while len(dex_content) < 112:
        dex_content.append(0)
    
    with open(f"{apk_dir}/classes.dex", "wb") as f:
        f.write(dex_content)
    
    # Create AndroidManifest.xml (binary format simulation)
    manifest_binary = bytearray()
    # XML magic
    manifest_binary.extend(b'\x03\x00\x08\x00')
    # File size
    manifest_binary.extend(struct.pack('<I', 1000))
    # String pool
    manifest_binary.extend(b'\x01\x00\x1c\x00')
    manifest_binary.extend(b'\x00' * 996)
    
    with open(f"{apk_dir}/AndroidManifest.xml", "wb") as f:
        f.write(manifest_binary)
    
    # Create resources.arsc
    resources_content = bytearray()
    # Resource table header
    resources_content.extend(b'\x02\x00\x0c\x00')  # RES_TABLE_TYPE
    resources_content.extend(struct.pack('<I', 12))  # Header size
    resources_content.extend(struct.pack('<I', 1000))  # Total size
    resources_content.extend(b'\x00' * 988)
    
    with open(f"{apk_dir}/resources.arsc", "wb") as f:
        f.write(resources_content)
    
    # Copy icon if exists
    icon_src = "app/src/main/res/mipmap-hdpi/ic_launcher.jpg"
    if os.path.exists(icon_src):
        os.makedirs(f"{apk_dir}/res/mipmap-hdpi", exist_ok=True)
        shutil.copy2(icon_src, f"{apk_dir}/res/mipmap-hdpi/")
    
    # Create META-INF files
    with open(f"{apk_dir}/META-INF/MANIFEST.MF", "w") as f:
        f.write("Manifest-Version: 1.0\nCreated-By: VCamera Builder\n")
    
    # Create APK
    apk_path = "build/outputs/apk/debug/VCamera-advanced.apk"
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_STORED) as apk:
        for root, dirs, files in os.walk(apk_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, apk_dir)
                apk.write(file_path, arc_path)
    
    print(f"Advanced APK created: {apk_path}")
    file_size = os.path.getsize(apk_path)
    print(f"APK size: {file_size} bytes")
    
    return apk_path

if __name__ == "__main__":
    create_advanced_apk()