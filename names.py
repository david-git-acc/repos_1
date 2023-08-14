import requests as rq
from bs4 import BeautifulSoup as BS, Comment

# This program is designed to collect all of the "bubles" (tags) found on the 4 different parts of each university page onthecompleteuniversityguide.co.uk. 
# It then will place all of the data onto pie charts, with one chart per subpage (student support, facilities, student life, student employability) showing
# the most common tags for each subpage (accumulated across visiting every university's page)
# The goal is to determine what the most common tags are, hence what unis think are the most attractive things to prospective students

# Convince them we are humans
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

# I'm totally not a bot. Beep boop.
params = {
    'sort': 'dd',
    'filter': 'reviews-dd',
    'res_id': 18439027
}

# Since we'll be counting the number of occurrences of each tag type, I figured a Counter would be a good resource to use
from collections import Counter

# These are the ordered names of all the universities whose pages we'll be checking
names = ['University of Cambridge', 'University of Oxford', 'Imperial College London', 'Durham University', 'UCL (University College London)', 'University of Bath', 'University of Birmingham', 'The University of Edinburgh', 'University of Southampton', 'University of St Andrews', 'University of Sheffield', 'University of Warwick', 'University of Manchester', "King's College London, University of London", 'University of Bristol', 'University of Glasgow', 'Loughborough University', 'University of York', 'University of Exeter', 'University of Nottingham', "Queen's University Belfast", 'Lancaster University', 'University of Leeds', 'University of Surrey', 'Royal Holloway, University of London', 'Cardiff University', 'Newcastle University', 'University of Dundee', 'Aberystwyth University', 'University of Strathclyde', 'Queen Mary University of London', 'University of East Anglia UEA', 'Heriot-Watt University', 'University of Liverpool', 'University of Kent', 'University of Reading', 'Swansea University', 'University of Leicester', 'City, University of London', 'Aston University, Birmingham', 'University of Sussex', 'Liverpool Hope University', 'University of Aberdeen', 'University of Lincoln', 'Ulster University', 'University of Essex', 'Bristol, University of the West of England', 'Manchester Metropolitan University', 'University of Huddersfield', 'Edge Hill University', 'Oxford Brookes University', 'Bangor University', 'University of Plymouth', 'University of Stirling', 'Nottingham Trent University', 'University of Hull', 'Brunel University London', 'Northumbria University, Newcastle', 'Edinburgh Napier University', 'Abertay University', 'University of Portsmouth', 'University of Hertfordshire', 'Keele University', 'Canterbury Christ Church University', 'Leeds Beckett University', 'Liverpool John Moores University', 'Falmouth University', 'University of Chichester', 'Bournemouth University', 'University of Brighton', 'Kingston University', 'Birmingham City University', 'University of Bradford', 'Staffordshire University', 'University of Winchester', 'Robert Gordon University', 'University of the Arts London', 'Bath Spa University', 'Glasgow Caledonian University', 'Coventry University', 'Goldsmiths, University of London', 'Sheffield Hallam University', 'University of Salford', 'University of Derby', 'University of East London', 'University of South Wales', 'University of Westminster, London', 'University of Greenwich', 'University of Worcester', 'De Montfort University', 'Teesside University, Middlesbrough', 'University of Chester', 'University of Central Lancashire', 'Cardiff Metropolitan University', 'London South Bank University', 'University of West London', 'Solent University (Southampton)', 'University of Gloucestershire', 'University of Sunderland', 'University of the West of Scotland', 'University of Buckingham', 'University of Northampton', 'Norwich University of the Arts', 'University for the Creative Arts', 'University of Suffolk', 'Glyndwr University, Wrexham', 'York St John University', 'Middlesex University', 'University of Bolton', 'Buckinghamshire New University', 'Anglia Ruskin University', 'University of Bedfordshire', 'University of Wales Trinity Saint David', 'London Metropolitan University', 'University of Wolverhampton']

# Sanity check, there should be exactly 115
print(len(names))

# These functions convert official names (e.g University of Cambridge) into their URL equivalents (university-of-cambridge) so we can put them into a URL search
# urlify maps from official name to url name, deurlify does the opposite - inverse functions
# urlify(deurlify(x)) == x and deurlify(urlify(x)) == x, hopefully

def urlify(name):
    # Kill the commas and apostrophes, replace spaces with dashes and convert to lowercase
    return name.replace(",","").replace("'","").replace(" ", "-").lower()

def deurlify(name):
    # Opposite of the above steps, sometimes some info cannot be recovered but should usually be bijective
    return " ".join([x.capitalize() for x in name.split("-")])

