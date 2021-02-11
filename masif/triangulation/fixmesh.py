import os, sys
import numpy as np
from numpy.linalg import norm

import pymesh
import json

try:
    from masif.input_output.read_msms import read_msms
except (ImportError, ModuleNotFoundError):
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "input_output"))
    from read_msms import read_msms

"""
fixmesh.py: Regularize a protein surface mesh.
- based on code from the PyMESH documentation.
"""


def _fix_mesh(mesh, resolution, detail="normal"):
    bbox_min, bbox_max = mesh.bbox;
    diag_len = norm(bbox_max - bbox_min);
    if detail == "normal":
        target_len = diag_len * 5e-3;
    elif detail == "high":
        target_len = diag_len * 2.5e-3;
    elif detail == "low":
        target_len = diag_len * 1e-2;

    target_len = resolution
    #print("Target resolution: {} mm".format(target_len));
    # PGC 2017: Remove duplicated vertices first
    mesh, _ = pymesh.remove_duplicated_vertices(mesh, 0.001)


    count = 0;
    #print("Removing degenerated triangles")
    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100);
    mesh, __ = pymesh.split_long_edges(mesh, target_len);
    num_vertices = mesh.num_vertices;
    while True:
        mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6);
        mesh, __ = pymesh.collapse_short_edges(mesh, target_len,
                preserve_feature=True);
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100);
        if mesh.num_vertices == num_vertices:
            break;

        num_vertices = mesh.num_vertices;
        #print("#v: {}".format(num_vertices));
        count += 1;
        if count > 10: break;

    mesh = pymesh.resolve_self_intersection(mesh);
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    mesh = pymesh.compute_outer_hull(mesh);
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5);
    mesh, __ = pymesh.remove_isolated_vertices(mesh);
    mesh, _ = pymesh.remove_duplicated_vertices(mesh, 0.001)

    return mesh

def fix_mesh(msms_file, mesh_res):
    vertices, faces, normals, names = read_msms(msms_file)
    mesh = pymesh.form_mesh(vertices, faces)
    fixed_mesh = _fix_mesh(mesh, mesh_res)

    return fixed_mesh


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise RuntimeError("Usage: ./fixmesh.py path/to/msms.file mesh_res")

    msms_file = sys.argv[1]
    mesh_res = float(sys.argv[2])
    fixed_mesh = fix_mesh(msms_file, mesh_res)

    print(json.dumps({"vertices": fixed_mesh.vertices.tolist(), "faces":fixed_mesh.faces.tolist()}))
