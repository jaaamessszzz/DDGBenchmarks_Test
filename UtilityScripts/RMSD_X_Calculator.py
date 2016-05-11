from Bio.PDB import *
import Bio.PDB
import os
import pyRMSD
from pyRMSD.matrixHandler import MatrixHandler
import pyRMSD.RMSDCalculator
from pyRMSD.availableCalculators import availableCalculators
import prody
import numpy as np
import scipy.spatial.distance
import json

#From Kyle's Finalize.py
def read_mutations_resfile(filenum_dir):
    resfile = os.path.join(filenum_dir, 'mutations_repack.resfile')
    mutations = []
    with open(resfile, 'r') as f:
        post_start = False
        for line in f:
            if post_start:
                line = line.strip()
                pdb_resnum, chain, pikaa, mut_res = line.split()
                mutations.append( [pdb_resnum, chain, pikaa, mut_res] )
            elif line.startswith('start'):
                post_start = True
    return mutations

#From Kyle's Finalize.py
def find_neighbors(filenum_dir, pdb_path, neighbor_distance = 8.0):
    mutations = read_mutations_resfile(filenum_dir)
    parser = PDBParser(PERMISSIVE=1)
    open_strct = parser.get_structure('Open', pdb_path)

    # There should only be one model in PDB file
    num_models = 0
    for model in open_strct.get_models():
        num_models += 1
    assert( num_models == 1 )

    chain_list = [chain.get_id() for chain in open_strct[0].get_chains()]
    neighbors = set()
    for mutation in mutations:
        res_id, chain_id, pikaa, mut_aa = mutation
        mut_chain = str(chain_id)
        try:
            mut_pos = int( res_id )
            mut_insertion_code = ' '
        except ValueError:
            mut_pos = int( res_id[:-1] )
            mut_insertion_code = res_id[-1]

        mut_residue = open_strct[0][mut_chain][(' ', mut_pos, mut_insertion_code)]
        for chain in chain_list:
            for residue in [res.get_id() for res in open_strct[0][chain].get_residues()]:
                try:
                    # Kyle note - might be good to do something else for consistency, since not all residues have CB
                    dist = mut_residue['CB'] - open_strct[0][chain][residue]['CB']
                    if dist < neighbor_distance:
                        neighbors.add( (residue, chain) )
                except KeyError:
                    try:
                        dist = mut_residue['CA'] - open_strct[0][chain][residue]['CA']
                        if dist < neighbor_distance:
                            neighbors.add( (residue, chain) )
                    except KeyError:
                        pass

    return neighbors

#Kyle's RMSDWrapper.py (Spread out all over the place now)
def rmsd(input_pdbs, pyrmsd_calc, coordinates):
    if type(coordinates) is dict:
        rmsd_list = []
        for mutres, coord_set in coordinates.iteritems():
            rmsd_matrix = pyRMSD.matrixHandler.MatrixHandler().createMatrix(coord_set, pyrmsd_calc)
            avg_rmsd = average_rmsd_calculator(rmsd_matrix)
            rmsd_list.append([mutres, avg_rmsd])
        return rmsd_list
    else:
        rmsd_matrix = pyRMSD.matrixHandler.MatrixHandler().createMatrix(coordinates, pyrmsd_calc)
        avg_rmsd = average_rmsd_calculator(rmsd_matrix)
        return avg_rmsd
    
def average_rmsd_calculator(rmsd_matrix):
    rmsd_sqform = scipy.spatial.distance.squareform( rmsd_matrix.get_data() )
    avg_rmsd_list = []
    for rmsd_row in enumerate(rmsd_sqform):
        for rmsd_value in enumerate(rmsd_row[1]):
            if rmsd_value[0] > rmsd_row[0]:
                avg_rmsd_list.append(rmsd_value[1])
    avg_rmsd = sum(avg_rmsd_list)/len(avg_rmsd_list)
    return avg_rmsd
    
def global_ca_rms(input_pdbs):
    coordinates = np.array( [prody.parsePDB(input_pdb).select('calpha').getCoords() for input_pdb in input_pdbs] )
    return coordinates    
    
