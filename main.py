# ElasticSearch has to be installed and running for this to work
# https://www.elastic.co/guide/en/elasticsearch/reference/current/windows.html
# pip install git+https://github.com/EdjoLabs/image-match
# scikit-image needed installation

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from image_match.goldberg import ImageSignature
import time

# Basic 1to1 image comparison
gis = ImageSignature()

char_1 = gis.generate_signature('https://thumbor.forbes.com/thumbor/249x350/https://specials-images.forbesimg.com/imageserve/602002b2d1dbfa6dce1da418/Charizard/960x0.jpg?fit=scale')
char_2 = gis.generate_signature('https://commondatastorage.googleapis.com/images.pricecharting.com/0aafce2658aa1583d864d9ee71c1e9eb607560745be990a8fb4796c3d56ca0d6/240.jpg')
frog = gis.generate_signature('https://static.wikia.nocookie.net/runescape2/images/5/56/Frog_%28NPC%29.png/revision/latest?cb=20160531202106')

nd = gis.normalized_distance(char_1, char_2)
nd2 = gis.normalized_distance(char_1, frog)

print(f'\nNormalized distances of less than 0.40 are very likely matches\n'
      f'char_1 vs char_2: {nd}\n'
      f'char_1 vs frog: {nd2}\n')

# Signature Elastic Search comparison

es = Elasticsearch([{'host': 'localhost'}])
ses = SignatureES(es, distance_cutoff=.45)

# adds all files from directory to the ses object
# for file in os.listdir('Test_Images'):
#     ses.add_image(f'Test_Images\\{file}')

start = time.time()
s = ses.search_image('Test_Images\\1067923.jpg')
end = time.time()
print(f'Total search time: {end - start}\n')
for i in s:
    if i['dist'] == 0.0:
        path = i['path']
        print(f'Identical Image Found at {path}')
    print(f'{i}')
