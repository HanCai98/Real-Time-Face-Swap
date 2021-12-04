import time
import cv2
import os

from numpy.core import numeric
from FaceMeshModule import FaceMeshDetector  
from transformation import transform


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No camera found or error opening camera; using a static image instead.")
    
    # store all the mask files name and label files name
    labels_path = '../conf'
    labels_files= os.listdir(labels_path)
    labels_files.sort(key= lambda x:int(x[5:7]))

    masks_path = '../masks'
    masks_files = os.listdir(masks_path)
    masks_files.sort(key= lambda x:int(x[5:7]))

    # get the first mask
    number = 0
    change_mask = True
    
    pTime = 0
    detector = FaceMeshDetector()
    while True:

        # press 'Esc' to stop
        if cv2.waitKey(1) == 27:
            break

        success, img = cap.read()
        img, face = detector.findFaceMesh(img)

        # number = 0
        mask = masks_files[number]
        mask_indices = labels_files[number]

        if len(face) != 0:
            img = transform(face, img, '../masks/' + mask, '../conf/' + mask_indices)
            change_mask = True
        else:
            if number < 14 and change_mask:
                number += 1
                change_mask = False
            elif number >= 14 and change_mask:
                number = 0
                change_mask = False

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # # press 'Esc' to stop
        # if cv2.waitKey(1) == 27:
        #     break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()