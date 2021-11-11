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


my_sdf = partial(sphere_sdf, Vec3f(0.0, 0.0, 0.0), 1.0)

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

    voxel_grid = marching_cubes(grid_params, my_sdf)

    glClear(GL_COLOR_BUFFER_BIT)

    vao = glGenVertexArrays(1)
    vertex_buffer = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER,
                 )
