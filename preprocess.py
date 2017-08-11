#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This is for preprocess AST from Java Corpus """
from __future__ import print_function
import sys
import traceback
import javalang

reload(sys)
sys.setdefaultencoding('utf-8')
print(javalang.__path__)

def print_ast(ast):
    """ Print the ast in order to debug"""
    stack = [ast]
    while stack:
        node = stack.pop()
        #print(node)
        if isinstance(node, list):
            for i in node:
                stack.append(i)
        elif hasattr(node, 'children'):
            for child in node.children:
                stack.append(child)
        else:
            print(node)

def check_file(line):
    """ Give a check on file, whether it can be parsed or not """
    try:
        javalang.parse.parse(line)
        return {'Status':True, 'Msg':None}
    except javalang.parser.JavaSyntaxError as error:
        trace_back = traceback.format_exc()
        print(trace_back)
        return {'Status':False, 'Msg':error.message}

def preprocess(path):
    """ Preprocess all lines in one file"""
    with open(path, 'r') as test_file:
        lines = test_file.readlines()

    for i, line in enumerate(lines):
        if i < 5960:
            continue
        result = check_file(line)
        if not result['Status']:
            print('Line %d failed with ERROR: %s'%(i, result['Msg']))
            return False
        else:
            print('Line %d parsing good'%i)

if __name__ == "__main__":
    preprocess('./data/java_1M_train')
