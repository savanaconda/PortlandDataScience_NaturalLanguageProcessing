# Portland Data Science Natural Language Processing

Work on Natural Language Processing at the Portland Data Science Meetup


System Requirements: Python, Pandas, Numpy, Requests, BS4, NLTK, Langdetect, Lxml

Code: isitenglish.py
Input files: boardgame-frequent-user-comments.csv
Output files: english_comments.csv, non_english_comments.csv, google_english_comments.csv, google_non_english_comments.csv


This python script looks a board game review comments and attempts to determine
if the comments are english or not. To do this, it scraps the 100 most common words
in English from a wikipedia page, then breaks the board game comments into individual words.
If a comment contains one of the 100 most common words, it is deemed English.

This algorithm is somewhat limiting as it fails if any of the 100 most common words
in English happen to exist in another language. Also, this algorithm fails if the comment is
too short (a common challenge). The code will warn the user that a comment is too short (less
than 4 words) to process.

Further, I loaded Google's public port of one of their language detection algorithms
to compare my results to their results. This algorithm had a similar challenge with
short comments as well

Results are printed in 4 csv files: english comments and non-english comments (my
algorithm) and google english comments and google non-english comments
