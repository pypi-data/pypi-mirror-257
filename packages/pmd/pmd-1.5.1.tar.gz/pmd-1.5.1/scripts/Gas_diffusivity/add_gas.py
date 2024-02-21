'''
Python script to add gas molecules into equilibrated
MD simulations of amorphous polymer systems
'''

import os
import random

import numpy as np


def read_data(data_file):

    def read_data_header(data_file, dict):
        f = open(data_file)
        lines = f.readlines()
        dict['natoms'] = int(lines[2].split()[0])
        dict['nbonds'] = int(lines[3].split()[0])
        dict['nangles'] = int(lines[4].split()[0])
        dict['ndihedrals'] = int(lines[5].split()[0])
        dict['nimpropers'] = int(lines[6].split()[0])

        parts = lines[8].split()
        if (len(parts) >= 2 and parts[1] == 'atom'):
            dict['natom_types'] = int(parts[0])

        parts = lines[9].split()
        if (len(parts) >= 2 and parts[1] == 'bond'):
            dict['nbond_types'] = int(parts[0])

        parts = lines[10].split()
        if (len(parts) >= 2 and parts[1] == 'angle'):
            dict['nangle_types'] = int(parts[0])

        parts = lines[11].split()
        if (len(parts) >= 2 and parts[1] == 'dihedral'):
            dict['ndihedral_types'] = int(parts[0])

        parts = lines[12].split()
        if (len(parts) >= 2 and parts[1] == 'improper'):
            dict['nimproper_types'] = int(parts[0])
        return dict

    def read_data_main(data_file, dict):
        current_section = None
        with open(data_file, 'rt') as f:
            for line in f:
                if any(x in line for x in dict.keys()):
                    current_section = line.strip()
                elif line == '\n' or not current_section:
                    continue
                else:
                    section_list = dict.get(current_section,
                                            'Invalid current section')
                    section_list.append(line.split())
        return dict

    # this switcher dict is to navigate through and store info for the header
    # part of a LAMMPS data file
    dict_stats = {
        'natoms': 0,
        'nbonds': 0,
        'nangles': 0,
        'ndihedrals': 0,
        'nimpropers': 0,
        'natom_types': 0,
        'nbond_types': 0,
        'nangle_types': 0,
        'ndihedral_types': 0,
        'nimproper_types': 0,
    }
    dict_stats = read_data_header(data_file, dict_stats)

    # this switcher dict is to navigate through and store info for each
    # section of a LAMMPS data file
    dict_main = {
        'Masses': [],
        'Pair Coeffs': [],
        'Bond Coeffs': [],
        'Angle Coeffs': [],
        'Dihedral Coeffs': [],
        'Improper Coeffs': [],
        'Atoms': [],
        'Bonds': [],
        'Angles': [],
        'Dihedrals': [],
        'Impropers': [],
    }
    dict_main = read_data_main(data_file, dict_main)
    return dict_stats, dict_main


def read_lammstrj(lammpstrj_file, nframes):
    with open(lammpstrj_file, 'rt') as f:
        # skip initial nframes-1 frames
        for i in range(nframes - 1):
            f.readline()
            line = f.readline()  # time step
            fields = line.split()
            step = int(fields[0])
            print('skipping frame {}'.format(step))
            f.readline()
            if i == 0:
                # read number of atoms from first configuration (assuming
                # number of atoms is fixed)
                line = f.readline()
                fields = line.split()
                natoms = int(fields[0])
            else:
                f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            for j in range(natoms):
                f.readline()

        # initialize 2D array of x, y, z coordinates, r[id][coordinate]
        r = np.zeros([natoms + 1, 3], float)
        box = np.zeros(3, float)

        f.readline()
        line = f.readline()  # time step
        fields = line.split()
        step = int(fields[0])
        print('reading atom coordinates from frame {}'.format(step))
        f.readline()
        f.readline()
        f.readline()
        line = f.readline()
        [xm, xp] = map(np.float, line.split())
        line = f.readline()
        [ym, yp] = map(np.float, line.split())
        line = f.readline()
        [zm, zp] = map(np.float, line.split())
        f.readline()
        box[0] = xp - xm
        box[1] = yp - ym
        box[2] = zp - zm
        for j in range(natoms):
            line = f.readline()
            [i, mol, typea, q, xs, ys, zs, ix, iy, iz] = line.split()
            id = int(i)
            r[id][0] = box[0] * np.float(xs) + int(ix) * box[0]
            r[id][1] = box[1] * np.float(ys) + int(iy) * box[1]
            r[id][2] = box[2] * np.float(zs) + int(iz) * box[2]

    return r, box