def neighborhood_rms(neighbors, reference, input_pdbs):
    temp = []

    for input_pdb in input_pdbs:
        if 'WT.' not in input_pdb:
            atom_list = []
            hv = prody.parsePDB(input_pdb).getHierView()
            res_list = [hv[neighbor[1], neighbor[0][1]] for neighbor in neighbors]
            for res in res_list:
                for atom in res:
                    if atom.getElement() != 'H':
                        atom_list.append(atom.getCoords())
                    else:
                        pass
                    temp.append(atom_list)
        
    coordinates = np.asarray(temp)
    return coordinates
        
#Calculates sidechain rmsd        
def mutant_rms(datadir, input_pdbs):
    mutations = read_mutations_resfile(datadir)
    mutation_dict = {}
    
    for mutation in mutations:
        temp = []
        temp_nparray = []
        
        for input_pdb in input_pdbs: 
            if 'WT.' not in input_pdb:
                atom_list = []
                hv = prody.parsePDB(input_pdb).getHierView()
                res_list = [hv[mutation[1], int(mutation[0])]]
                for res in res_list:
                    for atom in res:
                        if atom.getElement() != 'H':
                            atom_list.append(atom.getCoords())
                        else:
                            pass
                temp.append(atom_list)
        
        temp_nparray = np.asarray(temp)
        mutation_dict['%s%s' %(mutation[1], mutation[0])] = temp_nparray
    return mutation_dict

def chi_angles(datadir, input_pdbs):
    mutations = read_mutations_resfile(datadir)
    
    #http://www.ccp14.ac.uk/ccp/web-mirrors/garlic/garlic/commands/dihedrals.html
    chi1_dict = {'ARG':['N','CA','CB','CG'],
                 'ASN':['N','CA','CB','CG'],
                 'ASP':['N','CA','CB','CG'],
                 'CYS':['N','CA','CB','SG'],
                 'GLN':['N','CA','CB','CG'],
                 'GLU':['N','CA','CB','CG'],
                 'HIS':['N','CA','CB','CG'],
                 'ILE':['N','CA','CB','CG1'],
                 'LEU':['N','CA','CB','CG'],
                 'LYS':['N','CA','CB','CG'],
                 'MET':['N','CA','CB','CG'],
                 'PHE':['N','CA','CB','CG'],
                 'PRO':['N','CA','CB','CG'],
                 'SER':['N','CA','CB','OG'],
                 'THR':['N','CA','CB','OG1'],
                 'TRP':['N','CA','CB','CG'],
                 'TYR':['N','CA','CB','CG'],
                 'VAL':['N','CA','CB','CG1']}
    chi2_dict = {'ARG':['CA','CB','CG','CD'],
                 'ASN':['CA','CB','CG','OD1'],
                 'ASP':['CA','CB','CG','OD1'],
                 'GLN':['CA','CB','CG','CD'],
                 'GLU':['CA','CB','CG','CD'],
                 'HIS':['CA','CB','CG','ND1'],
                 'ILE':['CA','CB','CG1','CD'],
                 'LEU':['CA','CB','CG','CD1'],
                 'LYS':['CA','CB','CG','CD'],
                 'MET':['CA','CB','CG','SD'],
                 'PHE':['CA','CB','CG','CD1'],
                 'PRO':['CA','CB','CG','CD'],
                 'TRP':['CA','CB','CG','CD1'],
                 'TYR':['CA','CB','CG','CD1']}
    
    xangles_dict = {}
    
    for mutation in mutations:
        print mutation
        if mutation[3] == 'A' or mutation[3] == 'G':
            xangles_dict['%s%s' %(mutation[0], mutation[1])] = "Mutation is %s!" %mutation[3]
        else:
            xangles_dict['%s%s' %(mutation[0], mutation[1])] = {}
            x1_templist = []
            x2_templist = []
            for input_pdb in input_pdbs:
                if 'WT.pdb_' not in input_pdb:
                    print input_pdb
                    p = prody.parsePDB(input_pdb)
                    hv = p.getHierView()

                    current_res = hv[mutation[1], int(mutation[0])]
                    
                    if current_res.getResname() in chi1_dict.keys():
                        current_res.select('name %s' %chi1_dict[current_res.getResname()])
                        chi1 = prody.measure.measure.calcDihedral(current_res.select('name %s' %chi1_dict[current_res.getResname()][0]),
                                                              current_res.select('name %s' %chi1_dict[current_res.getResname()][1]),
                                                              current_res.select('name %s' %chi1_dict[current_res.getResname()][2]),
                                                              current_res.select('name %s' %chi1_dict[current_res.getResname()][3]))
                        x1_templist.append(chi1[0])
                        print 'Chi1 %s' %chi1[0]
                    if current_res.getResname() in chi2_dict.keys():
                        chi2 = prody.measure.measure.calcDihedral(current_res.select('name %s' %chi2_dict[current_res.getResname()][0]),
                                                              current_res.select('name %s' %chi2_dict[current_res.getResname()][1]),
                                                              current_res.select('name %s' %chi2_dict[current_res.getResname()][2]),
                                                              current_res.select('name %s' %chi2_dict[current_res.getResname()][3]))
                        x2_templist.append(chi2[0])
                        print 'Chi2 %s' %chi2[0]
            xangles_dict['%s%s' %(mutation[0], mutation[1])]['X1'] = sum(x1_templist)/len(x1_templist)
            xangles_dict['%s%s' %(mutation[0], mutation[1])]['X2'] = sum(x2_templist)/len(x2_templist)
            print x1_templist
            print x2_templist
    return xangles_dict

