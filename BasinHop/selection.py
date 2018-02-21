import selection_modules as selection

def select(eaObj):
    selectionType = eaObj.cfg['selection']['type']
    if selectionType == 'opo':
        return selection.oneplusone(eaObj)
