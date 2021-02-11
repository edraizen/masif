import os, sys
import json
import subprocess
import numpy as np

pymesh_container = os.environ.get("PYMESH_CONTAINER", "pymesh/pymesh")

try:
    import pymesh
except (ImportError, ModuleNotFoundError):
    pymesh = None
    use_singularity = os.environ.get("MASIF_SINGULARITY", "f").lower()[0]=="t"
    use_docker = os.environ.get("MASIF_DOCKER", "f").lower()[0]=="t"

    if not use_singularity and not use_docker:
        try:
            o = subprocess.check_output(["which", "singularity"])
            use_singularity = True
        except FileNotFoundError:
            try:
                subprocess.check_output(["which", "docker"])
                use_docker = True
            except FileNotFoundError:
                raise RuntimeError("You must install pymesh to run locally --or-- singularity or docker to run a containrized version")

class DumbMesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

def computeMesh(msms_file, mesh_res):
    if pymesh:
        from masif.triangulation.fixmesh import fix_mesh
        mesh = fix_mesh(msms_file, mesh_res)
    else:
        if use_singularity:
            output = subprocess.check_output(["singularity", "exec", "docker://"+pymesh_container,
                "python", os.path.relpath(os.path.join(os.path.dirname(__file__), "fixmesh.py")), msms_file, str(mesh_res)])
        elif use_docker:
            output = subprocess.check_output(["docker", "run", "--entrypoint",
                "python", "-v", f"{os.path.dirname(msms_file)}:/home/data",
                "-v", f"{os.path.dirname(__file__)}:/home/scripts",
                pymesh_container, "/home/scripts/fix_mesh.py",
                f"/home/data/{os.path.basename(msms_file)}", str(mesh_res)])

        result = json.loads(output)
        mesh = DumbMesh(np.array(result["vertices"]), np.array(result["faces"]))

    return mesh

def saveMesh(
    filename,
    vertices,
    faces=[],
    normals=None,
    charges=None,
    vertex_cb=None,
    hbond=None,
    hphob=None,
    iface=None,
    normalize_charges=False,
):
        """ Save vertices, mesh in ply format.
            vertices: coordinates of vertices
            faces: mesh
        """
        if pymesh:
            from masif.input_output.save_ply import save_ply
            return save_ply(filename, vertices, faces=faces, normals=normals,
                charges=charges, vertex_cb=vertex_cb, hbond=hbond, hphob=hphob,
                iface=iface, normalize_charges=normalize_charges)
        else:
            values = {"vertices":vertices.tolist(), "faces":faces.tolist()}
            if normals is not None:
                values["normals"] = [normals[:, 0].tolist(), normals[:, 1].tolist(), normals[:, 2].tolist()]
            if charges is not None:
                values["normalize_charges"] = normalize_charges
                values["charges"] = charges.tolist()
            if hbond is not None:
                values["hbond"] = hbond.tolist()
            if vertex_cb is not None:
                values["vertex_cb"] = vertex_cb.tolist()
            if hphob is not None:
                values["hphob"] = hphob.tolist()
            if iface is not None:
                values["iface"] = iface.tolist()

            tmp_file = f"{filename}.tmp.json"
            with open(tmp_file, "w") as f:
                json.dump(values, f)

            if use_singularity:
                output = subprocess.check_output(["singularity", "exec", "docker://"+pymesh_container,
                    "python", os.path.relpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "input_output", "save_ply.py")), filename, tmp_file])
            elif use_docker:
                output = subprocess.check_output(["docker", "run", "--entrypoint",
                    "python", "-v", f"{os.path.dirname(filename)}:/home/data",
                    "-v", f"{os.path.dirname(os.path.dirname(__file__))}/input_output:/home/scripts",
                    "/home/scripts/save_ply.py",
                    f"/home/data/{os.path.basename(filename)}",
                    f"/home/data/{os.path.basename(tmp_file)}"])

            try:
                os.remove(tmp_file)
            except (OSError, FileNotFoundError):
                pass
