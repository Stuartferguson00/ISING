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
matplotlib.use("module://backend_interagg")

def run_full_kawisaki():
    #
    N = 10
    
    T_arr = np.arange(1,3.1,0.3)
    #T_arr = [2.2, 2.25, 2.3]
    #T_arr = [1,2,2.26]
    wait_sweeps = 100
    num_tot_sweeps = 1000
    
    #T_arr = [1,3]
    #susc_list = []
    #hc_list = []
    #M_list = []
    #E_list = []
    lattices = []
    for count, T in enumerate(T_arr):
        start = time.time()
        
        if T == 1:
            L = Lattice(N,T, dynamics = "Kawasaki", lattice = "halved")#np.ones((N,N)))
        else:
            if count !=0:
                L = Lattice(N,T, dynamics = "Kawasaki", lattice = lattices[-1].lattice)#np.ones((N,N)))
            else:
                L = Lattice(N,T, dynamics = "Kawasaki", lattice = "uniform")#np.ones((N,N)))
        L.run(wait_sweeps = wait_sweeps , num_tot_sweeps = num_tot_sweeps , plot_anim = False, find_M = True)
        

        

        
        
        

        
        
        
        #L.plot_M()
        #L.plot_E()
        lattices.append(L)
        
        #M_list.append(np.mean(L.magnetisation))
        #E_list.append(np.mean(E.magnetisation))
        #hc_list.append(L.find_heat_capacity())
        #susc_list.append(L.susceptibility())
        
        #L = Lattice(50,T, dynamics = "Kawasaki")

        #L.run(wait_sweeps = 0, num_tot_sweeps = 100, plot_anim = True, find_M = False)
        

        end = time.time()
        print("time taken for one T: "+ str(start-end))
        
    #save to file iteritively not like this
    #np.savetxt("G_results/G_E_all",[np.mean(L.energies)])#, delimiter = ",")
    #np.savetxt("G_results/G_M_all",[np.mean(L.magnetisation)])#, delimiter = ",")
    #np.savetxt("G_results/G_S_all",[L.susceptibility()])#, delimiter = ",")
    #np.savetxt("G_results/G_HC_all", [L.find_heat_capacity()])#, delimiter = ",")

    
    
    
    
    
    
    
    susc_list = []
    hc_list = []
    M_list = []
    E_list = []
    M_all_list = []
    E_all_list = []
    
    #susc_err_list = []
    hc_err_list = []

        
    for L in lattices:
        M_list.append(np.mean(L.magnetisation))
        E_list.append(np.mean(L.energies))
        hc_list.append(L.find_heat_capacity())
        hc_err_list.append(L.jacknife_c())
        M_all_list.append(L.magnetisation)
        E_all_list.append(L.energies)
        susc_list.append(L.susceptibility())
    
    
    np.savetxt("G_results/KAW_ALL",np.vstack((T_arr,M_list,E_list,hc_list,susc_list)))#, delimiter = ",")
    np.savetxt("G_results/KAW_M_ALL",M_all_list)#, delimiter = ",")
    np.savetxt("G_results/KAW_E_ALL",E_all_list)#, delimiter = ",")
    
    
        
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
    return lattices
  
 
 
 
 
 
 
 
lattice_list = run_full_kawisaki()