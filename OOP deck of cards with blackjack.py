import random

#Card and Deck classes
class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
    self.name = '{} of {}'.format(self.correct_name(value), suit)

  def __repr__(self):
    return self.name
    
  def correct_name(self, card):
    if card == 1:
      card = "Ace"
    elif card == 11:
      card = "Jack"
    elif card == 12:
      card = "Queen"
    elif card == 13:
      card = "King"
    else:
      card = str(card)
    return card
      
class Deck:
  def __init__(self):
    self.contents = []
    self.build_deck()
    self.shuffle()

  def __repr__(self):
    return str(self.contents)

  def __getitem__(self, index):
    return self.contents[index]

  def deal_cards(self, recipient, cards_to_be_dealt):
    for card in range(cards_to_be_dealt):
      recipient.hand.append(self.pop())

  def build_deck(self):
    for suit in ['Spades', 'Clubs', 'Hearts', 'Diamonds']:
      for value in range(1, 14):
        self.contents.append(Card(value, suit))

  def shuffle(self):
    random.shuffle(self.contents)

  def pop(self, index =-1):
    item_to_be_popped = self.contents[index]
    self.contents = [card for card in self.contents if 
    card is not item_to_be_popped]
    return item_to_be_popped
    

#Player and Dealer class
class Player:
  def __init__(self, name):
    self.hand = []
    self.name = name
    self.account_balance = 2000
    self.score = 0
    #for blackjack specifically 
    self.stand = False
    self.outcome_num = 0
      
  def __repr__(self):
    return self.name

####Blackjack game functions####

#deal cards
def deal_cards():
  for recipient in [player, dealer]:
    deck_of_cards.deal_cards(recipient, 2)
    #this only applies to player to prevent immediate blackjack by dealer
    player.score = calculate_score(player.hand)

#display cards
def display_cards():
  print('\nThe dealer\'s cards are: {}\nScore: {}'.format(dealer.hand, calculate_score(dealer.hand)))
  print('\nYour cards are: {}\nScore: {}'.format(player.hand, calculate_score(player.hand)))
  set_scores()

#hide dealer card for first turn
def display_cards_turn1():
  print('\nThe dealer\'s cards are: [Unknown, {}]\nScore: {}'.format(dealer.hand[-1], calculate_score(dealer.hand[-1])))
  dealer.score = calculate_score(dealer.hand[-1])
  print('\nYour cards are: {}\nScore: {}'.format(player.hand, calculate_score(player.hand)))
  player.score = calculate_score(player.hand)

#place bid
def place_bid():
  choice_made = False
  while choice_made == False: 
    try:
      amount_to_bet = int(input('Your current balance is ${}, how much would you like to bet?\n'.format(player.account_balance)))
      if amount_to_bet > player.account_balance:
        print('\nI\'m sorry, you have insufficiant funds, please enter a valid amount.\n')
        continue
      else:
        choice_made = True
    except ValueError:
      print('\nI\'m sorry that choice is invalid, please enter a numerical\n')
      continue
  return amount_to_bet
    

#awards winnings or losses
def award_winnings_or_losses(pot):
  if player.outcome_num == 0:
    player.account_balance -= pot
    print('\n${} was debited from your account'.format(pot))
  elif player.outcome_num == 1:
    player.account_balance += pot
    print('\n${} was credited to your account'.format(pot))
  else:
    print('\nYour account balance has remained unchanged')

