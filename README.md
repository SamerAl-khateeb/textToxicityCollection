# textToxicityCollection
This repository has Python script that can be used to collect the toxicity score of a given text (e.g., Tweets) using Google Perspective API

## getToxicityScores.py
This script reads each row in the **input_file.csv** file, take the second column which contain the text, make a request to Google Perspective API to determine the text toxicity, then write the output to another CSV file called **outputWithToxicityScoreDateofToday.csv**

### Input & Output
Input: **input_file.csv** this sample file contain the expected file format which will work with the provided code without any code modification. However, if the input file change in format, the Python script need to be updated as well to reflect the change in the input file, e.g., this file assume the second column contain the text, if the text is not in the second column, the code might not work or give incorrect results.

Output: **outputWithToxicityScoreDateofToday.csv** this file will be generated one the code successfully run. it will contan the input file columns + one column containing the toxcity score as returned by Google Perspective API. The score in range on 0-1, 1 represnet the maximum toxicty score (given to very toxic texts).