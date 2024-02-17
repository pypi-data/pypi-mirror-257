import numpy.typing


def merge_hessian_mesh_laplacian(
        tri2vtx: numpy.typing.NDArray,
        vtx2xyz,
        row2idx,
        idx2col,
        row2val, idx2val):
    from .del_fem import merge_hessian_mesh_laplacian_on_trimesh3
    merge_hessian_mesh_laplacian_on_trimesh3(
        tri2vtx, vtx2xyz,
        row2idx, idx2col,
        row2val, idx2val)