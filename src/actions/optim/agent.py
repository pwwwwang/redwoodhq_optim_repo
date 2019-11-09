# OPTIM Agent Simulator 

import os,time
class agent:
    def report(self,params):
        repeat=params['repeat']
        para=params['para']
        sn=os.getenv('sn')
        print sn
        if para:
            cmd="python C:\Users\AgentSimulator.py -S %s -m single -r %s -p %s"%(sn,repeat,para)
        else:
            cmd="python C:\Users\AgentSimulator.py -S %s -m single -r %s"%(sn,repeat)
        print cmd
        rc=os.system(cmd)
        print rc
        time.sleep(60)