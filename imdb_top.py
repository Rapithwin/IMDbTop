from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

all_films = []
def find_html(soup):
    global all_films
    if all_films != []:
        all_films = []
    else:
        pass
    rows = soup.find("tbody", class_ = "lister-list")  # Finds a tbody tag in a class named "lister-list"
    movies = rows.find_all("tr") # Finds all the rows in that tag
    for movie in movies:
        title = movie.find("td", class_ = "titleColumn").find("a").text.strip()  # For the movie title
        year = movie.find("span", class_ = "secondaryInfo").text.strip()  # For the release year
        imdb_rating = movie.find("td", class_ = "ratingColumn imdbRating").text.strip()  # For IMDb rating
        films = {
            "Title" : title,
            "Year" : year,
            "IMDb Rating" : imdb_rating,
        }
        all_films.append(films)

def excel_save(filename):
    df = pd.DataFrame.from_dict(all_films)  # Construct dataframe from the list of dict
    writer = pd.ExcelWriter(f"{filename}.xlsx")  # Init Pandas excel writer, using the 'filename' variable
    df.to_excel(writer, "IMDb_sheet")  # Writes to a sheet called 'IMDb_sheet'. Format follows the Dataframe format.
    writer.save()  # Save excel

        
def top_movies():
    url = r"https://www.imdb.com/chart/top/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    find_html(soup)
    filename = "TopMovies"
    excel_save(filename)

def top_series():
    url = r"https://www.imdb.com/chart/toptv/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    find_html(soup)
    filename = "TopSeries"
    excel_save(filename)

def most_popular_movies():
    url = r"https://www.imdb.com/chart/moviemeter/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    find_html(soup)
    filename = "MostPopularMovies"
    excel_save(filename)

def most_popular_series():
    url = r"https://www.imdb.com/chart/tvmeter/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    find_html(soup)
    filename = "MostPopularSeries"
    excel_save(filename)

if __name__ == "__main__":

    while True:
        while True:
            print(""" 
Choose an option:
Enter tm for getting top 250 movies of IMDb
Enter ts for getting top 250 tv shows of IMDb
Enter mpm for getting the most popular movies on IMDb
Enter mps for getting the most popular tv shows on IMDb
Enter all for getting it all!
            """)
            user_input = input("> ")

            if user_input.lower() == "tm":
                top_movies()
                print("\nDone!")
                break
            elif user_input.lower() == "ts":
                top_series()
                print("\nDone!")
                break
            elif user_input.lower() == "mpm":
                most_popular_movies()
                print("\nDone!")
                break
            elif user_input.lower() == "mps":
                most_popular_series()
                print("\nDone!")
                break
            elif user_input.lower() == "all":
                top_movies()
                top_series()
                most_popular_movies()
                most_popular_series()
                print("\nDone!")
                break
            else:
                print("\nUndefined command, try again.")
                continue

        yes_no = input("\nDo you want to run the program again?(yes/no): ")
        if yes_no.lower() in ["yes", "y"]:
            continue
        elif yes_no.lower() in ["no", "n"]:
            raise SystemExit
