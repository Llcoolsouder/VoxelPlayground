/**
 * Geometry shader for voxel rendering
 */
#version 440 core

layout(points) in;
layout(triangle_strip, max_vertices=24) out;

in VERTEX_DATA {
    float sdf;
} inData[];

out VERTEX_DATA {
    float sdf;
    vec4 normal;
} outData;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;
uniform mat4 uModelMatrix = mat4(1.0f);

uniform float uVoxelResolution = 1.0f;

mat3 RotateAboutX(float rDegrees)
{
    const float rRadians = radians(rDegrees);
    return mat3(
        1, 0, 0,
        0, cos(rRadians), -sin(rRadians),
        0, sin(rRadians), cos(rRadians));
}

mat3 RotateAboutY(float rDegrees)
{
    const float rRadians = radians(rDegrees);
    return mat3(
        cos(rRadians), 0, sin(rRadians),
        0, 1, 0,
        -sin(rRadians), 0, cos(rRadians));
}

/**
 * @param rotation rotation matrix to rotate a front facing quad
 * @param center center of the cube that this quad is part of
 * @param MVP model-view-projection matrix
 */
void GenerateRotatedQuad(mat3 rotation, vec4 center, mat4 MVP)
{
    const float halfRes = uVoxelResolution * 0.5f;
    vec4 normal = (MVP * vec4(rotation * vec3(0, 0, -1), 1.0));
    normal = normal / normal.z;

    outData.sdf = inData[0].sdf;
    outData.normal = normal;
    gl_Position = MVP * (center + vec4(rotation * vec3(-halfRes, halfRes, -halfRes), 0.0));
    EmitVertex();

    outData.sdf = inData[0].sdf;
    outData.normal = normal;
    gl_Position = MVP * (center + vec4(rotation * vec3(-halfRes, -halfRes, -halfRes), 0.0));
    EmitVertex();

    outData.sdf = inData[0].sdf;
    outData.normal = normal;
    gl_Position = MVP * (center + vec4(rotation * vec3(halfRes, halfRes, -halfRes), 0.0));
    EmitVertex();

    outData.sdf = inData[0].sdf;
    outData.normal = normal;
    gl_Position = MVP * (center + vec4(rotation * vec3(halfRes, -halfRes, -halfRes), 0.0));
    EmitVertex();
    EndPrimitive();
}

void main()
{
    const mat4 MVP = uProjectionMatrix *
                  uViewMatrix *
                  uModelMatrix;
    const vec4 center = gl_in[0].gl_Position;

    GenerateRotatedQuad(RotateAboutY(0), center, MVP);
    GenerateRotatedQuad(RotateAboutY(90), center, MVP);
    GenerateRotatedQuad(RotateAboutY(180), center, MVP);
    GenerateRotatedQuad(RotateAboutY(270), center, MVP);
    GenerateRotatedQuad(RotateAboutX(90), center, MVP);
    GenerateRotatedQuad(RotateAboutX(180), center, MVP);
}