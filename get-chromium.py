#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import platform

global revisionFile
revisionFile = 'LAST_INSTALL'

def findOS():
	global userOS
	global userArch
	
	userOS = platform.system()
	userArch = platform.machine()
	
def createStringFromOS():
	
	osString = ['Mac', 'Win', 'Linux', 'Linux_x64', 'Arm']

	global osStringAppend
	global dlfile
	
	if userOS == 'Darwin':
		osStringAppend = osString[0]
		dlfile = 'chrome-mac.zip'
			
	elif userOS == 'Windows':
		osStringAppend = osString[1]
		
		WinSnapshotChoice = raw_input("Would you like to download an installable revision or portable revision (no installation required)? (install/portable) ")
		if WinSnapshotChoice != 'install' & WinSnapshotChoice != 'portable':
			sys.exit()
		elif WinSnapshotChoice == 'install':
			dlfile = 'mini_installer.exe'
		else:
			dlfile = 'chrome-win.zip'
	
	elif userOS == 'Linux':
		dlfile = 'chrome-linux.zip'
		
		if userArch == 'x86_64':
			osStringAppend = osString[3]
		
		elif 'arm' in 'userArch':
			osStringAppend = osString[4]
		
		else:
			osStringAppend = osString[2]
			
	else:
		
		print 'Platform not supported'
		sys.exit()
	
def findSnapshotVer():
	
	global SnapshotVer
	try:
		getSnapshotVer = urllib2.urlopen('https://commondatastorage.googleapis.com/chromium-browser-snapshots/' + osStringAppend + '/LAST_CHANGE', timeout=30)
	except urllib2.URLError:
		print "Couldn't access to the requested URL.\nCheck your Internet connection settings.\nExiting..."
		sys.exit()
		
	SnapshotVer = getSnapshotVer.read()
	
	print "Available Chromium snapshot revision: %s" % SnapshotVer
	
def checkPriorInstall():
	
	try:
		with open(revisionFile): pass
	except IOError:
		print "\nIt seems that this is the first time you fetch a Chromium snapshot.\nWould you like to create a file that keeps in memory the latest revision downloaded?\nThis will avoid redownloading Chromium if you already have the latest revision."
		createNewFile = raw_input("Create a file to remember the last downloaded revision? (y/n) ")
		if createNewFile != 'y' and createNewFile != 'n':
			sys.exit()
		else:
			touchRevisionFile = open(revisionFile, 'w+') # simply creating the file, it's updated with logNewInstall()
			touchRevisionFile.close()
			print "Revision file successfully created!"
			
	try:
		with open(dlfile): pass
		
		openRevisionFile = open(revisionFile, 'r')
		checkRevision = openRevisionFile.read()
		
		if checkRevision:
			print "Downloaded Chromium snapshot revision: %s" % checkRevision
			
			if SnapshotVer == checkRevision:
				print "You have already downloaded the latest Chromium snapshot.\nExiting..."
				sys.exit()
				
			elif SnapshotVer > checkRevision:
				print "The last revision you have downloaded is outdated.\nUpdating..."
		
		else:
			print "No Chromium snapshot has been downloaded yet. Downloading..."
			
		openRevisionFile.close()
		
	except IOError:
		print "You have not yet downloaded any Chromium snapshot, or they are stored in another directory."
	
def getSnapshot():
	
	SnapshotURL = 'https://commondatastorage.googleapis.com/chromium-browser-snapshots/' + osStringAppend + '/' + SnapshotVer + '/' + dlfile
			
	print "Download URL: %s" % SnapshotURL
	try:
		reachSnapshotFile = urllib2.urlopen(SnapshotURL, timeout=30)
		downloadSnapshot = urllib.urlretrieve(SnapshotURL, dlfile, reporthook=dlProgress)
		reachSnapshotFile.close()
	except urllib2.URLError:
		print "Couldn't retrieve the requested snapshot. Exiting..."
		sys.exit()
		
def dlProgress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\r" + "Downloading Chromium r%s... " % SnapshotVer + " %d%%" % percent)
	sys.stdout.flush()
		
def logNewInstall():
	
	updateRevisionFile = open(revisionFile, 'w+')
	updateRevisionFile.write(SnapshotVer)
	updateRevisionFile.close()

if __name__ == '__main__':
	findOS()
	createStringFromOS()
	findSnapshotVer()
	checkPriorInstall()
	getSnapshot()
	logNewInstall()
	print "Done. Exiting...\r"
