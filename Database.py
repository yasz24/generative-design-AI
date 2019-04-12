import json
from System import System
from Force import Load
from graphics import StructureVisual
import featureExtractor

outputFile = "Database.txt"
s = StructureVisual()
database = []

struct1 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0))}

struct2 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0)),
           'beam4': ((0, 4), (4, 0)),
           'beam5': ((0, 0), (4, 4))}

struct3 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0)),
           'beam4': ((0, 4), (4, 0))}

struct4 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0)),
           'beam4': ((0, 0), (4, 4))}

struct5 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (2, 4)),
           'beam2': ((2, 4), (4, 0))}

struct6 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (0, 2)),
           'beam2': ((4, 0), (4, 2)),
           'beam3': ((0, 2), (2, 2)),
           'beam4': ((2, 2), (4, 2)),
           'beam5': ((2, 2), (4, 0)),
           'beam6': ((0, 0), (2, 2))}

struct7 = {'beam0': ((0, 0), (2, 0)),
           'beam1': ((0, 0), (0, 2)),
           'beam2': ((0, 2), (2, 2)),
           'beam3': ((2, 2), (4, 2)),
           'beam5': ((4, 2), (4, 0)),
           'beam6': ((2, 0), (4, 0)),
           'beam7': ((2, 0), (2, 2))}

struct8 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (0, 2)),
           'beam2': ((4, 0), (4, 2)),
           'beam3': ((0, 2), (2, 2)),
           'beam4': ((2, 2), (4, 2)),
           'beam5': ((2, 2), (4, 0))}

struct9 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (0, 4)),
           'beam2': ((0, 4), (2, 4)),
           'beam3': ((2, 4), (4, 4)),
           'beam4': ((4, 4), (4, 0)),
           'beam5': ((2, 4), (2, 2)),
           'beam6': ((0, 0), (2, 2)),
           'beam7': ((2, 2), (4, 0))}

struct10 = {'beam0': ((0, 0), (2, 0)),
            'beam1': ((2, 0), (2, 4)),
            'beam2': ((2, 0), (4, 0))}

struct11 = {'beam0': ((0, 0), (0, 4)),
            'beam1': ((0, 4), (4, 4)),
            'beam2': ((0, 4), (4, 0))}

struct12 = {'beam0': ((0, 0), (4, 0)),
            'beam1': ((0, 0), (4, 4)),
            'beam2': ((4, 4), (0, 4))}

database.append(struct1)
database.append(struct2)
database.append(struct3)
database.append(struct4)
database.append(struct5)
database.append(struct6)
database.append(struct7)
database.append(struct8)
database.append(struct9)
database.append(struct10)
database.append(struct11)
database.append(struct12)

with open(outputFile, 'w') as outFile:
    for struct in database:
        json.dump(struct, outFile)
        outFile.write('\n')

StructureVisual().drawStructure(struct8)
print(featureExtractor.FeatureExtractorUtil().pointDistribution(struct8))