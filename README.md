# cset-ds-task

# 1

## a
1051 papers reference facial recognition or related topics in their titles or abstracts. 

## b
31389 papers have facial recognition as a category. 83.73% of the 1051 papers above are part of this group.
Conversely, only 2.8% of the papers in the computer vision category have something about facial recognition
in their title or abstract. 880 papers fall in both groups. In other words, the vast majority of papers 
about facial recognition fall under the broader category of computer vision, but relatively little of the 
literature on computer vision has to do with facial recognition. 

## c
I think my solution to (a) is a good first attempt, but could certainly be improved. I thought about using spacy
to lemmatize the words, but I tried it out and found that all of the synonyms I was considering are lemmas anyway.
Perhaps the most questionable choice I made is to make it so that the words have to appear next to each other in the
title or abstract. This is potentially valuable, and potentially faulty. It might underestimate the true amount of 
papers that talk about facial recognition in their titles or abstracts, but I thought that the inverse, allowing the
words facial or recognition to appear anywhere independtly in the title and abstract, would be much too wide a net.

# 2

## a
![2a_plot_basic](https://github.com/mmerrittsmith/cset-ds-task/blob/main/papers_started_by_year.png?raw=true)
First, note that for the plot above I extrapolated the count for 2019 from the 9 months of data we have to the full year.
That might be faulty since I would expect that November and December have lower research output than other months.
Research output relevant to facial recognition visually appears to be increasing exponentially y.o.y., but in reality it
had a huge surge of growth from 2009 to 2010 and has since been growing steadily and slowly. In absolute terms, the biggest years
of growth are from 2016-17 and 2017-18. Facial recognition is growing as a % of the total research output. 
I think it would be a mistake to try to fit this as a regression with a squared term, it seems more likely to
be a linear relationship with time. This timeline makes sense, given that random forests were the state of the art in ML
around 2008 but were superseded by neural nets by 2012.

![2a_plot_pct](https://github.com/mmerrittsmith/cset-ds-task/blob/main/papers_started_pct_change.png?raw=true)

![2a_plot_pct_of_total](https://github.com/mmerrittsmith/cset-ds-task/blob/main/fr_papers_as_pct_of_total_by_year.png?raw=true)

## b
Facial recognition is a growing field. There were more papers started on ArXiv in one month of 2019 than in all of 2009. 
It's not exploding though, as that statistic might make it seem. Rather, there was a significant uptick in research volume
in the early 2010s which has led to slow, steady growth in the field that continues up to the end of this data in 2019.
Despite this growth, facial recognition research is only slightly more than .16% of the overall research papers submitted 
to ArXiv in 2019.
