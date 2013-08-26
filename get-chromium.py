#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#		get-chromium - A Python script to retrieve the latest Chromium snapshots.
#		git repository: https://github.com/iceTwy/get-chromium.git
#		website: https://github.com/iceTwy/get-chromium
#	
#		author: iceTwy <icetwy@inventati.org> (icetwy.re)
#		
# LICENSE
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org/>
#

import urllib
import urllib2
import sys
import platform
import os
	
def BuildURLFromOS():
	osString = ['Mac', 'Win', 'Linux', 'Linux_x64', 'Linux_ARM_Cross-Compile', 'Android']

	userOS = platform.system()
	userArch = platform.machine()
	
	if userOS == 'Darwin':
		osStringAppend = osString[0]
		dlfile = 'chrome-mac.zip'
			
	elif userOS == 'Windows':
		osStringAppend = osString[1]
		
		WinSnapshotChoice = raw_input("Would you like to download an installable revision or portable revision (no installation required)? (install/portable) ")
		if WinSnapshotChoice != 'install' and WinSnapshotChoice != 'portable':
			sys.exit()
		elif WinSnapshotChoice == 'install':
			dlfile = 'mini_installer.exe'
		else:
			dlfile = 'chrome-win32.zip'
	
	elif userOS == 'Linux':		
		try:
			import android
			osStringAppend = osString[5]
			dlfile = 'chrome-android.zip'
		except ImportError:
			dlfile = 'chrome-linux.zip'
			
			if userArch == 'x86_64':
				osStringAppend = osString[3]
			
			elif 'arm' in userArch:
				osStringAppend = osString[4]
			
			else:
				osStringAppend = osString[2]
				
	else:
		print 'Platform not supported'
		sys.exit()
		
	return osStringAppend, dlfile
	
def FindSnapshotRevision(osStringAppend):
	try:
		getSnapshotRev = urllib2.urlopen('https://commondatastorage.googleapis.com/chromium-browser-snapshots/' + osStringAppend + '/LAST_CHANGE', timeout=30)
	except urllib2.URLError:
		print "Couldn't access to the requested URL.\nCheck your Internet connection settings.\nExiting..."
		sys.exit()
		
	SnapshotRev = getSnapshotRev.read()
	print "Available Chromium snapshot revision: %s" % SnapshotRev
	
	return SnapshotRev
	
def CheckDirsFiles():
	SettingsDir = os.path.expanduser("~/.get-chromium") # default directory to save get-chromium settings
	DLDirFile = os.path.expanduser("~/.get-chromium/DOWNLOAD_DIR") # file containing userDLDir
	RevisionFile = os.path.expanduser("~/.get-chromium/LAST_INSTALL") # file containing SnapshotRev
		
#SettingsDir check
	check_SettingsDir = os.path.exists(SettingsDir)
	
	if check_SettingsDir == False:
		os.mkdir(SettingsDir)
	else:
		pass
		
#RevisionFile check
	check_RevisionFile = os.path.exists(RevisionFile)
	
	if check_RevisionFile == False:
		print "\nIt seems that this is the first time you fetch a Chromium snapshot.\nWould you like to create a file that keeps in memory the latest revision downloaded?\nThis will avoid redownloading Chromium if you already have the latest revision."
		createNewFile = raw_input("Create a file to remember the last downloaded revision? (y/n) ")
		if createNewFile != 'y' and createNewFile != 'n':
			sys.exit()
		elif createNewFile == 'y':
			touchRevisionFile = open(RevisionFile, 'w+') # simply creating the file, it's updated with logNewInstall()
			touchRevisionFile.close()
			print "Revision file successfully created!"
		else:
			print "Revision file not created. Revision number will not be tracked."
	else:
		pass
		
