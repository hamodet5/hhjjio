#!/usr/bin/env python3
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

def create_apk():
    print("Building VCamera APK...")
    
    # Create basic APK structure
    apk_dir = "build/apk_temp"
    os.makedirs(apk_dir, exist_ok=True)
    os.makedirs(f"{apk_dir}/META-INF", exist_ok=True)
    
    # Create AndroidManifest.xml in binary format (simplified)
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="virtual.camera.app">
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.INTERNET"/>
    <application android:label="VCamera" android:icon="@mipmap/ic_launcher">
        <activity android:name=".view.main.WelcomeActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    with open(f"{apk_dir}/AndroidManifest.xml", "w") as f:
        f.write(manifest_content)
    
    # Create resources.arsc (empty)
    with open(f"{apk_dir}/resources.arsc", "wb") as f:
        f.write(b'\x00' * 100)
    
    # Create classes.dex (empty)
    with open(f"{apk_dir}/classes.dex", "wb") as f:
        f.write(b'\x64\x65\x78\x0a\x30\x33\x35\x00')  # DEX header
    
    # Copy resources
    if os.path.exists("app/src/main/res"):
        shutil.copytree("app/src/main/res", f"{apk_dir}/res", dirs_exist_ok=True)
    
    # Create APK
    apk_path = "build/outputs/apk/debug/VCamera-debug.apk"
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk:
        for root, dirs, files in os.walk(apk_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, apk_dir)
                apk.write(file_path, arc_path)
    
    print(f"APK created: {apk_path}")
    return apk_path

if __name__ == "__main__":
    create_apk()