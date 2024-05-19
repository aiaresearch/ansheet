import json
import numpy as np

def write_json(dst,b,c,number_top,xx,top,ww):
    dst=dst.tolist()
    dst.pop(3)
    config_dict ={
        'b':b,
        'c':c,
        'number_top': number_top,
        'column_location': xx,
        'dst': dst,
        'top':top,
        'w':ww[-1]
    }
    with open('config.json','w') as f:
        json.dump(config_dict,f)


def read_json():
    with open('config.json','r') as f:
        config= json.load(f)
    f.close()
    b=config['b']
    c=config['c']
    number_top=config['number_top']
    column_location=config['column_location']
    dstlist=config['dst']
    dst=np.array(dstlist, dtype=np.float32)
    top=config['top']
    W=config['w']
    return b,c,number_top,column_location,dstlist,dst,top,W