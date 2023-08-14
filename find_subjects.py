import requests as rq
from bs4 import BeautifulSoup as BS

# Program to get the list of all university subjects on thecompleteuniversityguide
# After the list is obtained, no further need for this program

url = "https://www.thecompleteuniversityguide.co.uk/subject-guide#sb"

# Persuade them we are human
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

# This is the complete list that we found in the last iteration in the program
subjects = ['Accounting & Finance', 'Acting', 'Aeronautical & Aerospace Engineering', 'African & Middle Eastern Studies', 'Agriculture & Forestry', 'American Studies', 'Anthropology', 'Archaeology', 'Architecture', 'Art & Design', 'Artificial Intelligence', 'Asian Studies', 'Astrophysics', 'Biological Sciences', 'Biomedical Sciences', 'Building', 'Business & Management Studies', 'Celtic Studies', 'Chemical Engineering', 'Chemistry', 'Childhood & Youth Studies', 'Chinese', 'Civil Engineering', 'Classics', 'Communication & Media Studies', 'Complementary Medicine', 'Computer Science', 'Counselling, Psychotherapy & Occupational Therapy', 'Creative Writing', 'Criminology', 'Dentistry', 'Dietetics, Study Dietetics', 'Drama, Dance & Cinematics', 'Ecology', 'Economics', 'Education', 'Electrical & Electronic Engineering', 'English', 'Fashion', 'Film Making', 'Food Science', 'Forensic Science', 'French', 'General Engineering', 'Geography & Environmental Science', 'Geology', 'German', 'Health Studies', 'History', 'History of Art, Architecture & Design', 'Hospitality & Catering', 'Human Resources Management', 'Iberian Languages', 'Information Technology & Systems', 'Interior Design', 'Italian', 'Journalism', 'Land & Property Management', 'Law', 'Linguistics', 'Manufacturing & Production Engineering', 'Marine Biology', 'Marketing', 'Materials Technology', 'Mathematics', 'Mechanical Engineering', 'Medical Technology & Bioengineering', 'Medicine', 'Midwifery', 'Modern Languages', 'Music', 'Natural Sciences', 'Neuroscience', 'Nursing', 'Nutrition', 'Occupational Therapy', 'Optometry, Ophthalmics & Orthoptics', 'Paramedic Science', 'Pharmacology & Pharmacy', 'Philosophy', 'Photography', 'Physics & Astronomy', 'Physiotherapy', 'Podiatry', 'Politics', 'Prosthetics & Orthotics', 'Psychology', 'Robotics', 'Russian & East European Languages', 'Social Policy', 'Social Work', 'Sociology', 'Spanish', 'Speech & Language Therapy', 'Sports Science', 'Statistics', 'Theology & Religious Studies', 'Tourism, Transport, Travel & Heritage Studies', 'Town & Country Planning and Landscape Design', 'Veterinary Medicine', 'Youth Work', 'Zoology']

# First, get the website's text
page_found = rq.get(url, headers=headers).text

# Parse through BS to make it useable
page = BS(page_found, "html.parser")

# There is only one div on the page with this class, and it contains the list of subjects (hence the term sub_lst (subject list) 
the_list = page.find("div" , {"class" : "sub_lst"  } )

# Gets a list of all the subjects, but each element is still a tag itself
the_subs = the_list.find_all("a" , {"data-ga-category" : "Subject Listing"})

# The actual string-name of the subject in each element is given by the "data-ga-label"=(stringname)
print([x["data-ga-label"] for x in the_subs])