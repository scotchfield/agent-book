import json
import random
import sys

VERBOSE = False


def dead( st, line=False ):
    line_st = ''

    if line is not False:
        line_st = ' Line ' + str( line )

    print( 'SORRY' + line_st + ': ' + st )

    sys.exit(1)

def getKey( key, value, obj ):
    for x in obj:
        if key in x and x[key] == value:
            return x

    return None

def getPhrase( phrases, key, variables ):
    phrase = random.choice( phrases[key] )

    for variable in variables:
        search = '{' + variable + '}'
        while phrase.find( search ) > -1:
            phrase = phrase.replace( search, variables[variable] )

    return phrase

def updateStory( world, phrases, agent, location ):
    output = []

    output.append( getPhrase( phrases, 'in-room', { 'room': location['name'] } ) )

    if 'objects' in location:
        thing = random.choice( location['objects'] )
        output.append( getPhrase( phrases, 'object-see', { 'thing': thing['name'] } ) )

    if 'movement' in location:
        move = random.choice( location['movement'].keys() )
        new_location = getKey( 'id', location['movement'][move], world['locations'] )
        output.append( getPhrase( phrases, 'movement', { 'direction': move, 'location': location['movement'][move] } ) )

    print ' '.join( output )

    return new_location


try:
    input_filename = sys.argv[1]
except IndexError:
    dead( 'Please pass the input world filename as the first argument. For example,\n> python story.py worlds/my-house.json phrases/english.json' )
input_file = open( input_filename, 'r' )
world = json.load( input_file )
input_file.close()

try:
    input_filename = sys.argv[2]
except IndexError:
    dead( 'Please pass the phrase filename as the second argument. For example,\n> python story.py worlds/my-house.json phrases/english.json' )
input_file = open( input_filename, 'r' )
phrases = json.load( input_file )
input_file.close()


if VERBOSE:
    print( world )

agent = random.choice( world['agents'] )
if 'location' in agent:
    location = getKey( 'id', agent['location'], world['locations'] )
else:
    location = random.choice( world['locations'] )

print getPhrase( phrases, 'introduction', { 'name': agent['name'] } )

for i in range( 2 ):
    location = updateStory( world, phrases, agent, location )
