from genre import Genre
from game import Game
import ipdb

from helpers import clear, pause, space, invalid_choice

class Cli:
    def start(self):
        clear()
        space()
        print("+++++++++++++++++")
        print("++ GAME LOGGER ++")
        print("+++++++++++++++++")
        space()
        space()
        pause()

        self.menu()

    def menu(self):
        clear()
        space()
        print("+++++++++++++++++")
        print("++ GAME LOGGER ++")
        print("+++++ MENU ++++++")
        print("+++++++++++++++++")
        space()
        print("1. Log a Game")
        space()
        print("2. Show All Logged Games")
        space()
        print("3. Search Game Title")
        space()
        print("4. Search Game by Genre")
        space()
        print("5. Delete Game")
        space()
        print("6. Exit")
        space()
        self.menu_choice()

    def menu_choice(self):
        user_input = input("Enter Choice... ")
        if user_input == "1":
            self.log_game()
            space()
            pause()
            self.menu()
        elif user_input == "2":
            self.show_games()
            space()
            pause()
            self.menu()
        elif user_input == "3":
            self.search_game()
            space()
            pause()
            self.menu()
        elif user_input == "4":
            self.search_genre()
            space()
            pause()
        elif user_input == "5":
            self.delete_game()
            space()
            pause()
            self.menu()
        elif user_input == "6":
            clear()
            space()
            print("++++++++++++++++")
            print("+++ GOODBYE ++++")
            print("++++++++++++++++")
            space()
            pause()
            clear()
            exit()

    def log_game(self):
        clear()
        space()
        print("++++++++++++++++")
        print("++ LOG A GAME ++")
        print("++++++++++++++++")
        space()
        space()
        game_title = input("Enter Game: ")
        if game_title:
            game = Game.create(title = game_title.lower(), developer = "N/A")
            self.log_developer(game)
        else: 
            invalid_choice()
            self.menu()

    def log_developer(self, game):
        space()
        game_developer = input("Enter Game Developer: ")
        if game_developer:
            game.developer = game_developer.lower()
            game.update()
            space()
            clear()
            self.genre_menu(game)
        else: 
            invalid_choice()
            game.delete()
            self.menu()

    def genre_menu(self, game):
        clear()
        space()
        print("+++++++++++++++++")
        print("+++  GENRES  ++++")
        print("+++++++++++++++++")
        if Genre.all():
            for genre in Genre.all():
                self.genre_list(game, genre)
            self.genre_choice(genre, game)
        else: 
            space()
            print("No Genres have been created.")
            space()
            pause()
            self.create_genre(game)


    def genre_list(self, game, genre):
        space()
        print(":::::::::::::::::::::::")
        print(f"Genre: {genre.name}")
        print(f"ID: {genre.id}")
        print(":::::::::::::::::::::::")
        space()
        

    def genre_choice(self, genre, game):
        old_genre = input("Enter 0 to Create Genre or Enter Existing Genre: ")
        if old_genre == "0":
            self.create_genre(game)
        elif old_genre: 
            old_genre.lower() == genre.name
            game.genre = genre
            clear()
            space()
            print(f"+++++ Game: {game.title} +++ Devloper: {game.developer} +++ Genre: {game.genre.name} +++++")
            print("+++++++++++++++++++++++++   SUCESSFULLY LOOGGED   +++++++++++++++++++++++++++++++")
            space()
            pause()
            self.menu()
        else: 
            invalid_choice()
            game.delete()
            self.menu()
        

    def create_genre(self, game):
        clear()
        space()
        print("+++++++++++++++++")
        print("+++  GENRES  ++++")
        print("+++++++++++++++++")
        space()
        game_genre = input(f"Enter New Genre for {game.title}: ")
        genre = Genre.create(name = game_genre.lower())
        game.genre = genre
        clear()
        space()
        print(f"+++++ Game: {game.title} +++ Devloper: {game.developer} +++ Genre: {game.genre.name} +++++")
        print("+++++++++++++++++++++++++   SUCESSFULLY LOOGGED   +++++++++++++++++++++++++++++++")
        space()
        pause()
        self.menu()

    def show_games(self):
        clear()
        space()
        if Genre.all():
            space()
            print("++++++++++++++++++")
            print("++ GAMES LOGGED ++")
            print("++++++++++++++++++")
            for game in Game.all():
                self.game_details(game)
        else: 
            print("No Games Have Been Logged.")

    def game_details(self, game):
        space()
        print(":::::::::::::::::::::::")
        print(f'Title: {game.title}')
        print(f'Developer: {game.developer}')
        print(f'Genre: {game.genre.name}')
        print(":::::::::::::::::::::::")
        space()
        
    def search_game(self):
        clear()
        space()
        print("+++++++++++++++++")
        print("+++  SEARCH  ++++")
        print("+++++++++++++++++")
        space()
        space()
        title = input("Enter Game: ")
        game = Game.find_by_title(title.lower())
        if game:
            clear()
            space()
            print("+++++++++++++++++++++")
            print("++++ GAME FOUND +++++")
            print("+++++++++++++++++++++")
            space()
            space()
            self.game_details(game)
        else: 
            clear()
            space()
            print("Game Not Found, Try Again")
            space()
            pause()
            self.menu()

    def search_genre(self):
        clear()
        space()
        print("+++++++++++++++++++++")
        print("+++++ SEARCH BY +++++")
        print("++++++  GENRE  ++++++")
        print("+++++++++++++++++++++")
        space()
        space()
        genre = input("Enter Genre: ")
        genre = genre.lower()
        if Genre.find_by_name(genre):
            genre_inst = Genre.find_by_name(genre)
            self.genre_games(genre_inst)
        else: 
            clear()
            space()
            print("Genre not found.")
            space()
            pause()
            self.menu()

    def genre_games(self, genre_inst):
        clear()
        space()
        print("++++++++++++++++++++++++")
        print(f"+++ {genre_inst.name} +++")
        print("++++++++++++++++++++++++")
        for game in genre_inst.games:
            self.print_games(game)
        pause()
        self.menu()

    def print_games(self, game):
        space()
        print(":::::::::::::::::::::::")
        print(f"Game: {game.title}")
        print(f"Developer: {game.developer}")
        print(":::::::::::::::::::::::")


    def delete_game(self):
        clear()
        space()
        print("+++++++++++++++++++++")
        print("++++ DELETE GAME ++++")
        print("+++++++++++++++++++++")
        space()
        title = input("Enter Game: ")
        game = Game.find_by_title(title)
        if game:
            game.delete()
            clear()
            space()
            print(f"Game: {game.title} has been logged out")
            space()
            pause()
            self.menu()
        else:
            clear()
            space()
            print("Game not found")
            space()
            pause()
            self.menu()

        
        


        
