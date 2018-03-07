from time import time
def moea(eaObj):
    return eaObj.population

def truncate(eaObj, poses, tposes):
    merged_population = poses+tposes
    t0 = time()
    eaObj.PA.update_ranks(merged_population)
    eaObj.PA.update_counts(merged_population)
    print("R/C Updated in "+str(time()-t0))
    merged_population.sort(key=lambda x: eaObj.PA.ranks[x])
    return merged_population[:popsize]