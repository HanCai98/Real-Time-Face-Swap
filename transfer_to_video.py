import cv2
import glob

def main():
    
    convert_image_path = 'output_images'
    filename_list = glob.glob(convert_image_path + "/*.jpg")
    filename_list = sorted(filename_list, key = lambda name: int(name[14:-4]))

    fps = 10
    example = cv2.imread(filename_list[0])
    size = (example.shape[1], example.shape[0])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter('output.mp4',fourcc, fps, size)


    for img in filename_list:
        read_img = cv2.imread(img)
        videoWriter.write(read_img)
    print("Video convert successfuly!")

    videoWriter.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

