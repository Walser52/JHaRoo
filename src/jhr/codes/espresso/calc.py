#from jhr.core import Calculation
#
#class QECalculation(Calculation):
#  def __init__():
#  
#    return
#
#  


import sys
sys.path.append("/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Cloned/_forked/pymatgen-io-espresso/pymatgen/io/espresso/outputs")

#from pymatgen.io.espresso.outputs import PWxml
from pwxml import PWxml
import pwxml


from pymatgen.entries.computed_entries import ComputedEntry

from pathlib import Path
import numpy as np

def get_element_formation_energy(elem, pseudo = 'pbe'):
    root = Path('/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/jhr/data/formation_energies')
    elem_file = root / elem / f"{elem}_{pseudo}.xml"

    comp_entry = PWxml(elem_file).get_computed_entry(entry_id = "")
    n_atoms = comp_entry.composition.as_data_dict()["unit_cell_composition"][elem]
    
    energy = comp_entry.energy
    
    en_per_atom = energy/n_atoms
    return en_per_atom
    

def fileread(func):
    def wrapper(cls, xml_file, *args, **kwargs):
        calc = PWxml(xml_file)
        struct = calc.get_computed_entry(entry_id = "")

        return func(cls, struct, *args, **kwargs)
    return wrapper
    



class QECalcTools:
    
    @classmethod
    @fileread
    def standardize_total_energy(cls, struct):
        print("STRUCT ENERGY: ", struct.energy)
        e_bulk = struct.energy
        composition = struct.composition
        
        comp_dict = composition.as_data_dict()['unit_cell_composition']
        
        elements = comp_dict.keys()
        n_i = np.array(list(comp_dict.values()))
        u_i = np.array([get_element_formation_energy(elem) for elem in elements])
        
        std_form_energy = (e_bulk - np.sum(n_i*u_i))/np.sum(n_i)

        return std_form_energy
    
    @classmethod
    #@fileread
    def standardized_computed_entry(cls, xml_file):
        """
        Return a computed entry with the standard formation enthalpy as total energy
        """
        print(xml_file, "\n")
        
        calc = PWxml(xml_file)
        struct = calc.get_computed_entry(entry_id = "")

        d_ = {
           "energy": cls.standardize_total_energy(xml_file),
           "composition": struct.composition,
           "entry_id": "",
           "correction": 0, #pristine_calc.get_computed_entry(entry_id = "").correction
        }
        
        ent = ComputedEntry.from_dict(d_) #Computed entries list. Why twice?

        return ent

