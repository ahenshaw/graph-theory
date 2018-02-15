import tempfile
import os

# third-party libraries
import wx
import wx.adv
from wx.lib.pubsub import pub
import networkx as nx
import pandas as pd
from io import StringIO

## for later use ## a = pd.read_csv(StringIO(csv))

VERSION = '0.1'
FANCY_APP_NAME = 'SAS Graph'
APP_NAME = 'sasgraph'


class Dropper(wx.TextDropTarget):
    def __init__(self, parent):
        self.parent = parent
        wx.TextDropTarget.__init__(self)

    def OnDropText(self, x, y, data):
        self.parent.SetValue(data)
        return True

class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.bitmap   = None
        self.original = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        pub.subscribe(self.SetImage, 'NewImage')

    def OnPaint(self, event):
        if self.bitmap is None:
            return
        w, h = self.GetClientSize()
        iw, ih = self.bitmap.GetSize()
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, (w-iw)//2, (h-ih)//2)

    def OnSize(self, event):
        if self.original is None:
            return

        w, h = self.GetClientSize()
        iw, ih = self.original.GetSize()
        scale = min(w/iw, h/ih)
        iw = int(scale * iw)
        ih = int(scale * ih)
        try:
            img = self.original.Scale(iw, ih, wx.IMAGE_QUALITY_BICUBIC)
        except:
            return
        self.bitmap = wx.Bitmap(img)
        self.Refresh(True)
        self.Update()

    def SetImage(self, image):
        self.original = image
        self.OnSize(None)


class DotPanel(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, -1, style=wx.TE_MULTILINE)
        self.parent = parent
        self.drop = Dropper(self)
        self.SetDropTarget(self.drop)
        self.Bind(wx.EVT_TEXT, self.OnText)

    def OnText(self, event):
        edges = self.GetValue().split()
        edges = list(zip(*[edges[i::2] for i in range(2)]))
        g = nx.from_edgelist(edges)

        dot = nx.drawing.nx_pydot.to_pydot(g)
        dot.set('dpi', 300)

        temp = tempfile.NamedTemporaryFile(suffix='.png')
        temp.close()
        dot.write_png(temp.name)
        image = wx.Image()
        image.LoadFile(temp.name)
        os.remove(temp.name)
        pub.sendMessage('NewImage', image=image)
        


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.doLayout()
        
    def doLayout(self):
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_3DSASH)
        self.png = ImagePanel(splitter)

        self.code = DotPanel(splitter)
        self.code.SetBackgroundColour(wx.WHITE)
        self.png.SetBackgroundColour(wx.WHITE)
        splitter.SplitVertically(self.code, self.png, 300)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(splitter, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
    
class MainFrame(wx.Frame):
    def __init__(self, **kwargs):
        wx.Frame.__init__(self, None, **kwargs)
        self.main = MainPanel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.main, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.sb = self.CreateStatusBar(style=wx.STB_SIZEGRIP)
        
        self.doMenu()
        
    def doMenu(self):
        menubar = wx.MenuBar()

        # File Menu
        file_menu = wx.Menu()
                
        file_menu.AppendSeparator()
        mi_exit = file_menu.Append(-1, "E&xit")
        self.Bind(wx.EVT_MENU, self.onExit, mi_exit)

        menubar.Append(file_menu, "&File")
        
        # Help Menu
        help_menu = wx.Menu()
        
        mi_about = help_menu.Append(-1, '&About %s' % APP_NAME)
        self.Bind(wx.EVT_MENU, self.onAbout, mi_about)
        
        menubar.Append(help_menu, '&Help')

        self.SetMenuBar(menubar)
                       
       
    def onExit(self, event):
        self.Close()

    def onAbout(self, evt):
        info = wx.adv.AboutDialogInfo()
        info.SetName(FANCY_APP_NAME)
        info.SetVersion(VERSION)
        info.SetDescription('')
        info.SetDevelopers(['Andrew Henshaw\nandrew@henshaw.us'])
        info.SetCopyright('2017')
        
        wx.adv.AboutBox(info)        
        

def main():
    app = wx.App(redirect=False)
    frame = MainFrame(title=FANCY_APP_NAME, size=(1024, 600))
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
    
if __name__ == '__main__':
    main()