def build_gas_template(gas):
    dict_gas_stats = {
        'natoms': 0,
        'nbonds': 0,
        'nangles': 0,
        'ndihedrals': 0,
        'nimpropers': 0,
        'natom_types': 0,
        'nbond_types': 0,
        'nangle_types': 0,
        'ndihedral_types': 0,
        'nimproper_types': 0,
    }

    dict_gas_main = {
        'Masses': [],
        'Pair Coeffs': [],
        'Bond Coeffs': [],
        'Angle Coeffs': [],
        'Dihedral Coeffs': [],
        'Improper Coeffs': [],
        'Atoms': [],
        'Bonds': [],
        'Angles': [],
        'Dihedrals': [],
        'Impropers': [],
    }

    if gas == 'CH4':
        dict_gas_stats['natoms'] = 1
        dict_gas_stats['natom_types'] = 1
        dict_gas_main['Masses'] = [['1', '16.04', '# TraPPE CH4']]
        dict_gas_main['Pair Coeffs'] = [[
            '1', '0.294106636', '3.73', '# TraPPE CH4'
        ]]
        dict_gas_main['Atoms'] = [['1', '1', '1', '0.0', '0.0', '0.0', '0.0']]

    elif gas == 'CO2':
        dict_gas_stats['natoms'] = 3
        dict_gas_stats['nbonds'] = 2
        dict_gas_stats['nangles'] = 1
        dict_gas_stats['natom_types'] = 2
        dict_gas_stats['nbond_types'] = 1
        dict_gas_stats['nangle_types'] = 1
        dict_gas_main['Masses'] = [['1', '12.0107', '# TraPPE C in CO2'],
                                   ['2', '15.9994', '# TraPPE O in CO2']]
        dict_gas_main['Pair Coeffs'] = [[
            '1', '0.053649', '2.8', '# TraPPE C in CO2'
        ], ['2', '0.156973', '3.05', '# TraPPE O in CO2']]
        dict_gas_main['Bond Coeffs'] = [['1', '0', '1.16', '# TraPPE CO2']]
        dict_gas_main['Angle Coeffs'] = [['1', '0', '180', '# TraPPE CO2']]
        dict_gas_main['Atoms'] = [
            ['1', '1', '1', '0.7', '0.0', '0.0', '0.0'],
            ['2', '1', '2', '-0.35', '-1.16', '0.0', '0.0'],
            ['3', '1', '2', '-0.35', '1.16', '0.0', '0.0']
        ]
        dict_gas_main['Bonds'] = [['1', '1', '1', '2'], ['2', '1', '1', '3']]
        dict_gas_main['Angles'] = [['1', '1', '2', '1', '3']]

    elif gas == 'O2':
        dict_gas_stats['natoms'] = 3
        dict_gas_stats['nbonds'] = 2
        dict_gas_stats['nangles'] = 1
        dict_gas_stats['natom_types'] = 2
        dict_gas_stats['nbond_types'] = 1
        dict_gas_stats['nangle_types'] = 1
        dict_gas_main['Masses'] = [['1', '15.9994', '# TraPPE O in O2'],
                                   ['2', '0.00001', '# TraPPE M in O2']]
        dict_gas_main['Pair Coeffs'] = [[
            '1', '0.097363', '3.02', '# TraPPE O in O2'
        ], ['2', '0.0', '0.0', '# TraPPE M in O2']]
        dict_gas_main['Bond Coeffs'] = [['1', '0', '0.605', '# TraPPE O2']]
        dict_gas_main['Angle Coeffs'] = [['1', '0', '180', '# TraPPE O2']]
        dict_gas_main['Atoms'] = [[
            '1', '1', '2', '0.226', '0.0', '0.0', '0.0'
        ], ['2', '1', '1', '-0.113', '-0.605', '0.0',
            '0.0'], ['3', '1', '1', '-0.113', '0.605', '0.0', '0.0']]
        dict_gas_main['Bonds'] = [['1', '1', '1', '2'], ['2', '1', '1', '3']]
        dict_gas_main['Angles'] = [['1', '1', '2', '1', '3']]

    elif gas == 'N2':
        dict_gas_stats['natoms'] = 3
        dict_gas_stats['nbonds'] = 2
        dict_gas_stats['nangles'] = 1
        dict_gas_stats['natom_types'] = 2
        dict_gas_stats['nbond_types'] = 1
        dict_gas_stats['nangle_types'] = 1
        dict_gas_main['Masses'] = [['1', '14.005', '# TraPPE N in N2'],
                                   ['2', '0.00001', '# TraPPE M in N2']]
        dict_gas_main['Pair Coeffs'] = [[
            '1', '0.071532', '3.31', '# TraPPE O in N2'
        ], ['2', '0.0', '0.0', '# TraPPE M in N2']]
        dict_gas_main['Bond Coeffs'] = [['1', '0', '0.55', '# TraPPE N2']]
        dict_gas_main['Angle Coeffs'] = [['1', '0', '180', '# TraPPE N2']]
        dict_gas_main['Atoms'] = [[
            '1', '1', '2', '0.964', '0.0', '0.0', '0.0'
        ], ['2', '1', '1', '-0.482', '-0.55', '0.0',
            '0.0'], ['3', '1', '1', '-0.482', '0.55', '0.0', '0.0']]
        dict_gas_main['Bonds'] = [['1', '1', '1', '2'], ['2', '1', '1', '3']]
        dict_gas_main['Angles'] = [['1', '1', '2', '1', '3']]

    else:
        print(
            'Unrecognized gas type; gas molecule has to be CH4, CO2, O2, or N2.'
        )
    return dict_gas_stats, dict_gas_main


