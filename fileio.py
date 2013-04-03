#utils.py

import csv
import json
from collections import *
from itertools import *


def json_to_csv( json_filename, csv_filename ):
    
    infile = open( json_filename, "r" )
    
    
    #get meta data.
    first_line = json.loads( infile.readline() )
    flattened = flattenDict( first_line )
    fieldnames = flattened.keys()
    
    #set up the csv
    outfile = open( csv_filename, "wb" )
    csvfile = csv.DictWriter(outfile, fieldnames =fieldnames, delimiter = "|" )
    csvfile.writeheader()
    
    
    flattened[(u'text',)] = repr( flattened[(u'text',)] )
    csvfile.writerow( flattened )
    
    i = 1
    for line in infile:
        data_line = json.loads( line )
        flattened = flattenDict( data_line )
        flattened[(u'text',)] = repr( flattened[(u'text',)] )
        csvfile.writerow( flattened )
        i+=1
        if i%100==0:
            print i
        
    infile.close()
    outfile.close()
     
    return 
    
    
same = lambda x:x  # identity function
add = lambda a,b:a+b
_tuple = lambda x:(x,)  # python actually has coercion, avoid it like so
    
def flattenDict(dictionary, keyReducer=add, keyLift=_tuple, init=()):
    # http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
    # semi-lazy: goes through all dicts but lazy over all keys
    # reduction is done in a fold-left manner, i.e. final key will be
    #     r((...r((r((r((init,k1)),k2)),k3))...kn))

    def _flattenIter(pairs, _keyAccum=init):
        atoms = ((k,v) for k,v in pairs if not isinstance(v, Mapping))
        submaps = ((k,v) for k,v in pairs if isinstance(v, Mapping))
        def compress(k):
            return keyReducer(_keyAccum, keyLift(k))
        return chain(
            (
                (compress(k),v) for k,v in atoms
            ),
            *[
                _flattenIter(submap.items(), compress(k))
                for k,submap in submaps
            ]
        )
    return dict(_flattenIter(dictionary.items()))