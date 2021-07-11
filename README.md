# Information Retrieval

Algorithms for building inverted indexes, handling boolean queries, phrase queries, error correction, ranking documents (tf-idf + PageRank) and improving the query (relevance feedback) or the documents' representations (latent semantic indexing) are available.

## Indexing
Index builders are available for:
* Basic inverted index (each term is mapped to the document IDs of documents that contain it)
* Biword inverted index (each pair of term is mapped to the document IDs of documents that contain these terms consecutively)
* Positional inverted index (each term is mapped to the document IDs and for each ID there is the position of the term in that document)
* Inverted index with tf-idf score (each term is mapped to pairs [document ID, tf-idf score] of documents that contain it)

## Handling queries
Queries of different types can be handled:
* Boolean queries (using AND, OR, NOT)
* Phrase queries (with error correction based on either edit distance or n-grams)

## Ranking
Algorithms that give weights to documents are available:
* PageRank
* tf-idf scoring
* Hybrid algorithm that uses both

## Improvements
Some algorithms to improve query or document representation are available:
* Rocchio's algorithm (relevance feedback)
* Latent Semantic Indexing (improves document representation)

## Empirical Laws
There is some code to check and plot some empirical laws including:
* Heap's Law (there is a log-log relation between the total number of tokens in the corpus and the number of unique terms)
  * It suggests that the dictionary size (# of unique terms) always increase when there are more documents in the collection
* Zipf's Law (the ith most frequent term has frequency proportional to 1/i)
  * It suggests that there are few very frequent terms and many very rare terms in the collection
