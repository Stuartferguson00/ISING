import numpy as np
from matplotlib import pyplot as plt
import sys
import scipy

#matplotlib.use('TKAgg')
#matplotlib.use("module://backend_interagg")

def main(GLA_ALL = "GLA_ALL", KAW_ALL = "KAW_ALL"):
    """
        Function to graphically analyse the Glauber and Kawasaki dynamics Ising model simulation

        Uses results saved to files where each column is an ising lattice evaluated at a different temperature, and
        each row is as follows: T  M  E  c  Chi  c_err


        Parameters
        ----------

        GLA_ALL : filename
            filename for Glauber dynamics simulation
        KAW_ALL : filename
            filename for Kawasaki dynamics simulation


        Returns
        -------


        """









    GLA_ALL = np.loadtxt("G_results/"+GLA_ALL)
    #GLA_M_ALL = np.loadtxt("G_results/GLA_M_ALL")
    #GLA_E_ALL = np.loadtxt("G_results/GLA_E_ALL")

    GLA_T_arr = GLA_ALL[0]
    GLA_M_arr = abs(GLA_ALL[1])
    GLA_E_arr = GLA_ALL[2]
    GLA_hc_arr = GLA_ALL[3]
    GLA_susc_arr = GLA_ALL[4]
    #hc_err_arr = GLA_ALL[5]



    KAW_ALL = np.loadtxt("G_results/"+KAW_ALL)
    #GLA_M_ALL = np.loadtxt("G_results/GLA_M_ALL")
    #GLA_E_ALL = np.loadtxt("G_results/GLA_E_ALL")

    KAW_T_arr = KAW_ALL[0]
    KAW_M_arr = abs(KAW_ALL[1])
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

    def sigmoid_function(T, T_c, a, b, k):
        y = a / (1 + np.exp(-k * (T - T_c))) + b  # L / (1 + np.exp(-k*(x-x0))) + b
        return y

    p_0 = [0, -2500, 0, 0]
    x_ = np.arange(1, 3, 0.01)

    popt, pcov = scipy.optimize.curve_fit(sigmoid_function, GLA_T_arr, GLA_E_arr, p_0, method='dogbox')

    plt.plot(x_, sigmoid_function(x_, popt[0], popt[1], popt[2], popt[3]), color = "b", label = "Glauber sigmoid fit")
    plt.plot(GLA_T_arr, GLA_E_arr, marker = "x", linewidth = 0, color = "b", label = "Glauber im results")


    print("Critical temperature as estimated by Glauber energy: "+str(round(popt[0],2))+"+/-"+str(np.round(np.sqrt(np.diag(pcov))[0],3)))


    popt, pcov = scipy.optimize.curve_fit(sigmoid_function, KAW_T_arr, KAW_E_arr, p_0, method='dogbox')

    plt.plot(x_, sigmoid_function(x_, popt[0], popt[1], popt[2], popt[3]), color = "coral", label = "Kawasaki sigmoid fit")
    plt.plot(KAW_T_arr, KAW_E_arr, marker = "x", linewidth = 0, color = "coral", label = "Kawasaki results")

    print("Critical temperature as estimated by Kawasaki energy: "+str(round(popt[0],2))+"+/-"+str(np.round(np.sqrt(np.diag(pcov))[0],3)))
    plt.title("Total Energy against temperature")
    plt.ylabel("Total Energy")
    plt.xlabel("Temperature")
    plt.legend()
    plt.show()






    plt.title("Heat capacity against temperature")
    plt.ylabel("Heat Capacity")
    plt.xlabel("Temperature")
    plt.plot(GLA_T_arr, GLA_hc_arr, label = "Glauber")
    #plt.errorbar(GLA_T_arr, GLA_hc_arr, yerr=GLA_hc_err_arr, label="Glauber")
    #plt.plot(KAW_T_arr, KAW_hc_arr, label = "Kawasaki")
    plt.errorbar(KAW_T_arr, KAW_hc_arr, yerr = KAW_hc_err_arr, label = "Kawasaki")
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