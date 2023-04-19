from PIL import Image
import random

def check_overlap(position, pasted_images, random_image):
    x_pos, y_pos = position
    for pasted_image in pasted_images:
        if (x_pos + random_image.width > pasted_image[0] and x_pos < pasted_image[0] + pasted_image[2].width) and (y_pos + random_image.height > pasted_image[1] and y_pos < pasted_image[1] + pasted_image[2].height):
            return True
    return False

def create_random_image(width, height, num_images, image_list):
    new_image = Image.new("RGB", (width, height), "white")
    pasted_images = []

    for i in range(num_images):
        random_image = Image.open(random.choice(image_list))
        new_width, new_height = random.randint(25,int(width/3)), random.randint(25,int(height/3))
        random_image = random_image.resize((new_width, new_height))

        if random_image.width >= width or random_image.height >= height:
            continue

        random_rotation = random.randint(0, 359)
        random_image = random_image.rotate(random_rotation, expand=True, fillcolor="white")

        overlap = True
        max_attempts = 50
        attempts = 0

        while overlap and attempts < max_attempts:
            x_pos = random.randint(0, width - random_image.width)
            y_pos = random.randint(0, height - random_image.height)

            if not check_overlap((x_pos, y_pos), pasted_images, random_image):
                overlap = False
            attempts += 1

        if not overlap:
            new_image.paste(random_image, (x_pos, y_pos))
            pasted_images.append((x_pos, y_pos, random_image))

    return new_image, pasted_images

def save_coordinates_to_txt(pasted_images, filename):
    with open(filename, 'w') as f:
        for index, image_info in enumerate(pasted_images, start=1):
            x, y, img = image_info
            f.write(f"Image {index}: x={x}, y={y}, width={img.width}, height={img.height}\n")

counter = 0
while counter<20:
    new_image, pasted_images = create_random_image(1000, 1000, 77, ["1.jpg","2.jpg","3.jpg","4.jpg"])
    new_image.save("output"+str(counter)+".jpg")
    save_coordinates_to_txt(pasted_images, "coordinates"+str(counter)+".txt")
    counter +=1
