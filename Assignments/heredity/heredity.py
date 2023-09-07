import csv
import itertools
import sys

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
    jointProbability = 1
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
        probability = (1 - motherProbability) * (1 - fatherProbability)

    return probability

def update(probabilities, one_gene, two_genes, have_trait, p):
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
