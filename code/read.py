https://blog.csdn.net/qq_39216184/article/details/83023669


import  re
import os.path
import copy

fileName  = 'E:/code/python/amf.info'
def addChildNode(line, childList, childNode, isLeafNode):

    if "DW_AT_name:(indirect string, offset:" in line:

        childName = re.findall(r"indirect string, offset: (.+?)\): (.+?)$", line)
        if len(childName) != 0:
            childNode.append(childName[0][1])

    if "DW_AT_byte_size: " in line:
        byteSize = re.findall(r"DW_AT_byte_size: (.+?)$", line)
        bitSizeMap = {}
        if len(byteSize):
            isLeafNode = True
            bitSizeMap["bitSize"] = int(byteSize[0]) * 8
            childNode.append(bitSizeMap)

    if "DW_AT_sibling: " in line and isLeafNode is False:
        location = re.findall(r"DW_AT_sibling: (.+?)$", line)
        locationIndex = {}
        if len(location):
            reverse()
            locationIndex["location"] = location[0]
            childNode.append(locationIndex)

    if "DW_AT_data_member_location" in line:
        childList.append(copy.deepcopy(childNode))
        del  childNode[:]



def analysisObjDump():
    with open(fileName, 'r') as  file:
        contextFlag = False
        lineNum = 0
        preLine = None
        contextTree = []
        contextNode = {}
        childList = []
        selfAttribute = []
        childNode = []
        readChild = False

        isLeafNode = False

        for line in file:
            if"): AMPolicyContext" in line or contextFlag is True:

                if contextFlag is False:
                    contextName = re.findall(r'\): (.+?)$', line)
                    if len(contextName) != 0 and contextName[0] != 'AMPolicyContext\t':
                        contextFlag = True
                        continue

                if lineNum == 0:
                    print(preLine)

                lineNum = lineNum +1

                if 'DW_AT_byte_size' in line and readChild is False:
                    sizeMap = {}

                    byteSize = re.findall(r'DW_AT_byte_size:(.+?)$', line)
                    if len(byteSize) != 0:
                        sizeMap["size"] = byteSize[0]
                        selfAttribute.append(sizeMap)
                        readChild = True
                        continue

                if readChild is True:
                     addChildNode(line, childList, childNode, isLeafNode)
                     #print(childList)
                if 'Abbrev Number: 0' in line:
                    contextNode['AMPolicyContext'] = selfAttribute
                    selfAttribute.append(childList)
                    print(contextNode)
                    return
            preLine = line


def main():
    analysisObjDump()

22


main()

