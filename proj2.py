""" 507 Project 2
This assignment is all about web scraping with Beautiful Soup. There are four problems,
each worth 10 points.

Important Notes
Only modify the file proj2.py that is in the repository you cloned when you accepted the assignment
invitation. All of your solutions to the problems in this project should be contained within
proj2.py. Any additional files that you create will be ignored.
Make sure that you push your changes to your assignment repository before the deadline: NOON on
Thursday, Feb. 23, 2017.
Please follow the output format examples as closely as possible. We will create an autograder that
expects the output to precisely match the format of the output shown.
"""

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ssl

def get_soup(uri, request_headers):
    """ Get the html parsed soup for a url
    """
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    request = urllib.request.Request(uri, headers=request_headers)
    html = urllib.request.urlopen(request, context=ctx).read()
    return BeautifulSoup(html, "html.parser")

class Facultydirectorypage(object):
    """ Parse a page, get the faculty links and next link.
    """
    def __init__(self, uri_input, first_item):
        """ Get a collection of contact links from a page
        """
        self.item = first_item
        self.uri = urlparse(uri_input)
        self.soup = get_soup(uri_input, {'User-Agent': 'SI_CLASS'})

    def get_url(self, path):
        """ Create a new url from a path
        """
        return self.uri.scheme + "://" + self.uri.netloc + path

    def contact_links(self):
        """ Get the client page links
        """
        retlist = list()
        for detail in self.soup.find_all('a', text="Contact Details"):
            retlist.append(self.get_url(detail['href']))
        return retlist

    def next_page(self):
        """ Get the next page link object
        """
        path = self.soup.find('a', title="Go to next page")
        if path:
            return Facultydirectorypage(self.get_url(path['href']), self.item)
        return None

    def get_email_address(self, uri):
        """ Get a particular soup from a page
        """
        emailtab = get_soup(uri, {'User-Agent': 'SI_CLASS'} ).find('div', class_='field-name-field-person-email')
        email_string = emailtab.get_text().replace("Email:", str(self.item))
        self.item += 1
        return email_string


#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')
"""
Problem 1: Print headlines from the New York Times
Points: 10

Write a program that prints the first ten headlines that appear on the New York Times home page
(http://nytimes.com). A really, really helpful starting point for this would be to read through
the solution to a very closely related problem. You are encouraged to work through this solution
and use it as a starting point for your solution. The solution uses the third-party "requests"
library instead of "urllib" -- you can use whichever you prefer, as long as it works!

As of 11:09 pm on Feb. 7, 2017, here is what the NY Times web page looked like, and here is what
a correct implementation of the program should output:

*********** PROBLEM 1 ***********
New York Times -- First 10 Story Headings

Court Skeptical of Justice Dept. Arguments to Reinstate Ban
Listen to the Arguments Here
After Flawed Raid, Yemen Forbids U.S. Ground Missions
White House Weighs Terrorist Label for Muslim Brotherhood
Heres Our Coverage of Attacks Trump Said Were Ignored
Education Pick Confirmed as Pence Breaks Tie in Senate
"The Nomination Is Confirmed"
Suit Says Tabloid Cost Melania Trump Millions in Business
2 Refugees Describe the Multistep Vetting They Cleared
Homeland Security Chief Admits Travel Ban Was Rushed
Iranian Leader Thanks Trump for Showing "Real Face" of U.S.


You will notice that the definition of a "headline" is not entirely clear by visually inspecting
the NY Times site. For the purposes of this assignment, you can assume that the "first ten
headlines" means the first ten headline-looking blocks of HTML text that appear in the HTML page
at http://nytimes.com. As indicated by the solution, the definition of a "headline-looking block
of HTML" is a block that is enclosed by a tag that has the class "story-heading". You still need
to figure out (with the help of the example solution provided) how to print the text that best
represents the "headline" for that block, though.

Grading and partial credit: We will pull the current headlines at the time of grading and compare
them to your output. You will receive one point for each correct headline.
"""

