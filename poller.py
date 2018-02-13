from __future__ import absolute_import, division, print_function
from os import path, listdir, rename
import time
from timeit import default_timer as timer
import argparse
import sys
import scipy.io.wavfile as wav
import json
from deepspeech.model import Model

AUDIO_DIR = './'
POLL_TIME = 2.0
EXTENSION = '.wav'
MODEL_DIR = './deepspeech/models/'

# DEEPSPEECH CONSTANTS
BEAM_WIDTH = 500
LM_WEIGHT = 1.75
WORD_COUNT_WEIGHT = 1.00
VALID_WORD_COUNT_WEIGHT = 1.00
N_FEATURES = 26
N_CONTEXT = 9

# ARGUMENTS FOR DEEPSPEECH
MODEL_FILE = MODEL_DIR + 'output_graph.pb'
ALPHABET_FILE = MODEL_DIR + 'alphabet.txt'
LM_BINARY_FILE = MODEL_DIR + 'lm.binary'
TRIE_FILE = MODEL_DIR + 'trie'

ds = None

# deepspeech output_graph.pb joey16bit.wav alphabet.txt lm.binary trie

def initialize():
  loadModel()

def loadModel():
  global ds
  print('Loading model from file %s' % (MODEL_FILE), file=sys.stderr)
  model_load_start = timer()
  ds = Model(MODEL_FILE, N_FEATURES, N_CONTEXT, ALPHABET_FILE, BEAM_WIDTH)
  model_load_end = timer() - model_load_start
  print('Loaded model in %0.3fs.' % (model_load_end), file=sys.stderr)
  print('Loading language model from files %s %s' % (LM_BINARY_FILE, TRIE_FILE), file=sys.stderr)
  lm_load_start = timer()
  ds.enableDecoderWithLM(ALPHABET_FILE, LM_BINARY_FILE, TRIE_FILE, LM_WEIGHT,
                               WORD_COUNT_WEIGHT, VALID_WORD_COUNT_WEIGHT)
  lm_load_end = timer() - lm_load_start
  print('Loaded language model in %0.3fs.' % (lm_load_end), file=sys.stderr)

def audioToText(fileName):
  print('Running inference for %s.' % (fileName), file=sys.stderr)
  inference_start = timer()
  fs, audio = wav.read(fileName)
  audio_length = len(audio) * ( 1 / 16000)
  if(fs != 16000):
    print('Can process only 16000Hz input wav files')
    print('Skipping', fileName)
    return []
  else:
    words = ds.stt(audio, fs)
  inference_end = timer() - inference_start
  print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
  return words.split(' ')

def count(words):
  with open('data.json') as data_file:
    data = json.load(data_file)
  for word in words:
    if word in data:
        data[word] += 1
    else:
        data[word] = 1
  with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

def findAndProcessAudio():
  print('Looking for %s files' % (EXTENSION))
  fileList = listdir(AUDIO_DIR)
  fileList = [ fileName for fileName in fileList if path.splitext(fileName)[1] == EXTENSION]
  for fileName in fileList:
    words = audioToText(fileName)
    print("Words Inferred")
    print(words)
    count(words)
    rename(fileName, fileName+'.processed')

initialize()

while True:
  try:
    findAndProcessAudio()
    time.sleep(POLL_TIME)
  except KeyboardInterrupt:
    exit()
