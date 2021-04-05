For the instructions, please see instructions.md.

Solution Outline
----------------
For the sake of simplicity, I chose to solve the following problem.

_Given a corpus of text and a phrase prefix, return the top phrases containing the given prefix ranked by frequency in the corpus. If no phrase containing the input prefix is in the corpus, return an empty list._

Observe that this requires a large corpus containing most foreseeable input phrases. The given corpus (sample_conversations.json) seems to be large enough to yield useful results in many cases; hence, this solution may be useful to a customer service representative. 

Since we want the autocomplete engine to be fast, it would be ideal if we could precompute every answer for every possible input. This inspires the solution I used. Broadly, I took each sentence from the corpus that a customer service representative used and inserted it into a prefix tree. The prefix tree behaves like a set in that checking membership requires time proportional to the length of the input object. However, one major advantage that a prefix tree has over a set is that we can store prefix metadata at each node. This is where we store correct answers: we store a list of suffixes at every node and order this list by frequency. 

A query to the autocomplete engine thus boils down to a lookup of the prefix in this prefix tree and returning the top k entries in the appropriate list of suffixes. For more details, please see autocomplete.py.

Files
-----
Here's all the files I used in my project.

    - autocomplete.py : contains an implementation of the prefix tree data structure and an autocomplete engine implementing a basic autocomplete interface.
    - autocomplete_server.py : contains an implementation of a very basic web server that accepts a query in the URL and returns JSON with the query results.
    - autocomplete_test.py : contains test cases for the prefix tree data structure, the correctness of which is crucial to the entire program and is the hardest to verify.  
    - util.py : contains a few utility functions.

Running
-------
To run all tests:

    python3 autocomplete_tests.py. 

To start the web server:

    python3 autocomplete_server.py

To obtain text completions while the web server is running: 

    curl http://localhost:8080/autocomplete?q=< your_query_here > 


Follow-up questions
-------------------
_How would you evaluate your autocomplete server? If you made another version, how would you compare the two to decide which is better?_

Broadly, there are a few categories under which the autocomplete server should be evaluated. In no particular order:

- Speed of predictions. Measuring this is easy - sample from some realistic distribution of queries, hit the server with these queries, and measure the average response time.
- Quality of predictions. This is somewhat more subjective. One way to measure this is to have users rate the suggested completions; the server with the highest ratings wins. This is also useful if one wants to refine the ranking methodology. Another way to measure this is to consider every phrase prefix in the dataset (or in some held-out test set, which can be constructed by splitting the provided dataset into a training/test sets) and check how many suffixes are correctly predicted. 
- Complexity of model updates. If the model never changes, then this is not an issue. However, if the corpus is growing or if certain phrases are used with decreasing frequency over time, then one may have to recreate the model periodically. This can become cumbersome as the update frequency increases and as the model becomes increasingly difficult to recreate or update. 
- Interpretability of the model. All else equal, one prefers a model whose predictions are easier to understand and explain. 

_One way to improve the autocomplete server is to give topic-specific suggestions. How would you design an auto-categorization server? It should take a list of messages and return a TopicId. (Assume that every conversation in the training set has a TopicId)._

For each TopicID, we can construct a list of the most frequently used (nontrivial) words occurring in each discussion involving the TopicID. This can be done in some offline preprocessing step. Then, for each query, we can rank candidate TopicIDs by keyword presence in the query (for a fixed query, which TopicID is most well-represented in terms of keyword presence in the query?). We then return the topmost TopicID (or a ranking of the TopicIDs). This is an easily interpretable and straightforward solution; however, it might be too naive to be universally useful. 

For our solution, we therefore require some dictionary of trivial words so that we can appropriately filter these out when constructing the keyword set to TopicID mappings. Once our preprocessing is complete, we can construct a map mapping keywords to TopicIDs that they appear in. Upon receiving a query, we iterate over the words in the query and compute some histogram of TopicIDs, where the frequencies come from our map. We then sort the histogram by frequency and return the most frequently seen TopicIDs. 

_How would you evaluate if your auto-categorization server is good?_

Similar to the first question, there are a few criteria to evaluate. We can use the same methodology to evaluate the criterion as stated in the first question:

- Speed of predictions.
- Quality of predictions.  
- Complexity of model updates.
- Interpretability of the model. 

_Processing hundreds of millions of conversations for your autocomplete and auto-categorize models could take a very long time. How could you distribute the processing across multiple machines?_

The solution for the autocomplete problem that I implemented can be (at least, intuitively) scaled easily to many machines and many conversations. Since each branch in this prefix tree results in an independent subtree, at some fixed depth, every subtree can be stored on a unique machine. Then, the processing of disjoint queries can be parallelized. To prevent reprocessing of frequently used queries, we can cache the answers to FAQs using a similar data structure to the one used for the full model.

The autocategorize problem can also be scaled similarly. We can store our map of keywords across multiple machines; we can then parallelize the processing of phrases, making one thread per phrase and computing the histograms for each phrase independently. Finally, we can add up each histogram and proceed as normal. 
