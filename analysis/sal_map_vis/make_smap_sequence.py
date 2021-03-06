import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from PIL import Image

FILE_PATH = os.path.expanduser(sys.argv[1])
BAND_DIM = 3
NUM_BANDS = BAND_DIM ** 2
NUM_TIMES = 32

vis = np.load(FILE_PATH)

def assemble_all_vis(fmt_str, time):
    first_elt = vis[fmt_str % (0,0)]
    height, width = first_elt.shape
    total_height, total_width = BAND_DIM * height, BAND_DIM * width
    all_vis_n = np.zeros((total_height, total_width))
    for r in range(BAND_DIM):
        for c in range(BAND_DIM):
            all_vis_n[r*height:(r+1)*height,c*width:(c+1)*width] = vis[fmt_str % (time, r * BAND_DIM + c)]
    return all_vis_n

def gen_vis_sequence():
    f, axarr = plt.subplots(1, 2)
    loc1, loc2 = tuple(vis['loc'])
    dirname = 'smap_seq_%d_%d' % (loc1, loc2)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for t in range(NUM_TIMES):
        all_vis_soy_n = -1 * assemble_all_vis('vis_soy_t%d_b%d', t)
        all_vis_corn_n = -1 * assemble_all_vis('vis_corn_t%d_b%d', t)
        vmin = -0.05
        vmax = 0.05
        axarr[0].imshow(all_vis_soy_n, cmap='gray', vmin=vmin, vmax=vmax)
        axarr[0].axis('off')
        axarr[0].set_title('Soybeans (t=%d)' % t)
        axarr[1].imshow(all_vis_corn_n, cmap='gray', vmin=vmin, vmax=vmax)
        axarr[1].axis('off')
        axarr[1].set_title('Corn (t=%d)' % t)
        # plt.show()
        plt.savefig(os.path.join(dirname, 't%d.png' % t), bbox_inches='tight', pad_inches=0, dpi=300)

def graph_vis():
    f, axarr = plt.subplots(1, 2)
    loc1, loc2 = tuple(vis['loc'])
    all_vis_soy_n = assemble_all_vis('vis_soy_t%d_b%d')
    all_vis_corn_n = assemble_all_vis('vis_corn_t%d_b%d')
    all_vis_soy_n *= -1
    all_vis_corn_n *= -1
    # all_vis_soy_n += (all_vis_soy_n == 0)
    vmin = min(np.min(all_vis_soy_n), np.min(all_vis_corn_n))
    vmax = max(np.max(all_vis_soy_n), np.max(all_vis_corn_n))
    vmin = -0.05
    vmax = 0.05
    axarr[0].imshow(all_vis_soy_n, cmap='gray', vmin=vmin, vmax=vmax)
    axarr[0].set_xlabel('Bands')
    axarr[0].set_ylabel('Times')
    #axarr[0].set_title('Soy, 2013, loc=(%d, %d)' % (loc1, loc2))
    axarr[0].axis('off')
    axarr[1].imshow(all_vis_corn_n, cmap='gray', vmin=vmin, vmax=vmax)
    axarr[1].set_xlabel('Bands')
    axarr[1].set_ylabel('Times')
    #axarr[1].set_title('Corn, 2013, loc=(%d, %d)' % (loc1, loc2))
    axarr[1].axis('off')
    plt.show()
    #plt.savefig('smaps_%d_%d_t%d-%d_b%d-%d_soy_corn.png' % (loc1, loc2, START_TIME, END_TIME, START_BAND, END_BAND), bbox_inches='tight', pad_inches=0, dpi=300)
    
def graph_raw():
    loc1, loc2 = tuple(vis['loc'])
    all_vis = assemble_all_vis('raw_t%d_b%d')
    plt.imshow(all_vis, cmap='gray')
    #axarr[0].axis([START_BAND, END_BAND + 1, START_TIME, END_TIME + 1])
    plt.xlabel('Bands')
    plt.ylabel('Times')
    plt.title('Soy, 2013, loc=(%d, %d)' % (loc1, loc2))
    
    plt.show()

def sample_stats():
    raw_image = vis['raw_t31_b8']
    plt.hist(raw_image.ravel(), bins=256, fc='k', ec='k')
    plt.show()

gen_vis_sequence()
    # sample_stats()
#graph_raw()
