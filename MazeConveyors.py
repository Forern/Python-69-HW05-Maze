def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    if not maze or not maze[0]:
        return {"distance": -1, "path": []}
        
    rows = len(maze)
    cols = len(maze[0])
    
    start = None
    end = None
    
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
                
    if not start or not end:
        return {"distance": -1, "path": []}
        
    memo = {}
    
    def simulate_conveyor(r, c):
        if (r, c) in memo:
            return memo[(r, c)]
            
        dirs = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
        path_seg = [[r, c]]
        curr_r, curr_c = r, c
        seen = {(r, c)}
        
        while True:
            char = maze[curr_r][curr_c]
            if char not in dirs:
                result = ((curr_r, curr_c), path_seg)
                memo[(r, c)] = result
                return result
            
            dr, dc = dirs[char]
            nxt_r, nxt_c = curr_r + dr, curr_c + dc
            
            
            if not (0 <= nxt_r < rows and 0 <= nxt_c < cols):
                memo[(r, c)] = (None, [])
                return (None, [])
            if maze[nxt_r][nxt_c] == '#':
                memo[(r, c)] = (None, [])
                return (None, [])
            
            if (nxt_r, nxt_c) in seen:
                memo[(r, c)] = (None, [])
                return (None, [])
                
            path_seg.append([nxt_r, nxt_c])
            seen.add((nxt_r, nxt_c))
            curr_r, curr_c = nxt_r, nxt_c

    queue = [(start[0], start[1], 0)]
    visited = {start}
    
    parent = {}
    
    while queue:
        r, c, dist = queue.pop(0)
        
        if (r, c) == end:
            curr = (r, c)
            segments = []
            while curr != start:
                prev, seg = parent[curr]
                segments.append(seg)
                curr = prev
            segments.append([[start[0], start[1]]])
            segments.reverse() 
            
            final_path = [cell for seg in segments for cell in seg]
                    
            return {"distance": dist, "path": final_path}
            
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols:
                char = maze[nr][nc]
                if char == '#':
                    continue
                    
                if char in ['>', '<', '^', 'v']:
                    dest, conv_path = simulate_conveyor(nr, nc)
                    
                    if dest is not None and dest not in visited:
                        visited.add(dest)
                        parent[dest] = ((r, c), conv_path)
                        queue.append((dest[0], dest[1], dist + 1))
                else:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        parent[(nr, nc)] = ((r, c), [[nr, nc]])
                        queue.append((nr, nc, dist + 1))
                        
    return {"distance": -1, "path": []}
    

if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}


    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}
