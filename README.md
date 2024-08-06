**What does approach do?**

Evaluating and Improving ChatGPT-Based Expansion of Abbreviations

**How to obtain source code?**

The replication package can be downloaded from https://github.com/publicSE/ChatGPT-based-Expansion

**What does the replication package contain?**

There are two folders within the replication package:

**/Code:** The source code of ChatGPT-Based Expansion of Abbreviations

**/Dataset:** Data to replicate the evaluation in the paper


**Step-by-step running ChatGPT-Based Expansion of Abbreviations:**

1. Is ChatGPT accurate in expanding abbreviations in source code?
 
    `python basicPrompt.py`

2. To what extent can we improve the performance of ChatGPT-Based abbreviation expansion by including the enclosing file

    `python basicPromptEnclosingFile.py`

3. To what extent can we improve the performance of ChatGPT-Based abbreviation expansion by including the knowledge graph
    
    `python basicPromptKnowledgeGraph.py`

4. To what extent can we improve the performance of ChatGPT-Based abbreviation expansion by including the surrounding code
   
    `python basicPromptContext.py`

5. To what extent can we improve the performance of ChatGPT-Based abbreviation expansion by explicitly marking missed abbreviations

   `python basicPromptContexWithAbbrDecision.py`

6.  To what extent can we improve the performance of ChatGPT-Based abbreviation expansion by post-condition checking
 
    `python basicPromptContexWithAbbrDecisionSubsequence.py`

