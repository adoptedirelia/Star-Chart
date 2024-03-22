import PIL
from PIL import Image,ImageEnhance
import numpy as np 
from config import config
import os
import random
import tqdm

# 改变图像大小
def resize_image(input_image_path, output_image_path, new_width, new_height):

    image = Image.open(input_image_path)
    
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    
    resized_image.save(output_image_path)

def resize_image_ratio():

    image = Image.open(config.input_dir+config.input_id)
    
    w,h = image.size

    resized_image = image.resize((int(w*config.ratio),int(h*config.ratio)), Image.ANTIALIAS)
    
    resized_image.save(config.input_output+config.input_output_id)

def process_inner_pic():
    files = os.listdir(config.pre_dir)
    for file in files:
        image = Image.open(config.pre_dir+file)
        w,h = config.inner_pic_w,config.inner_pic_h
        resized_image = image.resize((w, h), Image.ANTIALIAS)

        resized_image.save(config.inner_dir+file)



# 拼接彩色图像
def concatenate_images():

    image = Image.open(config.input_output+config.input_output_id)
    image_np = np.array(image).T

    files = os.listdir(config.inner_dir)
    total = len(files)
    w,h = image.size

    total_width = w*config.inner_pic_w
    total_height = h*config.inner_pic_h

    new_image = Image.new('RGB', (total_width, total_height))

    x_offset = 0
    y_offset = 0
    for x in tqdm.trange(w):
        for y in range(h):
            #print(f"{x},{y}")
            part = Image.open(config.inner_dir+files[random.randint(0,total-1)])
            part_np = np.array(part).T
            lst = []
            for i in range(3):
                
                des = image_np[i][x][y]
                x_offset = config.inner_pic_w*x 
                y_offset = config.inner_pic_h*y
                now = np.mean(part_np[i])
                temp = Image.fromarray(part_np[i])
                enhancer = ImageEnhance.Brightness(temp)

                brightened_image = enhancer.enhance(des/now)
                lst.append(np.array(brightened_image).T)


            final = Image.fromarray(np.stack(lst,axis=2))

            new_image.paste(final, (x_offset, y_offset))

    new_image.save(config.output_dir+config.output_id)
    return new_image


def main():
    process_inner_pic()
    resize_image_ratio()
    concatenate_images()

if __name__ == '__main__':
    main()