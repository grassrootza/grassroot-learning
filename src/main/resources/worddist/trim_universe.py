from __future__ import print_function

import argparse
import numpy as np
import sys
import csv

def readGrassrootUniverseFile():
    universe = []
    parser = argparse.ArgumentParser()
    parser.add_argument('--universe_delim', default=' ', type=str)
    args = parser.parse_args()
    with open('universe_distances.csv', 'r') as file:
        reader = csv.reader(file, delimiter = args.universe_delim)
        for row in reader:
            if row[1].isalpha():
                universe.append(row[1])
    return universe

def generate():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab_file', default='vocab.txt', type=str)
    parser.add_argument('--vectors_file', default='vectors.txt', type=str)
    args = parser.parse_args()

    with open(args.vocab_file, 'r') as f:
        words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    with open(args.vectors_file, 'r') as f:
        vectors = {}
        for line in f:
            vals = line.rstrip().split(' ')
            vectors[vals[0]] = [float(x) for x in vals[1:]]

    vocab_size = len(words)
    vocab = {w: idx for idx, w in enumerate(words)}
    ivocab = {idx: w for idx, w in enumerate(words)}

    vector_dim = len(vectors[ivocab[0]])
    W = np.zeros((vocab_size, vector_dim))
    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word], :] = v

    # normalize each word vector to unit variance
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    return (W_norm, vocab, ivocab)


def distance(W, vocab, ivocab, input_term, max_terms = 100):
    for idx, term in enumerate(input_term.split(' ')):
        if term in vocab:
            if idx == 0:
                vec_result = np.copy(W[vocab[term], :])
            else:
                vec_result += W[vocab[term], :] 
        else:
            return
    
    vec_norm = np.zeros(vec_result.shape)
    d = (np.sum(vec_result ** 2,) ** (0.5))
    vec_norm = (vec_result.T / d).T

    dist = np.dot(W, vec_norm.T)

    for term in input_term.split(' '):
        index = vocab[term]
        dist[index] = -np.Inf

    a = np.argsort(-dist)
    count = 0
    for x in a:
        if dist[x] >= DISTANCE_THRESHOLD and not (ivocab[x] in newUniverse): 
                newUniverse.append(ivocab[x])
                count += 1
                if count == max_terms:
                    break 
    # print count # uncomment to show distribution of results

if __name__ == "__main__":
    DISTANCE_THRESHOLD = 0.1
    print("Reading in universe file ...")
    universe = readGrassrootUniverseFile()
    print("Universe size: " + str(len(universe)))
    W, vocab, ivocab = generate()
    v = open('new_vectors.txt', 'w')
    with open('new_vocab.txt', 'w') as f:
        newUniverse = []
        for word in universe:
            distance(W, vocab, ivocab, word)


        parser = argparse.ArgumentParser()
        parser.add_argument('--vocab_file', default='vocab.txt', type=str)
        parser.add_argument('--vectors_file', default='vectors.txt', type=str)
        args = parser.parse_args()
        with open(args.vectors_file, 'r') as g:
            for line in g:
                vals = line.rstrip().split(' ')
                if vals[0] in newUniverse:
                    f.write(vals[0] + '\n')
                    v.write(line)
        print(len(newUniverse))

