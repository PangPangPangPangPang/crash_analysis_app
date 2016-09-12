from threading import Thread
import crash_analysis
import wx
import time

class BackgroundThread(Thread):
    def __init__(self):
        super(BackgroundThread, self).__init__()
        self.start()
    def run(self):
        crash_analysis.downLoadSymbolicatecrash()
        wx.CallAfter(self.finish)
    def finish(self):
        print 'finish update symbolicatecrash file'

class AnalysisThread(Thread):
    def __init__(self, item):
        super(AnalysisThread, self).__init__()
        self.item = item
        self.start()

    def run(self):
        result = self.item.analysis()
        wx.CallAfter(self.item.update_result, result)

