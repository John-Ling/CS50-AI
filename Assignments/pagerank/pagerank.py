import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    distribution = {}
    linkCount = len(corpus[page])

    if linkCount == 0:
        # Divide probability evenly
        value = 1 / len(corpus)
        for page_ in distribution:
            distribution[page_] = value

        return distribution

    # With probability 1 - damping_factor random surfer should choose one of all pages in corpus with equal probability
    startingValue = (1 - damping_factor) / len(corpus)
    for page_ in corpus:
        distribution[page_] = startingValue
    
    # Divide damping_factor amongst all other pages linked to page
    value = damping_factor / linkCount
    for page_ in corpus[page]:
        distribution[page_] += value

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    Implementation Ideas and Details:
    Page Rank =  the proportion of all the samples that corresponded to that page

    function sample_pagerank(corpus, dampingFactor, n)
        create list of all pages
        create dict of all pages with values set to 0
        generate random page from the list and remove it 
        while samples still left
            call transition_model() with the previous sample
            create random value between 0 and 1
            match random value to the correct page generated through transition model to a sample
            add 1 to that corresponding page
            remove sample from list
        endwhile
        
        perform maths stuff on dict to normalise values and make them add to 1
    endfunction
    """

    if n < 0: raise RuntimeError

    pageRanks = { page: 0.0 for page in corpus }

    currentSample = random.choice(list(corpus))
    pageRanks[currentSample] += 1
    
    for _ in range(n - 1):
        # get the probabilities for the next sample
        distribution = transition_model(corpus, currentSample, damping_factor)
        nextPage = random.choices(list(distribution.keys()), list(float(value) for value in distribution.values()), k=1)[0]
        pageRanks[nextPage] += 1
        currentSample = nextPage

    for page in pageRanks: # Normalise values
        pageRanks[page] = pageRanks[page] /  n
    
    assert sum(pageRanks.values()) == 1

    return pageRanks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    function iterate_pagerank(corpus, dampingFactor)
        create dict for page ranks
        create identical dict called previous
        set each page's page rank to 1 / N where N is the total number of pages in in corpus

        while significantDifference == true
            create dict buffer
            for page in corpus
                pageRank of page = (1 - dampingFactor) / N + dampingFactor * sigma function(probabilitie of page i in previous / num_links(i))
                write value to buffer
            next page

            dict = deep copy of buffer

            if all values in dict and previous have a difference of 0.001 then
                significantDifference = false
            endif
            previous = dict
        endwhile

    endfunction

    For each item in the corpus they should have a calculated page rank value
    which is formed using (1 - d) / N + d * the total of PR(i) / NumLinks(i) where
    i refers to the pages that link to the page you want to know the page rank of

    """

    pageCount = len(corpus)
    pageRanks = { page: 1 / pageCount for page in corpus }
    previousRanks = { page: 1 / pageCount for page in corpus }

    # is only false when the difference between elements in pageRanks and previousRanks are all within 0.001
    significantDifference = True

    while significantDifference:
        for page in corpus:
            # Calculate summation 
            summation = 0
            for page_ in corpus:
                # find number of links on page    
                linkCount = len(corpus[page_])
                if linkCount == 0: # if a page has no links at all
                    linkCount = pageCount

                # Check if page_ links to page if so we include it
                if page in corpus[page_] and page != page_:
                    summation += previousRanks[page_] / linkCount
            
            pageRanks[page] = (1 - damping_factor) / pageCount + damping_factor * summation

        significantDifference = False
        for page in corpus:
            if abs(pageRanks[page] - previousRanks[page]) > 0.001:
                significantDifference = True
                break
        
        previousRanks = copy.deepcopy(pageRanks)

    assert sum(pageRanks.values()) == 1

    return pageRanks

if __name__ == "__main__":
    main()
