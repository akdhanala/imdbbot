"""
File: main.py
Author: Akhil Dhanala (akhild-uci)

This script scrapes the imdb site for movie posters to match the movies
described in a mysql database
"""

# STL
import sys
import os
import time
import datetime
import urllib
from pathlib import PurePosixPath

# Third party
import dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

# Locally defined
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

from imdbscraper.moviedb.models import Movie
import imdbscraper.exceptions as imdbexcept



class App:
    def __init__(self):
        options = Options()
        options.headless = True

        # Disable this if you'd like to see Selenium produced logs
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driverpath = os.getenv("CHROMIUM_PATH")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options, 
            service_log_path=os.devnull)
        self.driver.get("https://www.imdb.com")

        self.engine = sa.create_engine(os.getenv("MOVIEDB_CONNECTION_STRING"))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        logpath = os.path.dirname(__file__) + f"/../logs/log_{datetime.date.today().isoformat()}.txt"

        self.logfile = open(logpath, "a+")
        print(f"RAN AT {datetime.datetime.today().ctime()}", file=self.logfile)
        print("-------------------------------------------", file=self.logfile)

        self.closed = False


    # Public
    def run(self) -> None:
        for i, movie in enumerate(self.session.query(Movie).filter(Movie.poster == None), start=1):
            try:
                self._nav_to_poster(movie.movieId)
                url = self._grab_poster_url()

                print(movie.title, url)
                movie.poster = url

            except Exception as e:
                print(movie.title, "skipped")
                print("Error:", movie.title, file=self.logfile)
                print(str(e), file=self.logfile)
            
            if i % 1000 == 0:
                self.session.commit()


    def close(self) -> None:
        if not self.closed:
            self.session.commit()
            self.session.close()
            self.engine.dispose()
            self.driver.quit()

            print("\n", file=self.logfile)
            self.logfile.close()
        
            return

        raise imdbexcept.IMDBScraperAppException("already closed")

    # Private

    def _nav_to_poster(self, titleId: str) -> None:
        url = f"https://www.imdb.com/title/{titleId}/?ref_=fn_al_tt_1"
        self.driver.get(url)

        return titleId

    def _grab_poster_url(self) -> str:
        selector = ".ipc-poster img"
        try:
            poster = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            raise imdbexcept.IMDBScraperAppException("No poster")

        return poster.get_attribute("src")
        

if __name__ == "__main__":
    start = time.time()
    print("Running application")
    print("-----------------------------------------------")
    try:
        dotenv.load_dotenv()
        app = App()
        app.run()
        app.close()
    finally:
        end = time.time()
        print("-----------------------------------------------")
        print(f"Application ran in: {end - start:0.2f} seconds")