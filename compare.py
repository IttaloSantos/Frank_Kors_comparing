#!/usr/bin/env python
# -*- coding: utf-8 -*-

from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import xlsxwriter
import math as math

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar" # the two images are

    return err

def compare_images(imageA, imageB, title, worksheet):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)

    # Cálculo do PSNR
    if(m > 0):
        psnr = 10*math.log10(255*255/m);
    else:
        psnr = 99;

    worksheet.write(k[0], 0, psnr)
    worksheet.write(k[0], 1, s)

    k[0] += 1


    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("PSNR: %.2f, SSIM: %.2f" % (psnr, s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis("off")

    # show the images
    plt.show()

arq = open('patients.txt', 'r')
texto = arq.readlines()

# Abre o arquivo
workbook = xlsxwriter.Workbook("Grupo_III_.xlsx")
# Abre planilha
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'PSNR') # Peak Signal to Noise Ratio
worksheet.write('B1', 'SSIM') # Structural Similarity Measure

k = [1]*1

for paciente in texto:

    paciente = paciente[:len(paciente)-1]

    xy_frank = cv2.imread(paciente+"_Frank_xy.png")
    xz_frank = cv2.imread(paciente+"_Frank_xz.png")
    yz_frank = cv2.imread(paciente+"_Frank_yz.png")
    xy_kors = cv2.imread(paciente+"_xy.png")
    xz_kors = cv2.imread(paciente+"_xz.png")
    yz_kors = cv2.imread(paciente+"_yz.png")

    # Converter para escala de cinza
    xy_frank = cv2.cvtColor(xy_frank, cv2.COLOR_BGR2GRAY)
    xz_frank = cv2.cvtColor(xz_frank, cv2.COLOR_BGR2GRAY)
    yz_frank = cv2.cvtColor(yz_frank, cv2.COLOR_BGR2GRAY)

    xy_kors = cv2.cvtColor(xy_kors, cv2.COLOR_BGR2GRAY)
    xz_kors = cv2.cvtColor(xz_kors, cv2.COLOR_BGR2GRAY)
    yz_kors = cv2.cvtColor(yz_kors, cv2.COLOR_BGR2GRAY)

    # Comparar imagens
    compare_images(xy_frank, xy_kors, "XY", worksheet)
    compare_images(xz_frank, xz_kors, "XZ", worksheet)
    compare_images(yz_frank, yz_kors, "YZ", worksheet)

workbook.close()
