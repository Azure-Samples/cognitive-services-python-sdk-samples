# <imports>
import os
try:
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    # python <= 2.7
    from Tkinter import *
    import tkMessageBox as messagebox

from collections import namedtuple
from azure.cognitiveservices.inkrecognizer import ApplicationKind, InkStrokeKind
from azure.cognitiveservices.inkrecognizer import InkRecognizerClient

import logging
logging.basicConfig(level=logging.DEBUG)
# </imports>

# You can also use an Azure credential instance
# <inkRecognizerClientConfig>
INK_RECOGNIZER_URL = "https://api.cognitive.microsoft.com/inkrecognizer"
KEY = os.environ['INK_RECOGNITION_SUBSCRIPTION_KEY'].strip()

# The default locale is "en-US". Setting a different language for a stroke will overload this value. 
LANGUAGE_RECOGNITION_LOCALE = "en-US"

# The default ApplicationKind is "MIXED". Specify the kind of strokes being sent to the API with different ApplicationKind values.
# For example, ApplicationKind.WRITING or ApplicationKind.DRAWING

APPLICATION_KIND = ApplicationKind.MIXED
# </inkRecognizerClientConfig>

# Shows simple implementation of InkPoint and InkStroke
# <strokeImplementations>
InkPoint = namedtuple("InkPoint", "x y")

class InkStroke():
    def __init__(self,
                 ink_stroke_id,
                 ink_points,
                 stroke_kind=InkStrokeKind.UNKNOWN,
                 stroke_language=""):
        self.id = ink_stroke_id
        self.points = ink_points
        self.kind = stroke_kind
        self.language = stroke_language
# </strokeImplementations>

# Wrapper for InkRecognizerClient that shows how to
# (1) Convert stroke unit from pixel to mm
# (2) Set language recognition locale
# (3) Indexing a key word from recognition results
# (4) Set application kind if user know expected type of ink content


# <inkClient>
class InkClient:
    def __init__(self, url, key):
        self._client = InkRecognizerClient(
            url, 
            key,                 
            application_kind=APPLICATION_KIND, # default arguments for each request.
            )
    def send_request(self, ink_stroke_list):
        self._root = None
        try:
            root = self._client.recognize_ink(
                ink_stroke_list, # Arguments for this request only.
                language=LANGUAGE_RECOGNITION_LOCALE,
                logging_enable=True
            )
            
            result_text = []
            for word in root.ink_words:
                result_text.append(word.recognized_text)
            for shape in root.ink_drawings:
                result_text.append(shape.recognized_shape.value)
            result_text = "\n".join(result_text)
            return result_text
            self._root = root
        except Exception as e:
            messagebox.showinfo("Error", e)
# </inkClient>

# <recognitionManager>
class RecognitionManager:
    def __init__(self, pixel_per_mm):
        self._pixel_per_mm = pixel_per_mm
        self._client = InkClient(INK_RECOGNIZER_URL, KEY)
        self.reset_ink()

    def _reset_stroke(self):
        self._curr_stroke_points = []

    def _pixel_to_mm(self, pixel):
        return pixel * 1.0 / self._pixel_per_mm

    def reset_ink(self):
        self._ink_stroke_list = []
        self._root = None
        self._reset_stroke()

    # Convert from pixel to mm before adding to InkPoint.
    def add_point(self, x, y):
        
        self._curr_stroke_points.append(
            InkPoint(self._pixel_to_mm(x), self._pixel_to_mm(y)))

    def stroke_end(self):
        stroke = InkStroke(len(self._ink_stroke_list), self._curr_stroke_points)
        self._ink_stroke_list.append(stroke)
        self._reset_stroke()

    def recognize(self):
        result_text = self._client.send_request(self._ink_stroke_list)
        messagebox.showinfo("Result", result_text)
        
    def search(self, word):
        if self._root is not None:
            num_words = len(self._root.find_word(word))
        else:
            num_words = 0  
        search_result = "Find %s word%s" % (num_words, "s" if num_words != 1 else "")
        messagebox.showinfo("Search Result", search_result)
# </recognitionManager>


# <sampleUI>
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
STROKE_COLOR = "#476042"  # python green
STROKE_WIDTH = 3

class InkRecognizerDemo:
    def __init__(self):
        self._master = Tk()
        self._pack_widgets()

        self._recognition_manager = RecognitionManager(
            pixel_per_mm=self._master.winfo_fpixels("1m"))
        # point for drawing stroke
        self._last_point = None

    def _pack_widgets(self):
        self._master.title("Ink Recognizer Demo")
        # search words
        self._search_variable = StringVar(value="")
        search_entry = Entry(self._master, textvariable=self._search_variable)
        search_button = Button(self._master, text="search a word", command=self._search)
        search_entry.pack(pady=5)
        search_button.pack()
        # main canvas
        self._canvas = Canvas(
            self._master,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT)
        self._canvas.pack(expand=YES, fill = BOTH)
        self._canvas.bind("<B1-Motion>", self._draw)
        self._canvas.bind("<Button-1>", self._stroke_start)
        self._canvas.bind("<ButtonRelease-1>", self._stroke_end)
        # recognize and clear buttons
        recognize_button = Button(
            self._master, text="Recognize", command=self._recognize)
        recognize_button.pack(pady=5)
        clear_button = Button(
            self._master, text="Clear", command=self._clear_canvas)
        clear_button.pack(pady=5)

    def _draw(self, event):
        # paint on canvas
        x_curr, y_curr = event.x, event.y
        if self._last_point is not None:
            x_last, y_last = self._last_point[0], self._last_point[1]
            self._canvas.create_line(
                x_last, y_last, x_curr, y_curr, fill=STROKE_COLOR, width=STROKE_WIDTH)
        self._last_point = x_curr, y_curr
        # add point to stroke store
        self._recognition_manager.add_point(x_curr, y_curr)

    def _stroke_start(self, event):
        # nothing need to do
        pass

    def _stroke_end(self, event):
        self._recognition_manager.stroke_end()
        self._last_point = None

    def _clear_canvas(self):
        self._canvas.delete("all")
        self._recognition_manager.reset_ink()

    def _recognize(self):
        self._recognition_manager.recognize()

    def _search(self):
        self._recognition_manager.search(self._search_variable.get())

    def run(self):
        mainloop()
# </sampleUI>

# <entrypoint>
if __name__ == "__main__":
    demo = InkRecognizerDemo()
    demo.run()
# </entrypoint>