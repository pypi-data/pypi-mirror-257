# eSCAPyDL - a Deep Learning Side-Channel Analysis Python Framework
# Copyright (C) 2023  Weissbart Léo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os,sys
import argparse
import time
import signal
import shlex
import subprocess
import webbrowser
import gi
import json
import logging
import re
logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import fcntl

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from datasets.to_json import to_json

gi.require_version("Gtk", "4.0")
gi.require_version('GtkSource', '5')
gi.require_version('Adw', '1')
gi.require_version('Gdk', '4.0')
from gi.repository import GLib, Gtk, GtkSource, Adw, Gio, Gdk

class gtkFileMonitorWindow(Gtk.ScrolledWindow):
    def __init__(self, file_path):
        super().__init__()
        self.set_vexpand(True)
        self.file_path = file_path
        #open the file
        file = Gio.File.new_for_path(file_path)
        self.file_monitor = file.monitor_file(Gio.FileMonitorFlags.NONE, None)
        self.file_monitor.connect("changed", self.file_changed)
        
        # Create a text view to show the file content
        self.textview = GtkSource.View()
        self.set_child(self.textview)
        self.textview.buffer = GtkSource.Buffer()
        self.textview.set_editable(False)
        self.textview.set_buffer(self.textview.buffer)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_resource("/org/gnome/escapydl/themes/dark-theme.css")
        self.textview.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.log_linter()
    
    def log_linter(self):
        # Create a simple linter for log files
        # Create tags for various elements
        self.textview.numeric = self.textview.buffer.create_tag("numeric", foreground="#4b6cd0")
        self.textview.logging = self.textview.buffer.create_tag("logging", foreground="#50fa7b")
        self.textview.filepath = self.textview.buffer.create_tag("filepath", foreground="#d97c1a")
        # Connect the buffer's "changed" signal to update the linter
        self.textview.buffer.connect("changed", self.update_linter)
    
    def update_linter(self, buffer):
        # Clear all existing tags
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())
        # Get the current text from the buffer
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        # Apply tags for file path
        for match in re.finditer(r"\"[^\s]+\"", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.filepath, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
        # Apply tags for numeric
        for match in re.finditer(r"\b\d+\.*\d*\b", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.numeric, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
        # Apply tags for logging Does not contain a tag but only timestamp
        for match in re.finditer(r"\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.logging, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))

    def file_changed(self, file_monitor, file, other_file, event_type):
        # This function is called when the file is modified
        # Get the difference between the new text and the old text and write it to the textview
        new_text = file.load_contents(None)[1].decode()
        old_text = self.textview.buffer.get_text(self.textview.buffer.get_start_iter(), self.textview.buffer.get_end_iter(), False)
        new_text = new_text[len(old_text):]
        if new_text != "":
            self.textview.buffer.insert(self.textview.buffer.get_end_iter(), new_text)
            end_mark = self.textview.buffer.create_mark(None, self.textview.buffer.get_end_iter(), True)
            self.textview.scroll_to_mark(end_mark, 0, False, 0, 0)

class gtkPipeMonitorWindow(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.sub_proc = None
        self.set_vexpand(True)

        # Set a sticky flag to keep the scroll at the bottom
        self.sticky = True
        self.prev_value_vposition = 0
        self.vadjustment = self.get_vadjustment()
        self.vadjustment.connect("value-changed", self.on_scroll_child)
        
        # Create a text view to show the file content
        self.textview = GtkSource.View()
        self.set_child(self.textview)
        self.textview.buffer = GtkSource.Buffer()
        self.textview.set_editable(False)
        self.textview.set_buffer(self.textview.buffer)
        self.textview.textiter = self.textview.buffer.get_end_iter()

        self.is_progress = False

        style_provider = Gtk.CssProvider()
        style_provider.load_from_resource("/org/gnome/escapydl/themes/dark-theme.css")
        self.textview.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.log_linter()


    def on_scroll_child(self, adjustment):
        # If the user scrolls up, disable sticky, enable if the user scrolls down to bottom
        current_value = adjustment.get_value()
        if current_value < self.prev_value_vposition:
            self.sticky = False
        elif current_value > self.prev_value_vposition and adjustment.get_value() == adjustment.get_upper() - adjustment.get_page_size():
            self.sticky = True
        self.prev_value_vposition = current_value

    def non_block_read(self, output):
        ''' even in a thread, a normal read with block until the buffer is full '''
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read().decode("utf-8")
        except:
            return ''

    def update_terminal(self):
        self.textview.textiter = self.textview.buffer.get_end_iter()
        new_text = self.non_block_read(self.sub_proc.stdout)
        # logger.debug(repr(new_text))
        if new_text.endswith('\\r\n'): # nasty trick to show progressbar
            new_text = new_text.split('\n')[-2][:-2]+'\n'
            self.textview.textiter.backward_line()
            self.textview.buffer.delete(self.textview.textiter,self.textview.buffer.get_end_iter())
        self.textview.buffer.insert(self.textview.textiter, new_text)
        self.textview.textiter = self.textview.buffer.get_end_iter()
        if self.sticky:
            self.vadjustment.set_value(self.vadjustment.get_upper() - self.vadjustment.get_page_size())
        return self.sub_proc.poll() is None
    
    def attach_sub_proc(self, sub_proc):
        self.sub_proc = sub_proc
        GLib.timeout_add(100, self.update_terminal)
        logger.debug("Sub process attached to monitor window")

    def log_linter(self):
        # Create a simple linter for log files
        # Create tags for various elements
        self.textview.numeric = self.textview.buffer.create_tag("numeric", foreground="#4b6cd0")
        self.textview.logging = self.textview.buffer.create_tag("logging", foreground="#50fa7b")
        self.textview.filepath = self.textview.buffer.create_tag("filepath", foreground="#d97c1a")
        # Connect the buffer's "changed" signal to update the linter
        self.textview.buffer.connect("changed", self.update_linter)
    
    def update_linter(self, buffer):
        # Clear all existing tags
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())
        # Get the current text from the buffer
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        # Apply tags for file path
        for match in re.finditer(r"\"[^\s]+\"", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.filepath, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
        # Apply tags for numeric
        for match in re.finditer(r"\b\d+\.*\d*\b", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.numeric, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
        # Apply tags for logging Does not contain a tag but only timestamp
        for match in re.finditer(r"\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.logging, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))

class gtkGridbox(Gtk.Grid):
    def __init__(self):
        super().__init__()
        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_column_spacing(6)
        self.set_row_spacing(6)

class gtkAddRemoveGridbox(gtkGridbox):
    def __init__(self, add_button_function, remove_button_function):
        super().__init__()
        addlayerbutton = Gtk.Button.new_with_label("+")
        addlayerbutton.connect("clicked", add_button_function)
        self.attach(addlayerbutton, 0, 0, 1, 1)
        rmlayerbutton = Gtk.Button.new_with_label("-")
        rmlayerbutton.connect("clicked", remove_button_function)
        self.attach(rmlayerbutton, 1, 0, 1, 1)

class gtkComboText_with_items(Gtk.ComboBoxText):
    def __init__(self, items, set_active=0):
        super().__init__()
        for item in items:
            self.append_text(item)
        if set_active != None:
            self.set_active(set_active)

class gtkCodebox(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_size_request(-1, 150)
        self.set_margin_start(5)
        self.set_margin_end(5)
        
        self.textview = GtkSource.View()
        self.set_child(self.textview)
        self.textview.set_auto_indent(True)
        self.textview.set_indent_width(4)
        self.textview.set_accepts_tab(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_resource("/org/gnome/escapydl/themes/dark-theme.css")
        self.textview.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Set up the source buffer for the text view
        self.textview.buffer = GtkSource.Buffer()
        self.textview.set_buffer(self.textview.buffer)
        self.python_linter()
    
    def python_linter(self):
        # Create a simple linter for Python code

        # Create a language manager and set the language to Python
        lang_manager = GtkSource.LanguageManager()
        lang = lang_manager.get_language("python")
        self.textview.buffer.set_language(lang)

        # Create tags for various elements
        self.textview.function_tag = self.textview.buffer.create_tag("function", foreground="#E0BA30")#yellow
        self.textview.variable_tag = self.textview.buffer.create_tag("variable", foreground="#2F7AE3")#blue
        self.textview.package_tag = self.textview.buffer.create_tag("type", foreground="#2F7AE3")#blue
        self.textview.subpackage_tag = self.textview.buffer.create_tag("subpackage", foreground="#2F7AE3")#blue
        self.textview.subsubpackage_tag = self.textview.buffer.create_tag("subsubpackage", foreground="#2F7AE3")#blue
        self.textview.string_tag = self.textview.buffer.create_tag("string", foreground="#d97c1a")#orange
        # Connect the buffer's "changed" signal to update the linter
        self.textview.buffer.connect("changed", self.update_linter)
    
    def update_linter(self, buffer):
        # Clear all existing tags
        buffer.remove_all_tags(buffer.get_start_iter(), buffer.get_end_iter())
        # Get the current text from the buffer
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        # Apply tags for functions
        for match in re.finditer(r"def\s+([a-zA-Z_]\w*)\((.*)\)\:", text):
            start, end = match.span(1)
            buffer.apply_tag(self.textview.function_tag, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
            arguments_text = match.group(2)
            arguments_start = match.start(2)
            for arg in re.finditer(r"\b\w+\b", arguments_text): 
                start, end = arg.span(0)
                buffer.apply_tag(self.textview.variable_tag, buffer.get_iter_at_offset(arguments_start+start), buffer.get_iter_at_offset(arguments_start+end))
        # Apply tags for package names (up to three sub elements)
        for match in re.finditer(r"(\w+)\.(\w+)\.?(\w+)?", text):
            start, end = match.span(1)
            buffer.apply_tag(self.textview.package_tag, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
            if match.span(2) != (0,0):
                start, end = match.span(2)
                buffer.apply_tag(self.textview.subpackage_tag, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
            if match.span(3) != (-1,-1):
                start, end = match.span(3)
                buffer.apply_tag(self.textview.subsubpackage_tag, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))
        # Apply tags for any string
        for match in re.finditer(r"[\'\"]\w+?[\'\"]", text):
            start, end = match.span(0)
            buffer.apply_tag(self.textview.string_tag, buffer.get_iter_at_offset(start), buffer.get_iter_at_offset(end))

class gtkVerticalBox(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

class gtkResizableEntry(Gtk.Entry):
    def __init__(self,label=None):
        super().__init__()
        if label != None:
            self.set_buffer(Gtk.EntryBuffer.new(label,-1))
        self.connect("changed", self.on_entry_changed)
    
    def on_entry_changed(self,widget):
        self.set_width_chars(len(self.get_text()))

class gtkHorizontalBox(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

class gtkLabelLeftAlign(Gtk.Label):
    def __init__(self, label):
        super().__init__(label=label)
        self.set_halign(Gtk.Align.START)

class gtkLabelWithTooltip(Gtk.Grid):
    #Makes a grid containing a label and an interogation mark icon next to it with a tooltip
    def __init__(self, label, tooltip):
        super().__init__()
        self.set_column_spacing(6)
        self.set_row_spacing(6)
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.CENTER)
        self.label = Gtk.Label(label=label)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_valign(Gtk.Align.CENTER)
        self.attach(self.label, 0, 0, 1, 1)
        self.icon = Gtk.Image.new_from_icon_name("info-symbolic")
        self.icon.set_halign(Gtk.Align.START)
        self.icon.set_valign(Gtk.Align.CENTER)
        self.attach(self.icon, 1, 0, 1, 1)
        self.icon.set_tooltip_text(tooltip)

    def get_buffer(self):
        return self.label.get_buffer()

class gtkButtonFileSelection(Gtk.Button):
    def __init__(self, entry, file_path=None):
        super().__init__()
        self.set_halign(Gtk.Align.START)
        self.set_valign(Gtk.Align.CENTER)
        self.set_icon_name("document-open-symbolic")
        self.connect("clicked", self.on_file_clicked)
        self.file_path = file_path
        self.entry = entry
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_resource("/org/gnome/escapydl/themes/dark-theme.css")

    def set_file_path(self, file_path):
        self.file_path = file_path
    
    def on_file_clicked(self, widget):
        self.window = Gtk.Window(title="Select file")
        self.window.set_icon_name("escapydl-icon")
        self.window.set_default_size(900, 600)
        content = gtkVerticalBox()
        self.dialog = Gtk.FileChooserWidget.new(0)
        self.dialog.set_current_folder(Gio.File.parse_name(os.getcwd()))
        self.dialog.set_vexpand(True)
        content.append(self.dialog)
        buttons = Gtk.HeaderBar.new()
        buttons.set_show_title_buttons(False)
        # buttons.append(Gtk.Box(hexpand=True))
        select_button = Gtk.Button.new_with_label("Select")
        select_button.get_style_context().add_provider(self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        select_button.set_name("button_green")
        select_button.connect("clicked", self.select_button_clicked)
        buttons.pack_end(select_button)
        cancel_button = Gtk.Button.new_with_label("Cancel")
        cancel_button.connect("clicked", lambda x: self.window.close())
        buttons.pack_start(cancel_button)
        # content.append(buttons)
        self.window.set_titlebar(buttons)
        self.window.set_child(content)
        self.window.present()

    def select_button_clicked(self, widget):
        self.file_path = self.dialog.get_file().get_path()
        self.entry.set_buffer(Gtk.EntryBuffer(text=self.file_path))
        self.entry.on_entry_changed(self.entry)
        logger.debug("File selected: " + self.file_path)

        self.window.close()

class eSCAPyDLgui(Gtk.Application):
    def __init__(self, timestamp=time.strftime("%Y%m%d_%H%M%S",time.localtime()), log_filename='', verbose=0):
        super().__init__(application_id="org.gnome.escapydl")
        self.timestamp = timestamp
        self.log_filename = log_filename
        self.verbose = verbose
        GLib.set_application_name("eSCAPyDL")
        self.style_manager = Adw.StyleManager().get_default()
        self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

        # Create an icon theme with local icons for better transferability
        resource_filename = os.path.join(os.path.dirname(__file__), "resources/resource.gresource")
        resource = Gio.Resource.load(resource_filename)
        Gio.resources_register(resource)
        self.icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.icon_theme.add_resource_path("/org/gnome/escapydl/icons")
        
        self.window = None
        self.outerbox = Gtk.Box(spacing=6)
        self.dataset = None
        self.study_name = ""

        self.template_models = ["Specific Model", "MLP", "CNN", "ASCAD_mlp", "ASCAD_cnn"]
        self.json_data = {}
        self.parameter_fields = ['dataset_name', 'dataset_size', 'training_size', 'val_size', 'subkey', 'num_key_hypotheses', 'n_samples', 'shuffle']
        self.parameter_fields_wval = ['dataset_name', 'validation_name', 'dataset_size', 'training_size', 'val_size', 'subkey', 'num_key_hypotheses', 'n_samples', 'shuffle']
        self.callbacks_fileds = ['ModelCheckpoint', 'Tensorboard', 'GuessingEntropy']
        self.functions_fields = ['get_attack_parameters', 'get_known_key', 'intermediate_value']
        self.script_action = 'train'
        self.modeltype = None
        self.mlp_parameters = ['num_epochs', 'bs', 'loss_function', 'lr', 'activation_function', 'pooling', 'optimizer', 'weight_init']
        self.cnn_parameters = ['num_epochs', 'bs', 'loss_function', 'lr', 'activation_function', 'pooling', 'optimizer', 'weight_init']
        self.n_conv_block = 0
        self.optuna_database_name = "sqlite:///cnn_sca.db"

    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title="eSCAPyDL",default_width=800, default_height=600)
        self.window.set_icon_name("escapydl-icon")
        self.window.connect("close-request", self.on_button_close_clicked)
        self.to_first_window(self)

    def add_navigation_bar(self, prev_action, next_action,fill_gap=True):
        if fill_gap:
            #Fill with empty box
            dbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=6)
            dbox.set_vexpand(True)
            self.outerbox.append(dbox)
        # Add previous/next button on the bottom of the window
        bbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=6)
        pbutton = Gtk.Button.new_with_label("Previous")
        pbutton.set_halign(Gtk.Align.START)
        pbutton.connect("clicked", prev_action)
        bbox.append(pbutton)
        fillbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=6)
        fillbox.set_hexpand(True)
        bbox.append(fillbox)
        nbutton = Gtk.Button.new_with_label("Next")
        nbutton.set_halign(Gtk.Align.END)
        nbutton.connect("clicked", next_action)
        bbox.append(nbutton)
        # bbox.set_baseline_position(Gtk.BaselinePosition.BOTTOM)
        self.outerbox.append(bbox)

    def on_button_clicked(self, widget):
        logger.info("Hello World")

    def on_button_validationdataset_clicked(self, button):
        if button.get_active():
            self.use_validation_dataset = False
            #Remove the line below
            self.paramgridbox.remove_row(button.row_index+1)
        else:
            self.use_validation_dataset = True
            #Add a newline in paramGridBox and create a field for validation dataset name
            self.paramgridbox.insert_row(button.row_index+1)
            self.paramgridbox.attach(gtkLabelLeftAlign(label="validation_name: "), 0, button.row_index+1, 1, 1)
            entryval = gtkResizableEntry(self.json_data['parameters']['validation_name'] if 'validation_name' in self.json_data['parameters'].keys() else "")
            self.paramgridbox.attach(entryval, 1, button.row_index+1, 1, 1)
            self.paramgridbox.attach(gtkButtonFileSelection(entry=entryval), 2, button.row_index+1, 1, 1)

    def on_button_close_clicked(self, widget):
        logger.debug("Closing window")
        try:
            logger.debug("Killing child process {}".format(self.child_process.pid))
            self.child_process.send_signal(signal.SIGINT)
        except AttributeError as e:
            logger.debug("No child process started")
        try:
            logger.debug("Killing tensorboard child process {}".format(self.tb_child_process.pid))
            self.tb_child_process.send_signal(signal.SIGINT)
        except AttributeError as e:
            logger.debug("No tensorboard child process started")
        try:
            logger.debug("Killing optuna child process {}".format(self.optuna_child_process.pid))
            self.optuna_child_process.send_signal(signal.SIGINT)
        except AttributeError as e:
            logger.debug("No optuna child process started")
        self.window.close()

    def on_button_tensorboarb_clicked(self, widget):
        command = "tensorboard --logdir=runs"
        logger.debug("Starting tensorboard")
        try:
            if not hasattr(self, "tb_child_process") or self.tb_child_process.poll() is not None:
                self.tb_child_process = subprocess.Popen(shlex.split(command))
                logger.debug("Tensorboard child process created, id:{}".format(self.tb_child_process.pid))
            else:
                logger.debug("Tensorboard child process already running, id:{}".format(self.tb_child_process.pid))
            time.sleep(1)
            webbrowser.open_new("http://localhost:6006/?runFilter={}".format(self.study_name))
        except Exception as e:
            logger.warning(e)

    def on_button_optuna_dashboard_clicked(self, widget):
        if os.path.isfile(os.path.join(os.getcwd(),self.optuna_database_name[10:])):
            command = "optuna-dashboard {} --port 2021".format(self.optuna_database_name)
            logger.debug("Starting optuna dashboard")
            try:
                if not hasattr(self, "optuna_child_process") or self.optuna_child_process.poll() is not None:
                    self.optuna_child_process = subprocess.Popen(shlex.split(command))
                    logger.debug("Optuna dashboard child process created, id:{}".format(self.optuna_child_process.pid))
                else:
                    logger.debug("Optuna dashboard child process already running, id:{}".format(self.optuna_child_process.pid))
                time.sleep(1)
                webbrowser.open_new("http://localhost:2021")
            except Exception as e:
                logger.warning(e)
        else:
            logger.warning("Optuna database not found: {}".format(os.path.join(os.getcwd(),self.optuna_database_name[10:])))

    def on_button_run_script_clicked(self, widget):
        logger.debug("Run script")
        self.output_window.textview.buffer.set_text("")
        self.timestamp=time.strftime("%Y%m%d_%H%M%S",time.localtime())#refresh timestamp
        self.study_name = "{}/{}/{}".format(self.dataset.lower(),self.modeltype,self.timestamp)
        main_py_filename = os.path.join(os.path.dirname(__file__), "main.py")
        command = sys.executable + " {} --{} -d {} -m {} -j {} -s{} -a {} -l '{}'".format(main_py_filename, self.script_action, str.lower(self.dataset), self.modeltype, self.json_filename, self.study_name, self.timestamp, self.log_filename)
        if self.verbose > 0:
            command += " -v"
        logger.debug("Command: {}".format(command))
        try:
            self.child_process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            logger.debug("Child process created, id:{}".format(self.child_process.pid))
            self.output_window.attach_sub_proc(self.child_process)
            widget.set_sensitive(False)
        except Exception as e:
            logger.warning(e)

    def on_button_stop_script_clicked(self, widget):
        logger.debug("Stop script")
        if hasattr(self, "child_process") and isinstance(self.child_process, subprocess.Popen):
            logger.debug("Child process killed, id:{}".format(self.child_process.pid))
            self.child_process.send_signal(signal.SIGINT)
            if self.child_process.poll() is not None:
                self.child_process = None
            widget.get_parent().get_first_child().set_sensitive(True)#Set run button sensitive again
        try:
            logger.debug("Killing tensorboard child process {}".format(self.tb_child_process.pid))
            self.tb_child_process.send_signal(signal.SIGINT)
        except AttributeError as e:
            logger.debug("No tensorboard child process started")
        try:
            logger.debug("Killing optuna-dashboard child process {}".format(self.optuna_child_process.pid))
            self.optuna_child_process.send_signal(signal.SIGINT)
        except AttributeError as e:
            logger.debug("No tensorboard child process started")

    def on_button_trainopt_clicked(self, button):
        if button.get_label().lower() == "train":
            self.script_action = 'train'
            logger.debug("Train button is active")
        elif button.get_label().lower() == "optimize":
            self.script_action = 'optimize'
            logger.debug("Optimize button is active")
        self.refresh_listbox_content()
    
    def on_button_addlayer_clicked(self, widget):
        #insert a new row in the gridbox
        self.mlp_layers_box.insert_row(self.json_data['model']['n_layers'])
        self.mlp_layers_box.attach(Gtk.Label(label="Layer {}".format(self.json_data['model']['n_layers']+1)), 0, self.json_data['model']['n_layers'], 1, 1)
        previous_layer_text = self.mlp_layers_box.get_child_at(1,self.json_data['model']['n_layers']-1).get_text()
        self.mlp_layers_box.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(previous_layer_text,-1)), 1, self.json_data['model']['n_layers'], 1, 1)
        self.json_data['model']['n_layers'] += 1

    def on_button_removelayer_clicked(self, widget):
        if self.json_data['model']['n_layers'] > 1:
            self.mlp_layers_box.remove_row(self.json_data['model']['n_layers']-1)
            self.json_data['model']['n_layers'] -= 1

    def on_button_addconv_clicked(self, widget):
        #insert a new row in the gridbox
        self.n_conv_block += 1
        self.cnn_block_box.insert_row(self.n_conv_block)
        self.cnn_block_box.attach(Gtk.Label(label="Conv {}".format(self.n_conv_block)), 0, self.n_conv_block, 1, 1)
        previous_layer_text1 = self.cnn_block_box.get_child_at(1,self.n_conv_block-1).get_text()
        self.cnn_block_box.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(previous_layer_text1,-1)), 1, self.n_conv_block, 1, 1)
        previous_layer_text2 = self.cnn_block_box.get_child_at(2,self.n_conv_block-1).get_text()
        self.cnn_block_box.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(previous_layer_text2,-1)), 2, self.n_conv_block, 1, 1)

    def on_button_removeconv_clicked(self, widget):
        if self.n_conv_block > 1:
            self.cnn_block_box.remove_row(self.n_conv_block)
            self.n_conv_block -= 1

    def on_callback_selected(self, widget):
        logger.debug("Callback selected: {}".format(widget.get_active_text()))
        if widget.get_active_text().lower() not in self.json_data["callbacks"]:
            self.json_data["callbacks"][widget.get_active_text().lower()] = {}
        if widget.get_active_text().lower() == "modelcheckpoint":
            self.json_data["callbacks"][widget.get_active_text().lower()] = {**{'period':'-1'}, **self.json_data["callbacks"][widget.get_active_text().lower()]}
        elif widget.get_active_text().lower() == "tensorboard":
            self.json_data["callbacks"][widget.get_active_text().lower()] = {**{'training_accuracy':'True', 'training_loss':'True', 'validation_accuracy':'True', 'validation_loss':'True'}, **self.json_data["callbacks"][widget.get_active_text().lower()]}
        elif widget.get_active_text().lower() == "guessingentropy":
            self.json_data["callbacks"][widget.get_active_text().lower()] = {**{'ge_rate':'5', 'r':'0.6', 'n_repeat':'5'}, **self.json_data["callbacks"][widget.get_active_text().lower()]}
        self.update_gridbox_callback(callback_key=widget.get_active_text().lower(), left_gridbox=widget)

    def update_gridbox_callback(self, callback_key, left_gridbox):
        parent_gridbox = left_gridbox.get_parent()
        position = parent_gridbox.query_child(left_gridbox)
        destroy_child = parent_gridbox.get_child_at(position[0]+1, position[1])
        if destroy_child != None:
            parent_gridbox.remove(destroy_child)
        gridbox = gtkGridbox()
        parent_gridbox.attach_next_to(gridbox, left_gridbox, Gtk.PositionType.RIGHT, 1, 1)
        try:
            callback_key = callback_key.lower()
            logger.debug(self.json_data["callbacks"][callback_key])
            for i,p in enumerate(self.json_data["callbacks"][callback_key]):
                gridbox.attach(gtkLabelLeftAlign(label=p), 0, i, 1, 1)
                if self.json_data["callbacks"][callback_key][p] == "True" or self.json_data["callbacks"][callback_key][p] == "False":
                    gridbox.attach(gtkComboText_with_items(["False", "True"], set_active=int(self.json_data["callbacks"][callback_key][p]=="True")), 1, i, 1, 1)
                else:
                    gridbox.attach(gtkResizableEntry(label=self.json_data["callbacks"][callback_key][p]), 1, i, 1, 1)
        except Exception as e:
            logger.debug("Got {}\nError setting callback fields".format(e))

    def on_button_addcallback_clicked(self, widget):
        #insert a new row in the gridbox
        self.callbackbox.insert_row(self.n_callbacks)
        callbackcombo = gtkComboText_with_items(self.callbacks_fileds, set_active=None)
        callbackcombo.connect('changed', self.on_callback_selected)
        self.callbackbox.attach(callbackcombo, 0, self.n_callbacks, 1, 1)
        self.n_callbacks += 1

    def on_button_removecallback_clicked(self, widget):
        if self.n_callbacks > 0:
            self.callbackbox.remove_row(self.n_callbacks-1)
            self.n_callbacks -= 1

    def refresh_listbox_content(self):
        #Remove all Grid elements
        while self.listbox.get_first_child() is not None:
            self.listbox.remove(self.listbox.get_first_child())
        #Add new child boxes
        modelbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=6)
        modelbox.append(gtkLabelLeftAlign(label="Model: "))
        if self.trainbutton.get_active():
            modelcombo = gtkComboText_with_items(self.template_models, set_active=None)
            modelcombo.connect('changed', self.on_model_selected)
            modelbox.append(modelcombo)
            self.listbox.append(modelbox)
            modelcombo.set_active(0)
        elif self.optbutton.get_active():
            modelcombo = gtkComboText_with_items(["MLP", "CNN"], set_active=None)
            modelcombo.connect('changed', self.on_optimize_model_selected)
            modelbox.append(modelcombo)
            self.listbox.append(modelbox)
            modelcombo.set_active(["make_MLP", "make_CNN"].index(self.json_data['hp_search_s']['model_type']) if 'model_type' in self.json_data['hp_search_s'].keys() else 0)
    
    def on_dataset_selected(self, widget):
        logger.debug("Dataset selected: {}".format(widget.get_active_text()))
        self.dataset = widget.get_active_text()
        self.update_gridbox_pyfile(widget.get_parent())

    def on_model_selected(self, widget):
        logger.debug("Model selected: {}".format(widget.get_active_text()))
        
        if "model" not in self.json_data.keys():
            self.json_data['model'] = {}
        if "model_type" in self.json_data['model'].keys():
            try:
                self.json_data['model']["model_type"] = eval(self.json_data['model']["model_type"])
            except Exception as e:
                pass
        if "loss_function" in self.json_data['model'].keys():
            if "crossentropy" in self.json_data['model']["loss_function"].lower():
                self.json_data['model']["loss_function"] = "CrossEntropy"
            elif "mse" in self.json_data['model']["loss_function"].lower():
                self.json_data['model']["loss_function"] = "MSE"
            else:
                self.json_data['model']["loss_function"] = "CrossEntropy"
        if widget.get_active_text() == 'Specific Model':
            self.json_data['model'] = {**{"model_type":"MLP", 
                                        "num_epochs":"100",
                                        "bs":"128",
                                        "loss_function":"CrossEntropy",
                                        "n_layers":1, 
                                        "n_units_l0":"100", 
                                        "activation_function":"ReLu", 
                                        "lr":"0.001", 
                                        "pooling":"Average", 
                                        "optimizer":"Adam", 
                                        "weight_init":"He_uniform"},**self.json_data['model']}
            self.modeltype = self.json_data['model']["model_type"]
        elif widget.get_active_text() == 'MLP':
            self.modeltype = 'MLP'
            self.json_data['model']["model_type"] = "MLP"
            #set default parameters
            self.json_data['model'] = {"model_type":"MLP", 
                                        "num_epochs":"100",
                                        "bs":"128",
                                        "loss_function":"CrossEntropy",
                                        "n_layers":1, 
                                        "n_units_l0":"100", 
                                        "activation_function":"ReLu", 
                                        "lr":"0.001", 
                                        "pooling":"Average", 
                                        "optimizer":"Adam", 
                                        "weight_init":"He_uniform"}
        elif widget.get_active_text() == 'ASCAD_mlp':
            self.modeltype = 'MLP'
            #set default parameters
            self.json_data['model'] = {"model_type":"MLP", 
                                        "num_epochs":"100",
                                        "bs":"128",
                                        "loss_function":"CrossEntropy",
                                        "n_layers":5, 
                                        "n_units_l0":"200",
                                        "n_units_l1":"200",
                                        "n_units_l2":"200",
                                        "n_units_l3":"200", 
                                        "n_units_l4":"200",
                                        "activation_function":"ReLu", 
                                        "lr":"0.00001", 
                                        "pooling":"Average", 
                                        "optimizer":"Adam", 
                                        "weight_init":"He_uniform"}
        elif widget.get_active_text() == 'CNN':
            self.modeltype = 'CNN'
            #set default parameters
            self.json_data['model'] = {"model_type":"CNN", 
                                        "num_epochs":"100",
                                        "bs":"128",
                                        "loss_function":"CrossEntropy",
                                        "n_conv_block":2,
                                        "kernel_size_0":"8",
                                        "c_out_0":"3",
                                        "kernel_size_1":"8",
                                        "c_out_1":"3",
                                        "n_layers":2, 
                                        "n_units_l0":"100",
                                        "n_units_l1":"100",
                                        "activation_function":"ReLu", 
                                        "lr":"0.00001", 
                                        "pooling":"Average", 
                                        "optimizer":"Adam", 
                                        "weight_init":"He_uniform"}
        elif widget.get_active_text() == 'ASCAD_cnn':
            self.modeltype = 'CNN'
            #set default parameters
            self.json_data['model'] = {"model_type":"CNN", 
                                        "num_epochs":"100",
                                        "bs":"128",
                                        "loss_function":"CrossEntropy",
                                        "n_conv_block":5,
                                        "kernel_size_0":"11",
                                        "c_out_0":"64",
                                        "kernel_size_1":"11",
                                        "c_out_1":"128",
                                        "kernel_size_2":"11",
                                        "c_out_2":"256",
                                        "kernel_size_3":"11",
                                        "c_out_3":"512",
                                        "kernel_size_4":"11",
                                        "c_out_4":"512",
                                        "n_layers":2, 
                                        "n_units_l0":"4096",
                                        "n_units_l1":"4096",
                                        "activation_function":"ReLu", 
                                        "lr":"0.001", 
                                        "pooling":"Average", 
                                        "optimizer":"RMSprop", 
                                        "weight_init":"He_uniform"}

        #Remove all child boxes related to model parameters if any
        while len(self.listbox.observe_children()) > 1:
            self.listbox.remove(self.listbox.get_last_child())
        #Add new child boxes related to model parameters
        self.model_parambox = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=6)
        self.layerbox = gtkGridbox()
        #cnn parameters
        lcol = 0
        lrow = 0
        self.n_conv_block = int(self.json_data['model']["n_conv_block"]) if "n_conv_block" in self.json_data['model'].keys() else 0
        if self.n_conv_block > 0:
            self.cnn_block_box = gtkGridbox()
            row = 0
            self.cnn_block_box.attach(Gtk.Label(label="kernel_size"), 1, row, 1, 1)
            self.cnn_block_box.attach(Gtk.Label(label="output_size"), 2, row, 1, 1)
            row += 1
            for i in range(self.n_conv_block):
                self.cnn_block_box.attach(Gtk.Label(label="Conv {}".format(row)), 0, row, 1, 1)
                self.cnn_block_box.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(self.json_data['model']["kernel_size_{}".format(i)],-1)), 1, row, 1, 1)
                self.cnn_block_box.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(self.json_data['model']["c_out_{}".format(i)],-1)), 2, row, 1, 1)
                row += 1
            ad_remove_gridbox = gtkAddRemoveGridbox(self.on_button_addconv_clicked, self.on_button_removeconv_clicked)
            self.cnn_block_box.attach(ad_remove_gridbox, 0, row, 1, 1)
            self.layerbox.attach(self.cnn_block_box, lcol, lrow, 1, 1)
            lcol += 1
        #mlp parameters
        self.mlp_layers_box = gtkGridbox()
        row = 0
        self.json_data['model']['n_layers'] = int(self.json_data['model']['n_layers'])
        for i in range(self.json_data['model']['n_layers']):
            self.mlp_layers_box.attach(Gtk.Label(label="Layer {}".format(i+1)), 0, i, 1, 1)
            self.mlp_layers_box.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(self.json_data['model']["n_units_l{}".format(i)],-1)), 1, i, 1, 1)
            row += 1
        ad_remove_gridbox = gtkGridbox()
        ad_remove_gridbox = gtkAddRemoveGridbox(self.on_button_addlayer_clicked, self.on_button_removelayer_clicked)
        self.mlp_layers_box.attach(ad_remove_gridbox, 0, row, 1, 1)
        self.layerbox.attach(self.mlp_layers_box, lcol, lrow, 1, 1)
        lrow += 1
        lcol = 0
        #Other parameters
        self.hparambox = gtkGridbox()
        prow = 0
        self.hparambox.attach(gtkLabelLeftAlign(label="num_epochs"), 0, prow, 1, 1)
        self.hparambox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(self.json_data['model']['num_epochs'],-1)), 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="bs"), 0, prow, 1, 1)
        self.hparambox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(self.json_data['model']['bs'],-1)), 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="loss_function"), 0, prow, 1, 1)
        combo_button = gtkComboText_with_items(['CrossEntropy', 'MSE'], set_active=[x.lower() for x in ['CrossEntropy', 'MSE']].index(self.json_data['model']['loss_function'].lower()))
        self.hparambox.attach(combo_button, 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="lr"), 0, prow, 1, 1)
        self.hparambox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(self.json_data['model']['lr'],-1)), 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="activation_function"), 0, prow, 1, 1)
        combo_button = gtkComboText_with_items(['ReLu', 'Tanh', 'SeLu'], set_active=[x.lower() for x in ['ReLu', 'Tanh', 'SeLu']].index(self.json_data['model']['activation_function'].strip('"').strip("'").lower()))
        self.hparambox.attach(combo_button, 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="pooling"), 0, prow, 1, 1)
        combo_button = gtkComboText_with_items(['Average', 'Max'], set_active=[x.lower() for x in ['Average', 'Max']].index(self.json_data['model']['pooling'].strip('"').strip("'").lower()))
        self.hparambox.attach(combo_button, 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="optimizer"), 0, prow, 1, 1)
        combo_button = gtkComboText_with_items(['Adam', 'SGD', 'RMSprop'], set_active=[x.lower() for x in ['Adam', 'SGD', 'RMSprop']].index(self.json_data['model']['optimizer'].strip('"').strip("'").lower()))
        self.hparambox.attach(combo_button, 1, prow, 1, 1)
        prow += 1
        self.hparambox.attach(gtkLabelLeftAlign(label="weight_init"), 0, prow, 1, 1)
        combo_button = gtkComboText_with_items(['He_uniform', 'Zero'], set_active=[x.lower() for x in ['He_uniform', 'Zero']].index(self.json_data['model']['weight_init'].strip('"').strip("'").lower()))
        self.hparambox.attach(combo_button, 1, prow, 1, 1)
        self.layerbox.attach(self.hparambox, lcol, lrow, 1, 1)
        self.model_parambox.append(self.layerbox)
        self.listbox.append(self.model_parambox)
        logger.debug("json_data['model']: {}".format(self.json_data['model']))

    def on_optimize_model_selected(self, widget):
        logger.debug("Model selected: {}".format(widget.get_active_text()))

        #TODO: if hp_search_s is defined by user in dataset file, load user parameters
        #TODO: remove the unnessary parameters from json_data['hp_search_s'] if user change model type (ex: n_conv_block_s if model_type is MLP), caution, some are added inside Optuna_models.py
        #TODO: add fields for all hparameters 
        if "hp_search_s" not in self.json_data.keys():
            self.json_data['hp_search_s'] = {}
        else:
            for k in self.json_data['hp_search_s']:
                try:
                    self.json_data['hp_search_s'][k] = eval(self.json_data['hp_search_s'][k])
                except Exception as e:
                    pass
        if widget.get_active_text() == 'MLP':
            self.modeltype = 'make_MLP'
            #set default parameters
            self.json_data['hp_search_s'] = {**{"n_layers_s":[1, 5, 1],
                                        "n_neurons_s":[10, 500, 10], 
                                        "activation_function_s":["ReLu", "Tanh", "SeLu"], 
                                        "lr_s":[0.001, 0.1, "log"],
                                        "pooling":"Average", 
                                        "optimizer_s":["Adam"], 
                                        "weight_init":"He_uniform"}, **self.json_data['hp_search_s']}
            self.json_data['hp_search_s']["model_type"] = "make_MLP"
        if widget.get_active_text() == 'CNN':
            self.modeltype = 'make_CNN'
            #set default parameters
            self.json_data['hp_search_s'] = {**{"n_conv_block_s":[1, 5, 1],
                                        "kernel_size_s":[3, 10, 2],
                                        "n_layers_s":[1, 5, 1],
                                        "n_neurons_s":[10, 500, 10], 
                                        "activation_function_s":["ReLu", "Tanh", "SeLu"], 
                                        "lr_s":[0.001, 0.1, "log"],
                                        "pooling":"Average", 
                                        "optimizer_s":["Adam"], 
                                        "weight_init":"He_uniform"}, **self.json_data['hp_search_s']}
            self.json_data['hp_search_s']["model_type"] = "make_CNN"
        #Remove all child boxes related to model parameters if any
        if len(self.listbox.observe_children()) > 1:
            self.listbox.remove(self.listbox.get_last_child())
        
        #Add new child boxes related to model parameters
        self.model_parambox = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=6)
        self.layerbox = gtkGridbox()
        row = 0
        self.layerbox.attach(Gtk.Label(label="parameter"), 0, row, 1, 1)
        self.layerbox.attach(Gtk.Label(label="min"), 1, row, 1, 1)
        self.layerbox.attach(Gtk.Label(label="max"), 2, row, 1, 1)
        self.layerbox.attach(Gtk.Label(label="inc"), 3, row, 1, 1)
        row += 1
        if self.json_data['hp_search_s']['model_type'] == 'make_CNN':
            self.layerbox.attach(gtkLabelLeftAlign(label="n_conv_block"), 0, row, 1, 1)
            self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_conv_block_s"][0]),-1)), 1, row, 1, 1)
            self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_conv_block_s"][1]),-1)), 2, row, 1, 1)
            self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_conv_block_s"][2]),-1)), 3, row, 1, 1)
            row += 1
            self.layerbox.attach(gtkLabelLeftAlign(label="kernel_size"), 0, row, 1, 1)
            self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["kernel_size_s"][0]),-1)), 1, row, 1, 1)
            self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["kernel_size_s"][1]),-1)), 2, row, 1, 1)
            self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["kernel_size_s"][2]),-1)), 3, row, 1, 1)
            row += 1
        self.layerbox.attach(gtkLabelLeftAlign(label="n_layers"), 0, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_layers_s"][0]),-1)), 1, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_layers_s"][1]),-1)), 2, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_layers_s"][2]),-1)), 3, row, 1, 1)
        row += 1
        self.layerbox.attach(gtkLabelLeftAlign(label="n_neurons"), 0, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_neurons_s"][0]),-1)), 1, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_neurons_s"][1]),-1)), 2, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["n_neurons_s"][2]),-1)), 3, row, 1, 1)
        row += 1
        self.layerbox.attach(gtkLabelLeftAlign(label="lr"), 0, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["lr_s"][0]),-1)), 1, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["lr_s"][1]),-1)), 2, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(str(self.json_data['hp_search_s']["lr_s"][2]),-1)), 3, row, 1, 1)
        row += 1
        self.layerbox.attach(Gtk.Label(label="values comma separated"), 0, row, 4, 1)
        row += 1
        self.layerbox.attach(gtkLabelLeftAlign(label="activation_functions"), 0, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(",".join(self.json_data['hp_search_s']["activation_function_s"]),-1)), 1, row, 3, 1)
        row += 1
        self.layerbox.attach(gtkLabelLeftAlign(label="optimizers"), 0, row, 1, 1)
        self.layerbox.attach(Gtk.Entry.new_with_buffer(Gtk.EntryBuffer.new(",".join(self.json_data['hp_search_s']["optimizer_s"]),-1)), 1, row, 3, 1)
        self.model_parambox.append(self.layerbox)
        self.listbox.append(self.model_parambox)
        logger.debug("json_data['hp_search_s']: {}".format(self.json_data["hp_search_s"]))
            
    def save_model_parameters(self):
        if self.script_action == 'train':
            if self.modeltype == 'MLP':
                for i in range(self.json_data['model']['n_layers']):
                    self.json_data['model']['n_units_l{}'.format(i)] = self.mlp_layers_box.get_child_at(1, i).get_buffer().get_text()
                for param in self.mlp_parameters:
                    child_widget = self.hparambox.get_child_at(1, self.mlp_parameters.index(param))
                    if isinstance(child_widget, Gtk.Entry):
                        self.json_data['model'][param] = self.hparambox.get_child_at(1, self.mlp_parameters.index(param)).get_buffer().get_text()
                    elif isinstance(child_widget, Gtk.ComboBoxText):
                        self.json_data['model'][param] = self.hparambox.get_child_at(1, self.mlp_parameters.index(param)).get_active_text()
            elif self.modeltype == 'CNN':
                self.json_data['model']['n_conv_block'] = self.n_conv_block
                for i in range(self.n_conv_block):
                    self.json_data['model']['kernel_size_{}'.format(i)] = self.cnn_block_box.get_child_at(1, i+1).get_buffer().get_text()
                    self.json_data['model']['c_out_{}'.format(i)] = self.cnn_block_box.get_child_at(2, i+1).get_buffer().get_text()
                for i in range(self.json_data['model']['n_layers']):
                    self.json_data['model']['n_units_l{}'.format(i)] = self.mlp_layers_box.get_child_at(1, i).get_buffer().get_text()
                for param in self.cnn_parameters:
                    child_widget = self.hparambox.get_child_at(1, self.cnn_parameters.index(param))
                    if isinstance(child_widget, Gtk.Entry):
                        self.json_data['model'][param] = self.hparambox.get_child_at(1, self.cnn_parameters.index(param)).get_buffer().get_text()
                    elif isinstance(child_widget, Gtk.ComboBoxText):
                        self.json_data['model'][param] = self.hparambox.get_child_at(1, self.cnn_parameters.index(param)).get_active_text()
            else:
                logger.debug("Unknown model type: {}".format(self.modeltype))
            logger.debug("self.json_data['model']: {}".format(self.json_data['model']))
        elif self.script_action == 'optimize':
            if self.modeltype == 'make_MLP':
                self.json_data['hp_search_s']['n_layers_s'] = [self.layerbox.get_child_at(i, 1).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['n_neurons_s'] = [self.layerbox.get_child_at(i, 2).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['lr_s'] = [self.layerbox.get_child_at(i, 3).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['activation_function_s'] = [x for x in self.layerbox.get_child_at(1, 5).get_buffer().get_text().split(',')]
                self.json_data['hp_search_s']['optimizer_s'] = [x for x in self.layerbox.get_child_at(1, 6).get_buffer().get_text().split(',')]
            elif self.modeltype == 'make_CNN':
                self.json_data['hp_search_s']['n_conv_block_s'] = [self.layerbox.get_child_at(i, 1).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['kernel_size_s'] = [self.layerbox.get_child_at(i, 2).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['n_layers_s'] = [self.layerbox.get_child_at(i, 3).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['n_neurons_s'] = [self.layerbox.get_child_at(i, 4).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['lr_s'] = [self.layerbox.get_child_at(i, 5).get_buffer().get_text() for i in range(1,4)]
                self.json_data['hp_search_s']['activation_function_s'] = [x for x in self.layerbox.get_child_at(1, 7).get_buffer().get_text().split(',')]
                self.json_data['hp_search_s']['optimizer_s'] = [x for x in self.layerbox.get_child_at(1, 8).get_buffer().get_text().split(',')]
            else:
                logger.debug("Unknown model type: {}".format(self.modeltype))
            logger.debug("self.json_data['hp_search_s']: {}".format(self.json_data['hp_search_s']))
        logger.debug(self.script_action)
        try:
            with open(self.json_filename, 'w') as outfile:
                json.dump(self.json_data, outfile)
        except Exception as e:
            logger.debug("Error writing json file: {}".format(e))

    def update_gridbox_pyfile(self, gridbox):
        #Parse the existing python file and convert to json format that can be reused later
        ds_filename = os.path.join(os.path.dirname(__file__), "datasets/" + str.lower(self.dataset) + ".py")
        self.json_filename = os.path.join(os.getenv('LOCALAPPDATA'),"{}.json".format(str.lower(self.dataset))) if os.name == 'nt' else "/tmp/escapydl/{}.json".format(str.lower(self.dataset))
        os.makedirs(os.path.dirname(self.json_filename), exist_ok=True)
        self.json_data = {}
        try:
            self.json_data = to_json(ds_filename, self.json_filename)
            self.use_validation_dataset = True if "validation_name" in self.json_data['parameters'] else False
            logger.debug(json.dumps(self.json_data, indent=4))
            row = 1
            for p in self.json_data['parameters']:
                if p in self.parameter_fields:
                    if p == "dataset_name":
                        gridbox.get_child_at(2, row).set_file_path(self.json_data['parameters'][p])
                        try:
                            self.json_data['parameters'][p] = eval(self.json_data['parameters'][p])
                        except ValueError:
                            pass
                        if self.use_validation_dataset:
                            gridbox.get_child_at(1, row).set_buffer(Gtk.EntryBuffer(text=self.json_data['parameters'][p]))
                            gridbox.get_child_at(1, row).on_entry_changed(None)#force resize
                            # Check the box will create a new row for a validation dataset field
                            gridbox.get_child_at(3, row).set_active(0)
                            row += 1
                            gridbox.get_child_at(2, row).set_file_path(self.json_data['parameters']["validation_name"])
                            try:
                                self.json_data['parameters']["validation_name"] = eval(self.json_data['parameters']["validation_name"])
                            except ValueError:
                                pass
                        else:
                            gridbox.get_child_at(3, row).set_active(1)
                    gridbox.get_child_at(1, row).set_buffer(Gtk.EntryBuffer(text=self.json_data['parameters'][p]))
                    gridbox.get_child_at(1, row).on_entry_changed(None)#force resize
                    row += 1
        except Exception as e:
            self.json_data = {}
            logger.debug("Got {}\nError reading json file, set all fields to empty".format(e))
            for p in self.parameter_fields:
                gridbox.get_child_at(1, self.parameter_fields.index(p)+1).set_buffer(Gtk.EntryBuffer(text=""))
    
    def update_textview_with_code(self, textview, func_name):
        #Read data from json file
        if not "functions" in self.json_data.keys():
            logger.debug("Error reading json file, set all fields to empty, set default code for known functions")
            self.json_data['functions'] = {}
            self.json_data['functions']["get_attack_parameters"] = "def get_attack_parameters(traceset, subkey, index):\n\treturn {'p':, \n\t\t'k':, \n\t\t'subkey':}"
            self.json_data['functions']["get_known_key"] = "def get_known_key(traceset, subkey, index):\n\treturn "
            self.json_data['functions']["intermediate_value"] = "def intermediate_value(traceset, subkey, index):\n\treturn "
        else:
            logger.debug(self.json_data['functions'])
        for p in self.json_data['functions']:
            if p == func_name:
                textview.buffer.set_text(text=self.json_data['functions'][p])

    def to_first_window(self, widget):
        self.outerbox = gtkVerticalBox()
        hbox = gtkHorizontalBox()
        #Set gridbox for parameters
        self.paramgridbox = gtkGridbox()
        self.paramgridbox.attach(gtkLabelWithTooltip("Dataset", "Select a dataset among the list of available datasets, or select Custom to enter your own dataset"), 0, 0, 1, 1)
        datasets = sorted([f[:-3] for f in os.listdir(os.path.join(os.path.dirname(__file__), "datasets")) if f.endswith(".py") and f!="__init__.py" and f!="to_json.py"])
        combo = gtkComboText_with_items(datasets, set_active=None)
        combo.append_text('Custom')
        self.paramgridbox.attach(combo, 1, 0, 1, 1)
        combo.connect('changed', self.on_dataset_selected)
        for i, f in enumerate(self.parameter_fields):
            self.paramgridbox.attach(gtkLabelLeftAlign(label="{}: ".format(f)), 0, i+1, 1, 1)
            entryval = gtkResizableEntry()
            self.paramgridbox.attach(entryval, 1, i+1, 1, 1)
            if f=="dataset_name":
                self.paramgridbox.attach(gtkButtonFileSelection(entry=entryval), 2, i+1, 1, 1)
                val_dataset_checkbutton = Gtk.CheckButton.new_with_label("use for validation")
                val_dataset_checkbutton.row_index = i+1 # Save the row index to later create or remove validation dataset row below it
                val_dataset_checkbutton.set_active(1) # Set to True by default
                val_dataset_checkbutton.connect("toggled", self.on_button_validationdataset_clicked)
                self.paramgridbox.attach(val_dataset_checkbutton, 3, i+1, 1, 1)
        hbox.append(self.paramgridbox)
        combo.set_active(0)
        self.outerbox.append(hbox)
        
        self.add_navigation_bar(self.to_first_window, self.to_second_window)

        self.window.set_child(self.outerbox)
        self.window.present()

    def to_second_window(self, widget):
        #save previous parameters set in first window to json file
        self.json_data['parameters'] = {}
        parameter_fields = self.parameter_fields_wval if self.use_validation_dataset else self.parameter_fields
        for i, f in enumerate(parameter_fields):
            self.json_data['parameters'][f] = self.paramgridbox.get_child_at(1, i+1).get_buffer().get_text()
        try:
            with open(self.json_filename, 'w') as outfile:
                json.dump(self.json_data, outfile)
        except Exception as e:
            logger.debug("Error writing json file: {}".format(e))
        logger.debug(json.dumps(self.json_data, indent=4))

        
        #set up second window
        self.outerbox = gtkVerticalBox()
        vbox = gtkVerticalBox()

        self.funcgridbox = gtkGridbox()
        #Set a enrtry block to enter code
        self.funcgridbox.attach(gtkLabelLeftAlign(label="get_attack_parameters :"), 0, 0, 1, 1)
        codebox = gtkCodebox()
        self.update_textview_with_code(codebox.textview, "get_attack_parameters")
        self.funcgridbox.attach(codebox, 0, 1, 1, 1)
        #Set a enrtry block to enter code
        self.funcgridbox.attach(gtkLabelLeftAlign(label="get_known_key :"), 0, 2, 1, 1)
        codebox = gtkCodebox()
        self.update_textview_with_code(codebox.textview, "get_known_key")
        self.funcgridbox.attach(codebox, 0, 3, 1, 1)
        #Set a enrtry block to enter code
        self.funcgridbox.attach(gtkLabelLeftAlign(label="intermediate_value :"), 0, 4, 1, 1)
        codebox = gtkCodebox()
        self.update_textview_with_code(codebox.textview, "intermediate_value")
        self.funcgridbox.attach(codebox, 0, 5, 1, 1)
        vbox.append(self.funcgridbox)
        self.outerbox.append(vbox)

        self.add_navigation_bar(self.to_first_window, self.to_third_window, fill_gap=False)

        self.window.set_child(self.outerbox)
        self.window.present()

    def to_third_window(self, widget):
        #save previous window parameters to json file
        for i, f in enumerate(self.functions_fields):
            textbuffer = self.funcgridbox.get_child_at(0, 2*i+1).textview.buffer
            text = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), False)
            self.json_data['functions'][f] = text
        try:
            with open(self.json_filename, 'w') as outfile:
                json.dump(self.json_data, outfile)
        except Exception as e:
            logger.debug("Error writing json file: {}".format(e))
        self.dataset_model = self.json_data['model']

        #set up third window
        self.outerbox = gtkVerticalBox()
        hbox = gtkHorizontalBox()

        self.callbackbox = gtkGridbox()
        self.callbackbox.attach(Gtk.Label(label="Callbacks"), 0, 0, 1, 1)
        row = 1
        #Fill with dataset loaded callbacks parameters
        for f in self.json_data["callbacks"].keys():
            #Set gridbox for parameters
            combo = Gtk.ComboBoxText()
            combo.append_text('ModelCheckpoint')
            combo.append_text('Tensorboard')
            combo.append_text('GuessingEntropy')
            self.callbackbox.attach(combo, 0, row, 1, 1)
            combo.connect('changed', self.on_callback_selected)
            callback_params = Gtk.Grid()
            self.callbackbox.attach(callback_params, 1, row, 1, 1)
            combo.set_active([x.lower() for x in ['ModelCheckpoint', 'Tensorboard', 'GuessingEntropy']].index(f.lower()))
            row += 1
        if len(self.json_data["callbacks"].keys()) == 0:
            #Set gridbox for parameters
            combo = Gtk.ComboBoxText()
            combo.append_text('ModelCheckpoint')
            combo.append_text('Tensorboard')
            combo.append_text('GuessingEntropy')
            self.callbackbox.attach(combo, 0, row, 1, 1)
            combo.connect('changed', self.on_callback_selected)
            callback_params = Gtk.Grid()
            self.callbackbox.attach(callback_params, 1, row, 1, 1)
            row += 1
        #Add +/- buttons
        self.n_callbacks = row
        row += 1
        ad_remove_gridbox = gtkGridbox()
        ad_remove_gridbox = gtkAddRemoveGridbox(self.on_button_addcallback_clicked, self.on_button_removecallback_clicked)
        self.callbackbox.attach(ad_remove_gridbox, 0, row, 1, 1)
        
        
        hbox.append(self.callbackbox)
        self.outerbox.append(hbox)
        
        self.add_navigation_bar(self.to_second_window, self.to_fourth_window)

        self.window.set_child(self.outerbox)
        self.window.present()

    def to_fourth_window(self, widget):
        #save previous window parameters to json file
        self.json_data["callbacks"] = {}
        for i in range(self.n_callbacks-1):
            callback_name = self.callbackbox.get_child_at(0, i+1).get_active_text().lower()
            if callback_name is not None:
                self.json_data["callbacks"][callback_name] = {}
                name_widget, value_widget = 0, 0
                j = 0
                name_widget = self.callbackbox.get_child_at(1, i+1).get_child_at(0, j)
                value_widget = self.callbackbox.get_child_at(1, i+1).get_child_at(1, j)
                while name_widget != None and value_widget != None:
                    param_name = name_widget.get_label()
                    if isinstance(value_widget, Gtk.ComboBoxText):
                        param_value = value_widget.get_active_text()
                    else:
                        param_value = value_widget.get_buffer().get_text()
                    self.json_data["callbacks"][callback_name][param_name] = param_value
                    j += 1
                    name_widget = self.callbackbox.get_child_at(1, i+1).get_child_at(0, j)
                    value_widget = self.callbackbox.get_child_at(1, i+1).get_child_at(1, j)
        try:
            with open(self.json_filename, 'w') as outfile:
                json.dump(self.json_data, outfile)
        except Exception as e:
            logger.debug("Error writing json file: {}".format(e))
        
        #set up fourth window
        self.outerbox = gtkVerticalBox()
        vbox = gtkVerticalBox()
        
        #define to do train or optimize with two check box marks muttually exlusives
        hbox = gtkHorizontalBox()
        self.trainbutton = Gtk.CheckButton.new_with_label("Train")
        self.optbutton = Gtk.CheckButton.new_with_label("Optimize")
        self.trainbutton.connect("toggled", self.on_button_trainopt_clicked)
        self.optbutton.connect("toggled", self.on_button_trainopt_clicked)
        self.trainbutton.set_group(self.optbutton)
        hbox.append(self.trainbutton)
        hbox.append(self.optbutton)
        vbox.append(hbox)
        vbox.append(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        #Contains the model parameters information, refreshed on actions from buttons
        self.listbox = gtkVerticalBox()
        
        #Append the box for model parameters to the main frame
        vbox.append(self.listbox)
        self.outerbox.append(vbox)

        self.add_navigation_bar(self.to_third_window, self.to_fifth_window)

        #Render the window again
        self.window.set_child(self.outerbox)
        self.trainbutton.set_active(self.script_action == 'train')
        self.optbutton.set_active(self.script_action == 'optimize')
        self.window.present()

    def to_fifth_window(self, widget):
        #save model parameters to json file
        self.save_model_parameters()

        #set up fourth window
        self.outerbox = gtkVerticalBox()
        vbox = gtkVerticalBox()

        #Create a ready label
        label = gtkLabelLeftAlign(label="Ready to run")
        label.set_halign(Gtk.Align.START)
        vbox.append(label)

        #Make a run and stop button
        #TODO: when the python script crashes, toggle the run button off
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=6)
        startScriptButton = Gtk.Button.new_with_label("Run")
        startScriptButton.connect("clicked", self.on_button_run_script_clicked)
        hbox.append(startScriptButton)
        stopScriptButton = Gtk.Button.new_with_label("Stop")
        stopScriptButton.connect("clicked", self.on_button_stop_script_clicked)
        hbox.append(stopScriptButton)
        tbButton = Gtk.Button.new_with_label("Tensorboard")
        tbButton.connect("clicked", self.on_button_tensorboarb_clicked)
        hbox.append(tbButton)
        if self.script_action == 'optimize':
            optButton = Gtk.Button.new_with_label("Optuna Dashboard")
            optButton.connect("clicked", self.on_button_optuna_dashboard_clicked)
            hbox.append(optButton)
        vbox.append(hbox)

        #Make a output textview to attach to the script log
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.append(gtkLabelLeftAlign(label="Output:"))
        vbox.append(hbox)
        
        #Make a scrolled window to attach to the output textview
        self.output_window = gtkPipeMonitorWindow()

        #Attach the scrolled window to the main frame
        vbox.append(self.output_window)
        self.outerbox.append(vbox)

        self.add_navigation_bar(self.to_fourth_window, self.to_fifth_window, fill_gap=False)

        self.window.set_child(self.outerbox)
        self.window.present()

def main():
    #Parse arguments
    parser = argparse.ArgumentParser(description='eSCAPyDL GUI: Deep Leaning SCA PyTorch framework. Training models for tracesets with SCA metrics.')
    parser.add_argument('-a', '--timestamp', help='Timestamp of the experiment', default=time.strftime("%Y%m%d_%H%M%S",time.localtime()))
    parser.add_argument('-v', '--verbose', help='Verbose level', action='count', default=0)
    parser.add_argument('-l', '--log', help='Activate log to file', default='')
    args = parser.parse_args()
    if args.verbose == 1:
        logger.setLevel(logging.DEBUG)
    app = eSCAPyDLgui(timestamp=args.timestamp, log_filename=args.log, verbose=args.verbose)
    exit_status = app.run()
    sys.exit(exit_status)

if __name__ == "__main__":
    sys.exit(main())