NYTSOUP = get_soup("http://www.newyorktimes.com", {})
NYTHEADLINES = NYTSOUP.find_all('h2', class_="story-heading")

for headline in NYTHEADLINES[:10]:
    print (headline.get_text().strip())

#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')
"""
Problem 2: Print the "Most Read" headlines from the Michigan Daily
Points: 10

For this problem we wont give as much guidance--you will need to inspect the Michigan Daily page
(https://www.michigandaily.com/) to figure out how to extract the "Most Read" headlines. Its the
part of the page that looks like this (as of 1:45pm, Feb. 7, 2017):

And it should not surprise you to learn that the output from a program that scrapes these
headlines should print out (as it did at 1:45pm on Feb. 7, 2017):

*********** PROBLEM 2 ***********
Michigan Daily -- MOST READ

Do it for Detroit: A look into Big Sean's intimate listening party
LSA-SG encourages change in Arabic class materials
Vince Staples confirms single, lays out vision, and ponders "activism"
Missing student found dead in car
Ross brothers start cookie company from scratch

Grading and partial credit: We will pull the current Most Read headlines at the time of grading
and compare them to your output. You will receive two points for each correct headline.
"""

MDSOUP = get_soup("https://www.michigandaily.com/", {})

for headline in MDSOUP.find_all('div', class_="view-most-read"):
    print (headline.get_text().strip())

#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

"""
Problem 3: Print some "alt" tags
Points: 10

There are 10 images on the page http://newmantaylor.com/gallery.html. Some of them have "alt text,"
which is the text that is displayed or spoken when the image cant be displayed (because of browser
limitations, or because someone is using a screen reader). Scrape this page and print out the alt
text for each image. If there is no alt text, print "No alternative text provided!"

Given the current version of the page, which will remain constant until after the deadline, Your
output should look like this:

*********** PROBLEM 3 ***********
Mark's page -- Alt tags

Waving Kitty 1
No alternative text provided!!
Waving Kitty 3
Waving Kitty 4
Waving Kitty 5
Waving Kitty 6
No alternative text provided!!
Waving Kitty 8
Waving Kitty 9
Waving Kitty 10


Grading and partial credit: We may test your code on a version of gallery.html that has different
alt text. For example, it may be that the 8th image is missing alt text and the 7th images has the
alt text "Waving Kitty 7." There will still be 10 images though. You will receive one point for
each correct alt text output.
"""

for kitty in get_soup("http://newmantaylor.com/gallery.html", {}).find_all('img'):
    if 'alt' in kitty.attrs:
        print (kitty['alt'])
    else:
        print ("No alternative text provided!")

#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

"""
Problem 4: Print all UMSI faculty emails
Points: 10

The UMSI faculty directory is here:

https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4

Starting at this page, your job is to print all of the faculty email addresses. Two things you will
notice right away:

There are not any email addresses visible on this page. The email address only shows up when you
click "Contact Details." Not all of the faculty appear on this page. As indicated at the bottom,
there are 6 pages.

This means that you will need to not only scrape, but crawl the directory by finding the relevant
links and opening the pages that they link to.

Your program should also print out a counter in front of each address.

In the end your output should look like this:

*********** PROBLEM 4 ***********
UMSI faculty directory emails

1 ackerm@umich.edu
2 eadar@umich.edu
...
101 yardi@umich.edu
102 szachary@umich.edu

Except of course your program should output all 102 email addresses.

Grading and partial credit: We will re-generate our list of faculty email addresses at the time of
grading (its not likely to change, but you never know!)  and compare your output to our list. You
will receive 5 points for getting at least 20 addresses correct (there are 20 faculty members listed
per page), and full credit for getting all of them right. Any number of correct responses between 20
and 102 will be considered on a case-by-case basis.

"""

URLMSI = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4"
CONTACTPAGE = Facultydirectorypage(URLMSI, 1)

while CONTACTPAGE:
    for contact_link in CONTACTPAGE.contact_links():
        print (CONTACTPAGE.get_email_address(contact_link))

    CONTACTPAGE = CONTACTPAGE.next_page()
