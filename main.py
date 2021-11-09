# Main excecutable script for sandbox.
# This is a sandbox project, so this script could do literally anything at a given point in time
#
# Author:   Lonnie L. Souder II
# Date:     11/09/21

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from functools import partial

from voxelizer import *


def sphere_sdf(pos: Vec3f, rad: float, point: Vec3f) -> float:
    '''Returns distance from point to surface; positive if outside surface or negative if inside'''
    return norm(pos, point) - rad


def single_voxel_from_sdf(index_3d, grid_params: VoxelGridParams, sdf: function[[Vec3f], float]) -> float:
    '''
    Calculates the value of a single voxel given its index in the grid, rid parameters, and some sdf to determine the value
    Parameters:
        index_3d: 3d index of item in voxel grid
        grid_params: parameters of the grid
        sdf: a function that takes a Vec3f and returns a float denoting the distance to the surface
    Returns:
        distance from center of denoted voxel to surface given by sdf
    '''
    def calculate_coordinate(index, min):
        return min + (index * grid_params.resolution) + (0.5 * grid_params.resolution)
    voxel_center_point = (
        calculate_coordinate(index_3d[0], grid_params.min_point.x),
        calculate_coordinate(index_3d[1], grid_params.min_point.y),
        calculate_coordinate(index_3d[2], grid_params.min_point.z))
    return sdf(voxel_center_point)


my_sdf = partial(sphere_sdf, Vec3f(0.0, 0.0, 0.0), 1.0)
my_sdf_to_voxel = partial(single_voxel_from_sdf, sdf=my_sdf)

grid_params = VoxelGridParams(
    0.1, Vec3f(-2.0, -2.0, -2.0), Vec3f(2.0, 2.0, 2.0))


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Voxelizer Sandbox")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, 500, 0, 500)

    voxel_grid = marching_cubes(grid_params, my_sdf_to_voxel)
