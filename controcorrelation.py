import requests as rq
from bs4 import BeautifulSoup as BS, Comment

# These functions are useful when creating URLs since all names get translated like this, e.g "University of Cambridge" -> "university-of-cambridge" 
# These functions perform this translation nearly perfectly (with a few edge cases but not worth the effort, only 1/100 or something)
def urlify(name):
    # Remove all commas, hyphens (these are never in URLs) and replace the spaces with the special "-" symbol, this completes the URLification
    return name.replace(",","").replace("'","").lower().replace(" ", "-")

# Inverse function, : urlify(deurlify(x)) = x (and vice versa)
def deurlify(name):
    # Remove the hyphens, we'll join them with the spaces at the end
    name = name.split("-")
    # All the indiv. words are capitalised, so we should do the same
    name = [x.capitalize() for x in name]
    # Once all names have been capitalised, join them with spaces instead of dashes to complete the string
    name = " ".join(name)
    return name

# These are copy-pasted tags to convince websites that we're human
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

params = {
    'sort': 'dd',
    'filter': 'reviews-dd',
    'res_id': 18439027
}

# List of names that thecompleteuniversityguide will read from
names = ['University of Cambridge', 'University of Oxford', 'Imperial College London', 'Durham University', 'UCL (University College London)', 'University of Bath', 'University of Birmingham', 'The University of Edinburgh', 'University of Southampton', 'University of St Andrews', 'University of Sheffield', 'University of Warwick', 'University of Manchester', "King's College London, University of London", 'University of Bristol', 'University of Glasgow', 'Loughborough University', 'University of York', 'University of Exeter', 'University of Nottingham', "Queen's University Belfast", 'Lancaster University', 'University of Leeds', 'University of Surrey', 'Royal Holloway, University of London', 'Cardiff University', 'Newcastle University', 'University of Dundee', 'Aberystwyth University', 'University of Strathclyde', 'Queen Mary University of London', 'University of East Anglia UEA', 'Heriot-Watt University', 'University of Liverpool', 'University of Kent', 'University of Reading', 'Swansea University', 'University of Leicester', 'City, University of London', 'Aston University, Birmingham', 'University of Sussex', 'Liverpool Hope University', 'University of Aberdeen', 'University of Lincoln', 'Ulster University', 'University of Essex', 'Bristol, University of the West of England', 'Manchester Metropolitan University', 'University of Huddersfield', 'Edge Hill University', 'Oxford Brookes University', 'Bangor University', 'University of Plymouth', 'University of Stirling', 'Nottingham Trent University', 'University of Hull', 'Brunel University London', 'Northumbria University, Newcastle', 'Edinburgh Napier University', 'Abertay University', 'University of Portsmouth', 'University of Hertfordshire', 'Keele University', 'Canterbury Christ Church University', 'Leeds Beckett University', 'Liverpool John Moores University', 'Falmouth University', 'University of Chichester', 'Bournemouth University', 'University of Brighton', 'Kingston University', 'Birmingham City University', 'University of Bradford', 'Staffordshire University', 'University of Winchester', 'Robert Gordon University', 'University of the Arts London', 'Bath Spa University', 'Glasgow Caledonian University', 'Coventry University', 'Goldsmiths, University of London', 'Sheffield Hallam University', 'University of Salford', 'University of Derby', 'University of East London', 'University of South Wales', 'University of Westminster, London', 'University of Greenwich', 'University of Worcester', 'De Montfort University', 'Teesside University, Middlesbrough', 'University of Chester', 'University of Central Lancashire', 'Cardiff Metropolitan University', 'London South Bank University', 'University of West London', 'Solent University (Southampton)', 'University of Gloucestershire', 'University of Sunderland', 'University of the West of Scotland', 'University of Buckingham', 'University of Northampton', 'Norwich University of the Arts', 'University for the Creative Arts', 'University of Suffolk', 'Glyndwr University, Wrexham', 'York St John University', 'Middlesex University', 'University of Bolton', 'Buckinghamshire New University', 'Anglia Ruskin University', 'University of Bedfordshire', 'University of Wales Trinity Saint David', 'London Metropolitan University', 'University of Wolverhampton']

# These lists will store all the data we're interested in
# The values will be connected implicitly via their ordering, e.g if names[i] == "Imperial College London", then ethnicpercs[i] gives the ethnic percentage of Imperial College London

# This stores the other pieces of data we want - this stores the ethnic percentages (international / EU students) of each uni 
ethnicpercs = []

# This stores the "Graduate Prospects" scores of each uni
prospectscores = []

