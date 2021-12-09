import dodoku.create as create
import dodoku.insert as insert
import dodoku.status as status
import dodoku.solve as solve
import dodoku.info as info
import dodoku.recommend as recommend

ERROR01 = 'error: no op is specified'
ERROR02 = 'error: parameter is not a dictionary'
ERROR03 = 'error: op is not legal'
STATUS = 'status'
OP = 'op'
OPS = {
    'create' : create._create,
    'insert' : insert._insert,
    'status' : status._status,
    'recommend' : recommend._recommend,
    'solve' : solve._solve,
    'info' : info._info,
    }

def _dispatch(parms = None):

    result = {}
    
    # Validate parm
    if(parms == None):
        result = {STATUS: ERROR01}
    elif(not(isinstance(parms, dict))):
        result = {STATUS: ERROR02}
    elif (not(OP in parms)):
        result = {STATUS: ERROR01}
    elif(not(parms[OP] in OPS)):
        result[STATUS] = ERROR03
    else:
        result = OPS[parms[OP]](parms)
    return result
