import sys
import random
import copy
import time
from collections import deque
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            newDomain = set()
            length = variable.length
            for word in self.domains[variable]:
                if len(word) == length:
                    newDomain.add(word)
            self.domains[variable] = newDomain

        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        if self.crossword.overlaps[x, y] is None:
            return False

        ith, jth = self.crossword.overlaps[x, y]
        revision = False

        newDomain = set()
        for wordX in self.domains[x]:
            for wordY in self.domains[y]:
                if wordX[ith] == wordY[jth]:
                    newDomain.add(wordX)
                    revision = True
        
        if revision:
            self.domains[x] = newDomain
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # find all arcs in the problem
            arcs = []
            for variable in self.crossword.variables:
                for neighbor in self.crossword.neighbors(variable):
                    arcs.append((variable, neighbor))
        
        queue = deque(arcs)

        while len(queue) != 0:
            (x, y) = queue.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0: 
                    return False
                
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        words = {}
        for variable in assignment:
            word = assignment[variable]
            
            # check if word is not distinct
            if word in words:
                return False

            if variable.length != len(word):
                return False
            
            for neighbor in self.crossword.neighbors(variable):
                ith, jth = self.crossword.overlaps[variable, neighbor]
                if neighbor in assignment:
                    if word[ith] != assignment[neighbor][jth]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        neighbors = self.crossword.neighbors(var)
        assignedWords = set((assignment.values()))
        unassignedNeighbors = neighbors - assignedWords

        ordered = {}
        for value in self.domains[var]:
            ruledOut = 0

            for neighbor in unassignedNeighbors:
                ith, jth = self.crossword.overlaps[var, neighbor]
                for word in self.domains[neighbor]:
                    if value[ith] != word[jth]:
                        ruledOut += 1

            ordered[value] = ruledOut
        
        ordered = sorted(ordered.items(), key=lambda item: item[1])
        return dict(ordered).keys()


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # go back and implement this with heuristic
        # assignedVariables = set((variable for variable in assignment))
        # unassignedVariables = self.crossword.variables - assignedVariables
        # return random.choice(list(unassignedVariables))

        bestVariable = None
        minimumRemainingVariable = (None, float("inf"))
        highestDegreeVariable = (None, -float("inf"))

        unassignedVariables = self.crossword.variables - assignment.keys()
        
        for variable in unassignedVariables:
            # calculate mrv heuristic
            domainSize = len(self.domains[variable])
            if domainSize < minimumRemainingVariable[1]:
                minimumRemainingVariable = (variable, domainSize)
                bestVariable = variable
            
            # calculate degree heuristic
            degreeCount = len(self.crossword.neighbors(variable))
            if degreeCount > highestDegreeVariable[1]:
                highestDegreeVariable = (variable, degreeCount)
            
            if domainSize == minimumRemainingVariable[1]:
                if degreeCount > highestDegreeVariable[1]:
                    bestVariable = variable
        
        assert bestVariable is not None
        return bestVariable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        def _backtrack(assignment, originalDomain=None):
            # stop code from constantly making a deep copy on every recursive call
            if originalDomain is None:
                originalDomain = copy.deepcopy(self.domains)
                
            if self.assignment_complete(assignment):
                return assignment

            variable = self.select_unassigned_variable(assignment)
            for value in self.order_domain_values(variable, assignment):
                # check if value is consistent with assignment
                assignment[variable] = value

                if self.consistent(assignment):
                    arcs = [(variable, neighbor) for neighbor in self.crossword.neighbors(variable)]
                    self.ac3(arcs=arcs) # run maintaining arc consistency algorithm
                    
                    result = _backtrack(assignment, originalDomain)
                    if result is not None:
                        return result

                del assignment[variable]
                # Remove inferences made by AC-3 by reverting
                self.domains = originalDomain

            return None
        timeStart = time.perf_counter()
        x = _backtrack(assignment)
        timeStop = time.perf_counter()
        print(f"Elapsed Time: {timeStop - timeStart}")
        return x

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