#DLDirFile check
	check_DLDirFile = os.path.exists(DLDirFile)
	
	if check_DLDirFile == False:
		create_DLDirFile = raw_input("You haven't defined a default download directory. Would you like to select one? (y/n) ")
		
		if create_DLDirFile != 'y' and create_DLDirFile != 'n':
			sys.exit()
			
		if create_DLDirFile == 'y':
			touch_DLDirFile = open(DLDirFile, 'w')
			choose_DLDir = raw_input("Choose a default download directory (e.g. ~/get-chromium): ")
			touch_DLDirFile.write(choose_DLDir)
			touch_DLDirFile.close()
			print "Default download directory successfully chosen!"
				
			open_DLDirFile = open(DLDirFile, 'r')
			userDLDir = open_DLDirFile.read()
			open_DLDirFile.close()
			
		else:
			print "Snapshots will be downloaded to the current directory."
			default_DLDir = os.getcwd()
			touch_DLDirFile = open(DLDirFile, 'w')
			touch_DLDirFile.write(default_DLDir)
			touch_DLDirFile.close()
				
			open_DLDirFile = open(DLDirFile, 'r')
			userDLDir = open_DLDirFile.read()
			open_DLDirFile.close()
	else: #DLDirFile exists
		open_DLDirFile = open(DLDirFile, 'r')
		userDLDir = open_DLDirFile.read()
		
		if not userDLDir: #if DLDir is an empty string
			touch_DLDirFile = open(DLDirFile, 'w')
			choose_DLDir = raw_input("Choose a default download directory (e.g. ~/get-chromium): ")
			
			if not choose_DLDir: #if the user doesn't select a default DL directory
				#save current directory to DLDirFile
				default_DLDir = os.getcwd()
				touch_DLDirFile.write(default_DLDir)
				touch_DLDirFile.close()
				
				userDLDir = open_DLDirFile.read()
				open_DLDirFile.close()
		else: #all is good, just save DLDir in userDLDir
			open_DLDirFile.close()
			
	return RevisionFile, userDLDir

def CheckPriorRevision(RevisionFile, SnapshotRev):
	
	check_RevisionFile = os.path.exists(RevisionFile)
	
	if check_RevisionFile == True:
		openRevisionFile = open(RevisionFile, 'r')
		checkRevision = openRevisionFile.read()
		
		if checkRevision:
			print "Downloaded Chromium snapshot revision: %s" % checkRevision
			
			if SnapshotRev == checkRevision:
				print "You have already downloaded the latest Chromium snapshot.\nExiting..."
				sys.exit()
				
			elif SnapshotRev > checkRevision:
				print "The last revision you have downloaded is outdated.\nUpdating..."
		
		else:
			print "You have not yet downloaded any Chromium snapshot, or they are stored in another directory. Downloading..."
			
		openRevisionFile.close()
	
	else:
		print "No revision file found. Downloading..."
		
def GetSnapshot(osStringAppend, SnapshotRev, dlfile, userDLDir):
	SnapshotURL = 'https://commondatastorage.googleapis.com/chromium-browser-snapshots/' + osStringAppend + '/' + SnapshotRev + '/' + dlfile
	print "Download URL: %s" % SnapshotURL
	
	try:
		reachSnapshotFile = urllib2.urlopen(SnapshotURL, timeout=30)
		os.chdir(userDLDir)
		downloadSnapshot = urllib.urlretrieve(SnapshotURL, dlfile, reporthook=dlProgress)
		reachSnapshotFile.close()
	except urllib2.URLError:
		print "Couldn't retrieve the requested snapshot. Exiting..."
		sys.exit()
		
def dlProgress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\r" + "Downloading Chromium r%s... " % SnapshotRev + " %d%%" % percent)
	sys.stdout.flush()
		
def LogNewInstall(RevisionFile, SnapshotRev):
	updateRevisionFile = open(RevisionFile, 'w+')
	updateRevisionFile.write(SnapshotRev)
	updateRevisionFile.close()

if __name__ == '__main__':
	osStringAppend, dlfile = BuildURLFromOS()
	SnapshotRev = FindSnapshotRevision(osStringAppend)
	RevisionFile, userDLDir = CheckDirsFiles()
	CheckPriorRevision(RevisionFile, SnapshotRev)
	GetSnapshot(osStringAppend, SnapshotRev, dlfile, userDLDir)
	LogNewInstall(RevisionFile, SnapshotRev)
	print "\nDone. Exiting...\r"
