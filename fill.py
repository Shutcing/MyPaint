from queue import Queue

def fill(canvas, image, x, y, color):
    Q = Queue()
    visited = set()
    
    w, h = image.size
    
    def is_transparent(pixel):
        return pixel[3] == 0

    pixels = image.load()

    if not is_transparent(pixels[x, y]):
        return

    Q.put((x, y))
    visited.add((x, y))

    while not Q.empty():
        cx, cy = Q.get()

        if is_transparent(pixels[cx, cy]):
            canvas.create_rectangle(cx, cy, cx+1, cy+1, outline=color, fill=color)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    Q.put((nx, ny))
                    visited.add((nx, ny))