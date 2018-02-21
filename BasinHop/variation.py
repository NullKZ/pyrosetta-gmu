import variation_modules as variation

def perturb(eaObj, pose):
    if eaObj.cfg['variation']['fragReplacement'] == '1':
        variation.fragReplace(eaObj,pose)
