/**
 * Vertex shader for voxel rendering
 */
#version 440 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in float aSdf;

out VERTEX_DATA {
    float sdf;
} outData;

void main()
{
    gl_Position = vec4(aPosition, 1.0f);
    outData.sdf = aSdf;
}