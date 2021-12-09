'''
    Created Sept 27, 2021
    @author: Jacob Calvin
    Purpose is to perform the op:create functionality of dodoku. Based on the user input, we return a specific grid or no grid (with status and integrity)
'''

import hashlib
import random

grid1 = '[0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1]'
grid2 = '[0,-6,0,0,0,0,0,-5,-9,-9,-3,0,-4,-8,0,0,0,0,0,0,0,0,0,-7,-3,0,0,0,-5,0,0,-1,0,0,-4,-6,0,0,0,0,0,-6,0,-9,0,0,-8,-1,-2,0,0,0,0,0,0,0,0,0,-7,0,0,0,0,0,0,0,0,-5,0,-8,0,-4,0,0,-1,0,0,0,-7,0,0,-6,0,-2,0,-9,0,0,0,0,0,0,0,0,-5,0,0,0,0,0,0,0,0,0,-9,-5,-3,0,0,-7,0,-4,0,0,0,0,0,-5,-8,0,0,-1,0,0,-9,0,0,0,-2,-1,0,0,0,0,0,0,0,0,0,-9,-8,0,-6,-1,-6,-1,0,0,0,0,0,-7,0]'
grid3 = '[0,0,0,0,-6,0,0,0,0,0,0,0,-4,0,-9,0,0,0,0,0,-9,-7,0,-5,-1,0,0,0,-5,-2,0,-7,0,-8,-9,0,-9,0,0,-5,0,-2,0,0,-4,0,-8,-3,0,-4,0,-7,-2,0,0,0,-1,-2,0,-8,0,0,0,0,-3,0,0,0,0,0,0,0,-6,0,-4,0,0,0,-8,0,-7,0,0,0,0,0,0,0,-5,0,0,0,0,-1,0,-6,-3,0,0,0,-9,-8,0,-5,0,-1,-2,0,-2,0,0,-7,0,-1,0,0,-3,0,-4,-3,0,-8,0,-6,-5,0,0,0,-7,-3,0,-5,-9,0,0,0,0,0,-4,0,-2,0,0,0,0,0,0,0,-6,0,0,0,0]'

def _create(parms):
    #if the user inputted level check to see if it has the correct input (1-3 or ''), if not then return error status
    if 'level' in parms.keys():
        if parms['level'] != '1' or parms['level'] != '2' or parms['level'] != '3' or parms['level'] != '':
            result = {'status' : 'error:'}
        
        #else if the user inputted correct params with level, then return the correct grid based off that input
        if parms['level'] == '1':
            grid =  grid1
            g = convertToArray(grid)
            grid = convertToCMO(g)
            grid = hashCMO(grid)
            integrity = getIntegrity(grid)
                
            result = {'grid' : g, 'status' : 'ok', 'integrity' : integrity}
            
        elif parms['level'] == '2':
            grid = grid2
            g = convertToArray(grid)
            grid = convertToCMO(g)
            grid = hashCMO(grid)
            integrity = getIntegrity(grid)
            
            result = {'grid' : g, 'status' : 'ok', 'integrity' : integrity}
            
        elif parms['level'] == '3':
            grid = grid3
            g = convertToArray(grid)
            grid = convertToCMO(g)
            grid = hashCMO(grid)
            integrity = getIntegrity(grid)
            
            result = {'grid' : g, 'status' : 'ok', 'integrity' : integrity}
            
        elif parms['level'] == '':
            grid = grid1
            g = convertToArray(grid)
            grid = convertToCMO(g)
            grid = hashCMO(grid)
            integrity = getIntegrity(grid)
            
            result = {'grid' : g, 'status' : 'ok', 'integrity' : integrity}
    
    #if the user inputted anything other than 'level' as a param, then return grid1 as default   
    else:
        grid = grid1
        g = convertToArray(grid)
        grid = convertToCMO(g)
        grid = hashCMO(grid)
        integrity = getIntegrity(grid)
        
        result = {'grid' : g, 'status' : 'ok', 'integrity' : integrity}
        
    return result

def convertToArray(x):
    x = x[1:-1]
    array = x.split(',')
    y = []
    for i in array:
        try:
            y.append(int(i))
        except:
            x = "Invalid Array"
            return x
    return y

def convertToCMO(rmo):
    cmo = []
    b = 63
    for i in range(15):
        if i > 5 and i < 9:
            y = i
            for x in range(6):
                cmo.append(rmo[y])
                y = y + 9
            for z in range(2):
                cmo.append(rmo[y])
                y = y + 15
            for a in range(7):
                cmo.append(rmo[y])
                y = y + 9

        elif i > 8:
            y = b
            for z in range(2):
                cmo.append(rmo[y])
                y = y + 15
            for x in range(7):
                cmo.append(rmo[y])
                y = y + 9
            b = b + 1

        else:
            y = i
            for x in range(6):
                cmo.append(rmo[y])
                y = y + 9
            for z in range(3):
                cmo.append(rmo[y])
                y = y + 15
    return cmo
    
def hashCMO(x):
    y = ''
    for i in x:
        y = y + str(i)
    myHash = hashlib.sha256()
    myHash.update(y.encode())
    myHashDigest = myHash.hexdigest()
    myHashDigest = myHashDigest.lower()
    
    return myHashDigest

def getIntegrity(x):
    rand = random.randint(0, (len(x) - 8))
    integrity = x[rand:rand+8]
    
    return integrity