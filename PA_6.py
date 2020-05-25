suits = 'CDHS'
ranks = '23456789TJQKA'

from abc import ABCMeta, abstractmethod
import sys
from enum import IntEnum
import logging

class Ranking(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")
    
    @property #인자처럼 쓸 수 있게 해준다 특정값에 따라 인자가 계속 바뀌어야하는경우 or 인자가 너무 많을때
    def rank(self):
        return self.card[0]
    
    @property
    def suit(self): 
        return self.card[1]

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()





class PKCard(Card):
    values = dict(zip(ranks, range(2, 2+len(ranks))))
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    def value(self):
        return PKCard.values[self.card[0]]
    

import random
class Deck:
    def __init__(self, cls):
        self.cards = []
        self.cards = [cls(i+j) for i in ranks for j in suits]
        
    
    def __str__(self):
        return str(self.cards)
    
    def shuffle(self):
        self.cards = random.sample(self.cards, len(self.cards))
        return self.cards
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]
    
    def pop(self):
        return self.cards.pop()



class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = sorted(cards, reverse=True)
    
    def __str__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]
    
    def pop(self):
        return self.cards.pop()
    
    def value(self, key):
        dic = dict(zip(ranks, range(2, 2+len(ranks))))
        return dic.get(key)

    def is_flush(self):
        test_suit = str(self.cards[0]) #ㄴself.cards의 원소에는 Card형이 들어가므로 str을 씌워줘야한다
        if(all(str(element)[1] == test_suit[1] for element in self.cards)):
            return True
        else:
            return False
    
    def is_straight(self):
        temp = []
        for i in self.cards:
            temp.append(self.value(str(i)[0])) #value함수에 인자를 추가해줘야했다.
        temp = sorted(temp, reverse=True)
        if temp == [14, 5, 4, 3, 2]:
            return True
        else:
            stop = 1
            for i in range (0, 4):
                if temp[i] != temp[i+1] + 1:
                    return False
                    stop = 0
            if stop == 1:
                return True
    
    def classify_by_rank(self):
        temp = []
        for i in self.cards:
            temp.append(self.value(str(i)[0]))  
        temp = sorted(temp, reverse=True)
        r_Dic = {}
        for i in temp:
            if i not in r_Dic:
                r_Dic[i] = 1
            else:
                r_Dic[i] += 1
        return r_Dic
    
    def find_a_kind(self):
        r_Dic2 = self.classify_by_rank()
        val_num = list(r_Dic2.values())

        if 4 in val_num:
            return 8 #'Four of a kind'
        elif 3 in val_num and 2 in val_num:
            return 7 #'Full house'
        elif val_num.count(2) == 2:
            return 3 #'Two pair'
        elif 3 in val_num:
            return 4 #'Three of a kind'
        elif 2 in val_num:
            return 2 #'One pair'
        else:
            return 1 #'High card'
    
    def tell_hand_ranking(self):
        if self.is_flush() == True:
            flush = True
        else:
            flush = False
        if self.is_straight() == True:
            straight = True
        else:
            straight = False
        fak = self.find_a_kind()
        if flush == True and straight == True:
            return 9 #'Straight flush'
        elif fak == 8: #'Four of a kind'
            return 8 #'Four of a kind'
        elif fak == 7: #'Full house':
            return 7 #'Full house'
        elif flush == True:
            return 6 #'Flush'
        elif straight == True:
            return 5 #'Straight'
        elif fak == 4: #'Three of a kind':
            return 4 #'Three of a kind'
        elif fak == 3: #'Two pair':
            return 3 #'Two pair'
        elif fak == 2: #'One pair':
            return 2 #'One pair'
        else:
            return 1 #'High card'
    def play_game(self, other):
        p1 = self.tell_hand_ranking()
        p2 = other.tell_hand_ranking()
        p1_dic0 = self.classify_by_rank()
        p2_dic0 = other.classify_by_rank()
        p1_dic = {}
        p2_dic = {}
        for k, v in p1_dic0.items():
            p1_dic[v] = k
        for i, j in p2_dic0.items():
            p2_dic[j] = i
        
        temp1 = []
        for i in self.cards:
            temp1.append(self.value(i[0]))  
        p1_sorted = sorted(temp1, reverse=True)
        temp2 = []
        for i in other.cards:
            temp2.append(other.value(i[0]))  
        p2_sorted = sorted(temp2, reverse=True)

        if(p1 > p2):
            return "p1 has won!"
        if(p1 < p2):
            return "p2 has won!"
        elif(p1 == 9 or p1 == 6 or p1 == 5 or p1 == 1):
            if(p1_sorted > p2_sorted):
                return "p1 has won!"
            elif(p1_sorted < p2_sorted):
                return "p2 has won!"
            else:
                return "draw!"
        elif(p1 == 8):
            if(p1_dic[4] > p2_dic[4]):
                return "p1 has won!"
            else:
                return "p2 has won!"
        elif(p1 == 7 or p1 == 4):
            if(p1_dic[3] > p2_dic[3]):
                return "p1 has won!"
            elif(p1_dic[3] == p2_dic[3]):
                if str(p1_dic.values()) > str(p2_dic.values()):
                    return "p1 has won!"
                elif str(p1_dic.values()) == str(p2_dic.values()):
                    return "draw!"
                else:
                    return "p2 has won!"
            else:        
                return "p2 has won!"
        elif(p1 == 3):
            k1 = []
            k2 = []
            for i in p1_dic0:
                if(p1_dic0[i] == 2):
                    k1.append(i)
            for i in p2_dic0:
                if(p2_dic0[i] == 2):
                    k2.append(i)

            if(k1 > k2):
                return "p1 has won!"
            elif(k1 < k2):
                return "p2 has won!"
            else:
                if(p1_dic[1] > p2_dic[1]):
                    return "p1 has won!"
                elif(p1_dic[1] < p2_dic[1]):
                    return "p2 has won!"
                else:
                    return "draw!"
        elif(p1 == 2):
            if(p1_dic[2] > p2_dic[2]):
                return "p1 has won!"
            elif(p1_dic[2] < p2_dic[2]):
                return "p2 has won!"
            else:
                k1 = []
                k2 = []
                for i in p1_dic0:
                    if(p1_dic0[i] == 1):
                        k1.append(i)
                for i in p2_dic0:
                    if(p2_dic0[i] == 1):
                        k2.append(i)
                if(k1 > k2):
                    return "p1 has won!"
                elif(k1 < k2):
                    return "p2 has won!"
                else:
                    return "draw!"
        elif(p1 == 1):
            if(p1_dic[1] > p2_dic[1]):
                return "p1 has won!"
            elif(p1_dic[1] < p2_dic[1]):
                return "p2 has won!"
            else:
                return "draw!"
                

        
        

