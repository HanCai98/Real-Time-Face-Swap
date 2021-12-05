import argparse
import numpy as np
import cv2
import os

import torch
import torchvision

from models.pfld import PFLDInference, AuxiliaryNet
from mtcnn.detector import detect_faces
from face_change.transformation import trans

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main(args):
    checkpoint = torch.load(args.model_path, map_location=device)
    pfld_backbone = PFLDInference().to(device)
    pfld_backbone.load_state_dict(checkpoint['pfld_backbone'])
    pfld_backbone.eval()
    pfld_backbone = pfld_backbone.to(device)
    transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()])

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No camera found or error opening camera; using a static image instead.")

    # store all the mask files name and label files name
    labels_path = 'conf'
    labels_files= os.listdir(labels_path)
    labels_files.sort(key= lambda x:int(x[5:7]))

    masks_path = 'masks'
    masks_files = os.listdir(masks_path)
    masks_files.sort(key= lambda x:int(x[5:7]))

    # get the first mask
    number = 0
    change_mask = True

    while True:
        success, img = cap.read()
        if not success: 
            break
        height, width = img.shape[:2]

        # number = 0
        mask = masks_files[number]
        mask_indices = labels_files[number]
        
        bounding_boxes, landmarks = detect_faces(img)
        for box in bounding_boxes:
            x1, y1, x2, y2 = (box[:4] + 0.5).astype(np.int32)

            w = x2 - x1 + 1
            h = y2 - y1 + 1
            cx = x1 + w // 2
            cy = y1 + h // 2

            size = int(max([w, h]) * 1.1)
            x1 = cx - size // 2
            x2 = x1 + size
            y1 = cy - size // 2
            y2 = y1 + size

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width, x2)
            y2 = min(height, y2)

            edx1 = max(0, -x1)
            edy1 = max(0, -y1)
            edx2 = max(0, x2 - width)
            edy2 = max(0, y2 - height)

            cropped = img[y1:y2, x1:x2]
            
            
            if (edx1 > 0 or edy1 > 0 or edx2 > 0 or edy2 > 0):
                cropped = cv2.copyMakeBorder(cropped, edy1, edy2, edx1, edx2,
                                             cv2.BORDER_CONSTANT, 0)

            input = cv2.resize(cropped, (112, 112))
            
            input = transform(input).unsqueeze(0).to(device)
            _, landmarks = pfld_backbone(input)
            # _, landmarks = pfld_backbone(img)
            pre_landmark = landmarks[0]
            pre_landmark = pre_landmark.cpu().detach().numpy().reshape(
                -1, 2) * [size, size] - [edx1, edy1]
            
            print(len(pre_landmark))
            if len(pre_landmark) != 0:
                img = trans(pre_landmark, img, 'masks/' + mask, 'conf/' + mask_indices)
                change_mask = True
            elif not pre_landmark:
                if number < 14 and change_mask:
                    number += 1
                    change_mask = False
                elif number >= 14 and change_mask:
                    number = 0
                    change_mask = False


            for (x, y) in pre_landmark.astype(np.int32):
                cv2.circle(img, (x1 + x, y1 + y), 1, (0, 0, 255))
        print(img.shape)
        cv2.imshow('face_landmark_68', img)

        if cv2.waitKey(10) == 27:
            break


def parse_args():
    parser = argparse.ArgumentParser(description='Testing')
    parser.add_argument('--model_path',
                        default="./checkpoint/snapshot/checkpoint_epoch_500.pth.tar",
                        type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
