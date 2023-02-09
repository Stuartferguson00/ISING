import numpy as np 
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
#%matplotlib inline
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation





    
    
class Lattice(object):

    def __init__(self, N, T, dynamics = "Glauber.py", lattice = None):
        
        self.N = N
        
        self.T = T
        self.beta = 1/self.T
        
        
        self.energies = []
        
        self.sweep_size = self.N**2
        
        if dynamics == "Glauber.py":
            self.dynamics = self.glauber
        elif dynamics == "Kawasaki":
            self.dynamics = self.kawasaki
        else:
            raise ValueError('The only options for dynamics are "Glauber.py" or "Kawasaki". Please input either of these')
        #print(type(lattice))
        
        if type(lattice) == np.ndarray:#'numpy.ndarray':
            if lattice.shape == (N,N):
                #print("yeye")
                self.lattice = lattice
            else:
                print("input lattice must be correct shape!!")
        
        elif lattice == "uniform":
            #assume uniform
            self.lattice = self.uniform_generate()
        elif lattice == "ground":
            self.lattice = self.ground_generate()
        elif lattice == "halved":
            self.lattice = self.halved_generate()
        else:
            print("your lattice input is wrong")
        #print(self.lattice)
            
        
        
       
    def halved_generate(self):

        a = np.hstack((np.ones((self.N**2)//2),np.ones((self.N**2)//2)*-1))
        if (self.N**2)%2 !=0:
            a = np.hstack((a,[1]))
        a = np.reshape(a, (self.N,self.N))
        return a

        
        

    def uniform_generate(self):
        #a = np.rint(np.random.uniform(0,1,(self.N,self.N))).astype(int)
        #a = np.where(a == 1,a,-1)
        a = np.random.choice((1,-1), size=[self.N,self.N], replace=True, p=[0.5,0.5])
        return a
    
    def ground_generate(self):
        #a = np.rint(np.random.uniform(0,1,(self.N,self.N))).astype(int)
        #a = np.where(a == 1,a,-1)
        a = np.ones((self.N,self.N))
        return a
    
    
    def glauber(self, find_M = False):
        flip_coords = self.rand_flip_coords()
        #flip_coords = [1,1]
        #print(flip_coords)
        #print(self.lattice[flip_coords[0],flip_coords[1]])
        #self.lattice = self.lattice[flip_coords[0],flip_coords[1]])
        #state of local system is :
        E_init = self.compute_E(flip_coords)
        
        #change in E is defined by -2*init_E (proven in my notes)
        delta_E = -2*E_init
        
        if delta_E<0:
            self.lattice[flip_coords[0],flip_coords[1]] = -1*self.lattice[flip_coords[0],flip_coords[1]]
        
        else:
            p = min(1,np.exp(-self.beta*delta_E))
            if np.random.uniform(0,1,1)<=p:
                self.lattice[flip_coords[0],flip_coords[1]] = -1*self.lattice[flip_coords[0],flip_coords[1]]
        """
        if find_M:
            self.find_magnetisation()
            self.find_magnetisation_squared()
        """
            
    
    
    
    def kawasaki(self):
        #get two different coordinates on grid
        #check not nearest neighbours
        coords_same = True
        while coords_same:
            flip_coords_1 = self.rand_flip_coords()
            flip_coords_2 = self.rand_flip_coords()
            if not np.array_equal(flip_coords_1,flip_coords_2):
                coords_same = False
                
        #if lattice values are identical
        if self.lattice[flip_coords_1[0],flip_coords_1[1]] == self.lattice[flip_coords_2[0],flip_coords_2[1]]:
            return
            
        
        #if nearest neighbours
        elif abs(np.sum(flip_coords_1-flip_coords_2)):
            #print("this loop is wronga nd you havent fixed it yet")
            
            E_init_1 = self.compute_E(flip_coords_1)
            E_init_2 = self.compute_E(flip_coords_2)
            delta_E = -1*(2*E_init_1+2*E_init_2-4)
            
        
        else:
            #not sure if there is a more efficient way to compute this....
            E_init_1 = self.compute_E(flip_coords_1)
            E_init_2 = self.compute_E(flip_coords_2)
            delta_E = -2*E_init_1 -2*E_init_2
            
            
        #if energy efficient, change
        if delta_E<0:
            self.lattice[flip_coords_1[0],flip_coords_1[1]] = -1*self.lattice[flip_coords_1[0],flip_coords_1[1]]
            self.lattice[flip_coords_2[0],flip_coords_2[1]] = -1*self.lattice[flip_coords_2[0],flip_coords_2[1]]
            return
        
        
        
        
        #if energy innefficient, change with probability related to temperature
        else:
            p = min(1,np.exp(-self.beta*delta_E))
            if np.random.uniform(0,1,1)<=p:
                self.lattice[flip_coords_1[0],flip_coords_1[1]] = -1*self.lattice[flip_coords_1[0],flip_coords_1[1]]
                self.lattice[flip_coords_2[0],flip_coords_2[1]] = -1*self.lattice[flip_coords_2[0],flip_coords_2[1]]
            return

        
        
        
    def find_magnetisation(self, return_val = False):
        #eqn21 notes
        M = np.sum(self.lattice)
        self.magnetisation.append(M)
        if return_val:
            return M
        
    """
    def find_magnetisation_squared(self, return_val = False):
        M_2 = np.sum(np.square(self.lattice/self.N**2))
        self.magnetisation_2.append(M_2)
        if return_val:
            return M_2
    """
        
        

        
    
        
    def spin(self):
        return np.sum(self.lattice)
        
        
    def rand_flip_coords(self):
        return np.random.randint(0,self.N,2)
    
    def compute_tot_E(self, return_val = False):
        E_list = []
        for i in range(self.N-1):
            for j in range(self.N-1):
                E_list.append(self.compute_E([i,j]))
        # sum energuies but divide by 2 to negate overcounting
        self.energies.append(np.sum(E_list)/2)       
        if return_val:
            return self.energies[-1]  
    
    
    def find_heat_capacity(self, energies = None):
        
        #ie if it is the full array of energies
        if energies is None:
            Es = self.energies
            
        #ie if it is a partial array of energies for bootstrap
        else:
            Es = energies
            
            
        #print(Es)
        #print(self.T)
        #print(self.N)
            
        #print(self.energies)
        hc = (1/(self.T**2*self.N**2)) *(np.mean(np.square(Es))-np.square(np.mean(Es)))
        return hc
        
        
    def susceptibility(self):

        susc = 1/(self.N**2*self.T) *(np.mean(np.square(self.magnetisation))-np.square(np.mean(self.magnetisation)))       
        
        return susc
    
    
    
    def jacknife_c(self):
        
        c = self.find_heat_capacity()
        
        #Es = self.energies
        
        sums = 0
        for i in range(len(self.energies)-1):
            Es = np.hstack((self.energies[:i],self.energies[i:-1]))
            #print(Es)
            c_i = self.find_heat_capacity(energies = Es)
            sums += (c_i - c)**2
        err = np.sqrt(sums)
        return err
        
    
    
    
    def compute_E(self,flip_coords):
        #assuming flip_coords = [1,1]
        #E = -S11 * (S01+S10,S21,S12)
        #use mod (%) for periodic boundary conditions
        return  -self.lattice[flip_coords[0],flip_coords[1]]*(self.lattice[flip_coords[0]-1,flip_coords[1]]+self.lattice[flip_coords[0],flip_coords[1]-1]+self.lattice[(flip_coords[0]+1)%self.N,flip_coords[1]]+self.lattice[flip_coords[0],(flip_coords[1]+1)%self.N])
    
    
    def plot_lattice(self): 

        #f=open('spins.dat','w')
        #for i in range(self.N):
        #    for j in range(self.N):
        #        f.write('%d %d %lf\n'%(i,j,self.lattice[i,j]))
        #f.close()
        print("hiii")
        plt.cla()
        plt.imshow(self.lattice, animated=True)
        #plt.show()
        plt.draw()
        plt.pause(0.1)
        
        
        
    def run(self,wait_sweeps = 100, num_tot_sweeps = 1000, plot_anim = True, find_M = False):
        if wait_sweeps>num_tot_sweeps:
            print("errorrrsss")
        #check inputs are compatable (with glauber or Kawasaki)
        
        
        
        
        
        if find_M:
            self.magnetisation = []
            self.magnetisation_2 = []
            self.sweep_list = []
        
        for i in range(num_tot_sweeps*self.sweep_size):
            #self.N**2 is the required length of time between visualisations as in the lecture notes
            if i%self.sweep_size == 0:
                #print(self.spin())
                if plot_anim:
                    self.plot_lattice()
                    
                if i%(self.sweep_size*10) == 0 and i > wait_sweeps*self.sweep_size:
                    if find_M:
                        self.sweep_list.append(i/self.sweep_size )
                        self.find_magnetisation()
                        #self.find_magnetisation_squared()
                        self.compute_tot_E()
                if i%(self.sweep_size*100) == 0:
                    print(i/self.sweep_size)
                    
            self.dynamics()

    
        
            
    def plot_M(self):
        plt.ylabel("Magnetisation")
        plt.xlabel("Sweep")
        plt.title("Magnetisation against sweep number for T:  "+ str(self.T) +"K")
        plt.plot(self.sweep_list, abs(self.magnetisation), label = str(self.T))
        plt.show()
        
    def plot_E(self):
        plt.ylabel("Energy")
        plt.xlabel("Sweep")
        plt.title("Energy against sweep number for T:  "+ str(self.T) +"K")
        plt.plot(self.sweep_list, self.energies, label = str(self.T))
        plt.show()
      
    """
    def plot_susc(self):
        susc = self.susceptibility()
        plt.ylabel("Susceptibility")
        plt.xlabel("sweep")
        plt.title("Susceptibility against sweep number for T:  "+ str(self.T) +"K")
        plt.plot(self.sweep_list, susc, label = str(self.T))
    """   

        
    def check_energy(self):
        flip_coords_1 = [1,2]
        flip_coords_2 = [1,1]
        
        
        if self.lattice[flip_coords_1[0],flip_coords_1[1]] != self.lattice[flip_coords_2[0],flip_coords_2[1]]:
            #print("yas")
            print("energy of two cells before:")
            #print(self.compute_E(flip_coords_1)+self.compute_E(flip_coords_2))
            
            E_init_1 = self.compute_E(flip_coords_1)
            E_init_2 = self.compute_E(flip_coords_2)

            print("initial_energies")
            print(E_init_1)
            print(E_init_2)

            
            delta_E_1 = -2*E_init_1
            delta_E_2 = -2*E_init_2
            print("initial changes in energy")
            print(delta_E_1)
            print(delta_E_2)
            
            
            print("possible fix")
            print(2*E_init_1+2*E_init_2-4)
            print(-(delta_E_1+delta_E_2)-4)
            print((E_init_1+4+E_init_2))
            

            self.lattice[flip_coords_1[0],flip_coords_1[1]] = -1*self.lattice[flip_coords_1[0],flip_coords_1[1]]
            self.lattice[flip_coords_2[0],flip_coords_2[1]] = -1*self.lattice[flip_coords_2[0],flip_coords_2[1]]
            
           
            E_init_1_ = self.compute_E(flip_coords_1)
            E_init_2_ = self.compute_E(flip_coords_2)
            
            
            delta_E_ = E_init_1+E_init_2 - (E_init_1_+E_init_2_)
            print("REAL CHANGE IN ENERGY")
            print(delta_E_)
        
            
