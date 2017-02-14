"""

Convert JSON ROI data to image crops

"""
import sys
import uuid
import os
import json
from PIL import Image

rootdir = 'static/uncropped/'
js = [x for x in os.listdir(rootdir) if x.endswith('.json')]
for j in js:
    jsonpath = rootdir + j
    srcpath = jsonpath.replace('.json', '')
    with open(jsonpath) as f:
        d = json.load(f)
    rois = d['roi']
    width = d['width']
    height = d['height']
    for roi in rois:
        feat = roi['feat']
        x1 = roi['x1']
        y1 = roi['y1']
        x2 = roi['x2']
        y2 = roi['y2']
        dstpath = 'cropped_images/{}/{}.jpg'.format(feat, uuid.uuid4())
        with Image.open(srcpath) as img:
            real_width, real_height = img.size
            left = int(x1 * real_width / width)
            upper = int(y1 * real_height / height)
            right = int(x2 * real_width / width)
            lower = int(y2 * real_height / height)

            if left > right:
                left_ = left
                left = right
                right = left_

            if upper > lower:
                upper_ = upper
                upper = lower
                lower = upper_

            if left == right:
                continue

            if lower == upper:
                continue

            assert left < right
            assert upper < lower
            assert right < real_width
            assert lower < real_height

            img = img.crop((left, upper, right, lower))
            os.makedirs(os.path.dirname(dstpath), exist_ok=True)
            print(srcpath, dstpath)
            img.save(dstpath)
