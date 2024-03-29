# ASAPP Challenge Project

ASAPP NLP / ML Engineering Challenge
====================================

Welcome to your challenge project!

For this challenge, we ask that you implement a solution and write up answers to the follow-up questions at home in your own time. When you're ready, please send us your code and results. We estimate that the challenge should take somewhere between 5 and 10 hours depending on your experience and speed.

To keep the process fair for everyone, we ask that you do not share or publish the challenge or your solution to it.


Motivation
----------


ASAPP builds state of the art Natural Language Processing and Machine Learning tools that empower human customer service representatives to become 10X more efficient than they are today. A key ingredient is our auto-complete service, which significantly speeds up the customer service representatives' responses.

Your challenge is to design and implement an auto-complete server using the sample chat histories in sample_conversations.json. The basic idea is for the agent to type a few letters or words, and the service will suggest sentence completions. Prepare to talk through how you might improve on your results, as well as what the challenges would be around scaling it up to a corpus of a billion conversations. 

This isn’t a research project, so please don’t focus on learning and implementing the state of the art. The goal instead should be to write well-written code that gives results that would be useful for a real customer service agent. 

If we mutually agree to proceed then your work will form the basis for a 30-minute followup phone-call.

Recommendations
---------------

- Focus on a solution that gets the task done well and is clearly understandable.  We prefer correctness and clarity over a highly complicated solution that doesn't perform well and is hard to follow.  High quality results and high quality code are most important to us.
- While you can do the assignment in any language you want, we mainly use Python 3 on our ML team.  We can more realistically evaluate your code if you work in Python.
- Use the tools that you're most familiar with.
- Use version control. It's a plus if your results come with e.g a git commit history.
- Use open source libraries instead of reinventing the wheel. (For example, we use Pandas, Scikit-learn, NLTK, Tornado, etc.)
- If any part of your submission was not written by you, please indicate the source in comments near to the specific code.
- Add tests to ensure the correctness of your code.
- Have fun! If you don't think this project sounds like fun, then working at ASAPP may not be your cup of tea :)


Goals
-----

1: Offline data processing

    · Write a function that reads the sample_conversations.json file, processes the data, and creates whatever data models you need to generate realtime auto-completions.
    · It's fine if this function takes a very long time to run. However, a week is probably a bit too long :)
    · Extra credit: Make the processed data model serializable, so that it can be saved to disk once it's been constructed

2: Realtime autocomplete

    · Write a function that uses the data model from step 1 and takes a text input prefix and sentence completions. Here are some examples of what it could look like:
    
        generate_completions('how ca') -> ['How can I help you today?']
        generate_completions('what is y') -> ['What is your account number?', 'What is your address?', 'What is your order number?']
        generate_completions('when w' -> ['When was the last time', 'When was the last time you changed your password?', 'When was the last time you rebooted your router?'])
    
    · This function should be *fast*! It would be called on every keystroke, so hundreds of times per second per server.
    · The input of the function should be a partial message input, and the output should be a small list of completions. Try to generate outputs that you believe would be genuinely useful for a customer service representative.

3: Autocomplete server

    · Wrap the realtime autocomplete engine in an HTTP server, and return completions as JSON, e.g.
    
        # curl http://localhost:13000/autocomplete?q=What+is+y
        {"Completions": ["What is your account number?", "What is your address?", "What is your order number?"]}


Follow-up questions
-------------------

Please take the time to write answers to these questions along with your solution. Think through them as thoroughly as you can. Our goal will be to get a sense of how comprehensively you understand and think about the type of problems we face.

It's fine if you don't have concrete answers to all of them. We would still want to hear your thought process. Sometimes asking the right questions is even more important than finding the answer.

- How would you evaluate your autocomplete server? If you made another version, how would you compare the two to decide which is better?

- One way to improve the autocomplete server is to give topic-specific suggestions. How would you design an auto-categorization server? It should take a list of messages and return a TopicId. (Assume that every conversation in the training set has a TopicId).

- How would you evaluate if your auto-categorization server is good?

- Processing hundreds of millions of conversations for your autocomplete and auto-categorize models could take a very long time. How could you distribute the processing across multiple machines?
