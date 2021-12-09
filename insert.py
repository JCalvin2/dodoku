import dodoku.create as create 
value = 0
def _insert(parms):
    for i in parms.keys():
        if (i == 'op') or (i == 'value') or (i == 'cell') or (i == 'grid') or (i == 'integrity'):
            pass
        else:
            result = {'status':'error: Invalid Key'}
            return result
        
    if ('cell' not in parms.keys()) or ('grid' not in parms.keys()) or ('integrity' not in parms.keys()):
        result = {'status': 'error: Missing Key(s)'}
        return result
    
    if parms['cell'] == '':
        result = {'status': 'error: Invalid Cell Input'}
        return result
    elif parms['grid'] == '':
        result = {'status': 'error: Invalid Grid Input'}
        return result
    elif parms['integrity'] == '':
        result = {'status': 'error: Invalid Integrity Input'}
        return result
    
    vv = validateValue(parms)
    if vv == {'status': 'ok'}:
        pass
    elif vv == {'status': 'change value'}:
        parms['value'] = value
    else:
        return vv
    
    vc = validateCell(parms['cell'])
    if vc != {'status': 'ok'}:
        return vc
    else:
        pass
    
    vg = validateGrid(parms['grid'])
    if vg != {'status': 'ok'}:
        return vg
    else:
        pass
        
    vi = validateIntegrity(parms)
    if vi != {'status': 'ok'}:
        return vi
    else:
        pass
    
    result = insertIntoGrid(parms)
    
    return result

def validateValue(parms):
    res = {}
    if 'value' in parms.keys():
        if parms['value'] == '':
            res = {'status': 'change value'}
            value = 0
        else:
            try:
                int(parms['value'])
                if int(parms['value']) < 1 or int(parms['value']) > 9:
                    res = {'status': 'error: Out of Bounds Value'}
                else:
                    res = {'status': 'ok'}
                    return res
            except:
                res = {'status' : 'error: Invalid Value'}

        return res
    else:
        res = {'status': 'change value'}
        value = 0
        return res

def validateCell(x):
    res = {}
    if x[0] == "r" or x[0] == "R":
        pass
    else:
        res = {'status': 'error: Invalid Row'}
        return res
    if x[1] == "c" or x[1] == "C":
        res = {'status': 'error: Invalid Row'}
        return res
    if x[2] == "c" or x[2] == "C" or x[3] == "c" or x[3] == 'C':
        pass
    else:
        res = {'status': 'error: Invalid Column'}
        return res
    for i in range(len(x)):
        if x[i] == 'c' or x[i] == 'C':
            row = x[:i]
            col = x[i:]
    try:
        rowNumber = int(row[1:])
    except:
        res = {'status': 'error: Invalid Row'}
        return res
    try:
        colNumber = int(col[1:])
    except:
        res = {'status': 'error: Invalid Column'}
        return res
     
    if (rowNumber<7 and colNumber>9) or (rowNumber>9 and colNumber<7) or rowNumber>15 or rowNumber < 1 or colNumber>15 or colNumber<1:
        res = {'status': 'error: Out of Bounds Cell'}
    
    else:
        res = {'status': 'ok'}
        
    return res

def validateGrid(x):
    x = create.convertToArray(x)
    res = {}
    if x == "Invalid Array":
        res = {'status': 'error: Invalid Array'}
        return res
    elif len(x) != 153:
            res = {'status': 'error: Invalid Array'}
            return res
        
    for i in x:
        if int(i) < -9 or int(i) > 9:
            res = {'status': 'error: Invalid Array'}
            return res
        
    res = {'status': 'ok'}
    return res
    
def validateIntegrity(parms):
    res = {}
    grid = create.convertToArray(parms['grid'])
    grid = create.convertToCMO(grid)
    grid = create.hashCMO(grid)
    
    if "'" in parms['integrity']:
        parms['integrity'] = parms['integrity'][1:-1]
        
    if parms['integrity'] not in grid:
        res = {'status': 'error: Invalid Integrity'}
        return res
    
    elif len(parms['integrity']) != 8:
        res = {'status': 'error: Invalid Integrity Length'}
        return res
    else:
        res = {'status': 'ok'}
        
    return res

