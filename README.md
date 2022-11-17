# IMDb Parser
I made this parser to make FabFlix (CS122b project) prettier. Amazon does provide data
sets but these didn't meet my needs. Rapidapi also provides endpoints for movie posters
but this also had a request cap that I was definitely going to exceed.

## Implementation
I noticed the data our professor provided was collected from IMDb through the unique
identifiers. Using these, I was able to scrape each movie page for their poster media
link. I used Selenium in case IMDb used javascript to generate html. If you find that
this isn't the case, you might be able to use a different parser (maybe BeatifulSoup or 
lxml). I also used sqlalchemy ([ORM](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping)) 
to interact with my MySQL backend without having to write sql. 

## Setup
1. Clone and setup repo
```
git clone <link/to/this/repo>
cd ./imdbparser
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```
2. Create environment file and add environment variables (.env file)
```
MOVIEDB_CONNECTION_STRING=mysql+pymysql://<user>:<password>@localhost:3306/moviedb
```

## Future
This parser currently only scrapes movie links for the data provided by the professor. If
you're trying to add posters for movies we've parsed from other sources, you'll have to use
selenium to search for the movie, pick the first title, and then scrape the poster url that
way. I had implemented it this way originally but found the run time to be too slow (almost 25 hours
if I had let it continue). Even without having to search the movie title, each movie takes
about 3 seconds to fetch a poster url (for 9000 records it took around 10 hours).
