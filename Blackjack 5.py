import random
import tkinter as tk


class BlackjackGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Black Jack")
        self.window.geometry("800x600")
        self.window.configure(bg="#3fba4c")

        self.result_text = tk.StringVar()
        self.result = tk.Label(self.window, textvariable=self.result_text, font=("Arial", 16))
        self.result.grid(row=0, column=0, columnspan=3)

        self.card_frame = tk.Frame(self.window, relief="sunken", borderwidth=1, bg="black")
        self.card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

        self.dealer_score_label = tk.IntVar()
        tk.Label(self.card_frame, text="Dealer", bg="black", fg="white", font=("Arial", 14)).grid(row=0, column=0)
        tk.Label(self.card_frame, textvariable=self.dealer_score_label, bg="black", fg="white", font=("Arial", 14)).grid(row=1, column=0)
        self.dealer_card_frame = tk.Frame(self.card_frame, bg="black")
        self.dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

        self.player_score_label = tk.IntVar()
        tk.Label(self.card_frame, text="Player", bg="black", fg="white", font=("Arial", 14)).grid(row=2, column=0)
        tk.Label(self.card_frame, textvariable=self.player_score_label, bg="black", fg="white", font=("Arial", 14)).grid(row=3, column=0)
        self.player_card_frame = tk.Frame(self.card_frame, bg="black")
        self.player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=3, column=1, columnspan=3, sticky='w')

        self.player_button = tk.Button(self.button_frame, text="Hit", command=self.deal_player, padx=8, pady=6, relief="solid", borderwidth=1, font=("Arial", 12))
        self.player_button.grid(row=0, column=0)

        self.dealer_button = tk.Button(self.button_frame, text="Stay", command=self.deal_dealer, padx=5, pady=6, relief="solid", borderwidth=1, font=("Arial", 12))
        self.dealer_button.grid(row=0, column=1)

        self.reset_button = tk.Button(self.button_frame, text="New Game", command=self.new_game, padx=5, pady=6, relief="solid", borderwidth=1, font=("Arial", 12))
        self.reset_button.grid(row=0, column=2)

        self.rules_text = '''Blackjack hands are scored by their point total. The hand with the highest total wins as long as it doesn't exceed 21; a hand with a higher total than 21 is said to bust. Cards 2 through 10 are worth their face value, and face cards (jack, queen, king) are also worth 10. An ace's value is 11 unless this would cause the player to bust, in which case it is worth 1. A hand in which an ace's value is counted as 11 is called a soft hand, because it cannot be busted if the player draws another card.
        The goal of each player is to beat the dealer by having the higher, unbusted hand.'''

        self.rules_frame = tk.Frame(self.window, relief="solid", borderwidth=1)
        self.rules_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.rules_label = tk.Label(self.rules_frame, text=self.rules_text, font=("Source Code Pro", 12, "italic"), wraplength=750, justify="left")
        self.rules_label.pack()

        self.deck = []
        self.load_images()
        self.create_deck()
        self.shuffle()

        self.dealer_hand = []
        self.player_hand = []
        self.initial_deal()

    def load_images(self):
        suits = ['heart', 'club', 'diamond', 'spade']
        face_cards = ['jack', 'queen', 'king']

        for suit in suits:
            for card in range(1, 11):
                name = f"cards/{card}_{suit}.png"
                image = tk.PhotoImage(file=name)
                self.deck.append((card, image))

            for card in face_cards:
                name = f"cards/{card}_{suit}.png"
                image = tk.PhotoImage(file=name)
                self.deck.append((10, image))

    def create_deck(self):
        self.deck = list(self.deck) + list(self.deck) + list(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self, frame):
        next_card = self.deck.pop(0)
        self.deck.append(next_card)
        tk.Label(frame, image=next_card[1], relief="raised").pack(side="left")
        return next_card

    def score_hand(self, hand):
        score = 0
        ace = False
        for next_card in hand:
            card_value = next_card[0]
            if card_value == 1 and not ace:
                ace = True
                card_value = 11
            score += card_value
            if score > 21 and ace:
                score -= 10
                ace = False
        return score

    def deal_dealer(self):
        self.player_button.configure(state="disabled")
        self.dealer_button.configure(state="disabled")

        dealer_score = self.score_hand(self.dealer_hand)
        while 0 < dealer_score < 17:
            self.dealer_hand.append(self.deal_card(self.dealer_card_frame))
            dealer_score = self.score_hand(self.dealer_hand)
            self.dealer_score_label.set(dealer_score)

        player_score = self.score_hand(self.player_hand)
        if player_score > 21:
            self.result_text.set("Dealer wins!")
        elif dealer_score > 21 or dealer_score < player_score:
            self.result_text.set("Player wins!")
        elif dealer_score > player_score:
            self.result_text.set("Dealer wins!")
        else:
            self.result_text.set("Draw!")

    def deal_player(self):
        self.player_hand.append(self.deal_card(self.player_card_frame))
        player_score = self.score_hand(self.player_hand)
        self.player_score_label.set(player_score)
        if player_score > 21:
            self.result_text.set("Dealer Wins!")
            self.player_button.configure(state="disabled")
            self.dealer_button.configure(state="disabled")

    def initial_deal(self):
        self.player_button.configure(state="normal")
        self.dealer_button.configure(state="normal")

        self.deal_player()
        self.dealer_hand.append(self.deal_card(self.dealer_card_frame))
        self.dealer_score_label.set(self.score_hand(self.dealer_hand))
        self.deal_player()

    def new_game(self):
        self.player_button.configure(state="normal")
        self.dealer_button.configure(state="normal")

        self.dealer_card_frame.destroy()
        self.dealer_card_frame = tk.Frame(self.card_frame, bg="black")
        self.dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

        self.player_card_frame.destroy()
        self.player_card_frame = tk.Frame(self.card_frame, bg="black")
        self.player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

        self.result_text.set("")

        self.dealer_hand = []
        self.player_hand = []
        self.initial_deal()

    def play(self):
        self.initial_deal()
        self.window.mainloop()


if __name__ == "__main__":
    mainWindow = tk.Tk()
    game = BlackjackGame(mainWindow)
    game.play()
