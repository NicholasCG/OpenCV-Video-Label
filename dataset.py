import os
import cv2
import csv
import datetime
from tkinter import filedialog
from PIL import Image, ImageTk
from xml.etree import ElementTree
from xml.dom import minidom
from constants import GUI_REDD_RGB, data_set_previewsize


class Dataset:
    def __init__(self, root):
        self.root = root
        self.classes = []
        self.dataset_dict = {}
        self.num_classes = 0
        self.export_setting = 0

    # add image to dataset
    def add_image(self, image_object):
        if image_object.image_class in self.classes:
            self.dataset_dict[image_object.image_class].append(image_object)
        else:
            self.classes.append(image_object.image_class)
            self.dataset_dict[image_object.image_class] = [image_object]

    # remove image from dataset
    def remove_image(self, image_object):
        if image_object in self.dataset_dict[image_object.image_class]:
            self.dataset_dict[image_object.image_class].remove(image_object)
        # remove class from classes if it contains no images
        if not self.dataset_dict[image_object.image_class]:
            self.classes.remove(image_object.image_class)
            self.dataset_dict.pop(image_object.image_class, None)
        del image_object

    def clear(self):
        self.classes.clear()
        self.dataset_dict.clear()

    def move_image(self, image, dest_class):
        pass

    def imort_dataset(self):
        pass

    # export the dataset
    def export(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/datasets"
        folder_selected = filedialog.askdirectory(initialdir=dir_path)
        time = datetime.datetime.now().strftime("%H_%M")
        base_folder = "Dataset_" + time + "/"
        if not folder_selected:
            return
        directory = os.path.join(folder_selected, base_folder)
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.root.status_bar.set("Exporting dataset...")

        # dictionary to prevent errors caused by changing dictionary while exporting
        copy_dict = self.dataset_dict.copy()

        index = {}
        images = {}
        for object_class in copy_dict.keys():
            # copy to prevent changing dictionary errors while exporting and tracking at the same time
            for image_object in copy_dict[object_class]:
                # filename = sub_dir + "/" + str(object_class) + "_" + str(image_object.image_id) + ".jpg"
                if image_object.image_name not in index:
                    index[image_object.image_name] = 0
                    images[image_object.image_name] = []
                filename = os.path.join(directory, 
                                        image_object.image_name + 
                                        "image" + 
                                        str(index[image_object.image_name]) + 
                                        ".png")
                

                # if export cropped images
                if self.export_setting == 0:
                    cv2.imwrite(filename, image_object.cropped_roi[..., ::-1])
                # if exporting full images with pascal voc xml
                elif self.export_setting == 1:
                    cv2.imwrite(filename, image_object.export_image[..., ::-1])
                    self.create_xml_for_image(image_object, directory)
                # if exporting full images with single csv file holding roi data
                else:
                    cv2.imwrite(filename, image_object.export_image[..., ::-1])
                    images[image_object.image_name].append((image_object, directory, index[image_object.image_name]))
                    # self.create_csv_entry(image_object, directory, index[image_object.image_name])
                    index[image_object.image_name] += 1
        
        if self.export_setting > 1:
            for image in images:
                for im_object in images[image]:
                    self.create_csv_entry(im_object[0], im_object[1], im_object[2])

        self.root.status_bar.set("Successfully exported dataset.")

        # Clear the dataset and the dataset frame.
        self.clear()
        self.root.dataset_frame.reset()

    @staticmethod
    def prettify(elem):
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    @staticmethod
    def create_csv_entry(image, directory, index):
        headers = ['Filename', 
                    'Annotation tag', 
                    'Upper left corner X', 
                    'Upper left corner Y', 
                    "Lower right corner X", 
                    "Lower right corner Y", 
                    "Occluded", 
                    "On another road",
                    "Origin file",
                    "Origin frame number",
                    "Origin track",
                    "Origin track frame number"]
        # filename = directory + directory.split("/")[-2] + ".csv"
        filename = os.path.join(directory, "frameAnnotations.csv")
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as outfile:
            writer = csv.writer(outfile)
            if not file_exists:
                writer.writerow(headers)
            item = [image.image_name + "image" + str(index) + ".png", 
                    image.image_class, 
                    image.tl_x, 
                    image.tl_y, 
                    image.br_x, 
                    image.br_y,
                    "Manually add",
                    "Manually add",
                    image.origin,
                    image.origin_frame,
                    image.source,
                    image.frame]

            writer.writerow(item)

    # creates pascal VOC format xml file for an dataset image
    def create_xml_for_image(self, image, directory):
        # create the file structure
        annotation = ElementTree.Element('annotation')

        folder = ElementTree.SubElement(annotation, 'folder')
        folder.text = image.image_class

        filename = ElementTree.SubElement(annotation, 'filename')
        filename.text = image.image_name + '.jpg'

        path = ElementTree.SubElement(annotation, 'path')
        path.text = directory + image.image_class + '/' + filename.text

        source = ElementTree.SubElement(annotation, 'source')
        database = ElementTree.SubElement(source, 'database')
        database.text = 'Unkown'

        size = ElementTree.SubElement(annotation, 'size')
        width = ElementTree.SubElement(size, 'width')
        width.text = str(image.width)
        height = ElementTree.SubElement(size, 'height')
        height.text = str(image.height)
        depth = ElementTree.SubElement(size, 'depth')
        depth.text = '3'

        object_tag = ElementTree.SubElement(annotation, 'object')
        name = ElementTree.SubElement(object_tag, 'name')
        name.text = image.image_class
        pose = ElementTree.SubElement(object_tag, 'pose')
        pose.text = "Unknown"
        truncated = ElementTree.SubElement(object_tag, 'truncated')
        truncated.text = '0'
        difficult = ElementTree.SubElement(object_tag, 'difficult')
        difficult.text = '0'
        occluded = ElementTree.SubElement(object_tag, 'occluded')
        occluded.text = '0'

        bndbox = ElementTree.SubElement(object_tag, 'bndbox')
        xmin = ElementTree.SubElement(bndbox, 'xmin')
        xmin.text = str(image.tl_x)
        xmax = ElementTree.SubElement(bndbox, 'xmax')
        xmax.text = str(image.br_x)
        ymin = ElementTree.SubElement(bndbox, 'ymin')
        ymin.text = str(image.tl_y)
        ymax = ElementTree.SubElement(bndbox, 'ymax')
        ymax.text = str(image.br_y)

        # export the a new XML file
        xml_file = open(directory + image.image_class + '/' + image.image_name + ".xml", "w")
        xml_file.write(self.prettify(annotation))


class DatasetImage:
    def __init__(self, image, image_id, image_class, tl_x, tl_y, br_x, br_y, frame, source):
        self.image = image
        self.image_id = image_id
        self.image_class = image_class
        self.tl_x, self.tl_y, self.br_x, self.br_y = tl_x, tl_y, br_x, br_y
        self.frame = frame - 1
        self.source = source

        source_split = source.split("-start")
        file_type = source_split[1].split('.')[1]

        self.origin = "-".join(source_split[0].split('-')[:-1]) + "." + file_type
        self.origin_frame = int(source_split[1].split('.')[0]) + self.frame
        
        self.image_name = source + "_"
        
        self.export_image = image.copy()
        self.cropped_roi = None
        self.preview_image = None
        self.id = None
        self.current_selection = []
        self.selected_button_ids = []
        self.height, self.width = self.image.shape[:2]

    # draws a red border and the label of the class on the frame
    def draw_roi(self, add_class_label=True):
        font = cv2.FONT_HERSHEY_DUPLEX

        # draw the bounding box
        cv2.rectangle(self.image, (self.tl_x, self.tl_y), (self.br_x, self.br_y), GUI_REDD_RGB, 2)
        # draw the class label background and label
        if add_class_label:
            cv2.rectangle(self.image, (self.tl_x - 1, self.tl_y - 15),
                          (self.tl_x + 10 + len(self.image_class) * 10, self.tl_y),
                          GUI_REDD_RGB, cv2.FILLED)
            cv2.putText(self.image, self.image_class, (self.tl_x + 5, self.tl_y - 2), font, .5,
                        (255, 255, 255), 1, cv2.LINE_AA)

    # crops image to objects location
    def crop(self):
        self.cropped_roi = self.image[self.tl_y:self.br_y, self.tl_x:self.br_x].copy()

    # takes the cropped roi and pads it with black borders, maintaining its original aspect ratio
    def crop_and_pad_roi(self, max_w=data_set_previewsize, max_h=data_set_previewsize):
        self.crop()
        (h, w) = self.cropped_roi.shape[:2]

        # prevent division by 0 on next lines and resize error
        if w > 5 and h > 5:
            resize_x = max_w / w
            resize_y = max_h / h
            top, bot, left, right = 0, 0, 0, 0

            if resize_y < resize_x:
                new_width = int(w * resize_y)
                resize = tuple((new_width, max_h))
                total_pad = max_w - new_width
                left = int(total_pad / 2)
                right = total_pad - left
            else:
                new_height = int(h * resize_x)
                resize = tuple((max_w, new_height))
                total_pad = max_h - new_height
                top = int(total_pad / 2)
                bot = total_pad - top

            cropped = cv2.resize(self.cropped_roi.copy(), resize, interpolation=cv2.INTER_LINEAR)
            padded_preview = cv2.copyMakeBorder(cropped, top, bot, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            photo = Image.fromarray(padded_preview)
            self.preview_image = ImageTk.PhotoImage(image=photo)
            return True
        return False
