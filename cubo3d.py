import os
import time
import math

def cube():
    # Dimensiones de la pantalla (ajustadas para un cubo más grande)
    width = 60
    height = 30
    # Buffer para la pantalla
    screen = [' '] * (width * height)
    
    # Parámetros de rotación
    A = 0  # Rotación en eje X
    B = 0  # Rotación en eje Y
    
    # Definir los vértices del cubo (tamaño aumentado)
    cube_size = 2.5  # Tamaño del cubo (mitad de la longitud de un lado)
    vertices = [
        [-cube_size, -cube_size, -cube_size],
        [cube_size, -cube_size, -cube_size],
        [cube_size, cube_size, -cube_size],
        [-cube_size, cube_size, -cube_size],
        [-cube_size, -cube_size, cube_size],
        [cube_size, -cube_size, cube_size],
        [cube_size, cube_size, cube_size],
        [-cube_size, cube_size, cube_size]
    ]
    
    # Aristas del cubo (conexiones entre vértices)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Cara frontal
        (4, 5), (5, 6), (6, 7), (7, 4),  # Cara trasera
        (0, 4), (1, 5), (2, 6), (3, 7)   # Conexiones entre caras
    ]
    
    while True:
        # Limpiar pantalla y z-buffer
        screen = [' '] * (width * height)
        zbuffer = [0] * (width * height)
        
        # Rotar y proyectar vértices
        projected = []
        for x, y, z in vertices:
            # Cálculos de rotación
            sinA = math.sin(A)
            cosA = math.cos(A)
            sinB = math.sin(B)
            cosB = math.cos(B)
            
            # Rotación en Y
            x_rot = x * cosB + z * sinB
            z_rot = -x * sinB + z * cosB
            
            # Rotación en X
            y_rot = y * cosA - z_rot * sinA
            z_final = z_rot * cosA + y * sinA
            
            # Proyección perspectiva (escala aumentada para cubo más grande)
            ooz = 1 / (z_final + 6)
            xp = int(width / 2 + 30 * ooz * x_rot)  # Escala aumentada
            yp = int(height / 2 - 15 * ooz * y_rot)  # Escala aumentada
            
            projected.append((xp, yp, ooz))
            
            # Dibujar vértices
            if 0 <= xp < width and 0 <= yp < height:
                index = xp + width * yp
                if ooz > zbuffer[index]:
                    zbuffer[index] = ooz
                    screen[index] = '@'  # Carácter para vértices
                
        # Dibujar aristas
        for v1, v2 in edges:
            x1, y1, z1 = projected[v1]
            x2, y2, z2 = projected[v2]
            
            # Interpolación lineal para dibujar la línea
            steps = max(abs(x2 - x1), abs(y2 - y1), 1)
            for t in range(int(steps) + 1):
                t = t / steps
                x = int(x1 + t * (x2 - x1))
                y = int(y1 + t * (y2 - y1))
                if 0 <= x < width and 0 <= y < height:
                    index = x + width * y
                    if (z1 + t * (z2 - z1)) > zbuffer[index]:
                        zbuffer[index] = z1 + t * (z2 - z1)
                        screen[index] = '#'  # Carácter para aristas
        
        # Imprimir pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        for j in range(height):
            for i in range(width):
                print(screen[i + j * width], end='')
            print()
        
        # Actualizar ángulos de rotación
        A += 0.07
        B += 0.03
        time.sleep(0.03)

if __name__ == "__main__":
    try:
        cube()
    except KeyboardInterrupt:
        print("\nAnimación terminada")