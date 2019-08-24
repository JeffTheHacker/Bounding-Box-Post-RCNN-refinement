import random
import cv2

class bbox:
    def __init__(self, name, occluded, xmin, ymin, xmax, ymax):
        self.name = name
        self.occluded = occluded
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def getName(self):
        return self.name

    def getOccluded(self):
        return self.occluded

    def getCoordinates(self):
        return self.xmin, self.ymin, self.xmax, self.ymax

    def getArea(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)


class img_with_box:
    def __init__(self, image,id):
        self.id = id
        self.image = image
        self.bboxlist = []

    def getID(self):
        return self.id

    def getImage(self):
        return self.image

    def getbboxList(self):
        return self.bboxlist

    def removebboxfromlist(self,obj):
        self.bboxlist.remove(obj)

    def appendBbox(self, name, occluded, xmin, ymin, xmax, ymax):
        box = bbox(name, occluded, xmin, ymin, xmax, ymax)
        self.bboxlist.append(box)

class img_with_side_enum:
    def __init__(self,image,id):
        self.image = image
        self.id = id
        self.leftborderlist = [] #contains class enumerations
        self.rightborderlist = []
        self.upborderlist = []
        self.downborderlist = []

    def getLeftBorderList(self):
        return self.leftborderlist

    def getRightBorderList(self):
        return self.rightborderlist

    def getUpBorderList(self):
        return self.upborderlist

    def getDownBorderList(self):
        return self.downborderlist

    def getImage(self):
        return self.image


    def generation(self,xmin, ymin, xmax, ymax):
        #first handle left border
        left_border_lines = []
        width_left = ymax - ymin
        scope_left = width_left * (0.5 + 1.4 / 2) * 0.4
        for _ in range(6):
            left_border_lines.append(random.randint(int(xmin - scope_left/2), int(xmin + scope_left/2)))
        for i in left_border_lines:
            for w in range(1,7):
                left_box_width = width_left * (0.5 + 1.4 / w) / 2.25
                left_box_height = width_left * (0.5 + 1.4 / w) / 1.50
                x_min_leftbox = int(i - left_box_width / 2)
                x_max_leftbox = int(i + left_box_width / 2)
                y_min_leftbox = int((ymin + ymax) / 2 - left_box_height / 2)
                y_max_leftbox = int((ymin + ymax) / 2 + left_box_height / 2)
                self.leftborderlist.append(enumeration(x_min_leftbox,y_min_leftbox,x_max_leftbox,y_max_leftbox,xmin,ymin, xmax, ymax, 'left'))

        # then handle right border
        right_border_lines = []
        width_right = ymax - ymin
        scope_right = 0.4 * width_right * (0.5 + 1.4 / 2)
        for _ in range(6):
            right_border_lines.append(random.randint(int(xmax - scope_right / 2), int(xmax + scope_right / 2)))
        for i in right_border_lines:
            for w in range(1, 7):
                right_box_width = width_right * (0.5 + 1.4 / w) / 2.25
                right_box_height = width_right * (0.5 + 1.4 / w) / 1.50
                x_min_rightbox = int(i - right_box_width / 2)
                x_max_rightbox = int(i + right_box_width / 2)
                y_min_rightbox = int((ymin + ymax) / 2 - right_box_height / 2)
                y_max_rightbox = int((ymin + ymax) / 2 + right_box_height / 2)
                self.rightborderlist.append(enumeration(x_min_rightbox, y_min_rightbox, x_max_rightbox, y_max_rightbox, xmin,ymin, xmax, ymax, 'right'))

        # then handle up border
        up_border_lines = []
        width_up = xmax - xmin
        scope_up = 0.4 * width_up * (0.5 + 1.4 / 2)
        for _ in range(9):
            up_border_lines.append(random.randint(int(ymin - scope_up / 2), int(ymin + scope_up / 2)))
        for i in up_border_lines:
            for w in range(3, 7):
                up_box_width = width_up * (0.5 + 1.4 / w) / 1.50
                up_box_height = width_up * (0.5 + 1.4 / w) / 2.25
                y_min_upbox = int(i - up_box_height / 2)
                y_max_upbox = int(i + up_box_height / 2)
                x_min_upbox = int((xmin + xmax) / 2 - up_box_width / 2)
                x_max_upbox = int((xmin + xmax) / 2 + up_box_width / 2)
                self.upborderlist.append(enumeration(x_min_upbox, y_min_upbox, x_max_upbox, y_max_upbox,xmin,ymin, xmax, ymax,'up'))

        # then handle down border
        down_border_lines = []
        width_down = xmax - xmin
        scope_down = 0.4 * width_down * (0.5 + 1.4 / 2)
        for _ in range(8):
            down_border_lines.append(random.randint(int(ymax - scope_down / 2), int(ymax + scope_down / 2)))
        for i in down_border_lines:
            for w in range(2, 7):
                down_box_width = width_down * (0.5 + 1.4 / w) / 1.50
                down_box_height = width_down * (0.5 + 1.4 / w) / 2.25
                y_min_downbox = int(i - down_box_height / 2)
                y_max_downbox = int(i + down_box_height / 2)
                x_min_downbox = int((xmin + xmax) / 2 - down_box_width / 2)
                x_max_downbox = int((xmin + xmax) / 2 + down_box_width / 2)
                self.downborderlist.append(enumeration(x_min_downbox, y_min_downbox, x_max_downbox, y_max_downbox,xmin,ymin, xmax, ymax, 'down'))



