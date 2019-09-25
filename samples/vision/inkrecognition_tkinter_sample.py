import six
if six.PY2:
    from Tkinter import *
    import tkMessageBox as messagebox
else:
    from tkinter import *
    from tkinter import messagebox
from collections import namedtuple
from azure.ai.inkrecognizer import ApplicationKind, InkStrokeKind
from azure.ai.inkrecognizer import InkRecognizerClient


# Ink Recognizer Client Config
URL = "https://api.cognitive.microsoft.com/inkrecognizer"
CREDENTIAL = "FakeCredential"  # Put Azure credential instance here


# Recognition Config
# This tell Ink Recognizer Service that the sample is in en-US.
# Default value is "en-US".
# If "language" in a stroke is specified, this will be overlaped in that stroke.
LANGUAGE_RECOGNITION_LOCALE = "en-US"
# This tell Ink Recognizer Service that domain of the application is writing,
# i.e. all strokes are writing.
# Default value is ApplicationKind.MIXED, which means let Ink Recognizer
# Service detect kind of strokes.
# If "kind" in a stroke is specified, this will be overlaped in that stroke.
APPLICATION_KIND = ApplicationKind.WRITING


# UI Config
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
STROKE_COLOR = "#476042"  # python green
STROKE_WIDTH = 3


# Stroke Implementations
# Shows simple implementation of InkPoint and InkStroke
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


# Sample wrapper for InkRecognizerClient that shows how to
# (1) Convert stroke unit from pixel to mm
# (2) Set language recognition locale
# (3) Indexing a key word from recognition results
# (4) Set application kind if user know expected type of ink content
class RecognitionManager:
    def __init__(self, pixel_per_mm):
        self._pixel_per_mm = pixel_per_mm
        self._client = InkRecognizerClient(URL, CREDENTIAL)
        self.reset_ink()

    def _reset_stroke(self):
        self._curr_stroke_points = []

    def _pixel_to_mm(self, pixel):
        return pixel * 1.0 / self._pixel_per_mm

    def reset_ink(self):
        self._ink_stroke_list = []
        self._root = None
        self._reset_stroke()

    def add_point(self, x, y):
        # Convert from pixel to mm before sending to InkPoint.
        # You can also specify keyword argument "unit_multiple" in
        # InkRecognizerClient constructor or in recognizer_ink() request.
        self._curr_stroke_points.append(
            InkPoint(self._pixel_to_mm(x), self._pixel_to_mm(y)))

    def stroke_end(self):
        stroke = InkStroke(len(self._ink_stroke_list), self._curr_stroke_points)
        self._ink_stroke_list.append(stroke)
        self._reset_stroke()

    def recognize(self):
        self._root = None
        try:
            root = self._client.recognize_ink(
                self._ink_stroke_list,
                # Pre-set recognition type
                application_kind=APPLICATION_KIND,
                # Set language recognition locale
                language=LANGUAGE_RECOGNITION_LOCALE
            )
            # Aruments in request is for this request only
            # You can also specify these arguments in InkRecognizerClient constructor, 
            # which will be default arguments for each call.
            result_text = []
            for word in root.ink_words:
                result_text.append(word.recognized_text)
            for shape in root.ink_drawings:
                result_text.append(shape.recognized_shape.value)
            result_text = "\n".join(result_text)
            messagebox.showinfo("Result", result_text)
            self._root = root
        except Exception as e:
            messagebox.showinfo("Error", e)

    def search(self, word):
        # Indexing a key word from recognition results
        if self._root is not None:
            words = self._root.find_word(word)
            messagebox.showinfo("Search Result", "Find %s words" % len(words))
        else:
            messagebox.showinfo("Search Result", "Find %s words" % 0)


# Sample UI
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


if __name__ == "__main__":
    demo = InkRecognizerDemo()
    demo.run()
