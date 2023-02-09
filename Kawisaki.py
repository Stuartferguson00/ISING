import time
import numpy as np 
from matplotlib import pyplot as plt
import matplotlib
#matplotlib.use('TKAgg')
#%matplotlib inline
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Lattice import Lattice
#matplotlib.use("module://backend_interagg")


def main(T_low, N = 50, num_sweeps = 1000, plot_anim = False, T_high = None, stepsize = None):

    if T_high is not None and stepsize is not None:
        print("helloo")
        T_arr = np.arange(T_low, T_high, stepsize)

    if T_high is None or stepsize is None:
        print("hiiiii")
        T_arr = np.asarray([int(T_low)])

    print(T_arr)



    wait_sweeps = 100

    if wait_sweeps >= num_sweeps:
        wait_sweeps = num_sweeps//10
    

    lattices = []
    for count, T in enumerate(T_arr):
        start = time.time()
        print(T)
        if T == 1:
            L = Lattice(N,T, dynamics = "Kawasaki", lattice = "halved")#np.ones((N,N)))
        else:
            if count !=0:
                L = Lattice(N,T, dynamics = "Kawasaki", lattice = lattices[-1].lattice)#np.ones((N,N)))
            else:
                L = Lattice(N,T, dynamics = "Kawasaki", lattice = "uniform")#np.ones((N,N)))
        L.run(wait_sweeps = wait_sweeps , num_tot_sweeps = num_sweeps , plot_anim = False, find_M = True)
        

        

        lattices.append(L)
        


        end = time.time()
        print("time taken for one T: "+ str(start-end))
        

    
    
    
    susc_list = []
    hc_list = []
    M_list = []
    E_list = []
    M_all_list = []
    E_all_list = []
    hc_err_list = []

        
    for L in lattices:
        M_list.append(np.mean(L.magnetisation))
        E_list.append(np.mean(L.energies))
        hc_list.append(L.find_heat_capacity())
        hc_err_list.append(L.jacknife_c())
        M_all_list.append(L.magnetisation)
        E_all_list.append(L.energies)
        susc_list.append(L.susceptibility())
    
    
    np.savetxt("G_results/KAW_ALL",np.vstack((T_arr,M_list,E_list,hc_list,susc_list, hc_err_list)))#, delimiter = ",")
    #np.savetxt("G_results/KAW_M_ALL",M_all_list)#, delimiter = ",")
    #np.savetxt("G_results/KAW_E_ALL",E_all_list)#, delimiter = ",")
    
    
    """
    plt.title("Magnetisation")
    plt.ylabel("Magnetisation")
    plt.xlabel("Sweeps")
    for L in lattices:
        plt.plot(L.sweep_list,abs(np.array(L.magnetisation)), label = L.T)
    plt.legend()
    plt.show()
    
    
    
    
    plt.title("Total energy")
    plt.ylabel("Energy")
    plt.xlabel("Sweeps")
    for L in lattices:
        plt.plot(L.sweep_list,L.energies, label = L.T)
    plt.legend()
    plt.show()
    """
        
        
        
        
        

    """
    plt.show()
    plt.title("Magnetisation against temperature for Kawisaki")
    plt.ylabel("Magnetisation")
    plt.xlabel("Temperature")
    plt.plot(T_arr, M_list)
    plt.show()
    
    
    
    
    
    plt.title("Total Energy against temperature for Kawisaki")
    plt.ylabel("Total Energy")
    plt.xlabel("Temperature")
    plt.plot(T_arr, E_list)
    plt.show()
    
    
    
    
    
    
    plt.title("Heat capacity against temperature for Kawisaki")
    plt.ylabel("Heat Capacity")
    plt.xlabel("Temperature")
    #plt.plot(T_arr, hc_list)
    plt.errorbar(T_arr, hc_list,yerr = hc_err_list)
    plt.show()
    
    

    
    plt.title("Susceptability against temperature for Kawisaki")
    plt.ylabel("Susceptability")
    plt.xlabel("Temperature")
    plt.plot(T_arr, susc_list)
    plt.show()
    
    
    
    
    plt.title("")
    plt.ylabel("")
    plt.xlabel("")
    
    #print(susc_list)
    #print(hc_list)
    """
    return
  
 
 
 
 
 
 
 




if __name__ == "__main__":

    #if incorrect umbe rof arguments are given, state what arguments are expected for which process
    if len(sys.argv) != 7 and len(sys.argv) != 5:
        print(len(sys.argv))
        print("Usage for a single T: \n T, N, num_sweeps, plot_anim")
        print("Usage for a range of T: \n T_low, N, num_sweeps, plot_anim, T_high, stepsize")
        sys.exit(1)

    #if only one Temperature is to be evaluated
    elif len(sys.argv) == 5:
        main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), eval(sys.argv[4]))
    #if a range of temperatures re to be evaluated
    elif len(sys.argv) == 7:
        main(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), eval(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

