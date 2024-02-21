# Tutorial to running gas diffusivity simulations

Before you start, make sure PSP and PMD are installed.

## Equilibrating a pure polymer system

As an example, we first equilibrate a polystyrene (PS) system. Note that at the beginning the gas molecules are not added. Run:

```python
python mkinput.py
```

This should generate all the necessary files for running MD simulation. Simply run the LAMMPS simulation.

## Adding gas molecules to the equilibrated structure

Once the equilibration is done, we can add gas molecules to the structure. Run:

```python
python add_gas.py
```

Note that `add_gas.py` reads in all atom coordinates from the `equil.lammpstrj` LAMMPS trajectory file which should exist if you run the equilibration simulation successfully. `add_gas.py` also reads in force field functional forms from the `data.lmps` file which should exist as this is the original data file created by `mkinput.py`.

If you are done running `add_gas.py`, you should see 4 folders corresponding to 4 different gas types - CO2, CH4, N2, and O2. You can also specify what gas type to add in in the script. Note that the force field we use for gases is the [TraPPE united atom force field](http://trappe.oit.umn.edu/#small) which is compatible with GAFF2 force field we used for polymers.
