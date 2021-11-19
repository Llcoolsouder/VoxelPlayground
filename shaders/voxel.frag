/**
 * Fragment shader for voxel rendering
 */
#version 440 core

uniform float uVoxelResolution = 1.0f;

in VERTEX_DATA {
    float sdf;
    vec4 normal;
} inData;

out vec4 fragColor;

const vec3 lightDirection = vec3(-1, -1, 0.5);
const vec3 lightColor = vec3(1, 1, 1);

void main()
{
    float diff = max(dot(inData.normal.xyz, lightDirection), 0.0f);
    vec3 diffuse = diff * lightColor;
    float showSdf = 1.0f - step(0.0f, inData.sdf);
    float normalizedSdf = - inData.sdf / (10.0f * uVoxelResolution);
    vec3 objectColor =  diffuse * vec3(showSdf, normalizedSdf, showSdf);
    fragColor = vec4(objectColor, showSdf);
}