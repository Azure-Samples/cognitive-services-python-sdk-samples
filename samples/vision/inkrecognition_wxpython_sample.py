import os
import wx
from azure.cognitiveservices.inkrecognizer import ApplicationKind, InkPointUnit, InkStrokeKind
from azure.cognitiveservices.inkrecognizer import InkRecognizerClient
from collections import namedtuple


# Ink Recognizer Client Config
URL = "https://api.cognitive.microsoft.com/inkrecognizer"
CREDENTIAL = os.environ['INK_RECOGNIZER_SUBSCRIPTION_KEY'].strip()
# You can also use Azure credential instance


# Recognition Config
# This tell Ink Recognizer Service that the sample is in en-US.
# Default value is "en-US".
# If "language" in a stroke is specified, this will be overlaped in that stroke.
LANGUAGE_RECOGNITION_LOCALE = "en-US"
# This tell Ink Recognizer Service that domain of the application is mixed,
# so Ink Recognizer Service will detect kind of each stroke.
# You can set it into ApplicationKind.WRITING or ApplicationKind.DRAWING to specify
# default kind of strokes and skip stroke kind detection precedure.
# Default value is ApplicationKind.MIXED.
# If "kind" in a stroke is specified, this will be overlaped in that stroke.
APPLICATION_KIND = ApplicationKind.MIXED


# This ratio map the number of pixel for x and y axis coordinates on canvas
# into number of mm.
# In InK Recognizer Server, every coordinate in InkPoint will multiply this number. 
# You may also want to mutliply /divide this value before sending request and
# after receiving response.
app = wx.App(False)
mm_on_canvas = float(wx.GetDisplaySizeMM()[1])
pixel_on_canvas = float(wx.GetDisplaySize()[1])
UNIT_MULTIPLE = mm_on_canvas / pixel_on_canvas


# UI config
canvas_width = 800
canvas_height = 600
linewidth = 3


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
    def __init__(self):
        self._client = InkRecognizerClient(
            URL,
            CREDENTIAL,
            ink_point_unit=InkPointUnit.MM,
            # Convert stroke unit from pixel to mm by specify unit_multiple
            # You can also multiply the number when creating InkPoints
            unit_multiple=UNIT_MULTIPLE,
            # Set language recognition locale
            language=LANGUAGE_RECOGNITION_LOCALE,
            # Pre-set recognition type
            application_kind=APPLICATION_KIND
        )
        # Aruments in constructor becomes default arguments for each request
        # You can also specify these arguments in recognize_ink() requests.
        self._reset_ink()

    def _reset_ink(self):
        self._stroke_list = []
        self._reset_stroke()
        self._root = None

    def _reset_stroke(self):
        self._curr_stroke_points = []

    def add_point(self, x, y):
        self._curr_stroke_points.append(
            InkPoint(x, y))

    def stroke_start(self):
        return

    def stroke_end(self):
        stroke = InkStroke(
            len(self._stroke_list),
            self._curr_stroke_points)
        self._stroke_list.append(stroke)
        self._reset_stroke()

    def get_stroke_list(self):
        return self._stroke_list

    def get_curr_points(self):
        return self._curr_stroke_points

    def recognize(self, call_back):
        self._root = self._client.recognize_ink(self._stroke_list)
        result_text = []
        for word in self._root.ink_words:
            result_text.append(word.recognized_text)
        for shape in self._root.ink_drawings:
            result_text.append(shape.recognized_shape.value)
        result_text = "\n".join(result_text)
        call_back(result_text)

    def search(self, word, call_back):
        if self._root is not None:
            # Indexing a key word from recognition results
            words = self._root.find_word(word)
            call_back(len(words))
        else:
            call_back(0)


# Sample canvas
class Canvas(wx.Panel):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_MOTION, self.on_drag)
        self.Bind(wx.EVT_LEFT_UP, self.on_release)

        self._recognition_manager = RecognitionManager()

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        self.dc = wx.PaintDC(self)
        self.dc.SetPen(wx.Pen(wx.BLACK, linewidth))
        self.dc.Clear()
        for stroke in self._recognition_manager.get_stroke_list():
            points = stroke.points
            for i in range(len(points) - 1):
                self.dc.DrawLine(points[i].x, points[i].y, points[i+1].x, points[i+1].y)
        
        points = self._recognition_manager.get_curr_points()
        for i in range(len(points) - 1):
            self.dc.DrawLine(points[i].x, points[i].y, points[i+1].x, points[i+1].y)
    
    def on_click(self, event):
        self._recognition_manager.stroke_start()

    def on_drag(self, event):
        if event.Dragging():
            self._recognition_manager.add_point(event.X, event.y)
            self.Refresh()

    def on_release(self, event):
        self._recognition_manager.stroke_end()
        self.Refresh()

    def recognize(self, event, call_back):
        self._recognition_manager.recognize(call_back)

    def clear(self, event):
        self._recognition_manager._reset_ink()
        self.Refresh()

    def search(self, event, word, call_back):
        self._recognition_manager.search(word, call_back)


# Sample wxpython app
class InkRecognizerDemo(wx.Frame):
    def __init__(self):
        super(InkRecognizerDemo, self).__init__(None)
        self.SetTitle('Ink Recognition Demo')
        self.SetClientSize((canvas_width, canvas_height))
        self.Center()
        self.view = Canvas(self)
        self.search_button = wx.Button(self.view, wx.ID_ANY, 'Search', (0, canvas_height - 90))
        self.recognize_button = wx.Button(self.view, wx.ID_ANY, 'Recognize', (0, canvas_height - 60))
        self.clear_button = wx.Button(self.view, wx.ID_ANY, 'Clear', (0, canvas_height - 30))

        self.search_text = wx.TextCtrl(self.view, wx.ID_ANY, "", (0, canvas_height - 120))
        self.search_button.Bind(wx.EVT_BUTTON, self._search_function)
        self.recognize_button.Bind(wx.EVT_BUTTON, self._recognize_function)
        self.clear_button.Bind(wx.EVT_BUTTON, self.view.clear)

    def _search_function(self, event):
        return self.view.search(
            event, 
            self.search_text.GetLineText(0), 
            call_back=self._show_search_result)

    def _recognize_function(self, event):
        return self.view.recognize(event, call_back=self._show_result)

    def _show_result(self, result):
        dlg = wx.MessageDialog(self, result, "Recognition Result")
        dlg.ShowModal()

    def _show_search_result(self, num_words):
        dlg = wx.MessageDialog(self, "Find %s words" % num_words, "Recognition Result")
        dlg.ShowModal()


def main():
    frame = InkRecognizerDemo()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
