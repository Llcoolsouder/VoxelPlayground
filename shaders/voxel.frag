/**
 * Fragment shader for voxel rendering
 */
#version 440 core

uniform float uVoxelResolution = 1.0f;

in VERTEX_DATA {
    float sdf;
    vec3 normal;
} inData;

out vec4 fragColor;

const vec3 lightDirection = normalize(vec3(0, 0, -1));
const vec3 lightColor = vec3(1, 1, 1);
const vec3 blockColor = vec3(1, 1, 1);

void main()
{
    float diff = max(dot(inData.normal, lightDirection), 0.0f);
    vec3 diffuse = diff * lightColor;
    vec3 objectColor =  diffuse * blockColor;
    fragColor = vec4(objectColor, 1.0);
}