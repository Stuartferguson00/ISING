import numpy as np
from matplotlib import pyplot as plt
import sys
import matplotlib
#matplotlib.use('TKAgg')
#matplotlib.use("module://backend_interagg")

def main(GLA_ALL = "GLA_ALL", KAW_ALL = "KAW_ALL"):
    GLA_ALL = np.loadtxt("G_results/"+GLA_ALL)
    #GLA_M_ALL = np.loadtxt("G_results/GLA_M_ALL")
    #GLA_E_ALL = np.loadtxt("G_results/GLA_E_ALL")

    GLA_T_arr = GLA_ALL[0]
    GLA_M_arr = GLA_ALL[1]
    GLA_E_arr = GLA_ALL[2]
    GLA_hc_arr = GLA_ALL[3]
    GLA_susc_arr = GLA_ALL[4]
    #hc_err_arr = GLA_ALL[5]



    KAW_ALL = np.loadtxt("G_results/"+KAW_ALL)
    #GLA_M_ALL = np.loadtxt("G_results/GLA_M_ALL")
    #GLA_E_ALL = np.loadtxt("G_results/GLA_E_ALL")

    KAW_T_arr = KAW_ALL[0]
    KAW_M_arr = KAW_ALL[1]
    KAW_E_arr = KAW_ALL[2]
    KAW_hc_arr = KAW_ALL[3]
    KAW_susc_arr = KAW_ALL[4]
    KAW_hc_err_arr = KAW_ALL[5]


    plt.title("Magnetisation against temperature")
    plt.ylabel("Magnetisation")
    plt.xlabel("Temperature")
    plt.plot(GLA_T_arr, GLA_M_arr, label = "Glauber")
    plt.plot(KAW_T_arr, KAW_M_arr, label = "Kawasaki")
    plt.legend()
    plt.show()





    plt.title("Total Energy against temperature")
    plt.ylabel("Total Energy")
    plt.xlabel("Temperature")
    plt.plot(GLA_T_arr, GLA_E_arr, label = "Glauber")
    plt.plot(KAW_T_arr, KAW_E_arr, label = "Kawasaki")
    plt.legend()
    plt.show()





    plt.title("Heat capacity against temperature")
    plt.ylabel("Heat Capacity")
    plt.xlabel("Temperature")
    plt.plot(GLA_T_arr, GLA_hc_arr, label = "Glauber")
    plt.plot(KAW_T_arr, KAW_hc_arr, label = "Kawasaki")
    plt.errorbar(KAW_T_arr, KAW_hc_arr, yerr = KAW_hc_err_arr)
    plt.legend()
    plt.show()




    plt.title("Susceptability against temperature")
    plt.ylabel("Susceptability")
    plt.xlabel("Temperature")
    plt.plot(GLA_T_arr, GLA_susc_arr, label = "Glauber")
    plt.plot(KAW_T_arr, KAW_susc_arr, label = "Kawasaki")
    plt.legend()
    plt.show()



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:   Glauber_data_filename   Kawasaki_data_filename")
        sys.exit(1)



    main(sys.argv[1],sys.argv[2])