def insertIntoGrid(parms):
    rmo = create.convertToArray(parms['grid'])
    
    x = parms['cell']
    for i in range(len(x)):
        if x[i] == 'c' or x[i] == 'C':
            row = x[:i]
            col = x[i:]
    
    rowNumber = int(row[1:]) - 1
    colNumber = int(col[1:]) - 1
    value = int(parms['value'])
    
    status = cellStatus(rmo, rowNumber, colNumber, value)
    
    res = {}

    if rowNumber < 6:
        if rmo[(rowNumber * 9) + colNumber] < 0:
            res = {'status': 'error: Immutable Cell'}
            return res
        elif rmo[(rowNumber * 9) + colNumber] == int(value) and int(value) > 0:
            rmo[(rowNumber * 9) + colNumber] = 0
            stat = cellStatus(rmo, rowNumber, colNumber, value)
            rmo[(rowNumber * 9) + colNumber] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            if stat == True:
                res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
                return res
            else:
                res =  {'grid': rmo, 'status': 'warning', 'integrity': hashIntegrity}
                return res
        elif int(value) == 0:
            rmo[(rowNumber * 9) + colNumber] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
            return res
        
        else:
            rmo[(rowNumber * 9) + colNumber] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            if status == True:
                res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'ok'}
                return res
            else:
                if int(value) == 0:
                    res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'ok'}
                else:
                    
                    res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'warning'}
                res = {'grid': rmo, 'status': 'warning', 'integrity': hashIntegrity}
                return res
                
            
    elif rowNumber > 5 and rowNumber < 9:
        if rowNumber == 6:
            z = 54
        elif rowNumber == 7:
            z = 69
        elif rowNumber == 8:
            z = 84
            
        if rmo[z + colNumber] < 0:
            res = {'status': 'error: Immutable Cell'}
            return res
        elif rmo[z + colNumber] == int(value) and int(value) > 0:
            rmo[z + colNumber] = 0
            stat = cellStatus(rmo, rowNumber, colNumber, value)
            rmo[z + colNumber] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            if stat == True:
                res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
                return res
            else:
                res =  {'grid': rmo, 'status': 'warning', 'integrity': hashIntegrity}
                return res
        elif int(value) == 0:
            rmo[z + colNumber] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
            return res
        
        else:
            rmo[z + colNumber] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            if status == True:
                res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'ok'}
                res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
                return res
            else:
                if int(value) == 0:
                    res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'ok'}
                else:
                    
                    res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'warning'}
                res = {'grid': rmo, 'status': 'warning', 'integrity': hashIntegrity}
                return res
                
    else:
        if rowNumber == 9:
            a = 99
        elif rowNumber == 10:
            a = 108
        elif rowNumber == 11:
            a = 117
        elif rowNumber == 12:
            a = 126
        elif rowNumber ==13:
            a = 135
        elif rowNumber ==14:
            a = 144
            
        c = colNumber - 6
        if rmo[a + c] < 0:
            res = {'status': 'error: Immutable Cell'}
            return res
        elif rmo[a + c] == int(value) and int(value) > 0:
            rmo[a + c] = 0
            stat = cellStatus(rmo, rowNumber, colNumber, value)
            rmo[a + c] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            if stat == True:
                res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
                return res
            else:
                res =  {'grid': rmo, 'status': 'warning', 'integrity': hashIntegrity}
                return res
        elif int(value) == 0:
            rmo[a + c] = value
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)
            res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
            return res
        
        else:
            rmo[a + c] = value  
            hashIntegrity = create.convertToCMO(rmo)
            hashIntegrity = create.hashCMO(hashIntegrity)
            hashIntegrity = create.getIntegrity(hashIntegrity)  
            if status == True:
                res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'ok'}
                res = {'grid': rmo, 'status': 'ok', 'integrity': hashIntegrity}
                return res
            else:
                if int(value) == 0:
                    res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'ok'}
                else:
                    
                    res = {'grid': rmo, 'integrity': hashIntegrity, 'status': 'warning'}
                res = {'grid': rmo, 'status': 'warning', 'integrity': hashIntegrity}
                return res
    return res
    
