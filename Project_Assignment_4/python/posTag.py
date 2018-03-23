import os
import subprocess
dirs_neg = os.listdir("/home/ubuntu/workspace/turney/data/imdb1/neg/")
dirs_pos = os.listdir("/home/ubuntu/workspace/turney/data/imdb1/pos/")

for filename in dirs_neg:
	os.system("./tagchunk.i686 -predict . w-5 /home/ubuntu/workspace/turney/data/imdb1/neg/"+filename+" /home/ubuntu/workspace/pos-tagger/resources > /home/ubuntu/workspace/turney/neg_tagged/" + filename)
	

for filename in dirs_pos:
	os.system("./tagchunk.i686 -predict . w-5 /home/ubuntu/workspace/turney/data/imdb1/pos/"+filename+" /home/ubuntu/workspace/pos-tagger/resources > /home/ubuntu/workspace/turney/pos_tagged/" + filename)