def write_new_input(output_file, dict_stats, dict_main, r, box, dict_gas_stats,
                    dict_gas_main, gas, Ngas):

    def get_random_position(box):
        return random.random() * box[0], random.random(
        ) * box[1], random.random() * box[2]

    with open(output_file, 'wt') as f:
        # header section
        f.write(
            'LAMMPS amorphous polymer system with {} {} gas molecules inserted\n'
            .format(Ngas, gas))
        f.write('\n')
        f.write('{:>12}  atoms\n'.format(dict_stats['natoms'] +
                                         (dict_gas_stats['natoms'] * Ngas)))
        f.write('{:>12}  bonds\n'.format(dict_stats['nbonds'] +
                                         (dict_gas_stats['nbonds'] * Ngas)))
        f.write('{:>12}  angles\n'.format(dict_stats['nangles'] +
                                          (dict_gas_stats['nangles'] * Ngas)))
        f.write('{:>12}  dihedrals\n'.format(dict_stats['ndihedrals'] +
                                             (dict_gas_stats['ndihedrals'] *
                                              Ngas)))
        f.write('{:>12}  impropers\n'.format(dict_stats['nimpropers'] +
                                             (dict_gas_stats['nimpropers'] *
                                              Ngas)))
        f.write('\n')
        f.write('{:>12}  atom types\n'.format(dict_stats['natom_types'] +
                                              (dict_gas_stats['natom_types'])))
        f.write('{:>12}  bond types\n'.format(dict_stats['nbond_types'] +
                                              (dict_gas_stats['nbond_types'])))
        f.write(
            '{:>12}  angle types\n'.format(dict_stats['nangle_types'] +
                                           (dict_gas_stats['nangle_types'])))
        f.write('{:>12}  dihedral types\n'.format(
            dict_stats['ndihedral_types'] +
            (dict_gas_stats['ndihedral_types'])))
        f.write('{:>12}  improper types\n'.format(
            dict_stats['nimproper_types'] +
            (dict_gas_stats['nimproper_types'])))
        f.write('\n')
        f.write('{:>12}  {:>12} xlo xhi\n'.format(0, box[0]))
        f.write('{:>12}  {:>12} ylo yhi\n'.format(0, box[1]))
        f.write('{:>12}  {:>12} zlo zhi\n'.format(0, box[2]))
        f.write('\n')

        for index, (key, value) in enumerate(dict_gas_main.items()):
            # Header and Coeff sections
            if index <= 5 and (value or dict_main.get(key)):
                f.write('{}\n'.format(key))
                f.write('\n')
                for fields in value:
                    atom_type = int(fields[0])
                    parts = ' '.join(['%s' % (i, ) for i in fields[1:]])
                    f.write('{:>12}  {:<}\n'.format(atom_type, parts))
                for fields in dict_main.get(key):
                    new_atom_type = int(fields[0]) + len(value)
                    parts = ' '.join(['%s' % (i, ) for i in fields[1:]])
                    f.write('{:>12}  {:<}\n'.format(new_atom_type, parts))
                f.write('\n')

            # Atoms section
            elif index == 6:
                f.write('{}\n'.format(key))
                f.write('\n')
                for fields in dict_main.get(key):
                    atom_id = int(fields[0])
                    mol_id = int(fields[1])
                    new_atom_type = int(
                        fields[2]) + dict_gas_stats['natom_types']
                    parts = ' '.join(['%s' % (i, ) for i in fields[3:]])
                    f.write('{:>12} {} {} {:<}\n'.format(
                        atom_id, mol_id, new_atom_type, parts))
                for n in range(Ngas):
                    rx, ry, rz = get_random_position(box)
                    for fields in value:
                        gas_atom_id = int(
                            fields[0]) + atom_id + dict_gas_stats['natoms'] * n
                        gas_mol_id = int(fields[1]) + mol_id + n
                        atom_type = int(fields[2])
                        charge = float(fields[3])
                        x = float(fields[4]) + rx
                        y = float(fields[5]) + ry
                        z = float(fields[6]) + rz
                        f.write('{:>12} {} {} {} {} {} {}\n'.format(
                            gas_atom_id, gas_mol_id, atom_type, charge, x, y,
                            z))
                f.write('\n')

            else:
                if dict_main.get(key) or dict_gas_main.get(key):
                    f.write('{}\n'.format(key))
                    f.write('\n')
                    for fields in dict_main.get(key):
                        id = int(fields[0])
                        new_atom_type = int(fields[1]) + list(
                            dict_gas_stats.values())[index - 1]
                        parts = ' '.join(['%s' % (i, ) for i in fields[2:]])
                        f.write('{:>12} {} {:<}\n'.format(
                            id, new_atom_type, parts))
                    for n in range(Ngas):
                        for fields in value:
                            gas_id = int(fields[0]) + id
                            shift = atom_id + dict_gas_stats['natoms'] * n
                            parts = ' '.join([
                                '%s' % (int(i) + shift, ) for i in fields[2:]
                            ])
                            f.write('{:>12} {} {:<}\n'.format(
                                gas_id, fields[1], parts))
                        id += list(dict_gas_stats.values())[index - 6]
                    f.write('\n')


def build_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        pass


def main():
    # Specify the data and equilibrated lammpstrj files
    data_file = 'data.lmps'
    lammpstrj_file = 'equil.lammpstrj'
    nframes = 202

    # Specify the gas type (CH4, CO2, O2, or N2) and number of gas molecules to add in
    gas_list = ['CO2', 'CH4', 'N2', 'O2']
    Ngas = 27

    # Extract necessary data from the equilibrium simulation
    dict_stats, dict_main = read_data(data_file)
    r, box = read_lammstrj(lammpstrj_file, nframes)
    box = box * 1.1

    for gas in gas_list:
        # Specify output data file name
        build_dir(gas)
        output_file = os.path.join(gas, 'amor_gas.lmps')

        # Build systems and write output files
        dict_gas_stats, dict_gas_main = build_gas_template(gas)
        write_new_input(output_file, dict_stats, dict_main, r, box,
                        dict_gas_stats, dict_gas_main, gas, Ngas)


if __name__ == '__main__':
    main()
