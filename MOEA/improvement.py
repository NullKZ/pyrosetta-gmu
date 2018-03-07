import improvement_modules as improvement

def run(eaObj, pose):
    if eaObj.relaxtype == 'local':
        improvement.local(eaObj, pose)
    elif 'relax' in eaObj.relaxtype:
        improvement.relax(eaObj, pose)
