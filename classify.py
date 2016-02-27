import sklearn, pickle, os
import get_data
import numpy as np

f = open("/Users/joosep/Dropbox/diplohack_team2/bdt2.pkl", "r")
s = f.read()
clf = pickle.loads(s)
vs = ['cela_hist_0',
 'cela_hist_10',
 'cela_hist_20',
 'cela_hist_30',
 'cela_hist_40',
 'cela_hist_50',
 'cela_hist_60',
 'bstat_64_0',
 'bstat_64_1',
 'bstat_64_2',
 'bstat_64_3',
 'bstat_64_4',
 'bstat_64_5',
 'bstat_64_6',
 'bstat_64_7',
 'bstat_64_8',
 'bstat_64_9']

from PIL import Image
import uuid

def make_thumb(fn):
    if not os.path.exists("thumb"):
        os.mkdir("thumb")
    image = Image.open(fn)
    image.thumbnail((128,128), Image.NEAREST)
    thpath = "thumb/{0}.jpg".format(uuid.uuid4())
    image.save(thpath)
    image.close()
    return thpath


def score(img):
    if not os.path.isfile(img):
        print "not an image"
        return -1
    dt = get_data.get_image_data(img)[vs]
    for v in vs:
        dt.loc[np.isnan(dt[v]), v] = 0
        dt.loc[np.isinf(dt[v]), v] = 0
    sc = clf.predict_proba(dt)[0,0]
    return sc

import multiprocessing
pool = multiprocessing.Pool(4)

def score_folder(path):
    good_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if "png" in file or "jpg" in file or "jpeg" in file:
                good_files += [root + "/" + file]
    responses = []
    thumbs = pool.map(make_thumb, good_files)
    scores = pool.map(score, good_files)
    for fi, thumb, sc in zip(good_files, thumbs, scores):
        print "scoring", fi
        response = {}
        response["filename"] = fi
        response["grade"] = sc
        response["thumbnail"] = thumb
        response["filename"] = fi
        responses += [response]
        print response
    responses = sorted(responses, key=lambda x: x["grade"], reverse=True)
    return responses
            
