# cheatX
Plagarism detection tool.

cheatX uses machine learning to be able to detect plagarism in text by automating the all
the reading and comparing text. In a way such that, anyone willing to detect any type of
plagiarism, can download the available CheatX application. Once downloaded, multiple files
can be imported and all files selected will be compared to each other. Any user that has
downloaded the CheatX application can view the plagiarism results by percentage and the
uniqueness by percentage as well. The CheatX application can also display the plagiarized
text which either a paraphrased text or a text that is similar and detected.


Features:
Compare multiple files together
Detect the exact sentences that are copied from other documents 
Detect text that is paraphrased from other documents
Display the percentage of the plagiarism
Display the sentences/paragraphs that have plagiarism


how it works:
The algorithm used is the universal sentence encoder which is for embedding sentences. It
makes getting sentence-level embeddings as easy as it has historically been to lookup the
embeddings for individual words. The sentence embeddings can then be trivially used to
compute sentence-level meaning similarity as well as to enable better performance on
downstream classification tasks using less supervised training data. The universal sentence
encoder model encodes textual data into high dimensional vectors known as embeddings
which are numerical representations of the textual data. It specifically targets transfer
learning to other NLP tasks, such as text classification, semantic similarity, and clustering.
The pre-trained universal sentence encoder is publicly available in Tensorflow-hub. After
getting the entire embedding the algorithm compares it with the pre trained module and get
the accurate result.

how to use:
1) Run source code
2) Upload pdf Files 
3) Choose type of test
4) Display Results
