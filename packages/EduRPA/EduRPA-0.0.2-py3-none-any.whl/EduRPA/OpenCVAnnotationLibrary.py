import cv2
import json
from robot.api import logger
from robot.api.deco import keyword, not_keyword

class OpenCVAnnotationLibrary:
    def __init__(self):
        # Global variables
        self.annotations = []
        self.current_annotation = None
        self.image = None  # Initialize the image variable
        self.selected_annotation = None

        # Colors
        self.annotation_color = (0, 255, 0)  # Initial color (green) for annotations
        self.selected_color = (0, 0, 255)  # Color (red) for the selected annotation

    # Mouse callback function
    @not_keyword
    def draw_bbox(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.current_annotation = {"x1": x, "y1": y}
            self.selected_annotation = None  # Clear selected annotation

        elif event == cv2.EVENT_LBUTTONUP:
            self.current_annotation["x2"] = x
            self.current_annotation["y2"] = y
            self.annotations.append({"bbox": self.current_annotation.copy(), "color": self.annotation_color})
            self.current_annotation.clear()

        elif event == cv2.EVENT_MOUSEMOVE and self.current_annotation:
            temp_image = self.image.copy()
            cv2.rectangle(temp_image, (self.current_annotation["x1"], self.current_annotation["y1"]),
                          (x, y), self.annotation_color, 2)
            cv2.imshow("Image", temp_image)

        # Check if the click is within an existing annotation
        if event == cv2.EVENT_RBUTTONDOWN:
            for idx, annotation in enumerate(self.annotations):
                bbox = annotation["bbox"]
                x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.selected_annotation = idx
                    break
    @not_keyword
    def render_annotations(self):
        for idx, annotation in enumerate(self.annotations):
            bbox = annotation["bbox"]
            color = self.selected_color if self.selected_annotation == idx else annotation["color"]
            x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
            cv2.rectangle(self.image, (x1, y1), (x2, y2), color, 2)

    @keyword("Open Annotate Bounding Box")
    def main(self, image_path):
        print(image_path)
        image = cv2.imread(image_path)
        self.image = image.copy()
        cv2.imshow("Image", image)
        cv2.setMouseCallback("Image", self.draw_bbox)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                annotation_file = "annotations.json"
                with open(annotation_file, 'w') as json_file:
                    json.dump(self.annotations, json_file, indent=4)
                logger.info(f"Annotations saved to {annotation_file}")
                break
            elif key == ord('d'):
                if self.selected_annotation is not None:
                    logger.info(self.selected_annotation)
                    removed_annotation = self.annotations.pop(self.selected_annotation)
                    del removed_annotation
                    self.selected_annotation = None
            elif key == ord('q'):
                break

            # Render the annotations on the image and continuously update the display
            self.render_annotations()
            cv2.imshow("Image", self.image)

        cv2.destroyAllWindows()
        return image, [box["bbox"] for box in self.annotations]
    @keyword("Save Annotation")
    def save_annotations(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.annotations, json_file, indent=4)
        logger.info(f"Annotations saved to {filename}")

    @not_keyword
    def delete_selected_annotation(self):
        if self.selected_annotation is not None:
            logger.info(self.selected_annotation)
            self.annotations.pop(self.selected_annotation)
            self.selected_annotation = None

    def quit_application(self):
        cv2.destroyAllWindows()

