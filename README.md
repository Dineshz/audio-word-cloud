# audio-word-cloud
Convert audio files to word cloud

# DIR structure
```

  |-- deepspeech
      |-- alphabet.txt
      |-- lm.binary
      |-- output_graph.pb
      |-- trie
  |-- data.json
  |-- poller.py
  |-- revertRename.py
  |-- requirements.txt

```

# Installation

Install the following on ubuntu
- ffmpeg

For python dependencies
```
  pip install -r requirements.txt
```

## Download Deepspeech Models from
https://github.com/mozilla/DeepSpeech/releases

## Audio file conversion
```
  ffmpeg -i source.wav -acodec pcm_s16le -ar 16000 -ac 1 dest.wav
```

## Reference
http://www.phpied.com/taking-mozillas-deepspeech-for-a-spin/