# "Research Quality" scores of each uni
qualityscores = []

# Stores the population sizes of each uni, this became redundant since thecompleteuniversityguide doesn't give exact values for uni populations (e.g 15000-25000)
# I didn't remove it because I would never need this code ever again so why bother
sizes = []

get_the_data = rq.get("https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/", ).text

# Parse it with BS so we can extract the data in a way that doesn't make us want to pull our hair out
soup = BS(get_the_data, "html.parser")

# I used inspect to find the tag names of all the important data - this collects all the numbers in the tables that we want
tables = soup.find("div" , {"class" : "tabl_wrap clr tabl_div"}).find("div" , {"class" : "rgt_col swiper-container swiper-container-initialized swiper-container-horizontal"})

# Their website was nice enough to divide the tags into these subsections. 
# Those list numbers (rt_list2,rt_list3,...) are just the order in which each column appears in the tables on the site, so easy to match them by inspection
# For some reason they were all tagged with "col_one" instead of the numbers, must be a design change

# These extractions won't give us the final data, just the tags that contain the final data - if the data is N/A it could cause a problem
# So we need a function to apply to each element that can do this for us and extract a order-preserving list (ordering connects the stats together) of the final values
entry_standards_data = tables.find("li" , {"class" : "swiper-slide rt_list2 swiper-slide-next"}).find_all("div" , {"class" : "col_one"})
student_satisfaction_data = tables.find("li" , {"class" : "swiper-slide rt_list3"}).find_all("div" , {"class" : "col_one"})
research_quality_data = tables.find("li" , {"class" : "swiper-slide rt_list4"} ).find_all("div" , {"class" : "col_one"})
grad_prospects_data = tables.find("li" , {"class" : "swiper-slide rt_list6"} ).find_all("div" , {"class" : "col_one"})

# This function "converts" the tag containing a piece of data into just the numerical data itself - e.g <tag>85%</tag> ----> 85 (as int)
def convert(x):
    # Sometimes the data will be N/A so need to account for this
    try:
        # Finds the actual data and cast to an int (will always be integer values)
        return int( x.find("span" , {"class" : "smtxt"}).text[:-1:])
    except:
        # In case the data is N/A
        return -1
    
# Now take our data and map them onto the actual numerical values - these will give us the lists of just the numbers themselves, no strings attached (literally)
# Again the index of each element details which uni it applies to, so must preserve this
entry_standards = [ convert(x) for x in  entry_standards_data] 
student_satisfaction =  [ convert(x) for x in  student_satisfaction_data]
research_quality = [ convert(x) for x in  research_quality_data]
grad_prospects = [ convert(x) for x in  grad_prospects_data] 

# Iterate through each uni's page on thecompleteuniversityguide to obtain its ethnic percentages, these stats are always contained on their page 
for i, name in enumerate(names):
    
    # Sanity check
    print(name)
    
    # Sometimes there's a timeout or urlify doesn't map correctly
    try:

        url = f"https://www.thecompleteuniversityguide.co.uk/universities/{urlify(name)}"
        
        page_found = rq.get(url, headers=headers, timeout=2).text
        
        # Parse so we can extract the data more easily
        soup = BS(page_found,"html.parser")
        
        # These get us the div containing the stats about the uni, including most importantly its ethnic percentages
        # These class names are just the ones containing the data we need, found through inspection
        wherefrom = soup.find("div" , {"class" : "st_lst stat4"})
        fields = wherefrom.find_all("div" , {"class" : "st_per"})
        
        # Like the convert function but I didn't realise this until it was already completed
        values = [int( x.find("span").text[:-1:] ) for x in fields]
        
        # Get the quality and grad prospects of this particular university 
        quality = research_quality[i]
        prospect = grad_prospects[i]
        
        # values[0] is the percentage of UK students, so 100 - values[0] = percentage of intnl. / EU students (I combined them together)
        ethnic_percentage= 100 - values[0]
        
        # Now add the data - because we add them all at once ordering is preserved
        ethnicpercs.append(ethnic_percentage)
        qualityscores.append(quality)
        prospectscores.append(prospect)

    # If it fails, it fails, don't bother trying again because the error will likely just happen again
    except:
        pass

# This chunk of code is designed to eradicate all data points with even a single N/A data point 
# Since all N/As get a score of -1 (and there's no "natural" score to map N/A to),
# we should just remove them as we don't want anomalous results tainting our plot     
for i,v in enumerate(prospectscores):
    
    # If either stat == -1 (indicates N/A value), remove it from both lists and the ethnic percs
    # Need to also remove from ethnicpercs so we preserve the implicit ordering property, so we don't get mismatches between unis and their data 
    if prospectscores[i] == -1 or qualityscores[i] == -1:
        # Kill them all!
        ethnicpercs.remove(ethnicpercs[i])
        prospectscores.remove(v)
        qualityscores.remove(qualityscores[i])   

