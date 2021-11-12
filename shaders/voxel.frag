/**
 * Fragment shader for voxel rendering
 */
#version 440 core

uniform float uVoxelResolution = 1.0f;

in VERTEX_DATA {
    float sdf;
} inData;

out vec4 fragColor;

void main()
{
    float showSdf = 1.0f - step(0.0f, inData.sdf);
    float normalizedSdf = - inData.sdf / (10.0f * uVoxelResolution);
    // fragColor = vec4(normalizedSdf, normalizedSdf, normalizedSdf, showSdf);
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}