# repos_1
This is my first git repos so please forgive any inevitable things I will have missed.

This is the code for one of my data collection projects on thecompleteuniversityguide.co.uk. 
I collected data from the site and compared things like entry standards vs graduate prospects, percentage of international students vs 
graduate prospects and research quality, etc. I also recorded the most common tags used on each university page to see what unis believe 
are the most attractive features to prospective students.

This is one of the groups of files I'd already completed before I started using Git(hub), so the formatting is very basic.

All of the programs have been commented. There are 3 main programs, each operating on 115 universities:

# controcorrelation.py
This program compares the proportion of international students at a given university with its percentage-normalised research quality and graduate prospects to search for a correlation.
This is a controversial topic given how the results effectively suggest that more ethnically diverse universities perform better by a non-negligible margin, although the PMCC is
quite low (just below 0.4). However, I believe that given the large sample size, there is sufficient evidence to back this claim. The data was plotted on 2 scatter plots, one for
research quality and the other for graduate prospects.

# attempt 1.py
This program compares the student entry standards with the graduate prospects on a scatter plot, based on the cynical idea that universities raise their entry standards so that they
can obtain stronger students, which in turn means greater graduate prospects without actually having to invest further in their university. Of course, this trend is
accurate, and the non-coded PMCC for this graph was nearly 0.7, suggesting a strongly linear relationship. I've also colour coded the data points by student satisfaction to see if 
stronger students are also more dissatisfied (if so, this would support the theory) but I didn't notice any meaningful colour pattern in the results, so I did not conduct further
analysis on it.

# names.py
This program takes each university's page on thecompleteuniversityguide and examines the 4 subsections: student support, facilities, student life, and employability. For each section
it records the tags (bubles) that the university chooses and adds them to a counter. Once this is done for all universities (the program can only retrieve about 100 due to some unis
having unconventional names) a pie chart for each is constructed, allowing us to visualise what universities believe is the most important set of attributes that will attract
prospective students.



If you want to see the finished results, you can find them on my LinkedIn page:
https://www.linkedin.com/in/david-litchfield-1a6b27274/
