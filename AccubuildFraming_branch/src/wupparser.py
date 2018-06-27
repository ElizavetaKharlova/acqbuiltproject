#This module provides functionality for working with WUP files
#that are used by ACQBUILTs machines. See the wupparsertest.py 
#in the tests directory to see an example of use

import re

WUP_DEFAULT_ERR = 3
WUP_DEFAULT_CLEAR = 0  



class WupFile:
    def __init__(self,fileObj,path):
        self.componentList = []
        self.modList = []
        self.fileObj = fileObj
        self.path = path
        self.version = ""

class WupComponent:
    def __init__(self,stype,length,width,height,xpos,ypos,zpos,extra,index):
        self.stype  = stype
        self.length = length
        self.width  = width
        self.height = height
        self.xpos   = xpos
        self.ypos   = ypos
        self.index   = index
        self.extra  = extra
        self.zpos   = zpos
    def __str__(self):
        return "{0} {1},{2},{3},{4},{5},{6},{7},{8};\n".format(\
                                                     self.stype, \
                                                     self.length, \
                                                     self.width, \
                                                     self.height, \
                                                     self.xpos, \
                                                     self.ypos, \
                                                     self.index, \
                                                     self.extra, \
                                                     self.zpos)
	def markError(self,err = WUP_DEFAULT_ERR):
		self.index = err        
class WupModule:
    def __init__(self,length,width,height,xpos,ypos,extra,zpos):
        self.length = length
        self.width  = width
        self.height = height
        self.xpos   = xpos
        self.ypos   = ypos
        self.zpos   = zpos
        self.extra  = extra
        self.componentList = []
    def markError(self,err = WUP_DEFAULT_ERR):
        self.index = err	

def getWupFile(path):
    studParser     = re.compile('OG.*|UG.*|QS.*|LS.*')
    modParser      = re.compile('MODUL.*')
    endmodParser   = re.compile('ENDMODUL.*')
    versionParser  = re.compile('VERSION.*')
    numParser      = re.compile('(?<=\s)\d+(?=,)|(?<=\s)\d+(?=;)')
    extParser      = re.compile('.*,\s*(.*)(?=,\s*\d+\s*;)')
    module = 0
    outFileObj = WupFile(open(path),path)
    rawFileObj = outFileObj.fileObj
    inModule = False
    for line in rawFileObj:
        if(versionParser.match(line)):
            outFileObj.version = line
        if(modParser.match(line)):
            valList = numParser.findall(line)
            extData = extParser.findall(line)
            outFileObj.modList.append(WupModule(int(valList[0]), \
                               int(valList[1]), \
                               int(valList[2]), \
                               int(valList[3]), \
                               int(valList[4]), \
                               extData, \
                               int(valList[5])))
            inModule = True
        if(endmodParser.match(line)):
            inModule = False
        if(studParser.match(line)):
            valList = numParser.findall(line)
            extData = extParser.findall(line)[0]
            try:
                if(inModule):
                    print("Parsing stud in module")
                    outFileObj.modList[-1].componentList.append(\
                                            WupComponent(line[0:2], \
                                            int(valList[0]), \
                                            int(valList[1]), \
                                            int(valList[2]), \
                                            int(valList[3]), \
                                            int(valList[4]), \
                                            WUP_DEFAULT_CLEAR, \
                                            extData, \
                                            int(valList[6])))
                    print(outFileObj.modList[-1].componentList[-1])
                else:
                    print("Parsing stud")
                    outFileObj.componentList.append(WupComponent( \
                                            line[0:2], \
                                            int(valList[0]), \
                                            int(valList[1]), \
                                            int(valList[2]), \
                                            int(valList[3]), \
                                            int(valList[4]), \
                                            WUP_DEFAULT_CLEAR, \
                                            extData, \
                                            int(valList[6])))
                    print(outFileObj.componentList[-1])
            except Exception as e:
                print(e)
                #print("wupParser: Could not parse object at line")
    line = rawFileObj.readline()
    return outFileObj
def outputWupFile(wupFile):
    fReplace = re.compile(re.escape('.WUP'), re.IGNORECASE)
    newFile = open(fReplace.sub('_ERRORS.WUP',wupFile.path),"w")
    studs = wupFile.componentList
    modules = wupFile.modList
    newFile.write(wupFile.version)
    for stud in studs:
        newFile.write(str(stud))
    for module in modules:
        newFile.write("MODUL {0} {1},{2},{3},{4},{5},{6};\n".format( \
                                                     module.length, \
                                                     module.width, \
                                                     module.height, \
                                                     module.xpos, \
                                                     module.ypos, \
                                                     module.extra, \
                                                     module.zpos))
        for stud in module.componentList:
            newFile.write(str(stud)) 
            
        newFile.write(".ENDMODUL\n")