#calculate card values
def calculate_score(player_hand):
  score = 0
  #this is applies during turn 1 when there is a single card object being calculated for the dealer
  if type(player_hand) == Card: 
    if player_hand.name[:1] in ['K', 'Q', 'J']:
      player_hand.value = 10
    elif player_hand.name[:1] == 'A':
      player_hand.value = 11
    score += player_hand.value
  else:
    for card in player_hand:
      if card.name[:1] in ['K', 'Q', 'J']:
        card.value = 10
        score += card.value
      #this changes the value of an ace to 1 to prevent player going bust unnessessarily
      elif card.name[:1] == 'A':
        card.value = 11
        temp_score = score + card.value
        if temp_score > 21:
          card.value = 1
          score += card.value
        else: 
          score = temp_score
      else:
        temp_score = score + card.value
        #if there is an ace already in the hand, this prevents the player from going bust by changing as many aces as nessessary to a value of 1
        if temp_score > 21:
          new_score = 0
          for e in player_hand:
            if e.name[:1] == 'A':
              e.value = 1
            new_score += e.value
          score = new_score
        else:
          score = temp_score
  return score

#hit or stand fucntions
def hit_or_stand(recipient):
  choice_made = False
  while choice_made == False:
    answer = input('\nWould you like to hit or stand?\nPress h to hit or s to stand')
    if answer not in ['h', 's']:
      print('\nI\'m sorry, please enter a valid selection.')
    elif answer == 'h':
      hit(recipient)
      choice_made = True
    else:
      stand()
      choice_made = True

def hit(recipient):
  recipient.hand.append(deck_of_cards.pop())
  recipient.score = calculate_score(recipient.hand)

def stand():
  player.stand = True
  dealer.score = calculate_score(dealer.hand)
  while dealer.score < 17:
    hit(dealer)

def dealers_turn():
  if dealer.score < 17:
    hit(dealer)
  
#checks for  victory conditions
def check():
  if player.score > 21:
    print('\nBust!')
    player.outcome_num = 0
    declare_winner(dealer)
    return True
  elif dealer.score == 21:
    player.outcome_num = 0
    declare_winner(dealer)
    return True
  elif dealer.score > 21:
    print('\nDealer is bust')
    player.outcome_num = 1
    declare_winner(player)
    return True
  elif player.score == 21:
    print('\nBlackjack!')
    player.outcome_num = 1
    declare_winner(player)
    return True
  elif player.stand == True:
    if dealer.score == player.score:
      print('\nIt\'s a draw!')
      player.outcome_num = 2
      return True
    elif player.score > dealer.score:
      player.outcome_num = 1
      declare_winner(player)
      return True
    elif dealer.score > player.score:
      player.outcome_num = 0
      declare_winner(dealer)
      return True
  else:
    return False

#declare a winner
def declare_winner(winner):
  print('{} has won the game'.format(winner))

#resets game
def reset_game():
  choice_made = False
  while choice_made == False:
    answer = input('\nWould you like to play again?\nPress y for Yes or n for No')
    if answer not in ['y', 'n']:
      print('I\'m sorry, please enter a valid answer')
      continue
    elif answer == 'y':
      player.score = 0
      player.hand = []
      player.stand = False
      dealer.score = 0
      dealer.hand = []
      deck_of_cards.contents = []
      deck_of_cards.build_deck()
      deck_of_cards.shuffle()
      play_blackjack()
    else:
      exit()

#applies card calculation to player/dealer score
def set_scores():
  player.score = calculate_score(player.hand)
  dealer.score = calculate_score(dealer.hand)

#Blackjack function
def play_blackjack():
  if player.account_balance <= 0:
    print('\nI\'m sorry, your account balance is $0. Have a nice day.')
    exit()
  turn_count = 1
  print('#### Welcome to Blackjack ####\n')
  pot = place_bid()
  deal_cards()
  while True:
    if turn_count == 1:
      display_cards_turn1()
      conditons_met = check()
      if conditons_met == True:
        break
    hit_or_stand(player)
    if turn_count == 1:
      turn_count += 1
      #Turn 2 starts here and dealer flips upside down card
      display_cards()
      conditons_met = check()
      if conditons_met == True:
        break
      continue
    dealers_turn()
    display_cards()
    conditons_met = check()
    if conditons_met == True:
      break
  award_winnings_or_losses(pot)
  reset_game()

deck_of_cards = Deck()
dealer = Player('Dealer')
player = Player('Player')
play_blackjack()