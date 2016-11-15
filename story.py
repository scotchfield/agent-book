import json
import sys


def dead( st, line=False ):
    line_st = ''

    if line is not False:
        line_st = ' Line ' + str( line )

    print( 'SORRY' + line_st + ': ' + st )

    sys.exit(1)


try:
    input_filename = sys.argv[1]
except IndexError:
    dead( 'Please pass the input world filename as an argument. For example,\n> python story.py worlds/my-house.json' )
input_file = open( input_filename, 'r' )
world = json.load( input_file )

print( world )
