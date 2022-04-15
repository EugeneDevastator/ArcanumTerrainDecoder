# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:35:30 2019

@author: DaveAstator
"""
import numpy as np
import cv2
import scipy
from PIL import Image

def decode2d(i,base=120):
    a = i // base
    b = i % base
    return a,b
decode2d(80664855162,67108860)

# remainder is <-X
#big num is y = 67108864.sec
Y_STEP = 67108864 #fixed do not change

#n = 106166224215
#yc = n // Y_STEP
#xc = n - yc * Y_STEP
#print(xc * 64,yc * 64)

sectorIdList = []
import glob
import os
os.chdir("s:\\Games\\arcanumU\\modules\\_UNPACK\\maps\\Arcanum1-024-fixed")
for file in glob.glob("*.sec"):
    sectorIdList.append(file[:-4])
    
sectorCoordinatesList = []
for sec in sectorIdList:
    n = int(sec)
    yc = n // Y_STEP
    xc = n - yc * Y_STEP
    sectorCoordinatesList.append((xc,yc))

#whole map of arcanum is 2000x2000 sectors. generated sectors are not saved.
#mark point on a map where an edited sector exists.
arcamap = np.zeros((2000,2000))
for pt in sectorCoordinatesList:
    arcamap[1999 - pt[0],pt[1]] = 1
plt.imsave('d:\\arcamap.png',arcamap)

#get world coordinate of a sector, unused.
def sector2wpos(snum):
    yc = snum // Y_STEP
    xc = snum - yc * Y_STEP
    return np.asarray([xc,yc]) * 64
    
#convert sector num to chunk coordinates
def sector2chunknum(snum):
    yc = snum // Y_STEP
    xc = snum - yc * Y_STEP
    return np.asarray([xc,yc])

def xy2sector(x,y):
    return y * getRowMultiplier() + x


#reads terrain data from sector file into array
#first byte is offset in 3x16 blocks from start of file till tilemap begin!  +4
#blocks
def extractTilemapFromSector(fname):
    f = open(fname,"rb")
    pos = 0
    #first byte is cound of offset chunks which come in size 3*16
    base = int.from_bytes(f.read(1),byteorder='little') * 3 * 16
    #also 4 more bytes are necesary.
    startpos = base + 4

    f.seek(startpos,0)
    #each sector has 64x64 tilemap
    tilemap = np.zeros((64,64))
    for i in range(0,64):
        for k in range(0,64):
            f.read(2)
            tilemap[i,k] = int.from_bytes(f.read(1),byteorder='little')
            f.read(1)
    f.close()
    
    return tilemap
    
#==========
#   plt.imshow(sector2tilemap2(sourcepath+"\\101602821845.sec"))
#======= generate tiles


gamepath = "s:\\Games\\arcanumU\\modules\\_UNPACK\\maps\\"
sourcepath = gamepath + "Arcanum1-024-fixed"

#running this second time, perhaps cuz of paranoia?
sectorIdList = []
import glob
import os
os.chdir(sourcepath)
for file in glob.glob("*.sec"):
    sectorIdList.append(file[:-4])

for sectorId in sectorIdList:
    tileMap = (extractTilemapFromSector(sectorId + ".sec"))
    chunkPos = sector2chunknum(int(sectorId))
    xyName = str(chunkPos[0]).zfill(4) + "_" + str(chunkPos[1]).zfill(4)
    cv2.imwrite(sourcepath + "\\png\\" + xyName + ".png", tileMap)

    
#============= generating chunks
#functions for resolving local chunk names
def fname2coords(s):
    return np.asarray([int(s[:4]),int(s[5:9])])
def coords2fname(c):
    return str(c[0]).zfill(4) + "_" + str(c[1]).zfill(4)


sourcepath = gamepath + "Arcanum1-024-fixed\\png"
sectorIdList = []
import glob
import os
os.chdir(sourcepath)
for file in glob.glob("*.png"):
    sectorIdList.append(file[:-4])

#=== Generate list of clusters that contain nearby maps.
mapClusterList = []
allchunks = sectorIdList
while len(allchunks) > 0:
    f = allchunks[0]
    sectorCoordinatesList = np.asarray([int(f[:4]),int(f[5:9])])
    allchunks.pop(0)    
    chunklist = [coords2fname(sectorCoordinatesList)]
    more = 1
    while more == 1:
        more = 0
        for stpos in chunklist:
            curpos = fname2coords(stpos)
            offs = ([0,1],[1,0],[-1,0],[0,-1])
            for of in offs:
                if coords2fname(curpos + of) in allchunks:
                    allchunks.remove(coords2fname(curpos + of))
                    more = 1
                    chunklist.append(coords2fname(curpos + of))
    mapClusterList.append(chunklist)
    print(len(allchunks))

#=== generate picmap for each cluster
#map is saved as a name of first chunk.
for curMap in mapClusterList:
    indexlist = []
    for chunk in curMap:
        indexlist.append(fname2coords(chunk))
    indexlist = np.asarray(indexlist)        
    coordslist = indexlist - np.asarray(indexlist).min(0)
    picmap = np.zeros((coordslist.max() * 64 + 64,coordslist.max() * 64 + 64))
    
    for fn,idx in zip(curMap,coordslist):
        pic = cv2.imread(sourcepath + "\\" + fn + ".png",0)
        picmap[idx[1] * 64:idx[1] * 64 + 64,idx[0] * 64:idx[0] * 64 + 64] = pic
    #plt.imshow(picmap)
    cv2.imwrite(sourcepath + "\\map_" + curMap[0] + ".png", numpy.fliplr(picmap))



xy2sector(1749,1514)
        

sector2chunknum(16508781330)
16508781330 
134217734
67108860

134217730 / 2
2080374816 // 67108860
2080374784 - 2080374816
