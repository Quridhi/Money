[app]

# (str) Title of your application
title = Money

# (str) Package name (no spaces or symbols)
package.name = moneyapp

# (str) Package domain (should be unique)
package.domain = org.quraidy

# (str) Source code where main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy,kivymd

# (str) Application orientation
orientation = portrait

# (bool) Fullscreen mode (1 = yes, 0 = no)
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum Android API supported
android.minapi = 21

# (int) NDK version to use
android.ndk = 25b

# (int) Android SDK version to use


# (bool) Use Android backup
android.allow_backup = True

# (bool) Disable byte-compile (optional)
android.no-byte-compile-python = False

# (list) Android permissions (for example: INTERNET)
android.permissions = INTERNET

# (list) Architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Bootstrap to use (Kivy/KivyMD)
p4a.bootstrap = sdl2

# (str) Artifact format (APK for debug)
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
