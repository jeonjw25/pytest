import pytest
from PA_6 import*

non_flush_suit = 'CHSDS'
flush_suit = 'SSSSS'
test_cases = {
    
     Ranking.STRAIGHT_FLUSH: (
         tuple(zip('AKQJT', flush_suit)),
         tuple(zip('KQJT9', flush_suit)),
     ),
     Ranking.FOUR_OF_A_KIND: (
         tuple(zip('TTTTQ',non_flush_suit)),
         tuple(zip('9999A', flush_suit)),
     ),
     Ranking.FULL_HOUSE: (
         tuple(zip('88877', non_flush_suit)),
         tuple(zip('22299', flush_suit)),
     ),
     Ranking.FLUSH: (
         tuple(zip('AJT98', flush_suit)),
         tuple(zip('AJ987', flush_suit)),
     ),
     Ranking.STRAIGHT: (
         tuple(zip('AKQJT', non_flush_suit)),
         tuple(zip('5432A', non_flush_suit)),
         tuple(zip('KQJT9', non_flush_suit)),
     ),
     Ranking.THREE_OF_A_KIND: (
         tuple(zip('888A9', non_flush_suit)),
         tuple(zip('888A7', non_flush_suit)),
     ),
     Ranking.TWO_PAIRS: (
         tuple(zip('AA998', non_flush_suit)),
         tuple(zip('AA778', non_flush_suit)),
         tuple(zip('JJTTK', non_flush_suit)),
     ),
     Ranking.ONE_PAIR: (
         tuple(zip('88AT9', non_flush_suit)),
         tuple(zip('88AT7', non_flush_suit)),
         tuple(zip('77AKQ', non_flush_suit)),
     ),
     Ranking.HIGH_CARD: (
         tuple(zip('AJT98', non_flush_suit)),
         tuple(zip('AJT97', non_flush_suit)),
         tuple(zip('QJT97', non_flush_suit)),
     )

 }

draw_cases = {
    
     Ranking.FULL_HOUSE: (
         tuple(zip('88877', non_flush_suit)),
         tuple(zip('88877', flush_suit)),
     ),
     Ranking.FLUSH: (
         tuple(zip('AJT98', flush_suit)),
         tuple(zip('AJT98', flush_suit)),
     ),
     Ranking.STRAIGHT: (
         tuple(zip('AKQJT', non_flush_suit)),
         tuple(zip('AKQJT', non_flush_suit)),
     ),
     Ranking.THREE_OF_A_KIND: (
         tuple(zip('888A9', non_flush_suit)),
         tuple(zip('888A9', non_flush_suit)),
     ),
     Ranking.TWO_PAIRS: (
         tuple(zip('AA998', non_flush_suit)),
         tuple(zip('AA998', non_flush_suit)),
     ),
     Ranking.ONE_PAIR: (
         tuple(zip('88AT9', non_flush_suit)),
         tuple(zip('88AT9', non_flush_suit)),
     ),
     Ranking.HIGH_CARD: (
         tuple(zip('AJT98', non_flush_suit)),
         tuple(zip('AJT98', non_flush_suit)),
     )

 }



def test_PKCard_init():
    c = PKCard('AD')
    assert c.rank == 'A' and c.suit == 'D'
    assert c.card == 'AD'

def test_PKCard_repr():
    assert repr(PKCard('AC')) == 'AC'

@pytest.fixture #테스트파일에서 쓰이는 고정재료설정
def all_faces():
    return [r+s for r in ranks for s in suits]

def test_PKCArd_value(all_faces):
    for face in all_faces:
        card, expected = PKCard(face), PKCard.values[face[0]]
    assert card.value() == expected

@pytest.fixture
def c9C():
    return PKCard('9C')

@pytest.fixture
def c9H():
    return PKCard('9H')

@pytest.fixture
def cTH():
    return PKCard('TH')

def test_PKCard_comp(c9C, c9H, cTH):
    assert c9C == c9C and c9C ==c9H
    assert c9H < cTH and c9C < cTH
    assert c9C <= c9H <= cTH
    assert cTH > c9H and cTH > c9C
    assert cTH >= c9H >= c9C
    assert c9C != cTH and c9H != cTH

def test_PKCard_sort(all_faces):
    all_cards = [PKCard(c) for c in all_faces]
    import random
    random.shuffle(all_cards)
    all_cards.sort()
    numbers = []
    for i in range(2, 2+len(ranks)):
        for s in suits:
            numbers.append(i)
    assert [c.value() for c in all_cards] == [i for i in numbers]

@pytest.fixture
def deck():
    return Deck(PKCard)

def test_Deck_init(deck): #fixture를 인자로!
    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], PKCard)

