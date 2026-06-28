import os
BOARDS = {
    "easy.txt": (
        "004030050\n609400000\n005100489\n"
        "000060930\n300807002\n026040000\n"
        "453009600\n000004705\n090050200\n"
    ),
    "medium.txt": (
        "000030040\n109700000\n000851070\n"
        "002607830\n906010207\n031502900\n"
        "010369000\n000005703\n090070000\n"
    ),
    "hard.txt": (
        "102040007\n000080000\n009500304\n"
        "000607900\n540000026\n006405000\n"
        "708003400\n000010000\n200060509\n"
    ),
    "veryhard.txt": (
        "001007000\n600400300\n000030064\n"
        "380076000\n000000036\n270015000\n"
        "000020051\n700100200\n008009000\n"
    )
}

def generate_board_files():
   
    for filename, content in BOARDS.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Generated {filename}")
    print("-" * 30)



class SudokuCSP:
    def __init__(self, board):
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = {}
        self.neighbors = {}
        
        
        for r, c in self.variables:
            peers = set()
            for i in range(9):
                peers.add((r, i))  
                peers.add((i, c))  
            
        
            box_r, box_c = (r // 3) * 3, (c // 3) * 3
            for i in range(3):
                for j in range(3):
                    peers.add((box_r + i, box_c + j))
                    
            peers.remove((r, c))
            self.neighbors[(r, c)] = list(peers)
            
          
            val = board[r][c]
            if val == 0:
                self.domains[(r, c)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                self.domains[(r, c)] = [val]

class Stats:
    def __init__(self):
        self.calls = 0
        self.failures = 0



def ac3(csp):
   
    queue = [(xi, xj) for xi in csp.variables for xj in csp.neighbors[xi]]
    
    while queue:
        xi, xj = queue.pop(0)
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False 
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
  
    revised = False
    if len(csp.domains[xj]) == 1:
        val = csp.domains[xj][0]
        if val in csp.domains[xi]:
            csp.domains[xi].remove(val)
            revised = True
    return revised



def select_unassigned_variable(assignment, csp):
    
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda var: len(csp.domains[var]))

def is_consistent(var, value, assignment, csp):
   
    for neighbor in csp.neighbors[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

def forward_check(csp, var, value, assignment, removals):
    
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            if value in csp.domains[neighbor]:
                csp.domains[neighbor].remove(value)
                removals.append((neighbor, value))
                if not csp.domains[neighbor]:
                    return False
    return True

def backtrack(assignment, csp, stats):
    
    stats.calls += 1
    
   
    if len(assignment) == len(csp.variables):
        return assignment
        
    var = select_unassigned_variable(assignment, csp)
    
    for value in list(csp.domains[var]):
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            removals = []
            
           
            if forward_check(csp, var, value, assignment, removals):
                result = backtrack(assignment, csp, stats)
                if result is not None:
                    return result
            
           
            for r_var, r_val in removals:
                csp.domains[r_var].append(r_val)
            del assignment[var]
            
    stats.failures += 1
    return None

def read_board(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                row = [int(char) for char in line.strip()]
                board.append(row)
    return board

def print_board(assignment):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("- - - + - - - + - - -")
        row_str = ""
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row_str += "| "
            row_str += str(assignment.get((r, c), 0)) + " "
        print(row_str)

def solve_sudoku_file(filename):
    print(f"\nSolved {filename}:")
    board = read_board(filename)
    csp = SudokuCSP(board)
    stats = Stats()
    ac3(csp)

    assignment = {}
    for var in csp.variables:
        if len(csp.domains[var]) == 1:
            assignment[var] = csp.domains[var][0]
    solved_assignment = backtrack(assignment, csp, stats)
    
    if solved_assignment:
        print("SOLUTION:")
        print_board(solved_assignment)
    else:
        print("No solution found.")
        
    print(f"\nMetrics for {filename}:")
    print(f"BACKTRACK calls: {stats.calls}")
    print(f"BACKTRACK failures: {stats.failures}")
    return stats

if __name__ == '__main__':
    generate_board_files()
    
    files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
    for file in files:
        solve_sudoku_file(file)