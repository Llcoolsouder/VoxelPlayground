# Code to make voxel grids from other things.
#
# Author:   Lonnie L. Souder II
# Date:     11/09/21

from math import ceil, sqrt
from typing import Callable
import numpy as np


class Vec3f:
    '''Simple 3D vector of floats'''

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


def norm(p: Vec3f, q: Vec3f) -> float:
    '''Returns distance (L2-norm) between 2 points'''
    return sqrt((p.x - q.x) ** 2 +
                (p.y - q.y) ** 2 +
                (p.z - q.z) ** 2)


class VoxelGridParams:
    '''Set of parameters to define a voxel grid in space'''

    def __init__(self, resolution: float, min_point: Vec3f, max_point: Vec3f):
        self.resolution = resolution
        self.min_point = min_point
        self.max_point = max_point

    def get_grid_dimensions(self):
        '''Returns a triple of integers denoting grid dimensions in x, y, and z'''
        def get_dim(min, max): return ceil((max - min) / self.resolution)
        return (get_dim(self.min_point.x, self.max_point.x),
                get_dim(self.min_point.y, self.max_point.y),
                get_dim(self.min_point.z, self.max_point.z))


class VoxelGrid:
    '''Container for voxel grid data'''

    voxel_datatype = np.dtype(
        [('x', np.float32), ('y', np.float32), ('z', np.float32), ('distance', np.float32)])

    def __init__(self, params: VoxelGridParams, data):
        self.params = params
        expected_dims = self.params.get_grid_dimensions()
        dimensions_are_correct = (data.shape[0] == expected_dims[0] and
                                  data.shape[1] == expected_dims[1] and
                                  data.shape[2] == expected_dims[2])
        if dimensions_are_correct:
            self.data = data
        else:
            raise RuntimeError(
                "Data is not the correct dimensions for these voxel grid params")


def marching_cubes(grid_params: VoxelGridParams, f: Callable) -> VoxelGrid:
    '''
    Solves f for each voxel to populate a voxel grid
    Parameters:
        grid_params: parameters fo the desired voxel grid
        f: function that takes a 3d point vec3f and returns a float
        '''
    def calculate_coordinate(index, min):
        return min + (index * grid_params.resolution) + (0.5 * grid_params.resolution)

    grid_shape = grid_params.get_grid_dimensions()
    voxels = np.ndarray(grid_shape, dtype=VoxelGrid.voxel_datatype)
    x_dim, y_dim, z_dim = grid_shape
    for z_ind in range(z_dim):
        for y_ind in range(y_dim):
            for x_ind in range(x_dim):
                voxel_center = Vec3f(
                    calculate_coordinate(x_ind, grid_params.min_point.x),
                    calculate_coordinate(y_ind, grid_params.min_point.y),
                    calculate_coordinate(z_ind, grid_params.min_point.z))
                voxels[x_ind][y_ind][z_ind] = (
                    voxel_center.x, voxel_center.y, voxel_center.z, f(voxel_center))
    return VoxelGrid(grid_params, voxels)
