import math
from PIL import Image


im = Image.open("/Users/McInnis/Dropbox/Work in UK/Assignment/Fisheye_photo-600x600.jpg")
im.show()

width, high = im.size
sqrt_len = min(width, high)
im = im.transform((sqrt_len, sqrt_len),
                    Image.EXTENT,
                    ((width-sqrt_len)/2, (high-sqrt_len)/2, 
                    sqrt_len+(width-sqrt_len)/2, sqrt_len+(high-sqrt_len)/2)
                    )
width = high = sqrt_len

idata = im.getdata()
odata = []

alpha = math.pi/2

out_high = round(high * math.tan(alpha/2))
out_width = round(width * math.tan(alpha/2))
out_radius = round(high * math.tan(alpha/2))
out_center_x = out_width / 2
out_center_y = out_high / 2

out_bl_x = 0
out_br_x = out_width - 1
out_bt_y = 0
out_bb_y = out_high - 1

out_bl_cx = out_bl_x - out_center_x
out_br_cx = out_br_x - out_center_x
out_bt_cy = out_bt_y - out_center_y
out_bb_cy = out_bb_y - out_center_y

src_radius = round(high * math.sin(alpha/2))
src_center_x = width / 2
src_center_y = high / 2

for i in range(0, high * width):
    ox = math.floor(i / out_width)
    oy = i % out_high
    
    cx = ox - out_center_x;
    cy = oy - out_center_y;
    
    out_distance = round(math.sqrt(pow(cx, 2) + pow(cy, 2)))
    theta = math.atan2(cy, cx)
    if (-math.pi/4 <= theta <= math.pi/4):
        bx = out_radius * math.cos(math.pi/4)
        by = bx * math.tan(theta)
    elif (math.pi/4 <= theta <= math.pi*3/4):
        by = out_radius * math.sin(math.pi/4)
        bx = by / math.tan(theta)
    elif (-math.pi*3/4 <= theta <= -math.pi/4):
        by = out_radius * math.sin(-math.pi/4)
        bx = by / math.tan(theta)
    else:
        bx = out_radius * math.cos(-math.pi*3/4)
        by = bx * math.tan(theta)
        
    
    bdy_distance = round(math.sqrt(pow(cx, 2) + pow(cy, 2)))
    src_distance = src_radius * bdy_distance / out_radius
        
    
    src_x = round(src_center_x + math.cos(theta) * src_distance)
    src_y = round(src_center_y + math.sin(theta) * src_distance)
    
    src_idx = src_x*width + src_y    
    if(0 < src_idx < high*width):
        odata.append(idata[src_idx])
    else:
        odata.append((0,0,0))
    


om = Image.new("RGB", (high, width))
om.putdata(odata)
om.show()

