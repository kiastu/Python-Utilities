import os, sys, zipfile, shutil, errno

# TODO:
# - Handle nested zip files
# - Flatten folder structures
# - OPTIONAL: Allow for folder renames
#
# Accepts 2 inputs: 
# Directory of the image folder
# Directory of the output folder.
def main():
	brandFolderDirectory = sys.argv[1]
	destDir = sys.argv[2]
	unzipEverything(brandFolderDirectory,destDir)
	flattenEverything(destDir)
	print("Operations Complete")


# Accepts brand folders, and sends them over to the out folder.
# rootDir - path of the folder containing all of the brand image folders
def unzipEverything(rootDir,destDir):
	print("Beginning unzipping")
	brandFolders = [ f for f in os.listdir( rootDir ) if os.path.isdir(os.path.join(rootDir,f)) ]
	print("Creating new out folder")
	createFolderIfNotExists(destDir)
	for brandFolder in brandFolders:
		print("Creating new brandFolder: "+brandFolder)
		newBrandPath = os.path.join(destDir,brandFolder)
		createFolderIfNotExists(newBrandPath)
		# walk dives in to all of the files within a particular brandFolder, and traverses the folder tree.
		for dirPath, dirNames, fileNames in os.walk(os.path.join(rootDir,brandFolder)):
			for fileName in fileNames:
				if fileName.endswith(".zip"):
					try:
						with zipfile.ZipFile(os.path.join(dirPath,fileName)) as zf:
							print("UnZipping " + fileName + " to:" + newBrandPath)
							zf.extractall(newBrandPath)
					except zipfile.BadZipfile as e:
						print("BadZipfile error, attempting to fix...")
						#fixBadZipFile(os.path.join(dirPath,fileName))
						print("Weird bad zipfile error for zipfile: " + os.path.join(dirPath,fileName))
						print(e)
						#don't wanna deal with this weird file......
						continue
				else:
					#this is a regular file, who knows what the extension is, copy it over.
					print("Copying over file/folder from: "+ os.path.join(dirPath,fileName))
					shutil.copy(os.path.join(dirPath,fileName),newBrandPath)
		print("Finished with brand: "+brandFolder)
	# seek and destroy(unzip) any straggled nested zips.
	isZipLeft = True
	while isZipLeft:
		print("Seeking out nested zips")
		isZipLeft = False
		for dirPath, dirNames, fileNames in os.walk(destDir):
			for fileName in fileNames:
				if fileName.endswith(".zip"):
					try:
						with zipfile.ZipFile(os.path.join(dirPath,fileName)) as zf:
							print("UnZipping Nested Zip " + fileName + " from: " + os.path.join(dirPath,fileName) + " to: " + dirPath)
							zf.extractall(dirPath)
							#delete this file
							os.remove(os.path.join(dirPath,fileName))
							isZipLeft = True

					except zipfile.BadZipfile as e:
						print("BadZipfile error, attempting to fix...")
						#fixBadZipFile(os.path.join(dirPath,fileName))
						print("Weird bad zipfile error for zipfile: " + os.path.join(dirPath,fileName))
						print(e)
						#don't wanna deal with this weird file......
						continue
# creates a new folder at path if it does not already exists.
def createFolderIfNotExists(path):
	try:
		os.mkdir(path)
		print("Creating new folder at:" + path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise # The exception is actually not a folder exists problem.
		print("Folder already exists at:" + path)

def flattenEverything(destDir):
	#Flatten them like pancakes!
	print("Beginning flattening...")
	brandFolders = [ f for f in os.listdir( destDir ) if not os.path.isfile(os.path.join(destDir,f)) ]
	for brandFolder in brandFolders:
		brandFolderPath = os.path.join(destDir,brandFolder)
		print("Flattening brand folder: "+ brandFolder)
		for dirpath, dirnames, filenames in os.walk(brandFolderPath):
			for filename in filenames:
				try:
					os.rename(os.path.join(dirpath, filename), os.path.join(brandFolderPath,filename))
				except OSError as e:
					print ("Could not move %s " % os.path.join(dirpath, filename))
					print(e)
		
		emptyFolders = [f for f in os.listdir(brandFolderPath)if os.path.isdir(os.path.join(brandFolderPath, f))]
		# delete all the empty folders
		for emptyFolder in emptyFolders:
			try:
				shutil.rmtree(os.path.join(brandFolderPath, emptyFolder))
				print("Deleted: "+ os.path.join(brandFolderPath,emptyFolder))
			except OSError as e:
				print("Oops, directory isn't empty: " + emptyFolder)
				print(e) 

	print("Everything's pancaked. Just need some syrup.")

def fixBadZipFile(zipFilePath):
	f = open(zipFilePath, 'r+b')  
	data = f.read()  
	pos = data.find('\x50\x4b\x05\x06') # End of central directory signature  
	if (pos > 0):  
		self._log("Trancating file at location " + str(pos + 22)+ ".")  
		f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
		f.truncate()  
		f.close()
	else:  
		print("Truncated ")
		# raise error, file is truncated  
main()