def cellStatus(rmo, rowNumber, colNumber, value):
    cmo = create.convertToCMO(rmo)
    if rowNumber < 6:
        for i in rmo[(rowNumber*9):((rowNumber+1)*9)]:
            if abs(i) == value:
                return False
    elif rowNumber > 5 and rowNumber < 9:
        if colNumber < 6:
            if rowNumber == 6:
                x = 54
                y = 63
            elif rowNumber == 7:
                x = 69
                y = 78
            elif rowNumber == 8:
                x = 84
                y = 93
        elif colNumber > 8:
            if rowNumber == 6:
                x = 60
                y = 69
            elif rowNumber == 7:
                x = 75
                y = 84
            elif rowNumber == 8:
                x = 90
                y = 99
        elif colNumber > 5 and colNumber < 9:
            if rowNumber == 6:
                x = 54
                y = 69
            elif rowNumber == 7:
                x = 69
                y = 84
            elif rowNumber == 8:
                x = 84
                y = 99
        for i in rmo[x:y]:
            if abs(i) == value:
                return False
    elif rowNumber > 8:
        if rowNumber == 9:
            x = 99
        elif rowNumber == 10:
            x = 108
        elif rowNumber == 11:
            x = 117
        elif rowNumber == 12:
            x = 126
        elif rowNumber == 13:
            x = 135
        elif rowNumber == 14:
            x = 144
        for i in rmo[x:(x+9)]:
            if abs(i) == value:
                return False
    
    if colNumber > 5 and colNumber < 9:
        if rowNumber < 6:
            if colNumber == 6:
                x = 54
                y = 63
            elif colNumber == 7:
                x = 69
                y = 78
            elif colNumber == 8:
                x = 84
                y = 93
        elif rowNumber > 8:
            if colNumber == 6:
                x = 60
                y = 69
            elif colNumber == 7:
                x = 75
                y = 84
            elif colNumber == 8:
                x = 90
                y = 99
        elif rowNumber > 5 and rowNumber < 9:
            if colNumber == 6:
                x = 54
                y = 69
            elif colNumber == 7:
                x = 69
                y = 84
            elif colNumber == 8:
                x = 84
                y = 99
        for i in cmo[x:y]:
            if abs(i) == value:
                return False
    elif colNumber > 8:
        if colNumber == 9:
            x = 99
        elif colNumber == 10:
            x = 108
        elif colNumber == 11:
            x = 117
        elif colNumber == 12:
            x = 126
        elif colNumber == 13:
            x = 135
        elif colNumber == 14:
            x = 144
        for i in cmo[x:(x+9)]:
            if abs(i) == value:
                return False
    elif colNumber < 6: 
        for i in cmo[(colNumber*9):((colNumber+1)*9)]:
            if abs(i) == value:
                return False
    
    if colNumber >= 0 and colNumber < 3: #column 0-2
        index = 0
    elif colNumber >= 3 and colNumber < 6: #column 3-5
        index = 3
    elif colNumber >= 6 and colNumber < 9: #column 6-8
        index = 6
    elif colNumber >= 9 and colNumber < 12: #column 9-11
        index = 9
    elif colNumber >= 12 and colNumber < 15: #column 12-14
        index = 12
        
    if rowNumber >= 0 and rowNumber < 3: #row 0-2
        list = []
        start = 0
        x = index
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 9
            x = index
        if value in list:
            return False
        
    elif rowNumber >= 3 and rowNumber < 6: #row 3-5
        list = []
        start = 27
        x = index
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 9
            x = index
        if value in list:
            return False
        
    elif rowNumber >= 6 and rowNumber < 9: #row 6-8
        list = []
        start = 54
        x = index
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 15
            x = index
        if value in list:
            return False
        
    elif rowNumber >= 9 and rowNumber < 12: #row 9-11
        list = []
        start = 99
        x = index - 6
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 9
            x = index - 6
        if value in list:
            return False
        
    elif rowNumber >= 12 and rowNumber < 15: #row 12-14
        list = []
        start = 126
        x = index - 6
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 9
            x = index - 6
        if value in list:
            return False
    
    return True
    
    
    
    
