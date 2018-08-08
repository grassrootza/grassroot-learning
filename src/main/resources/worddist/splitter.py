import argparse
import sys

#parser = argparse.ArgumentParser()
#parser.add_argument('--vectors_file', default='twitter.txt', type=str)
#args = parser.parse_args()
vectors_file = sys.argv[1]

with open(vectors_file, 'r') as f:
	words = [(x.rstrip().split(' ')[0], x) for x in f.readlines()]
	vocab_file = open("vocab.txt", "w")
	vector_out = open("vectors.txt", "w")
	for word in words:
		vocab_file.write(word[0] + "\n")
		vector_out.write(word[1])