#Action!!!
def do_math(datadir, reference, outputdir):   
    # Use CUDA for GPU calculations, if avialable
    if 'QCP_CUDA_MEM_CALCULATOR' in availableCalculators():
        pyrmsd_calc = 'QCP_CUDA_MEM_CALCULATOR'
    else:
        pyrmsd_calc = 'QCP_SERIAL_CALCULATOR'
        
    input_temp = []
    for i in os.listdir(outputdir):
        if i.endswith('.pdb'):
            input_temp.append(os.path.join(outputdir, i ))
    input_pdbs = sorted(input_temp)
    
    neighbors = find_neighbors(datadir, reference, 8)
    
    point_mutants = mutant_rms(datadir, input_pdbs)
    neighborhood = neighborhood_rms(neighbors, reference, input_pdbs)
    global_ca = global_ca_rms(input_pdbs)

    return_output_dict = {}

    return_output_dict['Point Mutant RMSDs'] = rmsd(input_pdbs, pyrmsd_calc, point_mutants)
    return_output_dict['Neighborhood RMSD'] = rmsd(input_pdbs, pyrmsd_calc, neighborhood)
    return_output_dict['Global RMSD'] = rmsd(input_pdbs, pyrmsd_calc, global_ca)
    chi_angles_output = chi_angles(datadir, input_pdbs)
    if chi_angles_output != {}:
        return_output_dict['X angles'] = chi_angles_output
        print chi_angles_output
    else:
        print 'No X angles!'
    return return_output_dict

def main():
    import sys
    #Change to root of output directory
    os.chdir('/kortemmelab/home/james.lucas/160412-kyleb_jl-brub-rscr-v2/DDG_Zemu_v2_output-Sum_DDG_only')
    cwd = os.getcwd()
    #Define things
    output_dict = {}
    outdir = sys.argv[1]
    datadir = '../data/%s' %outdir
    print "\n***Calculating RMSDs for %s***\n" %outdir
    for asdffile in os.listdir(datadir):
        if asdffile.endswith('.pdb'):
            mypdb_ref = asdffile
                
    reference = '../data/%s/%s' %(outdir, mypdb_ref) 
    output_dict[outdir] = do_math(datadir, reference, outdir)
    print output_dict
    
#    for outdir in os.listdir(cwd):
#        print "\n***Calculating RMSDs for %s***\n" %outdir
#        #Define things
#        datadir = '../data/%s' %outdir

#        for asdffile in os.listdir(datadir):
#            if asdffile.endswith('.pdb'):
#                mypdb_ref = asdffile
                
#        reference = '../data/%s/%s' %(outdir, mypdb_ref) 
#        output_dict[outdir] = do_math(datadir, reference, outdir)
    
    with open('RMSD_dict_X.txt', 'a') as outfile:
        json.dump(output_dict, outfile)
        
main()