# The following chunk of code is literally just the mathematical formulae for calculating our regression line and the PMCC
# I studied these from online and then just applied the formulae
# Go and learn some stats if you want to understand this
    
# This gathers the data itself, these aren't the values of the regression line functions but instead the values we'll use to calculate them
n=len(prospectscores)
xy_1_sum = sum( [ ethnicpercs[i] * qualityscores[i] for i in range(n)] )
xy_2_sum = sum( [ ethnicpercs[i] * prospectscores[i] for i in range(n)] )
x_sum = sum(ethnicpercs)
y1_sum = sum(qualityscores)
y2_sum = sum(prospectscores)
x_2_sum = sum([ x*x for x in ethnicpercs] )
avg_x = x_sum / n
avg_y1 = y1_sum / n
avg_y2 = y2_sum / n

# Sanity check to determine how many unis we have successfully gathered data from with no N/A values
print("N: " , n)

# Literally maths
# m1,b1 are the coefficients of the regression line mx+b, m1 and b1 for research quality, r1 is the PMCC
m1 = (n * xy_1_sum - x_sum * y1_sum) / (n * x_2_sum - (x_sum)**2 )
b1 = (y1_sum - m1 * x_sum) / n
r1 = ( sum( [ ( ethnicpercs[i] - avg_x ) * ( qualityscores[i] - avg_y1 ) for i in range(n)  ] ) 
     / ( sum( [( ethnicpercs[i] - avg_x ) ** 2 for i in range(n) ] ) * ( sum( [( qualityscores[i] - avg_y1 ) ** 2 for i in range(n) ] )  )  ) ** 0.5 )

# Respective ditto for m2,b2,r2, go and learn some maths if you want to understand this
m2 = (n * xy_2_sum - x_sum * y2_sum) / (n * x_2_sum - (x_sum)**2 )
b2 = (y2_sum - m2 * x_sum) / n
r2 = ( sum( [ ( ethnicpercs[i] - avg_x ) * ( prospectscores[i] - avg_y2 ) for i in range(n)  ] ) 
     / ( sum( [( ethnicpercs[i] - avg_x ) ** 2 for i in range(n) ] ) * ( sum( [( prospectscores[i] - avg_y2 ) ** 2 for i in range(n) ] )  )  ) ** 0.5 )

# It's graphin time.

from matplotlib import pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# This x array will be used to plot our regression line for both y1 = m1x+b1 and y2=m2x+b2
x = np.arange(0,105)

# I don't understand imperial units like inches, I only understand pixels
# Multiplying by this constant converts our figsize from being measured in inches to being measured in pixels
px=1/96

# Create our 2 subplots, we want high res so 1920 by 1080 px
fig, (ax1,ax2) = plt.subplots(ncols=2,nrows=1,figsize=(1920*px,1080*px))

# These scatter plots are the actual distributions themselves, not the regression lines
scatter_plot_1 = ax1.scatter(ethnicpercs, qualityscores, edgecolor="black",s=32,   c="yellow"             )
scatter_plot_2 = ax2.scatter(ethnicpercs, prospectscores, edgecolor="black",s=32,            c="yellow"          )

ax1.set_xlabel("Percentage of international students")
ax2.set_xlabel("Percentage of international students")

ax1.set_ylabel("Research Quality (percentage)")
ax2.set_ylabel("Graduate Prospects (percentage)")

# We don't want any data going beyond 100% obviously, how can you have more than 100% ethnic students
ax1.set_xlim(0,100)
ax2.set_xlim(0,100)

ax1.set_ylim(0,100)
ax2.set_ylim(0,100)

# Grid so it looks cool
ax1.grid(True)
ax2.grid(True)

# Plot our regression lines and give labels so people can see what the coefficients are
the_approx1 = ax1.plot(x, m1*x + b1, label=f"y = {m1:.2f}x + {b1:.2f}, r={r1:.3f}", c="blue")
the_approx2 = ax2.plot(x, m2*x + b2, label=f"y = {m2:.2f}x + {b2:.2f}, r={r2:.3f}",c="green")

plt.suptitle("Comparing percentage of international students per university with graduate prospects (Computer Science)")

ax1.legend()
ax2.legend()


plt.show()