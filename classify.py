import sklearn, pickle, os
import get_data

f = open("/Users/joosep/Dropbox/diplohack_team2/bdt2.pkl", "r")
s = f.read()
clf = pickle.loads(s)
vs = ['cela_hist_0', 'cela_hist_10', 'cela_hist_20', 'cela_hist_30']
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

def score_folder(path):
    good_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if "png" in file or "jpg" in file or "jpeg" in file:
                good_files += [root + "/" + file]
    responses = []
    for fi in good_files:
        print "scoring", fi
        thumb = make_thumb(fi)
        response = {}
        sc = score(fi)
        response["filename"] = fi
        response["grade"] = sc
        response["thumbnail"] = thumb
        response["filename"] = fi
        responses += [response]
        print response
    responses = sorted(responses, key=lambda x: x["grade"], reverse=True)
    return responses
            
def score(img):
    if not os.path.isfile(img):
        print "not an image"
        return -1
    sc = clf.predict_proba(
        get_data.get_image_data(img)[vs]
    )[0,1]
    return sc
