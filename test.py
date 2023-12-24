import cv2
import os
import numpy as np


def readDirectoryImages(directory):
    directoryImages = list()
    if os.path.isdir(directory):
        images = os.listdir(directory)
        for image in images:
            if extensionCheck(image):
                imagePath = f'{directory}/{image}'
                images.append(imagePath)
    return directoryImages


def extensionCheck(imagePath):
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    for ext in extensions:
        if imagePath.lower().endswith(ext):
            return True

    return False


def normalize_image(sourceImagePath, outputImagePath):
    image = cv2.imread(sourceImagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    heightMin = 256
    heightMax = -1
    widthMin = 256
    widthMax = -1

    for i in range(len(gray)):
        if 0 in gray[i]:
            if i < heightMin:
                heightMin = i
            if i > heightMax:
                heightMax = i
        for j in range(len(gray[i])):
            if gray[i][j] < 50:
                if j < widthMin:
                    widthMin = j

                if j > widthMax:
                    widthMax = j

    cropped_image = gray[heightMin:heightMax, widthMin:widthMax]
    scale_percent = 4
    height = int(cropped_image.shape[0] * scale_percent / 100)
    width = int(cropped_image.shape[1] * scale_percent / 100)
    dimension = (width, height)
    resized = cv2.resize(cropped_image, dimension, interpolation=cv2.INTER_AREA)

    new_image_frame = np.ones((28, 28), dtype=np.uint8) * 255

    x_offset = (28 - resized.shape[1]) // 2
    y_offset = (28 - resized.shape[0]) // 2

    new_image_frame[y_offset:y_offset + resized.shape[0], x_offset:x_offset + resized.shape[1]] = resized

    for i in range(len(new_image_frame)):
        for j in range(len(new_image_frame[i])):
            if new_image_frame[i][j] < 244:
                new_image_frame[i][j] = 255
            else:
                new_image_frame[i][j] = 0

    cv2.imwrite(outputImagePath, new_image_frame)
    


def createNormalizedImagesDirectory(sourceDirectory, outputDirectory):
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

    images_list = readDirectoryImages(sourceDirectory)
    for index, image in enumerate(images_list, start=1):
        outputImagePath = os.path.join(outputDirectory, f'{index}.jpg')
        normalize_image(image, outputImagePath)


createNormalizedImagesDirectory('./','nomalized images')
#normalize_image("alpha\WhatsApp Image 2023-12-20 at 15.10.30_530678e5.jpg", "normalized images/28.jpg")