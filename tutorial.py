#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

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

    # Create a client instance.
    classifier = Classifier(options.server_ip,options.server_port, options.name, 10)

    # Show configuration.
    print("--- Configuration ----------")
    print(classifier.get_config())
    print()

    # Show the status of classifier before training.
    print("--- Status ----------")
    print(classifier.get_status())
    print()

    # Start processing the training dataset.
    print("--- Training ----------")
    for line in open('train.dat'):
        label, file = line[:-1].split(',')
        dat = open(file, 'rb').read()
        datum = Datum({"message": dat.decode('latin1')})
        classifier.train([LabeledDatum(label, datum)])
    print()

    # Show the status of classifier after training.
    print("--- Status ----------")
    print(classifier.get_status())
    print()

    # Save the trained model to local file (under /tmp by default).
    print("--- Save Model ----------")
    print(classifier.save("tutorial"))
    print()

    # You can load the saved model file to memory using `load` RPC.
    #print(classifier.load("tutorial"))

    # Now confirm the precision of the trained classifier using test dataset.
    print("--- Test ----------")
    count_ok = 0
    count_ng = 0
    for line in open('test.dat'):
        label, file = line[:-1].split(',')
        dat = open(file, 'rb').read()
        datum = Datum({"message": dat.decode('latin1')})
        ans = classifier.classify([datum])
        if ans != None:
            estm = get_most_likely(ans[0])
            if (label == estm[0]):
                result = "OK"
                count_ok += 1
            else:
                result = "NG"
                count_ng += 1
            print(result + "," + label + ", " + estm[0] + ", " + str(estm[1]))
    print("===================")
    print("OK: {0}".format(count_ok))
    print("NG: {0}".format(count_ng))