# urlify them!
url_names = [urlify(x) for x
             in names]

# These are the 4 subcategories, so we want a counter to check the number of occurrences in each
# The tags for each subcategory do not seem to be found in the other 3 (I didn't see any)
pages = ["student-support", "facilities", "student-life","student-employability"]


counters = [Counter({}),Counter({}),Counter({}),Counter({})]

# Total number of unis that were successfully checked
totalcount=0

# Loop through the urlified names so we can include the iterator in our loop
for name in url_names:
    
    # Sanity check to make sure it's actually checking diff. unis
    print(name)

    # Checking each subcategory (page) for each uni (name)
    # i is the index, with i=0 corresponding to student support, i=1 being facilities, etc... (see the pages list above)
    for i,page in enumerate( pages ) :

        # This is the format of the URLs - uni name, then the subcategory
        url = f"https://www.thecompleteuniversityguide.co.uk/universities/{name}/{page}"

        # Sometimes there may be an error in trying to get the data, e.g invalid name (urlify is not 100% accurate) or no data found
        try:
            # Get and parse the content of the page
            page_found = rq.get(url, headers=headers, timeout=2).text
            soup = BS(page_found, "html.parser")
            
            # For some reason there were tags which were commented out in the HTML markup, so these had to be removed
            for element in soup(text=lambda text: isinstance(text, Comment)):
                element.extract()
            
            # This is where all the "bubles" as they're called, can all be found
            main_soup = soup.find("section" , {"class" : "main_cont uni_cont"})
            
            # Conveniently all of these tags have the "buble" class (comments containing them already removed)
            bubles = main_soup.find_all("span" , {"class" : "buble"})
            
            # They're all initially UPPERCASE, so I thought lowercase would be a nice aesthetic
            text_bubles = [x.text.lower() for x in bubles]
            
            # Now that we have the bubles, all we need to do is update the corresponding counters
            for buble in list(set(text_bubles)):
                counters[i].update({buble : 1})
        except:
            # If it fails somewhere then we need to cancel it and reduce the total number of successful unis found (this increments at the beginning)
            totalcount -=1
            # Need to see what % of the unis being checked fail to yield data
            print("fail")
            break
            
    # Increment the total number of unis successfully searched
    totalcount+=1

        
                

# It's plotting time!

from matplotlib import pyplot as plt
import numpy as np 

# I can only visualise pixels, need some standardisation
# Apparently 1px = 1/96 of an inch
px = 1/96
    
# Generating our 4 plots. 
# Because matplotlib arranges its plots in a numpy 2D array, we need to add our brackets specifically to reflex the shape of this to avoid an error
fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(1920*px, 1080*px))

# When you have the axes, this ((a,b) , (c,d)) format is annoying, much easier to address them as a list 
# (they will not be duplicated because they are objects, and objects are always by-reference in python)
axes = [ax1,ax2,ax3,ax4]


# Largest font size I could fit that wouldn't be too small
plt.rcParams.update({"font.size" : 8})

# Creating each pie chart in turn, one for each subcategory
for i in range(4):
    
    # This gets the official name of the subcategory, we don't want it in the ugly urlified format
    name = deurlify(pages[i])
    
    # The keys are the actual buble tags themselves, the values are the number of timese each one appears
    # It is vital that the respective ordering of these is preserved upon key-value split to avoid quantity-buble mismatches
    the_bubles = list( counters[i].keys() )
    quantities = list( counters[i].values() )
    
    # Sometimes due to some pages being cut halfway through inspection, a tag can end up with more occurrences than actually exist for the unis mentioned
    # We need to cap these at 100% obviously
    for ind,v in enumerate(quantities):
        if v > totalcount:
            # Checking that no quantity > the total number of unis, since each tag can only appear once per uni page
            quantities[ind] = totalcount
    
    # Get the total number of all tags (used to calculate the percentage occurrence of each tag)
    total_here = sum(quantities)

    # Set the title of each pie chart
    title = axes[i].set_title(name, fontsize=18)
    
    # Instantiate the pie chart on the next available axes object, with the labels obviously being the bubles, and this massive line of formatting is 
    # just specifying the number of occurrences and percentage occurrence for each tag on the plot
    the_pie_chart = axes[i].pie(quantities,labels = the_bubles, autopct=lambda x: '{:.0f}'.format(x*sum(quantities)/100) + f" ({( 100 *  (x*total_here/100) / totalcount ):.1f}%)",)
    

plt.suptitle("Most common university tags on thecompleteuniversityguide", fontsize=20)
        
plt.savefig("pies.png")
        
plt.show()

