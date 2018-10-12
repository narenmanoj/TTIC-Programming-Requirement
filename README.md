ASAPP NLP / ML Engineering Challenge
====================================
Here's my solution to the ASAPP Engineering Challenge. For the instructions, please see instructions.md.

Solution Outline
----------------
For the sake of simplicity, I chose to solve the following problem.
_Given a corpus of text and a phrase prefix, return the top phrases containing the given prefix ranked by frequency in the corpus. If no phrase containing the input prefix is in the corpus, return an empty list._
Observe that this requires a large corpus containing most foreseeable input phrases. The given corpus (sample_conversations.json) seems to be large enough to yield useful results in many cases; hence, this solution may be useful to a customer service representative. 

Since we want the autocomplete engine to be fast, it would be ideal if we could precompute every answer for every possible input. This inspires the solution I used. Broadly, I took each sentence from the corpus that a customer service representative used and inserted it into a prefix tree. The prefix tree behaves like a set in that checking membership requires time proportional to the length of the input object. However, one major advantage that a prefix tree has over a set is that we can store prefix metadata at each node. This is where we store correct answers: we store a list of suffixes at every node and order this list by frequency. 

A query to the autocomplete engine thus boils down to a lookup of the prefix in this prefix tree and returning the top k entries in the appropriate list of suffixes. For more details, please see autocomplete.py.

Files
-----
- autocomplete.py : contains an implementation of the prefix tree data structure and an autocomplete engine implementing a basic autocomplete interface.
- autocomplete_server.py : contains an implementation of a very basic web server that accepts a query in the URL and returns JSON with the query results.
- autocomplete_test.py : contains 

Running
-------
To run all tests, please call python3 autocomplete_tests.py. To start the web server, please call python3 autocomplete_server.py. To obtain text completions while the web server is running, please call curl http://localhost:8080/autocomplete?q=< your_query_here > 


Follow-up questions
-------------------
- _How would you evaluate your autocomplete server? If you made another version, how would you compare the two to decide which is better?_

Broadly, there are a few categories under which the autocomplete server should be evaluated. In no particular order:
- Speed of predictions. Measuring this is easy - sample from some realistic distribution of queries, hit the server with these queries, and measure the average response time.
- Quality of predictions. This is somewhat more subjective. One way to measure this is to have users rate the suggested completions; the server with the highest ratings wins. This is also useful if one wants to refine the ranking methodology. 

- _One way to improve the autocomplete server is to give topic-specific suggestions. How would you design an auto-categorization server? It should take a list of messages and return a TopicId. (Assume that every conversation in the training set has a TopicId)._

- _How would you evaluate if your auto-categorization server is good?_

- _Processing hundreds of millions of conversations for your autocomplete and auto-categorize models could take a very long time. How could you distribute the processing across multiple machines?_
