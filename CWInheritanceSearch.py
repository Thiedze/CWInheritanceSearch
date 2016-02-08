import fnmatch
import os
import sys
import json

searchStrings = []
ignoredClasses = []
ignoredPaths = []
foundFiles = []

classStart = 'class('
classEnd = ')'


def fillIgnoredList(result, filename):
	file = open(os.path.dirname((os.path.realpath(__file__))) + '\\' + filename, 'r', encoding="ISO-8859-1")
	
	for line in file:
		result.append(line.strip())

		
def parseFile (path):
	file = open(path, 'r', encoding="ISO-8859-1")
	lineNumber = 1
	
	for line in file:
		lineAsString = str(line)
		for searchString in searchStrings:
			if (searchString in lineAsString):
				foundFiles.append(searchString + ', ' + str(lineNumber) + ' : ' + os.path.basename(path))
		lineNumber = lineNumber + 1
				
def searchFiles():
	for root, dirnames, filenames in os.walk(sys.argv[2]):
		if not root in ignoredPaths:
			for filename in fnmatch.filter(filenames, '*.pas'):
				parseFile(os.path.join(root, filename))
			
			for filename in fnmatch.filter(filenames, '*.dfm'):
				parseFile(os.path.join(root, filename))
		
def parseClass(path):
	file = open(path, 'r', encoding="ISO-8859-1")

	for line in file:
		if (line.find(classStart) > -1):
			substring = line[line.index(classStart)+len(classStart):line.index(classEnd)]
			if (substring.find('TFP') == -1) and not (substring.strip() in ignoredClasses):
				searchStrings.append(substring.strip())

def searchClasses():
	for root, dirnames, filenames in os.walk(sys.argv[1]):
		for filename in fnmatch.filter(filenames, '*.pas'):
			if not root in ignoredPaths:
				parseClass(os.path.join(root, filename))
			
def printResult(results):
	results = sorted(set(results))
	for result in results:
		print(result)
			
def writeResult(results, filename, headline = ''):
	file = open(os.path.dirname((os.path.realpath(__file__))) + '\\' + filename, 'w+')
	results = sorted(set(results))	
	if headline != '':
		file.write(headline  + '\n')
	for result  in results:
		file.write(result + '\n')
		
		
if len(sys.argv) > 2:
	print('Search classes')
	fillIgnoredList(ignoredClasses, 'ignoredClasses.txt')
	fillIgnoredList(ignoredPaths, 'ignoredPaths.txt')
	searchClasses()
	writeResult(searchStrings, 'searchStrings.txt')
	print('Search files')
	searchFiles()
	writeResult(foundFiles, 'foundFiles.txt')
else:
	print('1. Argument: Classes to search for')
	print('2. Argument: Files to search in')