import pandas as pd
import os
import sys
import cv2

def main(dir):

    vids = []
    for file in os.listdir(dir):
        d = os.path.join(dir, file)
        if os.path.isdir(d):
            vids.append(d)

    for v in vids:
        try:
            df = pd.read_csv(os.path.join(v, "frameAnnotations.csv"))

            for i in range(len(df)):
                occluded = 0
                another_road = 0

                img = df.at[i, "Filename"]
                cur_image_path = os.path.join(v, img)
                cur_image = cv2.imread(cur_image_path)

                # Draw rectangle around sign
                ul = (df.at[i, "Upper left corner X"], df.at[i, "Upper left corner Y"])
                br = (df.at[i, "Lower right corner X"], df.at[i, "Lower right corner Y"])
                color = (0, 0, 255)
                thickness = 1
                cur_image = cv2.rectangle(cur_image, ul, br, color, thickness)

                cv2.imshow(cur_image_path, cur_image)
                k = cv2.waitKey(0)

                # Move to next image with enter key
                while k != 13:
                    if k == ord('o'):
                        occluded = 1 - occluded
                        print(f"{img} Occluded: {occluded}")
                    if k == ord('r'):
                        another_road = 1 - another_road
                        print(f"{img} On another road: {another_road}")

                    k = cv2.waitKey(0)
                    
                cv2.destroyAllWindows()
                df.at[i, "Occluded"] = occluded
                df.at[i, "On another road"] = another_road

            df.to_csv(os.path.join(v, "frameAnnotations.csv"), index=False)

        except FileNotFoundError:
            print(f"{v} not found to have frameAnnotations.csv. Something's wrong!")
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])