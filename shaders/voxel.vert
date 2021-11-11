/**
 * Vertex shader for voxel rendering
 */
#version 460 core

layout(location = 0) attribute vec3 aPosition;
layout(location = 1) attribute float aSdf;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;
uniform mat4 uModelMatrix = mat4(1.0f);

out VERTEX_DATA {
    float sdf;
} vertex_data;

void main()
{
    gl_Position = vec4(aPosition, 1.0f);
    vertex_data.sdf = aSdf;
}