import csv
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    KEYWORDS = {True: 1, False: 0, "Returning_Visitor": 1, 
        "Jan": 0, "Feb": 1, "March": 2, "April": 3, "May": 4, "Jun": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}
    
    evidence, labels = [], []
    dataframe = pd.read_csv("shopping.csv")
    
    for _, row in dataframe.iterrows():
        newEvidence = []
        for index, value in enumerate(row.to_list()):
            newValue = None
            if value in KEYWORDS:
                newValue = KEYWORDS[value]
            else:
                newValue = value

                # check for any words differing from "Returning_Vistor" like "New_Visitor" or "other"
                if isinstance(value, str):
                    newValue = 0

            if index == 17:
                labels.append(newValue)
            else:
                newEvidence.append(newValue)
        evidence.append(newEvidence)

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    X, Y = evidence, labels
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(X, Y)
    return classifier


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correctPositives, correctNegatives = 0, 0
    totalPositives, totalNegatives = 0, 0

    for (label, prediction) in zip(labels, predictions):
        if label == 1:
            totalPositives += 1
        
        if label == 0:
            totalNegatives += 1

        if prediction != label:
            continue
        
        if prediction == 1:
            correctPositives += 1
            continue

        if prediction == 0:
            correctNegatives += 1

    sensitivity = correctPositives / totalPositives
    specificity = correctNegatives / totalNegatives
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