# if __name__ == "__main__":
#     import sys
#     def test(did_pass):
#         """  Print the result of a test.  """
#         linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
#         if did_pass:
#             msg = "Test at line {0} ok.".format(linenum)
#         else:
#             msg = ("Test at line {0} FAILED.".format(linenum))
#         print(msg)
    
#     deck = Deck(PKCard)  # deck of poker cards
#     deck.shuffle()
#     c = deck[0]   # __getitem__
#     print('A deck of', c.__class__.__name__)
#     #print(deck)   #__str__
#     #print(deck[-5:])
#     while len(deck) >= 10:   # __len__
#         my_hand = []
#         your_hand = []
#         for i in range(5):
#             for hand in (my_hand, your_hand):
#                 card = deck.pop()
#                 hand.append(card)
#         p1 = Hands(my_hand)
#         p2 = Hands(your_hand)

#     p1 = Hands(['2D', '3D', '4D', '5D', 'AD'])
#     p2 = Hands(['3H', '4H', '5H', '6H', '7H']) #9
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['3H', '4H', '5H', '6H', '7H'])
#     p2 = Hands(['2D', '3D', '4D', '5D', 'AD']) #9
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['3D', '4D', '5D', '6D', '7D'])
#     p2 = Hands(['3H', '4H', '5H', '6H', '7H']) #9
#     test(p1.play_game(p2) == "draw!")

