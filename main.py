# Main excecutable script for sandbox.
# This is a sandbox project, so this script could do literally anything at a given point in time
#
# Author:   Lonnie L. Souder II
# Date:     11/09/21

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GL.ARB.shader_objects import glGetObjectParameterivARB
import glm

from functools import partial
from itertools import chain
import numpy as np

from voxelizer import *


def sphere_sdf(pos: Vec3f, rad: float, point: Vec3f) -> float:
    '''Returns distance from point to surface; positive if outside surface or negative if inside'''
    return norm(pos, point) - rad


my_sdf = partial(sphere_sdf, Vec3f(0.0, 0.0, 0.0), 1.0)

grid_params = VoxelGridParams(
    0.1, Vec3f(-2.0, -2.0, -2.0), Vec3f(2.0, 2.0, 2.0))


def display_func():
    # glDrawArrays(GL_POINTS, 0, voxel_grid.data.size)
    glDrawArrays(GL_POINTS, 0, 4)


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    window = glutCreateWindow("Voxelizer Sandbox")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_BLEND)
    glPointSize(100)

    voxel_grid = marching_cubes(grid_params, my_sdf)

    glClear(GL_COLOR_BUFFER_BIT)

    vao = glGenVertexArrays(1)
    vertex_buffer = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER,
                 # voxel_grid.data,
                 np.array([0.0, 0.0, 0.0, -1.0], dtype=np.float32),
                 GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4,
                          ctypes.c_void_p(0))  # position
    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 4,
                          ctypes.c_void_p(3))  # sdf

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, open("./shaders/voxel.vert").read())
    glCompileShader(vertex_shader)
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, open("./shaders/voxel.frag").read())
    glCompileShader(fragment_shader)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    glUseProgram(program)

    view_matrix = glm.lookAt(
        glm.vec3(0, 0, -2.0),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0))
    projection_matrix = glm.perspective(
        glm.radians(100.0), 1.0, 0.01, 1000.0)
    u_view_mat_loc = glGetUniformLocation(program, "uViewMatrix")
    u_projection_mat_loc = glGetUniformLocation(program, "uProjectionMatrix")
    u_voxel_res_loc = glGetUniformLocation(program, "uVoxelResolution")
    glUniformMatrix4fv(u_view_mat_loc, 1, GL_FALSE, view_matrix.to_list())
    glUniformMatrix4fv(u_projection_mat_loc, 1, GL_FALSE,
                       projection_matrix.to_list())
    glUniform1f(u_voxel_res_loc, grid_params.resolution)

    glutDisplayFunc(display_func)
    glutMainLoop()

    input("Press any key to close...")
