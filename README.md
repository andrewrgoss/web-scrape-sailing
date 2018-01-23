# web-scraping-py
Following a <a href="https://www.meetup.com/bostonpython/events/246254219" target="_blank">Boston Python Project Night</a> event that I attended (where my group focused on web scraping techniques), I wanted to try out some web scraping on my own with Python.

> Web scraping is a technique used to extract data from websites through an automated process.

## Dataset
A good site for web scraping that was recommended to me at the event is <a href="http://scores.collegesailing.org/f17/" target=_>College Sailing’s Techscore</a>. It is the home for real-time results of College Sailing regattas and includes scores and participation records for all fleet-racing and team-racing events within ICSA. An archive of all previous seasons is also available, so it offers a fair amount of subpage links to traverse. I don't know much about college sailing but set out to dig more into this data.

After inspecting the site layout through Chrome's developer tools, I recognized that this website has a pretty consistent table structure throughout which made scraping data from it easier. There are links to each regatta held during different seasons which contain a score summary in order of how each school placed. This is also separated into A & B divisions in many cases. The format for team scoring regattas deviated a bit from the other scoring formats (# Divisions, Combined, Singlehanded) so I wrote code to skip over these types. I also could have only parsed regatta scoring records where status is 'official' but didn't worry about it for this exploratory project.

## Tips and Tricks Guide
I used this <a href="https://hackernoon.com/web-scraping-tutorial-with-python-tips-and-tricks-db070e70e071" target=_>post</a> from <a href="https://hackernoon.com" target=_>Hacker Noon</a> as a guide for this excerise. The article offers good insights on common design patterns as well as pitfalls and rules related to web scraping. It also presents several use cases and a collection of typical problems, such as how not to be detected, dos and don’ts, and how to speed up (parallelization) your scraper.

## Python Libraries
<a href="https://www.crummy.com/software/BeautifulSoup" target=_>BeautifulSoup</a> is a library that allows you to parse HTML source code in a beautiful way. 

Along with this I used the popular <a href="http://docs.python-requests.org/en/master" target=_>Requests</a> library to fetch the content of the urls.

## Improving Speed with Parallelization
The initial runtime of my program to scrape regatta scores from each event dating back to 2010 was 0:06:19.282466. Per the guide I referenced, I wanted to try and see if I could cut this down by sending requests in parallel using a <a href="https://docs.python.org/2/library/multiprocessing.html" target=_>multiprocessing</a> package.

By sending requests in parallel I was able to reduce the runtime of my program to 0:01:46.565286 -- about a 24% improvement in speed.

## Next Steps
No API is available for this site, so I would like to create one using the data that I scraped.