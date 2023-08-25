import csv
import itertools
import sys

from decimal import Decimal

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.    
    
    Each parent passes 1 of their two genes onto the child
    so if child has 2 genes then either both parents have the gene or both parents don't have the gene but mutated
    if child hs 1 gene then either mum has gene and not dad or dad has gene and not mum
        
    Potential Pseudocode 

    function joint_probability(people, oneGene, twoGenes, haveTrait)
        joinProbability = None
        create set or array that consists of oneGene and twoGenes
        create dict containing names of all in people set their values to None
        create another dict, remaining, which is a deep copy of the above dict, names will be removed and what remains are people outside of the argument sets

        // Iterate through each set and adjust probabilities

        for set in set containing oneGene and twoGenes
            for person in set
                n = 1 or 2 depending on which set we're on
                if person has no parents
                    if their probability is none
                        set their probability to probability of n gene from PROBS
                    else
                        multiply their existing probability by that of n gene from PROBS
                    endif
                else // person has parents
                    // perform parent gene inheritence calculation stuff
                endif

                multiply their existing probability by that of trait (depending when it is true or false and how many genes they have)

                if joinProbability is None
                    set joinProbability to result
                else
                    multiple joinProbability by result
                endif

                remove person from remaining
            next person
        next set

        // people in remaining do not have any copies of the gene
        for person in remaining
            if their probability is none
                set their probability to probability of 0 genes (PROBS["gene"][0])
            endif
            multiply their existing probability by that of trait given that they have 0 genes and taking into account the value of the boolean value

            if jointProbability is None
                set jointProbability to result
            else
                multiple jointProbability by result
            endif
        next person

        for person in dict containing probabilities
            multiply probabilities together
        next person

        return result
    endfunction

    Pseudocode for handling parents

    // mutationFactor is the "mutation" in PROBS
    geneDict = {2: 1, 1: 0.5, 0: mutationFactor}
    motherProbability = geneDict[mother gene count]
    fatherProbability = geneDict[father gene count]

    if mother gene count != 0
        motherProbability -= mutationFactor
    endif

    if father gene count != 0
        fatherProbability -= mutationFactor
    endif

    if child is known to have 2 genes
        // Either both mum and dad have 1-2 genes or neither of them have genes but they both passed mutated genes
        probability = fatherProbability * motherProbability + mutationFactor squared
    else if child is known to have 1 gene
        inverseGeneDict = {2: mutationFactor, 1: 0.5 + mutationFactor, 0: mutationFactor}
        fatherInverseProbability = inverseGeneDict[father gene count]
        motherInverseProbability = inverseGeneDict[mother gene count]
        // Either dad has gene and mum does not or mum has gene and dad does not
        
        probability = fatherProbabiliy * motherInverseProbability + fatherInverseProbability * motherProbability
    endif
            
    """
    jointProbability = 1
    # print(f"People {people}")
    # print(f"One Gene {one_gene}")
    # print(f"Two Genes {two_genes}")
    # print(f"Have trait {have_trait}")

    remaining = [name for name in people]
    geneCount = 1 

    for set in (one_gene, two_genes):
        for person in set:
            personDict = people[person]
            probability = 1

            if personDict["mother"] is None and personDict["father"] is None:
                probability = PROBS["gene"][geneCount]
            else:
                probability = handle_parents(personDict, geneCount, one_gene, two_genes)
            
            # Include probability of traits
            probability *= PROBS["trait"][geneCount][person in have_trait]
            jointProbability *= probability
            remaining.remove(person)
        geneCount += 1
    
    # These people have 0 genes
    for person in remaining:
        probability = 1
        if people[person]["mother"] is not None and people[person]["father"] is not None:
            probability = handle_parents(people[person], 0, one_gene, two_genes)
        else:
            probability = PROBS["gene"][0]
        
        probability *= PROBS["trait"][0][person in have_trait]
        jointProbability *= probability

    return jointProbability


def handle_parents(child, childGeneCount, oneGene, twoGenes):
    """
    Returns the probability of a child inheriting N genes from their parents
    Where N is between 0 and 2 inclusive
    """
    probability = 1
    mother = child["mother"]
    father = child["father"]

    motherGeneCount = 0
    fatherGeneCount = 0

    if mother in oneGene: 
        motherGeneCount = 1

    if father in oneGene: 
        fatherGeneCount = 1

    if mother in twoGenes: 
        motherGeneCount = 2

    if father in twoGenes:
        fatherGeneCount = 2

    # Maps parent gene counts to the probability a mutated GJB2 gene will be passed down
    # assuming one gene is inherited from the pair
    # eg if both genes are mutated then you're guaranteed to pick a mutated gene if you pick 1 out of the 2
    geneDict = {2: 1 - PROBS["mutation"], 1: 0.5}
    motherProbability = PROBS["mutation"] if motherGeneCount == 0 else geneDict[motherGeneCount]
    fatherProbability = PROBS["mutation"] if fatherGeneCount == 0 else geneDict[fatherGeneCount]
    
    if childGeneCount == 2:
            probability = fatherProbability * motherProbability
    elif childGeneCount == 1:
        motherInverseProbability = 1 - motherProbability
        fatherInverseProbability = 1 - fatherProbability
        probability = fatherProbability * motherInverseProbability + fatherInverseProbability * motherProbability
    else:
        motherInverseProbability = 1 - motherProbability
        fatherInverseProbability = 1 - fatherProbability

        probability = motherInverseProbability * fatherInverseProbability

    return probability

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.

    function update(probabilities, oneGene, twoGenes, haveTrait, p)

        for person in probabilities
            if person in oneGene
                add p to probabilities[person]["gene"][1]
            else if person in twoGenes
                add p to probabilities[person]["gene"][2]
            else
                add p to probabilities[person]["gene"][0]
            endif

            if person in haveTrait
                add p to probabilities[person]["trait"][true]
            else
                add p to probabilities[person]["trait"][false]
            endif
            
            return
        next person
    endfunction

    """
    for person in probabilities:
        geneCount = 0

        if person in one_gene: 
            geneCount = 1
        elif person in two_genes: 
            geneCount = 2

        probabilities[person]["gene"][geneCount] += p

        hasTrait = False
        if person in have_trait:
            hasTrait = True

        probabilities[person]["trait"][hasTrait] += p

    return

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).

    for person in probabilities
        geneSum = total of all gene probabilities for that person
        traitSum = total of all trait probabilities for that person

        for gene in geneSet
            set value to gene / geneSum
        next gene

        for trait in traitSet
            set value to trait / traitSum
        next trait
    next person
    """
    
    for person in probabilities:
        geneSum = sum(probabilities[person]["gene"].values())
        traitSum = sum(probabilities[person]["trait"].values())

        for key in probabilities[person]["gene"]:
            probabilities[person]["gene"][key] = probabilities[person]["gene"][key] / geneSum

        for key in probabilities[person]["trait"]:
            probabilities[person]["trait"][key] = probabilities[person]["trait"][key] / traitSum

    return


if __name__ == "__main__":
    main()
