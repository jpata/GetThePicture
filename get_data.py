from PIL import Image, ImageChops, ImageEnhance
import sys, os.path
import glob
import pandas
import tempfile
import numpy as np
import random
import cv2

def get_ela(src):
    src_img = Image.open(src).convert('RGB')
    fn = tempfile.mkstemp("jpeg")[1]
    src_img.save(fn, 'JPEG', quality=95)
    resaved_im = Image.open(fn)

    ela_im = ImageChops.difference(src_img.convert('RGB'), resaved_im.convert('RGB'))
    resaved_im.close()
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 1.0
    if max_diff > 0:
        scale = 255.0/max_diff

    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
    src_img.close()
    return ela_im

def blockstats(src, s):
    img = Image.open(src).convert("RGB")
    blocks = []
    for x in range(0, img.size[1],s):
        for y in range(0, img.size[0],s):
            block = np.asarray(img)[x:x+s,y:y+s]
            if block.shape != (s, s, 3):
                continue
            blocks += [tuple(block.flatten())]
    #sb = blocks
    sb = sorted(blocks)
    
    vs = []
    for i in range(len(sb)-2):
        v = np.sqrt(np.sum(np.power(np.array(sb[i])-np.array(sb[i+1]), 2)))
        vs += [v]
    vs = np.array(vs)
    img.close()
    return np.percentile(vs, range(0,100,5))

bf = cv2.BFMatcher(cv2.NORM_L2)
def blockstats_surf(src, s):
    surf = cv2.SURF(1000)
    img = cv2.imread(src)
    blocks = []
    for x in range(0, img.shape[1],s):
        for y in range(0, img.shape[0],s):
            block = np.asarray(img)[x:x+s,y:y+s]
            if block.shape != (s, s, 3):
                continue
            kp, des = surf.detectAndCompute(block,None)
            if len(kp)>0:
                blocks += [des]
    blockdistances = []
    for ibl1, bl1 in enumerate(blocks):
        for ibl2, bl2 in enumerate(blocks):
            if ibl1 != ibl2:
                    matches = bf.match(bl1, bl2)
                    matches = sorted(matches, key = lambda x:x.distance)
                    dists = [m.distance for m in matches]
                    blockdistances += [(dists, ibl1, ibl2)]
    bls = sorted([bl[0][0] for bl in blockdistances])
    hbls = np.histogram(bls, normed=True, bins=np.linspace(0,5,11))
    return hbls[0]

def get_image_data(fname):
    print fname
    data = dict()
    diff = get_ela(fname)
    ela_hist = np.array(diff.convert('LA').histogram()).reshape(512/16, 16).sum(1)
    diff.close()
    ela_hist = ela_hist / float(sum(ela_hist))
    df_row = pandas.DataFrame()
    df_row["fn"] = [fname]
    cum_ela_hist = np.cumsum(ela_hist)
    for inh in range(0, len(ela_hist), 10):
        df_row["cela_hist_%d"%inh] = cum_ela_hist[inh]
    
    bstats = blockstats_surf(fname, 64)
    for i in range(len(bstats)):
        df_row["bstat_64_%d"%i] = bstats[i]
    
    # bstats = blockstats(fname,8)
    # for i in range(len(bstats)):
    #     df_row["bstat_8_%d"%i] = bstats[i]
    # 
    # bstats = blockstats(fname,32)
    # for i in range(len(bstats)):
    #     df_row["bstat_32_%d"%i] = bstats[i]

    df_row["type"] = 0
    if "jpg" in fname or "jpeg" in fname:
        df_row["type"] = 1
    elif "png" in fname:
        df_row["type"] = 2
    df_row["rnd"] = random.random()<0.25
    return df_row

def read_exif(fn):
    fi = open(fn, "rb")
    tags = exifread.process_file(fi)
    fi.close()
    return tags

if __name__ == "__main__":
    data_bkg = glob.glob("/Users/joosep/Dropbox/diplohack_team2/photos/training/true/*")
    data_sig = glob.glob("/Users/joosep/Dropbox/diplohack_team2/photos/training/fake/*")

    import multiprocessing
    pool = multiprocessing.Pool(processes=4)

    print "mapping"
    d1 = map(get_image_data, data_bkg)
    d2 = map(get_image_data, data_sig)

    print "concatting"
    bkg = pandas.concat(d1)
    sig = pandas.concat(d2)

    bkg["id"] = 0
    sig["id"] = 1

    print "concatting sig and bkg"
    data = pandas.concat([sig, bkg])

    print "saving"
    data.to_csv("training.csv")
