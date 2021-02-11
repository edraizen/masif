#!/usr/bin/python
import numpy as np
import os
import Bio
import shutil
from Bio.PDB import *
import sys
import importlib
from IPython.core.debugger import set_trace

# Local includes
from masif.default_config.masif_opts import masif_opts
from masif.default_config.chemistry import radii, polarHydrogens

from masif.triangulation.computeMSMS import computeMSMS
from masif.triangulation.computeMesh import computeMesh, saveMesh
#from masif.triangulation.fixmesh import fix_mesh
#import pymesh
from masif.input_output.extractPDB import extractPDB
#from masif.input_output.save_ply import save_ply
#from masif.input_output.read_ply import read_ply
from molmimic.parsers.reduce import Reduce
from masif.triangulation.computeHydrophobicity import computeHydrophobicity
from masif.triangulation.computeCharges import computeCharges, assignChargesToNewMesh
from masif.triangulation.computeAPBS import computeAPBS
from masif.triangulation.compute_normal import compute_normal
from sklearn.neighbors import KDTree

from molmimic.parsers.msms import MSMS
from molmimic.parsers.Electrostatics import Electrostatics

def pdb_extract_and_triangulate(pdb_chain, ligand=False):
    assert pdb_chain.count("_") == 1, "Pdb must have id and chains separated by single underscore"

    pdb_id, chain_ids1 = pdb_chain.split("_")

    if ligand:
        pdb_filename = os.path.join(masif_opts["ligand"]["assembly_dir"],pdb_id+".pdb")
    else:
        pdb_filename = os.path.join(masif_opts['raw_pdb_dir'], pdb_id+".pdb")

    tmp_dir= masif_opts['tmp_dir']
    protonated_file = tmp_dir+"/"+pdb_id+".pdb"

    reducer = Reduce(work_dir=masif_opts['tmp_dir'])
    protonated_file = reducer.reprotonate(in_file=pdb_filename, out_file=protonated_file)
    pdb_filename = protonated_file

    # Extract chains of interest.
    out_filename1 = tmp_dir+"/"+pdb_id+"_"+chain_ids1
    extractPDB(pdb_filename, out_filename1+".pdb", chain_ids1)

    # Compute MSMS of surface w/hydrogens,
    try:
        msms = MSMS(work_dir=masif_opts['tmp_dir'])
        vertices1, faces1, normals1, names1, areas1, msms_file = \
            msms.get_surface_and_area_from_pdb(out_filename1+".pdb", return_msms_file=True)
    except:
        raise
        set_trace()

    # Compute "charged" vertices
    if masif_opts['use_hbond']:
        vertex_hbond = computeCharges(out_filename1, vertices1, names1)

    # For each surface residue, assign the hydrophobicity of its amino acid.
    if masif_opts['use_hphob']:
        vertex_hphobicity = computeHydrophobicity(names1)

    # If protonate = false, recompute MSMS of surface, but without hydrogens (set radius of hydrogens to 0).
    vertices2 = vertices1
    faces2 = faces1

    # Fix the mesh.
    regular_mesh = computeMesh(msms_file, masif_opts['mesh_res'])

    # mesh = pymesh.form_mesh(vertices2, faces2)
    # regular_mesh = fix_mesh(mesh, masif_opts['mesh_res'])

    # Compute the normals
    vertex_normal = compute_normal(regular_mesh.vertices, regular_mesh.faces)
    # Assign charges on new vertices based on charges of old vertices (nearest
    # neighbor)

    if masif_opts['use_hbond']:
        vertex_hbond = assignChargesToNewMesh(regular_mesh.vertices, vertices1,\
            vertex_hbond, masif_opts)

    if masif_opts['use_hphob']:
        vertex_hphobicity = assignChargesToNewMesh(regular_mesh.vertices, vertices1,\
            vertex_hphobicity, masif_opts)

    if masif_opts['use_apbs']:
        #vertex_charges = computeAPBS(regular_mesh.vertices, out_filename1+".pdb", out_filename1)
        electrostatics = Electrostatics(work_dir=masif_opts['tmp_dir'])
        vertex_charges = electrostatics.get_electrostatics_at_coordinates_from_pdb(
            regular_mesh.vertices, out_filename1+".pdb", force_field="parse",
            noopt=True, apbs_input=True, whitespace=True
        )

    iface = np.zeros(len(regular_mesh.vertices))
    if 'compute_iface' in masif_opts and masif_opts['compute_iface']:
        # Compute the surface of the entire complex and from that compute the interface.
        # v3, f3, _, _, _, msms_file3 = computeMSMS(pdb_filename,\
        #     protonate=True, return_msms_file=True)

        v3, f3, _, _, _, msms_file3 = msms.get_surface_and_area_from_pdb(
            pdb_filename, return_msms_file=True, radii=radii, polarHydrogens=polarHydrogens)


        # Regularize the mesh
        full_regular_mesh = computeMesh(msms_file3, masif_opts['mesh_res'])
        # mesh = pymesh.form_mesh(v3, f3)
        # full_regular_mesh = fix_mesh(mesh, masif_opts['mesh_res'])
        # Find the vertices that are in the iface.
        v3 = full_regular_mesh.vertices
        # Find the distance between every vertex in regular_mesh.vertices and those in the full complex.
        kdt = KDTree(v3)
        d, r = kdt.query(regular_mesh.vertices)
        d = np.square(d) # Square d, because this is how it was in the pyflann version.
        assert(len(d) == len(regular_mesh.vertices))
        iface_v = np.where(d >= 2.0)[0]
        iface[iface_v] = 1.0
        # Convert to ply and save.
        saveMesh(out_filename1+".ply", regular_mesh.vertices,\
                            regular_mesh.faces, normals=vertex_normal, charges=vertex_charges,\
                            normalize_charges=True, hbond=vertex_hbond, hphob=vertex_hphobicity,\
                            iface=iface)

    else:
        # Convert to ply and save.
        saveMesh(out_filename1+".ply", regular_mesh.vertices,\
                            regular_mesh.faces, normals=vertex_normal, charges=vertex_charges,\
                            normalize_charges=True, hbond=vertex_hbond, hphob=vertex_hphobicity)
    if not os.path.exists(masif_opts['ply_chain_dir']):
        os.makedirs(masif_opts['ply_chain_dir'])
    if not os.path.exists(masif_opts['pdb_chain_dir']):
        os.makedirs(masif_opts['pdb_chain_dir'])
    shutil.copy(out_filename1+'.ply', masif_opts['ply_chain_dir'])
    shutil.copy(out_filename1+'.pdb', masif_opts['pdb_chain_dir'])

    print("DONE")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: {config} "+sys.argv[0]+" PDBID_A")
        print("A or AB are the chains to include in this surface.")
        sys.exit(1)

    ligand = (len(sys.argv)>2) and (sys.argv[2]=='masif_ligand')

    pdb_extract_and_triangulate(sys.argv[1], ligand=ligand)
