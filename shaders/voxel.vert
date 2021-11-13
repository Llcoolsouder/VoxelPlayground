/**
 * Vertex shader for voxel rendering
 */
#version 440 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in float aSdf;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;
uniform mat4 uModelMatrix = mat4(1.0f);

out VERTEX_DATA {
    float sdf;
} outData;

void main()
{
    gl_Position = uProjectionMatrix *
                  uViewMatrix *
                  uModelMatrix *
                  vec4(aPosition, 1.0f);
    outData.sdf = aSdf;
}