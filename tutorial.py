#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import jubatus

def parse_args():
    from optparse import OptionParser, OptionValueError
    p = OptionParser()
    p.add_option('-s', '--server_list', action='store',
                 dest='server_list', type='string', default='localhost:9199')
    p.add_option('-n', '--name', action='store',
                 dest='name', type='string', default='test')
    p.add_option('-a', '--algo', action='store',
                 dest='algo', type='string', default="PA")
    return p.parse_args()

def get_most_likely(estm):
    ans = None
    prob = None
    result = {}
    result[0] = ''
    result[1] = 0
    for res in estm:
        if prob == None or res[1] > prob :
            ans = res[0]
            prob = res[1]
            result[0] = ans
            result[1] = prob
    return result



if __name__ == '__main__':
    options, remainder = parse_args()

    classifier = jubatus.Classifier(options.server_list, options.name)

    config = {
            'converter': {
              "string_filter_types": {
              "detag": { "method": "regexp", "pattern": "<[^>]*>", "replace": "" }
               },
              "string_filter_rules":
                 [
                { "key": "message", "type": "detag", "suffix": "-detagged" }
                 ],
                'num_filter_types': {},
                'num_filter_rules': [],
                'string_types': {},
                'string_rules': [
                    {'key': 'message-detagged', 'type': "space", "sample_weight": "bin", "global_weight": "bin"}
                    ],
                'num_types': {},
                'num_rules': []
                },
            'method': options.algo
            }

    print classifier.set_config(config)
    
    print classifier.get_config()

    print classifier.get_status()

    i = 0
    for line in open('train.dat'):
        label, file = line[:-1].split(',')
        dat = open(file).read()
        classifier.train(
            [( label ,  ([["message", dat]], ) ,)]
        )
        i = i + 2
        print i, classifier.get_status()

    print classifier.save("tutorial")

    print classifier.load("tutorial")

    print classifier.set_config(config)

    print classifier.get_config()

    for line in open('test.dat'):
        label, file = line[:-1].split(',')
        dat = open(file).read()        
        ans = classifier.classify(
            [([["message", dat]], )]
           )
        print ans
        i = i + 1
        if ans != None:
            estm = get_most_likely(ans[0])
            if (label == estm[0]):
                result = "OK"
            else:
                result = "NG"
            print i, result + "," + label + ", " + estm[0] + ", " + str(estm[1])


