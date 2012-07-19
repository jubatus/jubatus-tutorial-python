#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,json
from jubatus.classifier import client
from jubatus.classifier import types

def parse_args():
    from optparse import OptionParser, OptionValueError
    p = OptionParser()
    p.add_option('-s', '--server_ip', action='store',
                 dest='server_ip', type='string', default='127.0.0.1')
    p.add_option('-p', '--server_port', action='store',
                 dest='server_port', type='int', default='9199')
    p.add_option('-n', '--name', action='store',
                 dest='name', type='string', default='tutorial')
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
        if prob == None or res.prob > prob :
            ans = res.label
            prob = res.prob
            result[0] = ans
            result[1] = prob
    return result



if __name__ == '__main__':
    options, remainder = parse_args()

    classifier = client.classifier(options.server_ip,options.server_port)

    converter = {
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
                }

    config = types.config_data(options.algo, json.dumps(converter))

    pname = options.name

    print classifier.set_config(pname,config)
    
    print classifier.get_config(pname)
    print classifier.get_status(pname)


    for line in open('train.dat'):
        label, file = line[:-1].split(',')
        dat = open(file).read()
        datum = types.datum(  [["message", dat]], [] )
#                           ([sv(=string vector)], [nv(=number vector)])
        classifier.train(pname,[(label,datum)])
        print classifier.get_status(pname)

    print classifier.save(pname, "tutorial")

    print classifier.load(pname, "tutorial")

    print classifier.set_config(pname, config)

    print classifier.get_config(pname)

    for line in open('test.dat'):
        label, file = line[:-1].split(',')
        dat = open(file).read()        
        datum = types.datum(  [["message", dat]], [] )
        ans = classifier.classify(pname,[(datum)])
        if ans != None:
            estm = get_most_likely(ans[0])
            if (label == estm[0]):
                result = "OK"
            else:
                result = "NG"
            print result + "," + label + ", " + estm[0] + ", " + str(estm[1])


