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

def updateStory( world, agent, location ):
    output = []

    output.append( 'I\'m standing in ' + location['name'] + '.' )
    if 'objects' in location:
        thing = random.choice( location['objects'] )
        output.append( 'As I look around, I see ' + thing['name'] + ' in the room with me.' )

    if 'movement' in location:
        move = random.choice( location['movement'].keys() )
        new_location = getKey( 'id', location['movement'][move], world['locations'] )
        output.append( 'I decide to leave, and go ' + move + ', taking me to ' + location['movement'][move] + '.' )

    print '. '.join( output )

    return new_location


try:
    input_filename = sys.argv[1]
except IndexError:
    dead( 'Please pass the input world filename as an argument. For example,\n> python story.py worlds/my-house.json' )
input_file = open( input_filename, 'r' )
world = json.load( input_file )

if VERBOSE:
    print( world )

agent = random.choice( world['agents'] )
location = random.choice( world['locations'] )

print 'My name is ' + agent['name'] + '. This is my story.'

for i in range( 2 ):
    location = updateStory( world, agent, location )
