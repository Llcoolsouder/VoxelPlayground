/**
 * Geometry shader for voxel rendering
 */
#version 440 core

layout(points) in;
layout(triangle_strip, max_vertices=4) out;

in VERTEX_DATA {
    float sdf;
} inData[];

out VERTEX_DATA {
    float sdf;
} outData;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;
uniform mat4 uModelMatrix = mat4(1.0f);

uniform float uVoxelResolution = 1.0f;

void main()
{
    const mat4 MVP = uProjectionMatrix *
                  uViewMatrix *
                  uModelMatrix;
    const vec4 center = gl_in[0].gl_Position;
    const float halfRes = uVoxelResolution * 0.5f;

    outData.sdf = inData[0].sdf;
    gl_Position = MVP * (center + vec4(-halfRes, halfRes, 0.0, 0.0));
    EmitVertex();
    outData.sdf = inData[0].sdf;
    gl_Position = MVP * (center + vec4(-halfRes, -halfRes, 0.0, 0.0));
    EmitVertex();
    outData.sdf = inData[0].sdf;
    gl_Position = MVP * (center + vec4(halfRes, halfRes, 0.0, 0.0));
    EmitVertex();
    outData.sdf = inData[0].sdf;
    gl_Position = MVP * (center + vec4(halfRes, -halfRes, 0.0, 0.0));
    EmitVertex();
    EndPrimitive();
}