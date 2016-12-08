import argparse
import numpy as np
import time
import sys

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
    x = 0
    print "LenW: " + str(W.shape)
    print "LenD: " + str(d.shape)
    W_norm = (W.T / d).T
    return (W_norm, vocab, ivocab)


def distance(W, vocab, ivocab, input_term, universe, out_file):
    for idx, term in enumerate(input_term.split(' ')):
        if term in vocab:
            print('Word: %s  Position in vocabulary: %i' % (term, vocab[term]))
            if idx == 0:
                vec_result = W[vocab[term], :] 
            else:
                vec_result += W[vocab[term], :] 
        else:
            print('Word: %s  Out of dictionary!\n' % term)
            return
    
    vec_norm = np.zeros(vec_result.shape)
    d = (np.sum(vec_result ** 2,) ** (0.5))
    vec_norm = (vec_result.T / d).T

    dist = np.dot(W, vec_norm.T)

    for term in input_term.split(' '):
        index = vocab[term]
        dist[index] = -np.Inf

    a = np.argsort(-dist)#[:N]

    x = a[0]
    out_file.write(str(input_term) + " " + str(ivocab[x]) + " " + str(dist[x]) + "\n")


if __name__ == "__main__":
    N = 10;          # number of closest words that will be shown
    W, vocab, ivocab = generate()
    universe = []
    universe_file = open('grassroot-universe-terms.csv', 'r')
    out_file = open('universe_distances.csv', 'w')
    for line in universe_file:
        universe.append(line.strip())
    for word in universe:
        distance(W, vocab, ivocab, word, universe, out_file)

