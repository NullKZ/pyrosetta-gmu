import setup_modules as setup

def run(eaObj, cfg):
    setup.config(eaObj, cfg)
    #initializing the bh constant params
    initConfig = eaObj.cfg['init']     
    setup.bh(eaObj, initConfig)    
    setup.converter(eaObj)
    setup.population(eaObj, initConfig)
    setup.evaluation(eaObj, initConfig)
    #setting up the variation function
    varConfig = eaObj.cfg['variation']
    setup.variation(eaObj, varConfig)
    #setting up the improvement
    impConfig = eaObj.cfg['improvement']
    setup.improvement(eaObj, impConfig)
    #misc variables
    setup.misc(eaObj)
