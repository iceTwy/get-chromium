get-chromium
============

A Python script to instantly download the latest Chromium snapshot. Works on Linux (including ARM), Windows, Mac, Android.

###  How does it work?

get-chromium attempts to retrieve the latest Chromium snapshots, available [here](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html "Chromium Snapshots"). It keeps track of the latest downloaded revision, enabling it to update accordingly.

Place get-chromium.py in the directory where you would like to download the snapshots, and run it from there.

Currently, the supported OS are Linux (x86, x86-64, ARM), Windows, Mac and Android.

### Requirements

Depending on your OS, you must install the following programs to run get-chromium:

* [Python 2.7.x](http://www.python.org/getit/ "Download Python") for Linux, Windows, Mac
* [Python4Android r5](https://code.google.com/p/python-for-android/downloads/detail?name=PythonForAndroid_r5.apk "Python4Android r5") & [SL4A r6](https://code.google.com/p/android-scripting/downloads/detail?name=sl4a_r6.apk "Scripting Layer 4 Android r6") for Android
* [PyPy 2.1](http://pypy.org/download.html "Download PyPy") for Linux ARM
* Python modules urllib & urllib2

_Note: get-chromium has not been tested on Linux ARM. Please open an issue if it doesn't work properly._

### Downloading Chromium

Once you launch get-chromium.py, it will automatically download Chromium (safely, over HTTPS) - have a cup of coffee in the meantime. Should any error occur, get-chromium will inform you.

On Android, you first need to install Python4Android, then run get-chromium.py through SL4A.

### Contribution

You are welcome to modify the script and add new features (especially installing Chromium on Mac & Linux).

To contribute, please fork the project and submit a pull request when appropriate. 

### License

get-chromium has been released into the public domain. Read LICENSE, WAIVER.md and check [unlicense.org](http://unlicense.org/) for further information.