#     p1 = Hands(['2D', '2H', '2S', '2C', 'AD'])
#     p2 = Hands(['4D', '4H', '4S', '4C', '7D']) #8
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['6D', '6H', '6S', '6C', 'AD'])
#     p2 = Hands(['4D', '4H', '4S', '4C', '7D']) #8
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['6D', '6H', '6S', '3C', '3D'])
#     p2 = Hands(['4D', '4H', '4S', '7C', '7D']) #7
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['2D', '2H', '6S', '2C', '6D'])
#     p2 = Hands(['4D', '2H', '4S', '4C', '2D']) #7
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['2D', '3D', '6D', '7D', 'KD'])
#     p2 = Hands(['4C', '2C', '5C', '8C', 'TC']) #6
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['4C', '2C', '5C', '8C', 'TC']) 
#     p2 = Hands(['2D', '3D', '6D', '7D', 'KD']) #6
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['4C', '2C', '5C', '8C', 'TC']) 
#     p2 = Hands(['4D', '2D', '5D', '8D', 'TD']) #6
#     test(p1.play_game(p2) == "draw!")

#     p1 = Hands(['7C', '6D', '8S', '9S', 'TH']) 
#     p2 = Hands(['4D', '5H', '6C', '3D', '2S']) #5
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['4D', '5H', '6C', '3D', '2S']) 
#     p2 = Hands(['7C', '6D', '8S', '9S', 'TH']) #5
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['4D', '5H', '6C', '3D', '2S']) 
#     p2 = Hands(['4C', '5D', '6S', '3S', '2H']) #5
#     test(p1.play_game(p2) == "draw!")

#     p1 = Hands(['7D', '7H', '7C', '3D', '2S']) 
#     p2 = Hands(['5C', '5D', '5S', '3S', '2H']) #4
#     test(p1.play_game(p2) == "p1 has won!")
    
#     p1 = Hands(['8C', '8D', '8S', '3S', '4H']) 
#     p2 = Hands(['7D', '7H', '7C', '3D', '2S']) #4
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['9C', '9D', '4S', '4D', '2H']) 
#     p2 = Hands(['7D', '7H', '3C', '3D', '2S']) #3
#     test(p1.play_game(p2) == "p1 has won!")
    
#     p1 = Hands(['5C', '5D', '4S', '4D', '2H']) 
#     p2 = Hands(['7D', '7H', '3C', '3D', '2S']) #3
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['5C', '5D', '4S', '4D', '7H']) 
#     p2 = Hands(['5S', '5H', '4C', '4H', '2S']) #3
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['5C', '5D', '4S', '4D', '2H']) 
#     p2 = Hands(['5S', '5H', '4C', '4H', '7S']) #3
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['5C', '5D', '4S', '4D', '7H']) 
#     p2 = Hands(['5S', '5H', '4C', '4H', '7S']) #3
#     test(p1.play_game(p2) == "draw!")

#     p1 = Hands(['5C', '5D', '4S', '3D', '7H']) 
#     p2 = Hands(['2S', '5H', '4C', '4H', '7S']) #2
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['2C', '2D', '4S', '3D', '7H']) 
#     p2 = Hands(['8S', '5H', '4C', '4H', '7S']) #2
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['5C', '5D', '4S', '2D', '7H']) 
#     p2 = Hands(['5S', '5H', '4C', '2H', '7S']) #2
#     test(p1.play_game(p2) == "draw!")

#     p1 = Hands(['5C', '5D', '4S', '2D', 'KH']) 
#     p2 = Hands(['5S', '5H', '4C', '2H', '7S']) #2
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['5C', '5D', '4S', '2D', 'KH']) 
#     p2 = Hands(['5S', '5H', '4C', '2H', 'AS']) #2
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['5C', '2D', '4S', '7D', 'KH']) 
#     p2 = Hands(['5S', '6H', '4C', '7H', '9S']) #1
#     test(p1.play_game(p2) == "p1 has won!")

#     p1 = Hands(['5C', '2D', '4S', '7D', '8H']) 
#     p2 = Hands(['5S', '6H', '4C', '7H', 'KS']) #1
#     test(p1.play_game(p2) == "p2 has won!")

#     p1 = Hands(['5C', '6D', '4S', '7D', 'KH']) 
#     p2 = Hands(['5S', '6H', '4C', '7H', 'KS']) #1
#     test(p1.play_game(p2) == "draw!")

    
    
