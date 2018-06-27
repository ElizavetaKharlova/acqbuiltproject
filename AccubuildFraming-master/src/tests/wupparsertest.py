#!/usr/bin/python3
import sys
sys.path.append('../')
import wupparser as wp

testFile = wp.getWupFile('35-1033.WUP')

for obj in testFile.componentList:
	if obj.xpos > 3000:
		obj.markError()

wp.outputWupFile(testFile)
print(len(testFile.componentList))
print(len(testFile.modList))
