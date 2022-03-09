import pygame
import json

pygame.init()

max_iter = 40
fps = 30
clock = pygame.time.Clock()

scale = 200
mandelbrot_x_bounds = [-3.25, 1.75]
mandelbrot_y_bounds = [-2.5, 2.5]
width = 400
height = 400
screen = pygame.display.set_mode((width, height))

def convert_reg_to_mandel(x, y):
    return (
        (x / width) * (mandelbrot_x_bounds[1] - mandelbrot_x_bounds[0])
            + mandelbrot_x_bounds[0],
        (y / height) * (mandelbrot_y_bounds[1] - mandelbrot_y_bounds[0])
            + mandelbrot_y_bounds[0]
    )

def load_palette():
    with open('colors.json') as f:
        colors_json = json.load(f)
        return [pygame.Color(*c) for c in colors_json]

def main():
    palette = load_palette()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                cx, cy = convert_reg_to_mandel(x, y)
                dx = cx - ((mandelbrot_x_bounds[0] + mandelbrot_x_bounds[1]) / 2)
                dy = cy - ((mandelbrot_y_bounds[0] + mandelbrot_y_bounds[1]) / 2)

                zx = (mandelbrot_x_bounds[1] - mandelbrot_x_bounds[0]) / 4
                zy = (mandelbrot_y_bounds[1] - mandelbrot_y_bounds[0]) / 4

                mandelbrot_x_bounds[0] += dx + zx
                mandelbrot_x_bounds[1] += dx - zx
                mandelbrot_y_bounds[0] += dy + zy
                mandelbrot_y_bounds[1] += dy - zy

        for cx in range(width):
            for cy in range(height):
                x, y = convert_reg_to_mandel(cx, cy)
                c = complex(x, y)
                output = complex(0, 0)
                i = 0
                while abs(output) <= 2 and i < max_iter:
                    output = output ** 2 + c
                    i += 1

                screen.set_at((cx, cy), palette[i-1])

        pygame.display.flip()
        clock.tick(fps)

        screen.fill((0, 0, 0))

if __name__ == '__main__':
    main()
