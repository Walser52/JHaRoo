#!/usr/bin/python3.4
#Created by Levi Lentz
#Covered under the MIT license
import sys
import numpy as np
import json
class Struct:
  """
  From: https://blog.levilentz.com/parse-quantum-espresso-output-file/

  Takes a pw.x output file and reads all the relevant values. 
  
  Example: 
    test = Struct()
    test.Process("vc.out")
   
    print(test.to_JSON())


  """


  def __init__(self):
    self.BOHRtoA = 0.529177249
    self.RYtoeV = 13.605698066
    self.program_version = ""
    self.volume = 0.0
    self.alat = 0.0
    self.natoms = 0
    self.nat = 0
    self.nelect = 0
    self.Ecut = 0.0
    self.RhoCut = 0.0
    self.Econv = 0.0
    self.beta = 0.0
    self.Exch = ""
    self.energy = 0.0
    self.natoms = 0
    self.bandgap = 0.0
    self.bands = 0
    self.lattice = {'a':np.zeros(3),'b':np.zeros(3),'c':np.zeros(3)}
    self.atoms = []
    self.norms = {'a':0.0,'b':0.0,'c':0.0}
    self.angles = {'alpha':0.0,'beta':0.0,'gamma':0.0}
    self.kpts = 0
    self.bnddiagram = np.zeros(0)
    self.FermiTest = False
    self.Fermi = 0.0
  def Process(self,filestring):
    f = open(filestring,'r')
    linenum = 0
    for i in f:
      if linenum < 1000:
        if "number of k points=" in i:
          self.kpts = int(i.split()[4])
          next
        if "Program PWSCF" in i:
          self.program_version = i.split()[2]
          next
        if "lattice parameter (alat)" in i:
          self.alat = float(i.split()[4])*self.BOHRtoA
          next
        if "number of Kohn-Sham states" in i:
          self.bands = int(i.split()[4]) 
        if "unit-cell volume" in i and "new" not in i:
          self.volume = float(i.split()[3])*(self.BOHRtoA**3.0)
          next
        if "number of atoms/cell" in i:
          self.natoms = int(i.split()[4])
          next
        if "number of atomic types" in i:
          self.nat = int(i.split()[5])
          next
        if "number of electrons" in i:
          self.nelect = float(i.split()[4])
          next
        if "kinetic-energy cutoff" in i:
          self.Ecut = float(i.split()[3])*self.RYtoeV
          next
        if "charge density cutoff" in i:
          self.RhoCut = float(i.split()[4])*self.RYtoeV
          next
        if "convergence threshold" in i:
          self.Econv = float(i.split()[3])
          next
        if "mixing beta" in i:
          self.beta = float(i.split()[3])
          next
        if "Exchange-correlation" in i:
          self.Exch = i.split()[2]
          next
        if "a(1) =" in i:
          tmp = i.split()
          for j in range(0,3):
            self.lattice['a'][j] = tmp[j+3]
          next
        if "a(2) =" in i:
          tmp = i.split()
          for j in range(0,3):
            self.lattice['b'][j] = tmp[j+3]
          next
        if "a(3) =" in i:
          tmp = i.split()
          for j in range(0,3):
            self.lattice['c'][j] = tmp[j+3] 
          next
        if "site n.     atom                  positions (alat units)" in i:
          for j in range(0,self.natoms):
            line = next(f).split()
            self.atoms.append([line[1],float(line[6])*self.alat,float(line[7])*self.alat,float(line[8])*self.alat])
          next
      if "!" in i:
        self.energy= float(i.split()[4])*self.RYtoeV
      if "new unit-cell volume" in i:
        self.volume = float(i.split()[4])*(self.BOHRtoA**3)
      if "Begin final coordinates" in i:
        #print(self.atoms)
        while "End final coordinates" not in line:
          line = next(f)
          if "CELL_PARAMETERS" in line:
            self.alat = float(line.replace(')','').split()[2])*self.BOHRtoA
            for j in ['a','b','c']:
              line = next(f)
              tmp = line.split()
              for k in range(0,3):
                self.lattice[j][k] = self.alat*float(tmp[k])
          if "ATOMIC_POSITIONS" in line:
            if "angstrom" in line:
              for j in range(0,self.natoms):
                line = next(f).split()
                self.atoms[j] = [line[0],float(line[1]),float(line[2]),float(line[3])]
      if "End of self-consistent calculation" in i: #The band diagram is stored in lines of 8 entries
        if np.floor(self.bands/8.)*8. <= self.bands:
          numlines = int(np.floor(self.bands/8.) + 1)
          remainder = int(self.bands - np.floor(self.bands/8.)*8.)
        else: 
          numlines = int(np.floor(self.bands/8.))
          remainder = 0
        self.bnddiagram = np.zeros((self.kpts,self.bands))
        counter = 0
        while counter < self.kpts:
          line = next(f)
          if "k =" in line:
            line = next(f)
            counter1 = 0
            for j in range(0,numlines):
              line = next(f)
              for k in range(0,len(line.split())):
                self.bnddiagram[counter][counter1 + k] = float(line.split()[k])
              counter1 += 8
            counter += 1 
        next
      if "highest occupied, lowest unoccupied level (ev)" in i:
        self.bandgap = float(i.split()[7]) - float(i.split()[6])
        next
      if "the Fermi energy is" in i:
        self.Fermi = float(i.split()[4])
        self.FermiTest = True
        next
      linenum += 1
    f.close()
    for i in ['a','b','c']:
      self.norms[i] = np.linalg.norm(self.lattice[i])
    self.angles['alpha'] = np.arccos(np.dot(self.lattice['b'],self.lattice['c'])/(self.norms['c']*self.norms['b'])) * 180./np.pi
    self.angles['gamma'] = np.arccos(np.dot(self.lattice['a'],self.lattice['b'])/(self.norms['a']*self.norms['b'])) * 180./np.pi
    self.angles['beta'] = np.arccos(np.dot(self.lattice['a'],self.lattice['c'])/(self.norms['a']*self.norms['c'])) * 180./np.pi
    if self.FermiTest == True: #The bandgap is now in the band diagram
      self.bnddiagram = np.subtract(self.bnddiagram,self.Fermi)
      emin = np.zeros(self.kpts)
      emax = np.zeros(self.kpts)
      counter = 0
      for j in self.bnddiagram:
        emin[counter] = j[np.searchsorted(j,  0.0,side='right')-1]
        emax[counter] = j[np.searchsorted(j,  0.0,side='right')]
        counter += 1
      self.bandgap = float(np.min(emax-emin))

  def to_JSON(self):
  """
  Convert to JSON
  """
    for i in self.lattice:
      self.lattice[i] = self.lattice[i].tolist() 
    self.bnddiagram = self.bnddiagram.tolist() #JSON doesnt like numpy arrays
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
 
#test = Struct()
#test.Process("vc.out")
# 
#print(test.to_JSON())
