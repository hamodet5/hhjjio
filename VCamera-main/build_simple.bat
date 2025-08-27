@echo off
echo Building VCamera APK...

echo Checking Android SDK...
if not exist "%ANDROID_HOME%" (
    echo Android SDK not found. Please install Android Studio and set ANDROID_HOME
    pause
    exit /b 1
)

echo Creating directories...
mkdir build 2>nul
mkdir build\classes 2>nul
mkdir build\dex 2>nul
mkdir build\apk 2>nul

echo Compiling Java sources...
javac -cp "%ANDROID_HOME%\platforms\android-33\android.jar" -d build\classes app\src\main\java\virtual\camera\app\**\*.java

echo Creating DEX file...
"%ANDROID_HOME%\build-tools\33.0.0\dx" --dex --output=build\dex\classes.dex build\classes

echo Creating APK...
"%ANDROID_HOME%\build-tools\33.0.0\aapt" package -f -m -J build\gen -S app\src\main\res -M app\src\main\AndroidManifest.xml -I "%ANDROID_HOME%\platforms\android-33\android.jar"

echo APK build process completed!
pause