import wx, crash_analysis, os
from BackgroundThread import BackgroundThread, AnalysisThread

class FileDrop(wx.FileDropTarget):
    def __init__(self, item):
        super(FileDrop, self).__init__()
        self.item = item
    def OnDropFiles(self, x, y, filePath):
        path = filePath[0]
        file = path.split('/')[-1]
        file_extension = file.split('.')[-1]
        if file_extension == 'dSYM':
            self.item.dsym_path = path
            self.item.panel.list.Clear()
            self.item.panel.list.Append(file)
        elif file_extension == 'crash' or file_extension == 'ips':
            self.item.crash_path = path
            self.item.panel1.list.Clear()
            self.item.panel1.list.Append(file)

class CustomPanel(wx.Panel):
    def __init__(self, parent, title, item=None):
        super(CustomPanel, self).__init__(parent)
        self.title = title
        self.item = item
        self.initSubView()
    def initSubView(self):
        vBox = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label=self.title)
        vBox.Add(label,flag=wx.TOP | wx.CENTER, border=8)

        self.list = wx.ListBox(self, size=(200, 30))
        if self.item is not None:
            self.list.Bind(wx.EVT_LISTBOX, self.item.onSelect)
        vBox.Add(self.list, flag=wx.TOP | wx.EXPAND, border=10)

        self.SetSizer(vBox)

class CustomFrame(wx.Frame):
    def __init__(self, parent, title):
        super(CustomFrame, self).__init__(parent, title=title, size=(400, 250))
        self.output_path = '~/Desktop'
        self.initUI()
        self.Show()
        BackgroundThread()

    def initUI(self):
        basePanel = wx.Panel(self)
        vSizer = wx.BoxSizer(wx.VERTICAL)

        defaultPanel = wx.Panel(basePanel)
        gSizer = wx.GridSizer(rows=2, cols=2)
        defaultPanel.SetSizer(gSizer)
        self.panel = CustomPanel(defaultPanel, 'dsym')
        gSizer.Add(self.panel, wx.EXPAND)
        self.panel1 = CustomPanel(defaultPanel, '.crash')
        gSizer.Add(self.panel1, wx.EXPAND)
        self.panel2 = CustomPanel(defaultPanel, 'arch', item=self)
        gSizer.Add(self.panel2, wx.EXPAND)
        self.panel3 = CustomPanel(defaultPanel, 'result', self)
        gSizer.Add(self.panel3, wx.EXPAND)
        drop = FileDrop(self)
        defaultPanel.SetDropTarget(drop)

        vSizer.Add(defaultPanel, wx.EXPAND)

        self.beginButton = wx.Button(basePanel, label='begin analysis')
        self.beginButton.Bind(wx.EVT_BUTTON,self.onStart)

        self.path_label = wx.StaticText(basePanel, label='',style=wx.ALIGN_CENTRE)

        self.chooseButton = wx.Button(basePanel, label='choose dictory')
        self.chooseButton.Bind(wx.EVT_BUTTON, self.onChoose)

        vSizer.Add(self.chooseButton, 1, wx.ALL|wx.EXPAND, 10)
        vSizer.Add(self.path_label, 1, wx.LEFT|wx.EXPAND, 10)
        vSizer.Add(self.beginButton, 1, wx.ALL|wx.EXPAND, 10)
        basePanel.SetSizer(vSizer)

    def onChoose(self, event):
        dialog = wx.DirDialog(self, "Choose a Dictory", style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.output_path = dialog.GetPath()
            self.path_label.SetLabel(self.output_path)
        dialog.Destroy()


    def onStart(self, event):
        obj = event.GetEventObject()
        obj.SetLabel('Analysis...')
        obj.Disable()
        AnalysisThread(self)

    def analysis(self):
        result_tuple = crash_analysis.analysis(self.dsym_path, self.crash_path, self.output_path)
        return result_tuple

    def update_result(self, result_tuple):
        self.beginButton.Enable()
        self.beginButton.SetLabel('begin analysis')

        self.panel3.list.Clear()
        self.panel3.list.Append(result_tuple[0])
        for k in result_tuple[1]:
            self.panel2.list.Clear()
            self.panel2.list.Append(k)
        pass
    def onSelect(self, event):
        print event.GetSelection()

if __name__ == '__main__':
    ex = wx.App()
    CustomFrame(None, title='crash_anasynic')
    ex.MainLoop()