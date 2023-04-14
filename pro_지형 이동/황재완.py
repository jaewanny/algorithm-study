from collections import deque
import heapq

m, group, N, H = None, 0, 0, 0
dx, dy = (-1, 1, 0, 0), (0, 0, -1, 1)


def bfs(x, y, gm):
    global group
    gm[x][y] = group
    q = deque([(x, y)])
    while q:
        x, y = q.popleft()
        for k in range(4):
            nx, ny = x + dx[k], y + dy[k]
            if 0 <= nx < N and 0 <= ny < N and gm[nx][ny] == -1 and abs(m[x][y] - m[nx][ny]) <= H:
                gm[nx][ny] = group
                q.append((nx, ny))
    group += 1


def solution(land, height):
    global m, N, H
    m = land
    H, N = height, len(land)
    gm = [[-1] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if gm[x][y] == -1:
                bfs(x, y, gm)
    adj_mat = [[float('inf')] * group for _ in range(group)]
    adj_list = [set() for _ in range(group)]
    for x in range(N):
        for y in range(N):
            for k in range(4):
                nx, ny = x + dx[k], y + dy[k]
                if 0 <= nx < N and 0 <= ny < N and gm[x][y] != gm[nx][ny]:
                    adj_mat[gm[x][y]][gm[nx][ny]] = adj_mat[gm[nx][ny]][gm[x][y]] = min(adj_mat[gm[x][y]][gm[nx][ny]],
                                                                                        abs(m[x][y] - m[nx][ny]))
                    adj_list[gm[x][y]].add(gm[nx][ny])
                    adj_list[gm[nx][ny]].add(gm[x][y])

    ans = 0
    visited = [False] * group
    q = []
    min_edge = [float('inf')] * group
    min_edge[0] = 0
    heapq.heappush(q, (0, 0))
    cnt = 0
    while q:
        w, u = heapq.heappop(q)
        if visited[u]:
            continue

        visited[u] = True
        ans += w
        cnt += 1

        if cnt == group:
            return ans

        for v in adj_list[u]:
            if not visited[v] and min_edge[v] > adj_mat[u][v]:
                heapq.heappush(q, (adj_mat[u][v], v))
    return ans
