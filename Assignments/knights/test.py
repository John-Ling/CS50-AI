from logic import *
p = Symbol("clapped")
q = Symbol("hagrid")
r = Symbol("Piffting")


sentence = And(Or(p, q), r)
knowledge = And(Implication(Not(p), r), sentence)

print(knowledge.formula())

print(sentence.formula())