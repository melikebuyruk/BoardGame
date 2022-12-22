import heapq
from os import name
from types import NoneType

class Node:
    def __init__(self, board, cost, tiles_order, prev_node=None):
        self.board = board
        self.cost = cost
        self.tiles_order = tiles_order
        self.prev_node = prev_node
        self.heuristic = self.hamming_distance()

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic

    def hamming_distance(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != '.' and self.board[i][j] != self.tiles_order[i][j]:
                    distance += 1
        return distance


def move_cost(tile, direction):
    if tile == 'R':
        if direction in ['left', 'right']:
            return 1
        elif direction in ['up', 'down']:
            return 1
    elif tile == 'G':
        if direction in ['left', 'right']:
            return 1
        elif direction in ['up', 'down']:
            return 2
    elif tile == 'B':
        if direction in ['left', 'right']:
            return 2
        elif direction in ['up', 'down']:
            return 1


def get_neighbors(node, tile):
    neighbors = []
    for i in range(3):
        for j in range(3):
            if node.board[i][j] == tile:
                # Try moving a tile to the left
                if j > 0:
                    board = [row[:] for row in node.board]
                    if board[i][j-1] == "." :
                      board[i][j] = board[i][j - 1]
                      board[i][j - 1] = tile
                      cost = move_cost(tile, 'left')
                      tiles_order = [row[:] for row in node.tiles_order]
                      if cost != None:
                        neighbors.append(Node(board, node.cost + cost, tiles_order, node))
                # Try moving a tile to the right
                if j < 2:
                    board = [row[:] for row in node.board]
                    if board[i][j+1] == "." :
                      board[i][j] = board[i][j + 1]
                      board[i][j + 1] = tile
                      cost = move_cost(tile, 'right')
                      tiles_order = [row[:] for row in node.tiles_order]
                      if cost != None:
                        neighbors.append(Node(board, node.cost + cost, tiles_order, node))
                # Try moving a tile up
                if i > 0:
                    board = [row[:] for row in node.board]
                    if board[i-1][j] == "." :
                      board[i][j] = board[i - 1][j]
                      board[i - 1][j] = tile
                      cost = move_cost(tile, 'up')
                      tiles_order = [row[:] for row in node.tiles_order]
                      if cost != None:
                        neighbors.append(Node(board, node.cost + cost, tiles_order,node))
                # Try moving a tile down
                if (i < 2):
                    board = [row[:] for row in node.board]
                    if board[i+1][j] == "." :
                      board[i][j] = board[i + 1][j]
                      board[i + 1][j] = tile
                      cost = move_cost(tile, 'down')
                      tiles_order = [row[:] for row in node.tiles_order]
                      if cost!=None:
                        neighbors.append(Node(board, node.cost + cost, tiles_order, node))
    return neighbors

def uniform_cost_search(initial_board, goal_board, tiles_order):
                initial_node = Node(initial_board, 0, tiles_order)
                fringe = []
                heapq.heappush(fringe, initial_node)
                visited = set()
                expanded_nodes = 0
                max_fringe_size = 0
                while fringe:
                  node = heapq.heappop(fringe)
                  if node.board == goal_board:
                    return node, expanded_nodes, max_fringe_size

                  if str(node.board) in visited:
                    continue

                  visited.add(str(node.board))
                  expanded_nodes += 1

                  neighbors = get_neighbors(node)
                  for neighbor in neighbors:
                    heapq.heappush(fringe, neighbor)
                    max_fringe_size = max(max_fringe_size, len(fringe))

                  if len(fringe) > 25:
                    heapq.heappop(fringe)

                  if expanded_nodes > 10:
                    break

                return None, expanded_nodes, max_fringe_size

def a_star_search(initial_board, goal_board, tiles_order, order):
              initial_node = Node(initial_board, 0, tiles_order)
              fringe = []
              heapq.heappush(fringe, initial_node)
              visited = set()
              expanded_nodes = 0
              max_fringe_size = 0
              i = 3
              while fringe:
                node = heapq.heappop(fringe)
                if node.board == goal_board:
                  return node, expanded_nodes, max_fringe_size
                if str(node.board) in visited:
                  continue

                visited.add(str(node.board))
                expanded_nodes += 1

                neighbors = get_neighbors(node,order[i%3])
                i += 1
                for neighbor in neighbors:
                  heapq.heappush(fringe, neighbor)
                  max_fringe_size = max(max_fringe_size, len(fringe))

                if len(fringe) > 25:
                  heapq.heappop(fringe)

                if expanded_nodes > 10:
                  break

              return None, expanded_nodes, max_fringe_size

def print_solution(node):
          if not node:
            print("No solution found.")
            return
          path = []
          while node:
            path.append(node.board)
            node = node.prev_node

          for board in reversed(path):
            print(board[0])
            print(board[1])
            print(board[2])
            print()

def main():
          row1=input("please enter a 3*3 board game with only 1 R, 1B and 1G. Write .(dot) for the places that doenst have any R G and B tiles. \n Row 1:")
          row1 = [x for x in row1]
          row2=input("row2:")
          row2 = [x for x in row2]
          row3=input("row3:")
          row3 = [x for x in row3]

          goalRow1 = input("please enter a goal state with only 1 R, 1B and 1G. Write .(dot) for the places that doenst have any R G and B tiles. \n Row 1:")
          goalRow1 = [x for x in goalRow1]
          goalRow2 = input("row2:")
          goalRow2 = [x for x in goalRow2]
          goaRrow3 = input("row3:")
          goalRow3 = [x for x in goaRrow3]

          initial_board = [row1, row2, row3]
          goal_board = [goalRow1, goalRow2, goalRow3]

          order=input("Please write an order for expansion.(For example R-G-B)")
          tiles_order = [goalRow1,goalRow2,goalRow3]

          search_type = input("Enter search type uniform(1) or A*(2): ")
          if search_type == "1":
            node, expanded_nodes, max_fringe_size = uniform_cost_search(initial_board, goal_board, tiles_order)
          elif search_type=="2":
            node, expanded_nodes, max_fringe_size = a_star_search(initial_board, goal_board, tiles_order, order)

          print_solution(node)
          print("Expanded nodes:", expanded_nodes)
          print("Max fringe size:", max_fringe_size)

if __name__ == "__main__":
  main()











