get-chromium
============

A Python script to instantly download the latest Chromium snapshot. Works on Linux, Windows, Mac, ARM.

![Chromium logo]("http://i.imgur.com/AcrrhKO.png")

###  How does it work?

get-chromium attempts to retrieve the latest Chromium snapshots, available [here](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html "Chromium Snapshots"). It keeps track of the latest downloaded revision, enabling it to update accordingly.

Place get-chromium.py in the directory where you would like to download the snapshots, and run it from there.

Currently, the supported OS are Linux, Windows, Mac, ARM, and Android will also be implemented in the future. 

### Requirements

The only programs required to run get-chromium are:

* [Python 2.7.x](http://www.python.org/getit/ "Download Python") or below, down to 2.5.x
* Python modules urllib & urllib2

### Downloading Chromium

Once you launch get-chromium.py, it will automatically download Chromium (safely, over HTTPS) - have a cup of coffee in the meantime. Should any error occur, get-chromium will inform you.

### Contribution

You are welcome to modify the script and add new features (especially installing Chromium on Mac & Linux).

To contribute, please fork the project and submit a pull request when appropriate. 

### License

get-chromium has been released into the public domain.
