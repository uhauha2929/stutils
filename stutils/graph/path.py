import numpy as np
from scipy.sparse import spmatrix, coo_matrix, lil_matrix


def dijkstra(graph: spmatrix, start_vertex) -> np.ndarray:
    """Dijkstra算法
    :param graph: 稀疏矩阵表示的图结构
    :param start_vertex: 开始顶点的位置
    :return: 开始顶点到其他顶点的最短距离数组
    """
    n = graph.shape[0]
    # 已求出最短路径的点
    result = np.full(n, np.inf)
    result[start_vertex] = 0
    # 未求出最短路径的点
    not_found = np.zeros(n)
    for i in range(n):
        not_found[i] = graph[start_vertex][i]
    not_found[start_vertex] = np.inf

    for _ in range(n - 1):
        # 将最短距离的点取出放入结果中
        min_index = not_found.argmin()
        result[min_index] = not_found[min_index]
        not_found[min_index] = np.inf
        # 更新剩余顶点的距离
        for j in range(n):
            # 出度点不能已经在结果集
            if graph[min_index][j] != np.inf and result[j] == np.inf:
                new_dist = result[min_index] + graph[min_index][j]
                if new_dist < not_found[j]:
                    not_found[j] = new_dist
    return result


def topological_sort(graph: lil_matrix):
    """对图进行拓扑排序
    :param graph: 以稀疏矩阵形式表示的有向无环图，自定义节点可考虑邻接表存储
    :return: 如果存在拓扑排序则返回排序列表，否则返回空列表
    """
    n = graph.shape[0]
    # 保存所有节点的入度
    in_degree = np.zeros(n)
    # 只考虑是否存在边的关系
    for row in graph.rows:
        for j in row:
            in_degree[j] += 1

    # 找到入度为0的节点
    queue = []
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    # 进行层次遍历
    res = []
    while len(queue) > 0:
        i = queue.pop()
        res.append(i)
        # 从队列弹出后，所有指向的节点的入度减一
        for j in graph.rows[i]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)
    return res if len(res) == n else []
