import argparse
import os
from PIL import Image

import threading

num_worker = 10

def resize_image(image, size):
    """Resize an image to the given size."""
    return image.resize(size, Image.ANTIALIAS)

def worker(b, images, image_dir, output_dir, size):
    num_images = len(images)
    bs = (num_images + num_worker) // num_worker
    ims = images[bs*b:bs*b+bs]
    num_images = len(ims)
    print ('Worker:', b, num_images)
    
    for i, image in enumerate(ims):
        image_path = os.path.join(image_dir, image)
        with open(image_path, 'r+b') as f:
            try:
                with Image.open(f) as img:
                    img = resize_image(img, size)
                    img.save(os.path.join(output_dir, image), img.format)
            except Exception:
                print("image open error : " + str(image_path))
    
        if i % 100 == 0:
            print ("[%d/%d] Resized the images and saved into '%s'."
                   %(i, num_images, output_dir))
    
    return

def resize_images(image_dir, output_dir, size):
    print (image_dir, output_dir, size)
    """Resize the images in 'image_dir' and save into 'output_dir'."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images = os.listdir(image_dir)
    num_images = len(images)
    
    batch_size = num_images // num_worker
    
    for b in range(num_worker):
        t = threading.Thread(target=worker, args=(b,images, image_dir, output_dir, size,))
        t.start()

def main(args):
    image_dir = args.image_dir
    output_dir = args.output_dir
    image_size = [args.image_size, args.image_size]
    resize_images(image_dir, output_dir, image_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default='./data/images/train/',
                        help='directory for train images')
    parser.add_argument('--output_dir', type=str, default='./data/resized/images/train/',
                        help='directory for saving resized images')
    parser.add_argument('--image_size', type=int, default=256,
                        help='size for image after processing')
    args = parser.parse_args()
    main(args)

