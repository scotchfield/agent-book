import json
import random
import re
import sys

VERBOSE = False


def wordCount( st ):
    return len( re.findall( r'\b\w+\b', st ) )

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

    for agent in world['agents']:
        if 'location' in agent and agent['location'] == location['id']:
            output.append( getPhrase( phrases, 'agent-see', { 'agent': agent['name'], 'adjective': random.choice( agent['adjectives'] ) } ) )

    if 'movement' in location:
        move = random.choice( location['movement'].keys() )
        new_location = getKey( 'id', location['movement'][move], world['locations'] )
        output.append( getPhrase( phrases, 'movement', { 'direction': move, 'location': location['movement'][move] } ) )

    for i in range( random.randint( 0, 6 ) ):
        flavour = getPhrase( phrases, 'flavour', { 'adjective': random.choice( phrases['adjectives'] ), 'adjective-2': random.choice( phrases['adjectives'] ) } )
        output.insert( random.randint( 0, len( output ) ), flavour )

    story = ' '.join( output )

    return story, new_location


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

story = getPhrase( phrases, 'introduction', { 'name': agent['name'] } )
story += "\n\n"

while wordCount( story ) < 55000:
    new_story, location = updateStory( world, phrases, agent, location )
    story += new_story + "\n\n"

print story
