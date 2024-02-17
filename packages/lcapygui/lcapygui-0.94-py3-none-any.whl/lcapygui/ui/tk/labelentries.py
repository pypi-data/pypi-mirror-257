from tkinter import StringVar, Label, Entry, OptionMenu
from tkinter.ttk import Checkbutton


class LabelEntry:

    def __init__(self, name, text, default, options=None,
                 command=None, **kwargs):

        self.name = name
        self.text = text
        if default is None:
            default = 'None'
        self.default = default
        self.cls = default.__class__
        self.options = options
        self.command = command
        # width, etc.
        self.kwargs = kwargs


class LabelEntries(dict):

    def __init__(self, window, ui, entries):

        self.row = 0
        self.ui = ui

        for labelentry in entries:

            var = StringVar(window)
            var.set(labelentry.default)
            self[labelentry.name] = (var, labelentry.cls)

            label = Label(window, text=labelentry.text + ': ', anchor='w')
            if isinstance(labelentry.options, (tuple, list)):
                entry = OptionMenu(
                    window, var, *labelentry.options,
                    command=labelentry.command)
            else:
                if isinstance(labelentry.default, bool):
                    entry = Checkbutton(
                        window, variable=var, command=labelentry.command)
                else:
                    entry = Entry(window, textvariable=var,
                                  **labelentry.kwargs)

                    # if labelentry.command:
                    #    var.trace_add('write', labelentry.command)
                    if labelentry.command:
                        entry.bind('<Return>', labelentry.command)

            label.grid(row=self.row, sticky='w')
            entry.grid(row=self.row, column=1, sticky='w')

            self.row += 1

    def get_var(self, name):

        return self[name][0]

    def get_cls(self, name):

        return self[name][1]

    def get_text(self, name):

        val = self.get_var(name).get()
        if val == 'None':
            val = None
        return val

    def get(self, name):

        val = self.get_text(name)
        if val is None:
            return val

        cls = self.get_cls(name)

        if cls is bool:
            val = {'1': True, '0': False}[val]

        try:
            return cls(val)
        except Exception:
            self.ui.show_error_dialog('Invalid value %s for %s' % (val, name))