def test_Deck_pop(deck):
    card = deck.pop()
    assert card.rank == ranks[-1] and card.suit == suits[-1] and len(deck.cards) == 51

def test_Deck_len(deck):
    deck.pop(); deck.pop()
    assert len(deck.cards) == deck.__len__() == len(deck) == 52-2
    
def test_Deck_getitem(deck):
    assert (deck[10].rank, deck[10].suit) == (deck.cards[10].rank, deck.cards[10].suit)

def cases(*rankings):
    if not rankings:
        rankings = test_cases.keys()
    return \
        [ ([r+s for r, s in case], ranking)
                    for ranking in rankings
                        for case in test_cases[ranking]
        ]

@pytest.mark.parametrize("faces, expected", cases(Ranking.FLUSH))
def test_is_flush(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    #print(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.is_flush()
    hand_org_sorted = sorted(hand_org, reverse = True)
    assert result == True
    assert hand.cards == hand_org_sorted


@pytest.mark.parametrize("faces, expected", cases(Ranking.STRAIGHT))
def test_is_straight(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    #print(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.is_straight()
    hand_org_sorted = sorted(hand_org, reverse = True)
    assert result == True
    assert hand.cards == hand_org_sorted

def test_classify_by_rank():
    c = Hands(['3D', '3C', '6H', '6D', '7D'])
    result = c.classify_by_rank()
    assert result == {7: 1, 6: 2, 3: 2}

@pytest.mark.parametrize("faces, expected", cases(Ranking.FOUR_OF_A_KIND, Ranking.FULL_HOUSE, Ranking.THREE_OF_A_KIND, Ranking.TWO_PAIRS, Ranking.ONE_PAIR, Ranking.HIGH_CARD))
def test_find_a_kind(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    #print(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.find_a_kind()
    hand_org_sorted = sorted(hand_org, reverse = True)
    assert result == expected
    assert hand.cards == hand_org_sorted


@pytest.mark.parametrize("faces, expected", cases(Ranking.FOUR_OF_A_KIND, Ranking.FULL_HOUSE, Ranking.THREE_OF_A_KIND, Ranking.TWO_PAIRS, Ranking.ONE_PAIR, Ranking.HIGH_CARD, Ranking.STRAIGHT_FLUSH, Ranking.FLUSH, Ranking.STRAIGHT))
def test_tell_hand_ranking(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    #print(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.tell_hand_ranking()
    hand_org_sorted = sorted(hand_org, reverse = True)
    assert result == expected
    assert hand.cards == hand_org_sorted

# print(len(t))
# print(t[0])         
def test_play_game():
    rankings = test_cases.keys()
    t = [ ([r+s for r, s in case])
                for ranking in rankings
                    for case in test_cases[ranking]
            ]
    n = len(t)
    for i in range(0, n):
        for j in range(i+1, n):
            p1 = Hands(t[i])
            p2 = Hands(t[j])
            result = p1.play_game(p2)
            assert result == 'p1 has won!'
    
    for i in range(0, n):
        for j in range(i+1, n):
            p2 = Hands(t[i])
            p1 = Hands(t[j])
            result = p1.play_game(p2)
            assert result == 'p2 has won!'

drankings = draw_cases.keys()

def dcases(*drankings):
    # print(rankings)
    if not drankings:
       drankings = draw_cases.keys()
       print('Here')
       print(drankings)
    return \
        [ ([r+s for r, s in case])
                for ranking in drankings
                    for case in draw_cases[ranking]
        ]

def test_is_draw():

    s1 = dcases(Ranking.FULL_HOUSE)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    s1 = dcases(Ranking.FLUSH)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    s1 = dcases(Ranking.STRAIGHT)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    s1 = dcases(Ranking.THREE_OF_A_KIND)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    s1 = dcases(Ranking.TWO_PAIRS)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    s1 = dcases(Ranking.ONE_PAIR)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    s1 = dcases(Ranking.HIGH_CARD)
    p1 = Hands(s1[0])
    p2 = Hands(s1[1])
    result = p1.play_game(p2)
    assert result == 'draw!'

    


# @pytest.mark.parametrize("fa", d_cases(Ranking.FULL_HOUSE))
# def test_draw(fa):
#     print(fa)
    # hand = [Hands([PKCard(c) for c in faces])]
    # p1 = hand[0]
    # p2 = hand[1]
    # result = p1.play_game(p2)
    #assert result == 'draw!'

    # m = len(d)
    # for i in range(0, m):
    #     for j in range(i+1, m):
    #         p1 = Hands(d[i])
    #         p2 = Hands(d[j])
    #         result = p1.play_game(p2)
    #         assert result == 'draw!'
    


