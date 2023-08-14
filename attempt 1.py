# This program attempts to find any link / correlation between the entry standards of universities, and the graduate prospects of students after leaving uni
# The obvious hypothesis is that universities with greater entry requirements will get better graduate standards, since good students coming in are probably going
# to be good students coming out of uni (and vice versa in the general case)

# As a bonus, I'll also add student satisfaction as the colour dimension so maybe there's a correlation there too? The better students are happier/more miserable?

import requests as rq
from bs4 import BeautifulSoup as BS

# Beep boop. I'm a human.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

# Ditto ^
params = {
    'sort': 'dd',
    'filter': 'reviews-dd',
    'res_id': 18439027
}

# I only understand pixels. A pixel is 1/96 of an inch apparently
px = 1/96

# Parse the incoming data
get_the_data = rq.get("https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/computer-science", headers=headers).text
soup = BS(get_the_data, "html.parser")

# Find the league tables themselves, this seeming gibberish is actually the tags required to find them
tables = soup.find("div" , {"class" : "tabl_wrap clr tabl_div"}).find("div" , {"class" : "rgt_col swiper-container swiper-container-initialized swiper-container-horizontal"})

# The tables are organised so thaat rt_list(x) is just the (x+1)th column on the table, so easy to read from
# They're all given the class of "col_one"

# Each element in these lists is actually just a tag, we need to extract the actual percentage from the tag using an element-wise function
# The ordering of this data is important, because entry_standards_data[i] is supposed to be mapped to grad_prospects_data[i] and student_satisfaction_data[i]
# So a change in the ordering of a list could result in data mismatches which would wipe out the data
entry_standards_data = tables.find("li" , {"class" : "swiper-slide rt_list2 swiper-slide-next"}).find_all("div" , {"class" : "col_one"})
student_satisfaction_data = tables.find("li" , {"class" : "swiper-slide rt_list3"}).find_all("div" , {"class" : "col_one"})
grad_prospects_data = tables.find("li" , {"class" : "swiper-slide rt_list6"} ).find_all("div" , {"class" : "col_one"})

# And that function is this one
# Converts tag to the numerical value
def convert(x):
    # If the data is N/A then it will not be possible to get the numerical data
    try:
        # This long complicated expression just extracts the string % value, kills the % at the end and casts to an int (always int percentages)
        return int( x.find("span" , {"class" : "smtxt"}).text[:-1:])
    except:
        # If data is N/A then just return -1 to make it obvious
        return -1
    
# It's graphin' time. (graphs all over the place)
    
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Darkred - yellow - lime/green, a colourmap I took from EU4
my_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["darkred", "yellow", "lime"], N=256) 

# This converts the obtained data into integer form so it can be plotted - order is preserved
entry_standards = [ convert(x) for x in  entry_standards_data] 
student_satisfaction =  [ convert(x) for x in  student_satisfaction_data]
grad_prospects = [ convert(x) for x in  grad_prospects_data] 

# This section of code removes any data points which have N/A values since this would skew our graph with anomalous results
# If a data point has an N/A datapoint, we also need to delete the corresponding 2 other pieces of data (student satisfaction, grad_prospects for example)
# So that no piece of data on the x-axis doesn't have a value to be mapped to
for i,v in enumerate(entry_standards):
    if entry_standards[i] == -1 or grad_prospects[i] == -1 or student_satisfaction[i] == -1:
        # If any N/A data, delete them all!
        entry_standards.remove(v)
        grad_prospects.remove(grad_prospects[i])
        student_satisfaction.remove(student_satisfaction[i])

# Since student satisfaction is quite universally 80-90% ish, we need to code the data so that min =0, max =100 so that we can see some proper colour contrast
min_satisfaction = min(student_satisfaction)
max_satisfaction = max(student_satisfaction)

# This coding formula will accomplish this goal for us
student_satisfaction = [ ( x - min_satisfaction ) * (100 / (max_satisfaction-min_satisfaction)) for x in student_satisfaction]

# The following data will be used to calculate the coefficients of our regression line (y=mx+b) and the PMCC (r) to determine the strength of the correlation
# If you want to understand this, learn stats, this is just copying the mathematical formulae

# This is all the data we need to calculate m,b and r
n=len(grad_prospects)
xy_sum = sum( [ entry_standards[i] * grad_prospects[i] for i in range(n)] )
x_sum =sum(entry_standards)
y_sum = sum(grad_prospects)
x_2_sum = sum([ x*x for x in entry_standards] )
avg_x = x_sum / n
avg_y = y_sum / n

# Using the formulas and the above parameters to determine the values of the coefficients m, b and r
m = (n * xy_sum - x_sum * y_sum) / (n * x_2_sum - (x_sum)**2 )
b = (y_sum - m * x_sum) / n
r = ( sum( [ ( entry_standards[i] - avg_x ) * ( grad_prospects[i] - avg_y ) for i in range(n)  ] ) 
     / ( sum( [( entry_standards[i] - avg_x ) ** 2 for i in range(n) ] ) * ( sum( [( grad_prospects[i] - avg_y ) ** 2 for i in range(n) ] )  )  ) ** 0.5 )

# This np array will be the x-axis for our regression line
x = np.arange(0,101)


# Generating the plots
fig, ax = plt.subplots(figsize=(1920*px, 1080*px))

# Grid so easier to see and understand
plt.grid(True)

# We need to see the variance from 0-100%, so I set the limits to be from 0-100%
plt.xlim(0,100)
plt.ylim(0,100)

# Plot the results
the_scatter_plot = ax.scatter(entry_standards, 
                              grad_prospects, 
                              s=32, edgecolor="black", 
                              c=student_satisfaction, 
                              cmap=my_cmap,
                              label="Results")

# Plot the regression line with the label explaining what the coefficients are, limit to reasonable number of decimal places
the_approx = ax.plot(x, m*x + b, label=f"y = {m:.2f}x + {b:.2f}, r = {r:.3f}")

plt.title("Entry standards vs Graduate prospects (Computer Science)")

plt.xlabel("Entry standards (0-100)")
plt.ylabel("Graduate prospects (0-100)")
plt.colorbar(mappable=the_scatter_plot, extend="both",label="Student satisfaction (coded: min = 0, max = 100)   ")

plt.legend()
plt.savefig("here")
# plt.show()
