# Main excecutable script for sandbox.
# This is a sandbox project, so this script could do literally anything at a given point in time
#
# Author:   Lonnie L. Souder II
# Date:     11/09/21

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GL.ARB.shader_objects import glGetObjectParameterivARB
import glm

from functools import partial
import time
import numpy as np

from voxelizer import *

WINDOW_SIZE = (1920, 1080)


def sphere_sdf(pos: Vec3f, rad: float, point: Vec3f) -> float:
    '''Returns distance from point to surface; positive if outside surface or negative if inside'''
    return norm(pos, point) - rad


my_sdf = partial(sphere_sdf, Vec3f(0.0, 0.0, 0.0), 1.0)

grid_params = VoxelGridParams(
    0.1, Vec3f(-2.0, -2.0, -2.0), Vec3f(2.0, 2.0, 2.0))


if __name__ == '__main__':
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(
        WINDOW_SIZE[0], WINDOW_SIZE[1], "Voxel Playground", None, None)
    glfw.make_context_current(window)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glPointSize(5)

    voxel_grid = marching_cubes(grid_params, my_sdf)

    vao = glGenVertexArrays(1)
    vertex_buffer = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER,
                 voxel_grid.data,
                 GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 16,
                          ctypes.c_void_p(0))  # position
    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 16,
                          ctypes.c_void_p(12))  # sdf

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
        glm.vec3(0, 0, -5.0),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0))
    projection_matrix = glm.perspective(
        100, WINDOW_SIZE[0] / WINDOW_SIZE[1], 0.01, 1000.0)
    u_view_mat_loc = glGetUniformLocation(program, "uViewMatrix")
    u_projection_mat_loc = glGetUniformLocation(program, "uProjectionMatrix")
    u_model_mat_loc = glGetUniformLocation(program, "uModelMatrix")
    u_voxel_res_loc = glGetUniformLocation(program, "uVoxelResolution")
    glUniformMatrix4fv(u_view_mat_loc, 1, GL_FALSE, view_matrix.to_list())
    glUniformMatrix4fv(u_projection_mat_loc, 1, GL_FALSE,
                       projection_matrix.to_list())
    glUniform1f(u_voxel_res_loc, grid_params.resolution)

    model_matrix = glm.mat4(1.0)
    frame_time = 0.0
    while not glfw.window_should_close(window):
        frame_start = time.process_time()
        model_matrix = glm.rotate(
            model_matrix, frame_time * glm.radians(15.0), glm.vec3(0.0, 1.0, 0.0))
        glUniformMatrix4fv(u_model_mat_loc, 1, GL_FALSE,
                           model_matrix.to_list())
        glfw.poll_events()
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_POINTS, 0, voxel_grid.data.size)
        glfw.swap_buffers(window)
        frame_time = time.process_time() - frame_start
