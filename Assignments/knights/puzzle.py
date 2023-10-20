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
    Not(And(AKnight, AKnave)),
    Implication(And(AKnight, AKnave), AKnight), 
    Implication(Not(And(AKnight, AKnave)), AKnave) 
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
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Implication(And(AKnave, BKnave), AKnight),
    Implication(Not(And(AKnave, BKnave)), AKnave),
    Implication(And(AKnave, BKnave), BKnave),
    Implication(Not(And(AKnave, BKnave)), BKnight)
)
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# If A is a knight then B would be lying (B would also be a knight due to A's statement) which is not possible if B is a knight
# If A was a knave then B would still be lying but it would be ok since B is a knave
# if we know B is knave then A is lying when they say we are the same kind becaues knaves always lie

# Expected answer: A and B are knaves

knowledge2 = And(
    Implication(Or(AKnight, AKnave), BKnave), 
    Implication(And(AKnave, BKnave), AKnave),
    Implication(Not(And(AKnave, BKnave)), AKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
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
