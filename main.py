import pandas as pd 
from scraper import scrape_table_1, scrape_table_2
from functions import clean_name,get_player_row,filter_by_surface
from player import Player
from predictor import MatchPredictor

url = "https://www.tennisabstract.com/reports/atp_elo_ratings.html"
df1 = scrape_table_1(url)
url_2 = "https://www.wheeloratings.com/tennis_atp_stats_last52.html"
df2 = scrape_table_2(url_2)
while True:
    surface = input ("Enter the type of tennis court :").strip().lower().capitalize()
    if surface not in ["Hard", "Clay", "Grass", "All"]:
        print ("Unknown surface ! Try again.\n")
    else:
        break
df2 = filter_by_surface (df2,surface)
df_total = df1.merge(df2, how = 'inner', on  = ["Player"])
while True:
    name_A = input("Enter the name of the first player : ").strip()
    player_A = get_player_row(df_total, name_A)
    
    if player_A is None:
        print("The first player is unfindable ! Try again.\n")
    else:
        break 
while True:
    name_B = input("Enter the name of the second player : ").strip()
    playerB = get_player_row(df_total, name_B)
    
    if player_B is None:
        print("The second player is unfindable ! Try again.\n")
    else:
        break
player_A = Player(name_A,player_A)
player_B = Player(name_B,player_B)
predictor = MatchPredictor(df_total)
result = predictor.predict_winner(name_A, name_B, surface)

probA, probB = result

print("\nResults:")
print("{} : {:.2%}".format(clean_name(name_A).title(), probA))
print("{} : {:.2%}".format(clean_name(name_B).title(), probB))

result2 = predictor.win_set_odds(name_A,name_B,surface)
print("\nResults:")
print("odds of ",clean_name(name_A).title()," winning a set are:", result2)
