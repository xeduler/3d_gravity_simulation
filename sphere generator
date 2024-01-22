# Sphere (icosphere for simplicity)
from math import sqrt, pi
import json

vertices_sphere = []
edges_sphere = []

def get_icosphere_vertices():
    t = (1.0 + sqrt(5.0)) / 2.0

    vertices = [
        (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)
    ]

    return vertices

def normalize_vector(v):
    length = sqrt(sum(v[i] ** 2 for i in range(len(v))))
    
    # Avoid division by zero
    if length == 0.0:
        return v
    
    return [v[i] / length for i in range(len(v))]


def get_middle_point(v1, v2):
    middle_point = [(v1[i] + v2[i]) / 2.0 for i in range(len(v1))]
    return normalize_vector(middle_point)

def subdivide_triangle(v1, v2, v3, depth):
    if depth <= 0:
        return [(v1, v2), (v2, v3), (v3, v1)]

    mid1 = get_middle_point(v1, v2)
    mid2 = get_middle_point(v2, v3)
    mid3 = get_middle_point(v3, v1)

    triangles = [
        (v1, mid1, mid3),
        (v2, mid2, mid1),
        (v3, mid3, mid2),
        (mid1, mid2, mid3)
    ]

    subdivided_triangles = []
    for triangle in triangles:
        subdivided_triangles.extend(subdivide_triangle(*triangle, depth=depth-1))

    return subdivided_triangles

# Subdivide icosphere to get more vertices and edges
icosphere_subdivisions = 3
icosphere_vertices = get_icosphere_vertices()
icosphere_edges = subdivide_triangle(*icosphere_vertices[:3], depth=icosphere_subdivisions)

# Convert vertices to tuple for consistency
vertices_sphere = tuple(tuple(v) for v in icosphere_vertices)
edges_sphere = tuple(tuple(e) for e in icosphere_edges)

with open("models/sphere0.json", "w") as output_file:
    json.dump([vertices_sphere, edges_sphere], output_file)