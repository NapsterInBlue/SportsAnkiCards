from anki import Collection as aopen
import getTrivia

path = r"C:\Users\Nick\Documents\Anki\User 1\collection.anki2"
frontDict = {'baseball': '{} World Series',
             'basketball': '{} NBA Finals',
             'hockey': '{} Stanley Cup Finals'
            }

def writeSeries(year, winner, loser, mvp, sport):
    deck = aopen(path)
    deck_id = deck.decks.id('Sports')
    deck.decks.select(deck_id)
    model = deck.models.byName('Basic')
    model['did'] = deck_id
    deck.models.save(model)
    deck.models.setCurrent(model)
    fact = deck.newNote()
    fact['Front'] = frontDict[sport].format(year)
    fact['Back'] = '{} > {}<br><br>MVP:<br>{}'.format(winner, loser, mvp)
    deck.addNote(fact)
    deck.save()
    deck.close()