import os, sys, shutil, errno
# Accepts 3 inputs: 
# Directory of the image folder
# Old file extension
# New file extension
def main():
	brandFolderDirectory = sys.argv[1]
	oldFileExt = sys.argv[2]
	newFileExt = sys.argv[3]
	renameFiles(brandFolderDirectory,oldFileExt,newFileExt)
	print("Operations Complete")


# Accepts brand folders, and sends them over to the out folder.
# rootDir - path of the folder containing all of the brand image folders
def renameFiles(rootDir,oldExt,newExt):
	imageFiles = [ f for f in os.listdir( rootDir ) if os.path.isfile(os.path.join(rootDir,f)) ]
	for imageFile in imageFiles:
		root,ext = os.path.splitext(imageFile)
		if(ext == "."+oldExt):
			print("Renaming : "+ os.path.join(rootDir,imageFile))
			os.rename(os.path.join(rootDir,imageFile),os.path.join(rootDir,root +"."+newExt))
	print("Finished with " + rootDir)

main()