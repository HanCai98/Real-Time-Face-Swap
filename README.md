# face_changing_v2
Final Project of CSCI 1430 with a self-implemented face landmark detection model

1. **Install requirements**

   ```shell
   pip3 install -r requirements.txt
   ```

2. **Dataset**

   (1) [Wider Facial Landmarks in-the-wild (WFLW)](https://wywu.github.io/projects/LAB/WFLW.html) is a new proposed face dataset. It contains 10000 faces (7500 for training and 2500 for testing)  with 98 fully manual annotated landmarks.

   (2) Download WFLW Training and Testing images at [[Google Drive](https://drive.google.com/file/d/1hzBd48JIdWTJSsATBEB_eFVvPL1bx6UC/view?usp=sharing)]

   (3) Download WFLW Annotations at  [Face Annotations](https://wywu.github.io/projects/LAB/support/WFLW_annotations.tar.gz)

   (4) Unzip above two packages and put them on `./data/WFLW/`

   (5) Move `Mirror98.txt` to `WFLW/WFLW_annotations`

   (6) Preprocess the dataset

   ```shell
   $ cd data 
   $ python3 SetPreparation.py
   ```

3. **Train and Test**

   (1) Train:

   ```shell
   $ python3 train.py
   ```

   (2) Use tensorbnoard to view the loss changing:

   ```shell
   $ tensorboard  --logdir=./checkpoint/tensorboard/
   ```

   (3) Test:

   ```shell
   $ python3 test.py
   ```


4. **Face Changing**

   (1) Extract and save the video frames

   ```shell
   $ python3 main.py
   ```

   (2) Create the output video using saved frames

   ```shell
   $ python3 transfer_to_video.py
   ```

5. **Result**
   <img src="images/output.gif" style="zoom:50%;" />
 
6. **Report and Poster**

   Final report: https://drive.google.com/file/d/1hst6AY2cbunJz6_fLI4KINTOAoNz8cAf/view?usp=sharing
   
   Poster: https://drive.google.com/file/d/1fDGP9QRNnN8bLNO9HHJ1RIW31amfG5Jz/view?usp=sharing

7. **Reference**

   PFLD: A Practical Facial Landmark Detector https://arxiv.org/pdf/1902.10859.pdf

   
