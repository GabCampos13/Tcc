import os                                                                       
import multiprocessing as mp
import sys

def run_python(process):                                                             
        os.system("python {}".format(process))  
#431276483
#890437369
#1339160301
#1852053714
#2320328068
#2675702260
if __name__ == "__main__":
    pos = [0,171700,344463,517631]
    processes = ("tccParaleloArgs.py " + str(pos[0])+ "", "tccParaleloArgs.py " + str(pos[1])+ "","tccParaleloArgs.py " + str(pos[2])+ "","tccParaleloArgs.py " + str(pos[3])+ "")                      
    pool = mp.Pool(processes=4)                                                        
    pool.map(run_python, processes) 