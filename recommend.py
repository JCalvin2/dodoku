import dodoku.insert as insert
import dodoku.create as create

def _recommend(parms):
    for i in parms.keys():
        if (i == 'op') or (i == 'cell') or (i == 'grid') or (i == 'integrity'):
            pass
        else:
            result = {'status':'error: Invalid Key'}
            return result
        
    if ('cell' not in parms.keys()) or ('grid' not in parms.keys()) or ('integrity' not in parms.keys()):
        result = {'status': 'error: Missing Key(s)'}
        return result
    
    vc = insert.validateCell(parms['cell'])
    if vc != {'status': 'ok'}:
        return vc
    else:
        pass
    
    vg = insert.validateGrid(parms['grid'])
    if vg != {'status': 'ok'}:
        return vg
    else:
        pass
        
    vi = insert.validateIntegrity(parms)
    if vi != {'status': 'ok'}:
        return vi
    else:
        pass

    result = getHints(parms)
    
    return result

def getHints(x):
    rmo = create.convertToArray(x['grid'])
    
    x = x['cell']
    for i in range(len(x)):
        if x[i] == 'c' or x[i] == 'C':
            row = x[:i]
            col = x[i:]
    
    rowNumber = int(row[1:]) - 1
    colNumber = int(col[1:]) - 1
    
    res = {}
    
    if rowNumber < 6:
        if rmo[(rowNumber * 9) + colNumber] < 0:
            res = {'recommend': [], 'status': 'ok'}
            return res
        elif rmo[(rowNumber * 9) + colNumber] > 0:
            rmo[(rowNumber * 9) + colNumber] = 0
    
    elif rowNumber > 5 and rowNumber < 9:
        if rowNumber == 6:
            z = 54
        elif rowNumber == 7:
            z = 69
        elif rowNumber == 8:
            z = 84
            
        if rmo[z + colNumber] < 0:
            res = {'recommend': [], 'status': 'ok'}
            return res
        elif rmo[z + colNumber] > 0:
            rmo[z + colNumber] = 0
    
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
            res = {'recommend': [], 'status': 'ok'}
            return res
        elif rmo[a + c] > 0:
            rmo[a + c] = 0
        
    res = statusCheck(rmo, rowNumber, colNumber)
    
    return {'recommend': res, 'status':'ok'}
        
def statusCheck(rmo, rowNumber, colNumber):
    cmo = create.convertToCMO(rmo)
    rowCheck = []
    colCheck = []
    subGridCheck = []
    
    if rowNumber < 6:
        for i in rmo[(rowNumber*9):((rowNumber+1)*9)]:
            rowCheck.append(abs(i))

    elif rowNumber > 5 and rowNumber < 9:
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
            rowCheck.append(abs(i))
            
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
            rowCheck.append(abs(i))
    
    if colNumber > 5 and colNumber < 9:
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
            colCheck.append(abs(i))
            
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
            colCheck.append(abs(i))
                            
    elif colNumber < 6: 
        for i in cmo[(colNumber*9):((colNumber+1)*9)]:
            colCheck.append(abs(i))
    
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
        subGridCheck = list
        
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
        subGridCheck = list
        
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
        subGridCheck = list
        
    elif rowNumber >= 9 and rowNumber < 12: #row 9-11
        list = []
        start = 99
        x = index
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 9
            x = index - 6
        subGridCheck = list
        
    elif rowNumber >= 12 and rowNumber < 15: #row 12-14
        list = []
        start = 126
        x = index
        for a in range(3):
            for i in range(3):
                list.append(abs(rmo[start+x]))
                x = x + 1
            start = start + 9
            x = index - 6
        subGridCheck = list
    
    result = []
    
    
    
    for i in range(1,10):
        if i not in rowCheck and i not in colCheck and i not in subGridCheck:
            if i != 0:
                result.append(i)
                                
    return result