class enumeration:
    def __init__(self,xmin,ymin, xmax, ymax, xminOg,yminOg, xmaxOg, ymaxOg,type):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xminOg = xminOg
        self.yminOg = yminOg
        self.xmaxOg = xmaxOg
        self.ymaxOg = ymaxOg
        self.type = type
        self.distance = 0

    def getCoordinates(self):
        return self.xmin,self.ymin,self.xmax, self.ymax

    def getWidthBase(self):
        if (self.type == 'left' or self.type == 'right'):
            return self.ymaxOg - self.yminOg
        elif (self.type == 'up' or self.type == 'down'):
            return self.xmaxOg - self.xminOg


    def getDistance(self):
        return self.distance

    def selfCheck(self):
        if (self.xmin < 0 or self.xmax < 0 or self.xmin >= 768 or self.xmax >= 768 or self.ymin < 0 or self.ymax < 0 or self.ymin >= 384 or self.ymax >= 384):
            return False
        if (self.type == 'left'):
            self.distance = self.xminOg - (self.xmin + self.xmax) / 2  #positive distance means ground truth to the right of enumerated border
            return self.xminOg <= self.xmax - 15 and self.xminOg >= self.xmin + 15 and self.xmaxOg > self.xmax
        elif (self.type == 'right'):
            self.distance = self.xmaxOg - (self.xmin + self.xmax) / 2  # positive distance means ground truth to the right of enumerated border
            return self.xmaxOg <= self.xmax - 15 and self.xmaxOg >= self.xmin + 15 and self.xminOg < self.xmin
        elif (self.type == 'up'):
            self.distance = self.yminOg - (self.ymin + self.ymax) / 2 #postive distance means ground truth below enumerated border
            return self.yminOg <= self.ymax - 15 and self.yminOg >= self.ymin + 15 and self.ymaxOg > self.ymax
        elif (self.type == 'down'):
            self.distance = self.ymaxOg - (self.ymin + self.ymax) / 2  # postive distance means ground truth below enumerated border
            return self.ymaxOg <= self.ymax - 15 and self.ymaxOg >= self.ymin + 15 and self.yminOg < self.ymin





def text_create(name, msg):
    desktop_path = '/Users/jeffhe/Desktop/黑芝麻/boundary box regression/kitti_extracted/kitti_extracted_labels_down/'
    full_path = desktop_path + name
    file = open(full_path,'a')
    file.write(msg)
    file.close()


