from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
# If the statement that one is a Knave and a Knight is actually true they must be a knight
# But if the statement is false (which it is) then they must be a Knave

# Expected answer: A is a knave

knowledge0 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# A cannot be a knight because if the statement "we are both knaves" is true then A would not be a knight despite being truthful
# Therefore A is a knave

# Since we are both knaves is false then B must be a knight since not BOTH of them are knaves but A is
# Therefore B is a knight

# Expected answer: A is a knave and B is a knight

knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."


# If B is a knight then A must be a knave.
# If A is a knave then their statement is false which is ok because A always lies

# Expected answer: A is a knave and B is a knight

statement = And(Or(And(AKnight, BKnave), And(AKnave, BKnight)), Not(And(And(AKnight, BKnave), And(AKnave, BKnight))))
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, statement),
    Implication(BKnave, Not(statement))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."


# Expected answer: I don't even know where to start with this one I'll just trust what the computer spits out

knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    Implication(BKnight, AKnave),
    Implication(BKnave, AKnight),
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
