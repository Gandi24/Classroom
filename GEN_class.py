import wx

from classroom import classroom

ID_NEW = 1
ID_RENAME = 2
ID_CLEAR = 3
ID_DELETE = 4
ID_LOAD = 5

class Example(wx.Frame):
    
	def __init__(self, *args, **kwargs):
		super(Example, self).__init__(*args, **kwargs)
		
		self.classroom_instance = classroom()
		
		self.InitUI()
		self.Centre()
		self.Show(True)
		
	def InitUI(self):    
	
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		reset = wx.MenuItem(fileMenu, wx.ID_ANY, '&Reset\tCtrl+R')
		fileMenu.AppendItem(reset)
	
		fileMenu.AppendSeparator()
	
		cred = wx.MenuItem(fileMenu, wx.ID_ANY, '&Credits\tCtrl+C')
		fileMenu.AppendItem(cred)
				
		qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
		fileMenu.AppendItem(qmi)

		menubar.Append(fileMenu, '&File')
        
		self.SetMenuBar(menubar)
        
		self.Bind(wx.EVT_MENU, self.OnReset, reset)
		self.Bind(wx.EVT_MENU, self.OnCredit, cred)
		self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
				
		self.panel = wx.Panel(self, -1)
		
		wx.StaticText(self.panel, label="Penalty ratio for forms :", pos=(400,3))
		self.forms_field = wx.TextCtrl(self.panel, value="5", pos=(550, 3), size=(50, 20))
		wx.StaticText(self.panel, label="Penalty ratio for teachers :", pos=(400,33))
		self.teachers_field = wx.TextCtrl(self.panel, value="1", pos=(550, 33), size=(50, 20))
		wx.StaticText(self.panel, label="Penalty ratio for short days :", pos=(400,63))
		self.short_days_field = wx.TextCtrl(self.panel, value="1", pos=(550, 63), size=(50, 20))
		wx.StaticText(self.panel, label="Length of generation :", pos=(400,93))
		self.genom_length = wx.TextCtrl(self.panel, value="10", pos=(550, 93), size=(50, 20))
		wx.StaticText(self.panel, label="Number of iterations :", pos=(400,123))
		self.iterations = wx.TextCtrl(self.panel, value="10", pos=(550, 123), size=(50, 20))
		wx.StaticText(self.panel, label="Number of classes :", pos=(400,153))
		self.forms_range = wx.TextCtrl(self.panel, value="5", pos=(550, 153), size=(50, 20))
		wx.StaticText(self.panel, label="Number of rooms :", pos=(400,183))
		self.rooms_range = wx.TextCtrl(self.panel, value="5", pos=(550, 183), size=(50, 20))
		
		
		wx.Button(self.panel, 10, 'Begin', (400, 213))
		
		wx.StaticText(self.panel, label="Which class to display :", pos=(400,243))
		self.display = wx.TextCtrl(self.panel, value="", pos=(550, 243), size=(50, 20))
		
		self.possibilities = ['forms', 'teachers', 'rooms']
		
		wx.StaticText(self.panel, label="Type of selection :", pos=(400,273))
		wx.ComboBox(self.panel, -1, pos=(400, 293), size=(150, -1), choices=self.possibilities, 
					style=wx.CB_READONLY)
		
		
		##################
		hbox = wx.BoxSizer(1)
		self.listbox = wx.ListBox(self.panel, -1)
		hbox.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 20)
		btnPanel = wx.Panel(self.panel, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		new = wx.Button(btnPanel, ID_NEW, 'New', size=(90, 30))
		ren = wx.Button(btnPanel, ID_RENAME, 'Rename', size=(90, 30))
		dlt = wx.Button(btnPanel, ID_DELETE, 'Delete', size=(90, 30))
		clr = wx.Button(btnPanel, ID_CLEAR, 'Clear', size=(90, 30))
		load = wx.Button(btnPanel, ID_LOAD, 'Load', size=(90, 30))
		vbox.Add((-1, 20))
		vbox.Add(new)
		vbox.Add(ren, 0, wx.TOP, 5)
		vbox.Add(dlt, 0, wx.TOP, 5)
		vbox.Add(clr, 0, wx.TOP, 5)
		vbox.Add(load, 0, wx.TOP, 5)
		btnPanel.SetSizer(vbox)
		hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
		self.panel.SetSizer(hbox)
		
		##################
		
		
		
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.forms_field)
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.teachers_field)
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.short_days_field)
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.genom_length)
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.iterations)
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.forms_range)
		self.Bind(wx.EVT_TEXT, self.OnTextModify, self.rooms_range)
		self.Bind(wx.EVT_BUTTON, self.OnBegin, id=10)
		self.Bind(wx.EVT_TEXT, self.OnFormDisplay, self.display)
		self.Bind(wx.EVT_COMBOBOX, self.OnSelect)
		self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
		self.Bind(wx.EVT_BUTTON, self.OnRename, id=ID_RENAME)
		self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
		self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)
		self.Bind(wx.EVT_BUTTON, self.OnLoad, id=ID_LOAD)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)
		
		self.class_name = wx.TextCtrl(self.panel, style=wx.TE_READONLY, pos=(610,3))
		

		column_count = 0
		for item in self.classroom_instance.day_list:
			wx.StaticText(self.panel, label=str(item), pos=(655+100*column_count,30))
			column_count += 1
			
		line_count = 0
		for item in self.classroom_instance.daycells:
			wx.StaticText(self.panel, label=str(item), pos=(610,50+line_count*30))
			line_count += 1
		
		self.schedule_field = []
		for i in range(len(self.classroom_instance.day_list)):
			temp = []
			for j in range(len(self.classroom_instance.daycells)):
				temp.append(wx.TextCtrl(self.panel, style=wx.TE_READONLY, pos=(650+100*i,50+j*30)))
			self.schedule_field.append(temp)
			
		self.selection = None
		
	def OnSelect(self, event):
		self.selection = self.possibilities[event.GetSelection()]
						
		self.OnFormDisplay(event)
		
	def OnFormDisplay(self, event):
		if not self.selection:
			wx.MessageBox('First choose a type of selection', 'Return', 
						wx.ICON_ERROR | wx.ICON_INFORMATION)
			return
			
		self.current = eval("self.result.%s"%self.selection)
			
		try:
			if self.display.Value not in self.current.keys():
				return
		except AttributeError:
			return
			
		for row in self.schedule_field:
			for item in row:
				item.SetValue("")
			
		reset_text = (" "*150 + "\n")*100
			
		classroom = self.current[self.display.Value]
		self.class_name.SetValue(str(classroom))
		
		for item, value in classroom.schedule.items():
			day = self.classroom_instance.day_list.index(str(item))
			for daycell in value:
				cell = self.classroom_instance.daycells.index(daycell[0])
				try:
					self.schedule_field[day][cell].SetValue("%s (%s) %s" %(daycell[2], daycell[1], daycell[3]))
				except IndexError:
					self.schedule_field[day][cell].SetValue("%s (%s)" %(daycell[2], daycell[1]))

		
	def OnBegin(self, event):
		self.result = self.classroom_instance.count()	
		
	def OnTextModify(self, e):
		try:
			for item in [self.forms_field, self.teachers_field, self.short_days_field, self.genom_length, self.iterations, self.forms_range, self.rooms_range]:
				if not item.Value:
					item.Value = "0"
			self.classroom_instance.penalty_for_forms = int(self.forms_field.Value)
			self.classroom_instance.penalty_for_teachers = int(self.teachers_field.Value)
			self.classroom_instance.short_days_field = int(self.short_days_field.Value)
			self.classroom_instance.genom_length = int(self.genom_length.Value)
			self.classroom_instance.iterations = int(self.iterations.Value)
			self.classroom_instance.forms_range = int(self.forms_range.Value)
			self.classroom_instance.rooms_range = int(self.rooms_range.Value)
		
		except ValueError:
			wx.MessageBox('Wrong value', 'Return', 
				wx.ICON_ERROR | wx.ICON_INFORMATION)
	
	def OnQuit(self, e):
		self.Close()

	def OnCredit(self, e):
		wx.MessageBox("The classroom generator created by Jakub Wasielak and Modesta Wis.", 'Exit', 
			wx.OK | wx.ICON_INFORMATION)
			
	def NewItem(self, event):
		text = wx.GetTextFromUser('Enter a new item\nFor subject insert: s <subject name> <number of hours per class>\nFor teacher insert: t <teacher name> <subject>', 'Insert dialog')
		if text != '':
			self.listbox.Append(text)
			
	def OnRename(self, event):
		sel = self.listbox.GetSelection()
		text = self.listbox.GetString(sel)
		renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)
		if renamed != '':
			self.listbox.Delete(sel)
			self.listbox.Insert(renamed, sel)
			
	def OnDelete(self, event):
		sel = self.listbox.GetSelection()
		if sel != -1:
			self.listbox.Delete(sel)
			
	def OnClear(self, event):
		self.listbox.Clear()
		
	def OnLoad(self, event):
		list_of_elems = self.listbox.GetStrings()
		
		subject_list = []
		teacher_list = []
		for elem in list_of_elems:
			if elem.split(" ")[0] == "s":
				subject_list.append([elem.split(" ")[1], int(elem.split(" ")[2])])
			else:
				teacher_list.append([elem.split(" ")[1], elem.split(" ")[2]])
			
		self.classroom_instance.subject_list = subject_list
		self.classroom_instance.teacher_list = teacher_list
		
	def OnReset(self, event):
		subject_list = (('math', 5), ('eng', 5), ('chem', 1), ('geo', 2), ('phis', 2), ('PE', 2), ('art', 1), ('hist', 2))
		teacher_list = (("Ann", "math"), ("Bert", "math"), ("Chris", "math"), ("Daniel", "eng"), ("Eustache", "eng"), ("Filip", "eng"), 
				("Goudy", "eng"), ("Hubert", "chem"), ("Ivone", "geo"), ("Jonas", "phis"), ("Kevin", "PE"), ("Louis", "art"),
				("Monica", "hist"))
		self.classroom_instance.subject_list = subject_list
		self.classroom_instance.teacher_list = teacher_list
		
		
def main():
    
    ex = wx.App()
    Example(None, size=(1300, 500), title="GEN_class")
    ex.MainLoop()    


if __name__ == '__main__':
    main()