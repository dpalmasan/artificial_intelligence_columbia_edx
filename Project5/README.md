# Project 5

Given the exponentially growing of online review data (Amazon, IMDB and etc), sentiment analysis becomes increasingly important. We are going to build a sentiment classifier, i.e., evaluating a piece of text being either positive or negative.

The "Large Movie Review Dataset"(*) shall be used for this project. The dataset is compiled from a collection of 50,000 reviews from IMDB on the condition there are no more than 30 reviews each movie. Number of positive and negative reviews are equal. Negative reviews have scores lesser or equal 4 out of 10 while a positive review greater or equal 7 out of 10. Neutral reviews are not included on the other hand. Then, 50,000 reviews are divided evenly into the training and test set.

Dataset is credited to Prof. Andrew Mass in the paper, Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. (2011). <a href="http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf">Learning Word Vectors for Sentiment Analysis</a>. The 49th Annual Meeting of the Association for Computational Linguistics (ACL 2011).

These are my solutions for the project 5. The project consisted on implementing sentiment analysis (NLP Task).

* driver.py: The main file for the project. Contain functions for loading data, preprocessing, creating document-term matrices and applying Stochastic Gradient Descent for learning a classifier of sentiments.

The data used for this project, can be downloaded here: <a href="http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz">Training data</a>, 
<a href="https://d37djvu3ytnwxt.cloudfront.net/assets/courseware/v1/9dbe589c9a231b5174729e059a17e8eb/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block/imdb_te.csv.zip">Test Data</a>

## To execute the codes:

`python driver.py`



