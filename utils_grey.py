import PIL
from PIL import Image,ImageEnhance
import numpy as np 
from config import grey_config as config
import random
import os 

# 改变图像大小
def resize_image(input_image_path, output_image_path, new_width, new_height):

    image = Image.open(input_image_path)
    
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    
    resized_image.save(output_image_path)

def resize_image_ratio(inputfile=None,outputfile=None):
    if inputfile == None:
        image = Image.open(config.input_dir+config.input_id)
    else:
        image = Image.open(inputfile)

    
    w,h = image.size

    resized_image = image.resize((int(w*config.ratio),int(h*config.ratio)), Image.ANTIALIAS)
    if outputfile == None:
        resized_image.save(config.input_output+config.input_output_id)
    else:
        resized_image.save(outputfile)

def convert_grey():

    image = Image.open(config.input_output+config.input_output_id)

    bw_image = image.convert("L")

    bw_image.save(config.grey_output+config.grey_output_id)

def process_inner_pic():
    files = os.listdir(config.pre_dir)
    for file in files:
        image = Image.open(config.pre_dir+file)
        w,h = config.inner_pic_w,config.inner_pic_h
        resized_image = image.resize((w, h), Image.ANTIALIAS)

        bw_image = resized_image.convert("L")

        bw_image.save(config.inner_dir+file)


# 拼接灰色图像
def concatenate_grey_images():

    image = Image.open(config.grey_output+config.grey_output_id)
    image_np = np.array(image).T

    files = os.listdir(config.inner_dir)
    total = len(files)
    w,h = image.size

    total_width = w*config.inner_pic_w
    total_height = h*config.inner_pic_h

    new_image = Image.new('L', (total_width, total_height))

    x_offset = 0
    y_offset = 0
    for x in range(w):
        for y in range(h):
            #print(f"{x},{y}")
            part = Image.open(config.inner_dir+files[random.randint(0,total-1)])
            part_np = np.array(part)
            des = image_np[x][y]
            x_offset = config.inner_pic_w*x 
            y_offset = config.inner_pic_h*y
            now = np.mean(part_np)

            enhancer = ImageEnhance.Brightness(part)

            brightened_image = enhancer.enhance(des/now)

            new_image.paste(brightened_image, (x_offset, y_offset))

    new_image.save(config.output_dir+config.output_id)
    return new_image


def grey_main():
    print("预处理被用作拼的图像")
    process_inner_pic()

    print("处理需要拼出来的图像")
    resize_image_ratio()
    convert_grey()
    
    print("开始拼图")
    concatenate_grey_images()

if __name__ == '__main__':
    grey_main()