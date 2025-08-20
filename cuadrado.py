import os
import math
import time

# Definir los vértices del cubo (coordenadas 3D)
vertices = [
    [-1, -1, -1],
    [-1, -1,  1],
    [-1,  1, -1],
    [-1,  1,  1],
    [ 1, -1, -1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [ 1,  1,  1],
]

# Conexiones entre los vértices para dibujar las aristas
edges = [
    (0,1), (0,2), (0,4),
    (1,3), (1,5),
    (2,3), (2,6),
    (3,7),
    (4,5), (4,6),
    (5,7),
    (6,7)
]

def rotate(x, y, z, ax, ay, az):
    """Rotación 3D en los ejes x, y, z"""
    # Rotación en X
    cosx, sinx = math.cos(ax), math.sin(ax)
    y, z = y*cosx - z*sinx, y*sinx + z*cosx
    # Rotación en Y
    cosy, siny = math.cos(ay), math.sin(ay)
    x, z = x*cosy + z*siny, -x*siny + z*cosy
    # Rotación en Z
    cosz, sinz = math.cos(az), math.sin(az)
    x, y = x*cosz - y*sinz, x*sinz + y*cosz
    return x, y, z

def project(x, y, z, screen_w, screen_h, scale=20, dist=5):
    """Proyecta coordenadas 3D en 2D"""
    factor = scale / (z + dist)
    px = int(screen_w/2 + x * factor)
    py = int(screen_h/2 - y * factor)
    return px, py

def draw_cube(ax, ay, az):
    screen_w, screen_h = 80, 24
    screen = [[" " for _ in range(screen_w)] for _ in range(screen_h)]
    
    # Rotar y proyectar vértices
    projected = []
    for v in vertices:
        x, y, z = rotate(v[0], v[1], v[2], ax, ay, az)
        px, py = project(x, y, z, screen_w, screen_h)
        projected.append((px, py))
    
    # Dibujar aristas
    for edge in edges:
        (x1, y1), (x2, y2) = projected[edge[0]], projected[edge[1]]
        # Bresenham para dibujar líneas
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= x1 < screen_w and 0 <= y1 < screen_h:
                screen[y1][x1] = "#"
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    # Imprimir pantalla
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in screen:
        print("".join(row))

# Animación
ax = ay = az = 0
while True:
    draw_cube(ax, ay, az)
    ax += 0.05
    ay += 0.03
    az += 0.02
    time.sleep(0.05)
