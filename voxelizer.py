from math import ceil
import numpy as np


class Vec3f:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class VoxelGridParams:
    def __init__(self, resolution: float, min_point: Vec3f, max_point: Vec3f):
        self.resolution = resolution
        self.min_point = min_point
        self.max_point = max_point

    def get_grid_dimensions(self):
        '''Returns a triple of integers denoting grid dimensions in x, y, and z'''
        def get_dim(min, max): return ceil((max - min) / self.resolution)
        return (get_dim(self.max_point.x - self.min_point.x),
                get_dim(self.max_point.y - self.min_point.y),
                get_dim(self.max_point.z - self.min_point.z))


class VoxelGrid:
    def __init__(self, params: VoxelGridParams, data):
        self.params = params
        expected_dims = self.params.get_grid_dimensions()
        data.si
        dimensions_are_correct = (len(data.shape[0]) == expected_dims[0] and
                                  len(data.shape[1]) == expected_dims[1] and
                                  len(data.shape[2]) == expected_dims[2])
        if dimensions_are_correct:
            self.data = data
        else:
            raise RuntimeError(
                "Data is not the correct dimensions for these voxel grid params")


def marching_cubes(grid_params: VoxelGridParams, f: function) -> VoxelGrid:
    '''
    Solves f for each voxel to populate a voxel grid
    Parameters:
        grid_params: parameters fo the desired voxel grid
        f: function that takes a 3d index (int) to the voxel grid and a set of VoxelGridParams and returns a float
        '''
    grid_shape = grid_params.get_grid_dimensions()
    voxels = np.ndarray(grid_shape, dtype=float)
    x_dim, y_dim, z_dim = grid_shape
    for z_ind in range(z_dim):
        for y_ind in range(y_dim):
            for x_ind in range(x_dim):
                index = (x_ind, y_ind, z_ind)
                voxels[x_ind][y_ind][z_ind] = f(index, grid_params)
    return VoxelGrid(grid_params, voxels)

