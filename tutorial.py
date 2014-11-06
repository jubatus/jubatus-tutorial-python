#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,json

from jubatus.classifier.client import Classifier
from jubatus.classifier.types import LabeledDatum
from jubatus.common import Datum

def parse_args():
    from optparse import OptionParser, OptionValueError
    p = OptionParser()
    p.add_option('-s', '--server_ip', action='store',
                 dest='server_ip', type='string', default='127.0.0.1')
    p.add_option('-p', '--server_port', action='store',
                 dest='server_port', type='int', default='9199')
    p.add_option('-n', '--name', action='store',
                 dest='name', type='string', default='tutorial')
    return p.parse_args()

def get_most_likely(estm):
    ans = None
    prob = None
    result = {}
    result[0] = ''
    result[1] = 0
    for res in estm:
        if prob == None or res.score > prob :
            ans = res.label
            prob = res.score
            result[0] = ans
            result[1] = prob
    return result



if __name__ == '__main__':
    options, remainder = parse_args()

    classifier = Classifier(options.server_ip,options.server_port, options.name, 10.0)

    print classifier.get_config()
    print classifier.get_status()


    for line in open('train.dat'):
        label, file = line[:-1].split(',')
        dat = open(file).read()
        datum = Datum({"message": dat})
        classifier.train([LabeledDatum(label, datum)])

    print classifier.get_status()

    print classifier.save("tutorial")

    print classifier.load("tutorial")

    print classifier.get_config()

    count_ok = 0
    count_ng = 0
    for line in open('test.dat'):
        label, file = line[:-1].split(',')
        dat = open(file).read()        
        datum = Datum({"message": dat})
        ans = classifier.classify([datum])
        if ans != None:
            estm = get_most_likely(ans[0])
            if (label == estm[0]):
                result = "OK"
                count_ok += 1
            else:
                result = "NG"
                count_ng += 1
            print result + "," + label + ", " + estm[0] + ", " + str(estm[1])
    print "==================="
    print "OK: {0}".format(count_ok)
    print "NG: {0}".format(count_ng)
