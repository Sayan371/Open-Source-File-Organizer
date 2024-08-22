import os
import shutil
import file_ext
import customtkinter as ctk
from tkinter import filedialog, messagebox
import ctypes
from PIL import Image, ImageTk
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from matplotlib.figure import Figure 
from pathlib import Path
import sys
sys.path.append('file_ext.py')
ctypes.windll.shcore.SetProcessDpiAwareness(True)
ctk.set_appearance_mode("Dark")

downloads_path = str(Path.home() / "Downloads")
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
def get_special_folder(path):
    file_path = path
    file_path_entry.delete(0, 'end')
    file_path_entry.insert(0, file_path)
    no_of_file, no_video_files, no_audio_files, no_image_files, no_document_files, no_archive_files, no_folders, no_other_files = no_of_files(file_path)
    global sizes
    sizes = [no_video_files, no_image_files, no_folders, no_audio_files, no_document_files, no_archive_files, no_other_files]  # Example new sizes
    update_pie_chart(sizes)  # Update the pie chart with new sizes
    video_num.configure(text=str(no_video_files))
    image_num.configure(text=str(no_image_files))
    folder_num.configure(text=str(no_folders))
    audio_num.configure(text=str(no_audio_files))
    document_num.configure(text=str(no_document_files))
    archives_num.configure(text=str(no_archive_files))
    others_num.configure(text=str(no_other_files))
    reposition()

    return file_path

def move_files(file_path, ext, destination):
    ext_map = {'pdf': 'pdf', 'doc': 'word', 'odt': 'word', 'docx': 'word', 'ppt': 'powerpoint', 'pptx': 'powerpoint', 'xls': 'excel', 'xlsx': 'excel', 'csv': 'excel'}
    if ext in file_ext.video_file_formats:
        sub_folder = 'Video'
    elif ext in file_ext.audio_file_formats:
        sub_folder = 'Audio'
    elif ext in file_ext.image_file_formats:
        sub_folder = 'images'
    elif ext in file_ext.document_file_formats:
        sub_folder = ext_map.get(ext, 'documents')
    elif ext in file_ext.archive_file_formats:
        sub_folder = 'archives'
    else:
        return

    dest_path = os.path.join(destination, sub_folder)
    os.makedirs(dest_path, exist_ok=True)

    file_name = os.path.basename(file_path)
    destination_file_path = os.path.join(dest_path, file_name)

    if os.path.exists(destination_file_path):
        messagebox.showerror(title="Error!", message="File already exists!")
        return

    shutil.move(file_path, dest_path)

def no_of_files(file_path):
    # Getting the number of files
    try:
        files = os.listdir(file_path)
        no_of_file = len(files)

        # Getting the number of video files
        no_video_files = len([file for file in files if any(file.endswith(ext) for ext in file_ext.video_file_formats)])

        # Getting the number of audio files
        no_audio_files = len([file for file in files if any(file.endswith(ext) for ext in file_ext.audio_file_formats)])

        # Getting the number of image files
        no_image_files = len([file for file in files if any(file.endswith(ext) for ext in file_ext.image_file_formats)])

        # Getting the number of document files
        no_document_files = len([file for file in files if any(file.endswith(ext) for ext in file_ext.document_file_formats)])

        # Getting the number of archive files
        no_archive_files = len([file for file in files if any(file.endswith(ext) for ext in file_ext.archive_file_formats)])

        # getting folders
        no_folders = len([file for file in files if os.path.isdir(os.path.join(file_path, file))])

        # getting others size
        known_size = no_video_files + no_audio_files + no_image_files + no_document_files + no_archive_files + no_folders
        no_other_files = no_of_file - known_size
    except:
        pass
    return no_of_file, no_video_files, no_audio_files, no_image_files, no_document_files, no_archive_files, no_folders, no_other_files

def reposition():
    canvas.get_tk_widget().place(x=640, y=35)
    table_label.place(x=500, y=390)
    video_num.place(x=607, y=394)
    image_num.place(x=612, y=424)
    folder_num.place(x=610, y=453)
    audio_num.place(x=608, y=484)
    document_num.place(x=641, y=514)
    archives_num.place(x=622, y=544)
    others_num.place(x=607, y=573)

def unposition():
    canvas.get_tk_widget().place(x=640, y=2000)
    table_label.place(x=500, y=2000)
    video_num.place(x=607, y=2000)
    image_num.place(x=612, y=2000)
    folder_num.place(x=610, y=2000)
    audio_num.place(x=608, y=2000)
    document_num.place(x=641, y=2000)
    archives_num.place(x=622, y=2000)
    others_num.place(x=607, y=2000)

def update_pie_chart(new_sizes):

    global sizes, canvas, ax
    sizes = new_sizes
    ax.clear()
    wedges, texts = ax.pie(sizes, explode=explode, labels=labels,shadow=True, startangle=90, wedgeprops=dict(width=0.3, edgecolor='white'), colors=colors, textprops={'color': 'white'})
    canvas.draw()

def get_file():
    file_path_entry.delete(0, 'end')
    if file_folder_btn.get() == file_folder_values[0]:
        try:
            file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Text Files",".txt")])
            unposition()
        except:
            pass
    elif file_folder_btn.get() == file_folder_values[1]:
        file_path = filedialog.askdirectory()
        no_files = len(os.listdir(file_path))
        if no_files > 0:
            no_of_file, no_video_files, no_audio_files, no_image_files, no_document_files, no_archive_files, no_folders, no_other_files = no_of_files(file_path)
        
            global sizes
            sizes = [no_video_files, no_image_files, no_folders, no_audio_files, no_document_files, no_archive_files, no_other_files]  # Example new sizes
            update_pie_chart(sizes)  # Update the pie chart with new sizes
            video_num.configure(text=str(no_video_files))
            image_num.configure(text=str(no_image_files))
            folder_num.configure(text=str(no_folders))
            audio_num.configure(text=str(no_audio_files))
            document_num.configure(text=str(no_document_files))
            archives_num.configure(text=str(no_archive_files))
            others_num.configure(text=str(no_other_files))
            reposition()
        else:
            messagebox.showerror(title="Error!", message="The directory is empty!")
    else:
        messagebox.showerror(title="Error!", message="Please select Folder or File Option.")
        return
    file_path_entry.insert(0, file_path)
    return file_path

def file_type(val):
    file_path = file_path_entry.get()
    no_of_file, no_video_files, no_audio_files, no_image_files, no_document_files, no_archive_files, no_folders, no_other_files = no_of_files(file_path)
    
    global explode, canvas, ax
    if select_type_dd.get() == 'All':
        explode = (0, 0, 0, 0, 0, 0, 0)
    elif select_type_dd.get() == 'Video' and no_video_files > 0:
        explode = (0.07, 0, 0, 0, 0, 0, 0)
    elif select_type_dd.get() == 'Image' and no_image_files > 0:
        explode = (0, 0.07, 0, 0, 0, 0, 0)
    elif select_type_dd.get() == 'Audio' and no_audio_files > 0:
        explode = (0, 0, 0, 0.07, 0, 0, 0)
    elif select_type_dd.get() == 'Document' and no_document_files > 0:
        explode = (0, 0, 0, 0, 0.07, 0, 0)
    elif select_type_dd.get() == 'Archive' and no_archive_files > 0:
        explode = (0, 0, 0, 0, 0, 0.07, 0)
    
    ax.clear()
    wedges, texts = ax.pie(sizes, explode=explode, labels=labels,shadow=True, startangle=90, wedgeprops=dict(width=0.3, edgecolor='white'), colors=colors, textprops={'color': 'white'})
    canvas.draw()

def execute():
    if file_path_entry.get() == '':
        messagebox.showerror(title="Error!", message="Please enter file path.")
        return

    file_path = file_path_entry.get()
    destination = destination_entry.get()

    # Determine if it's a file or a folder
    if destination == '':
        messagebox.showerror(title="Error!", message="Please enter destination path.")
        return
    is_folder = os.path.isdir(file_path)
    if not is_folder:  # If it's a single file
        if method.get() == method_values[1]:  # Move method

            if os.path.exists(destination):
                try:
                    shutil.move(file_path, destination)
                    messagebox.showinfo(title="File Moved", message="The file was moved successfully.")
                except Exception as e:
                    messagebox.showerror(title="Error!", message=f"Failed to move the file: {e}")
            else:
                messagebox.showerror(title="Error!", message="Destination path does not exist.")
        
        elif method.get() == method_values[0]:  # Delete method
            confirm_delete = messagebox.askyesno(title="Warning", message="Are you sure you want to delete this file?")
            if confirm_delete:
                try:
                    os.remove(file_path)
                    messagebox.showinfo(title="File Deleted", message="The file was deleted successfully.")
                except Exception as e:
                    messagebox.showerror(title="Error!", message=f"Failed to delete the file: {e}")
            else:
                messagebox.showinfo(title="Cancelled", message="File deletion cancelled.")
    
    else:  # If it's a folder
        try:
            if method.get() == method_values[1] and destination_entry.get() != '':
                if select_type_dd.get() == 'All':
                    for file in os.listdir(file_path):
                        if '.' in file:
                            raw_file, ext = file.rsplit(".", 1)
                            move_files(os.path.join(file_path, file), ext, destination)
                elif select_type_dd.get() == 'Video':
                    for file in os.listdir(file_path):
                        if '.' in file:
                            raw_file, ext = file.rsplit(".", 1)
                            if ext in file_ext.video_file_formats:
                                move_files(os.path.join(file_path, file), ext, destination)
                elif select_type_dd.get() == 'Audio':
                    for file in os.listdir(file_path):
                        if '.' in file:
                            raw_file, ext = file.rsplit(".", 1)
                            if ext in file_ext.audio_file_formats:
                                move_files(os.path.join(file_path, file), ext, destination)
                elif select_type_dd.get() == 'Image':
                    for file in os.listdir(file_path):
                        if '.' in file:
                            raw_file, ext = file.rsplit(".", 1)
                            if ext in file_ext.image_file_formats:
                                move_files(os.path.join(file_path, file), ext, destination)
                elif select_type_dd.get() == 'Document':
                    for file in os.listdir(file_path):
                        if '.' in file:
                            raw_file, ext = file.rsplit(".", 1)
                            if ext in file_ext.document_file_formats:
                                move_files(os.path.join(file_path, file), ext, destination)
                elif select_type_dd.get() == 'Archive':
                    for file in os.listdir(file_path):
                        if '.' in file:
                            raw_file, ext = file.rsplit(".", 1)
                            if ext in file_ext.archive_file_formats:
                                move_files(os.path.join(file_path, file), ext, destination)
                messagebox.showinfo(title="Files Moved", message="The files were moved successfully.")

            elif method.get() == method_values[0]:  # Delete all files in folder
                confirm_delete = messagebox.askyesno(title="Warning", message="Are you sure you want to delete all files?")
                if confirm_delete:
                    if select_type_dd.get() == 'All':
                        shutil.rmtree(file_path)
                    else:
                        for file in os.listdir(file_path):
                            if '.' in file:
                                raw_file, ext = file.rsplit(".", 1)
                                if (select_type_dd.get() == 'Video' and ext in file_ext.video_file_formats) or \
                                   (select_type_dd.get() == 'Audio' and ext in file_ext.audio_file_formats) or \
                                   (select_type_dd.get() == 'Image' and ext in file_ext.image_file_formats) or \
                                   (select_type_dd.get() == 'Document' and ext in file_ext.document_file_formats) or \
                                   (select_type_dd.get() == 'Archive' and ext in file_ext.archive_file_formats):
                                    os.remove(os.path.join(file_path, file))
                    messagebox.showinfo(title="Files Deleted", message="The files were deleted successfully.")
                else:
                    messagebox.showinfo(title="Request Cancelled", message="The files were not deleted.")
        
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File or directory not found.")

    try:
        if is_folder:
            no_files = len(os.listdir(file_path))
            if no_files > 0:
                no_of_file, no_video_files, no_audio_files, no_image_files, no_document_files, no_archive_files, no_folders, no_other_files = no_of_files(file_path)
                global sizes
                sizes = [no_video_files, no_image_files, no_folders, no_audio_files, no_document_files, no_archive_files, no_other_files] 
                update_pie_chart(sizes) 
                video_num.configure(text=str(no_video_files))
                image_num.configure(text=str(no_image_files))
                folder_num.configure(text=str(no_folders))
                audio_num.configure(text=str(no_audio_files))
                document_num.configure(text=str(no_document_files))
                archives_num.configure(text=str(no_archive_files))
                others_num.configure(text=str(no_other_files))
            elif no_files == 0:
                default()
    except FileNotFoundError:
        default()

def default():
    sizes = [1, 1, 1, 1, 1, 1, 1] 
    update_pie_chart(sizes)  
    video_num.configure(text=str(0))
    image_num.configure(text=str(0))
    folder_num.configure(text=str(0))
    audio_num.configure(text=str(0))
    document_num.configure(text=str(0))
    archives_num.configure(text=str(0))
    others_num.configure(text=str(0))
def method(val):
    if method.get() == method_values[0]:
        destination_entry.place(x=0, y=1000)
        destination_locate.place(x=0, y=1000)
        destination_label.place(x=0, y=1000)
        line3.place(x=0, y=1000)

    elif method.get() == method_values[1]:
        destination_entry.place(x=33, y=455)
        destination_locate.place(x=33, y=505)
        destination_label.place(x=33, y=410)
        line3.place(x=40, y=550)
def file_folder(val):
    if file_folder_btn.get() == file_folder_values[0]:
        desktop_btn.place(x=212, y=500)
        downloads_btn.place(x=212, y=500)
        get_file_btn.configure(width=368)
        get_file_btn.place(x=0, y=5)
    elif file_folder_btn.get() == file_folder_values[1]:
        desktop_btn.place(x=0, y=5)
        get_file_btn.configure(width=112)
        get_file_btn.place(x=124, y=5)
        downloads_btn.place(x=243, y=5)

def destination():
    ask_dest = filedialog.askdirectory()
    destination_entry.delete(0, 'end')
    destination_entry.insert(0, ask_dest)

def help():
    webbrowser.open("help.txt")
    


#### CREATING AND FORMATTING THE WINDOW ####
window = ctk.CTk()
background_color = '#212121'
secondry_color = '#00ba44' # Original '#1f6aa5'
hover_color = '#0d943f'    # Original '#144870'



window.config(bg=background_color)
window.title("File Organizer by-Sayan")
window.geometry('1000x650+300+100')
window.resizable(False, False)


   
#### CREATING THE BUTTON ####
frame = ctk.CTkFrame(window, 
                    bg_color=background_color, 
                    width=500, height=250,
                    fg_color=background_color)
frame.place(x=33, y=100)

get_file_btn = ctk.CTkButton(frame,
                            text="Locate", 
                            width=112, height=25, 
                            font=("TW cen MT", 21, "bold"), 
                            text_color='white', 
                            corner_radius=10,
                            fg_color=secondry_color,
                            hover_color=hover_color,
                            command=get_file)
get_file_btn.place(x=124, y=5)

desktop_btn = ctk.CTkButton(frame, 
                            text="Desktop", 
                            width=115, height=25, 
                            font=("TW cen MT", 21, "bold"), 
                            text_color='white', 
                            corner_radius=10, 
                            fg_color=secondry_color,
                            hover_color=hover_color,
                            command=lambda: get_special_folder('C:/Users/user/OneDrive/Desktop'))
desktop_btn.place(x=0, y=5)

downloads_btn = ctk.CTkButton(frame, 
                              text="Downloads", 
                              width=125, height=25, 
                              font=("TW cen MT", 21, "bold"), 
                              text_color='white', 
                              corner_radius=10, 
                              fg_color=secondry_color,
                              hover_color=hover_color,
                              command=lambda: get_special_folder(downloads_path))
downloads_btn.place(x=243, y=5)

#### EXECUTE BUTTON ####
execute_btn = ctk.CTkButton(window, 
                            text="GO", 
                            width=45, height=42, 
                            font=("TW cen MT", 22, "bold"), 
                            corner_radius=10, 
                            bg_color=background_color, 
                            text_color='white', 
                            fg_color=secondry_color,
                            hover_color=hover_color,
                            command=execute)
execute_btn.place(x=415, y=54)

#### FILE PATH ENTRY BOX ####
file_path_entry = ctk.CTkEntry(window, 
                               font=("TW cen MT", 15), 
                               height=40, width=368, 
                               bg_color=background_color, 
                               corner_radius=7)
file_path_entry.place(x=33, y=55)

#### LABEL ####
add_path = ctk.CTkLabel(window, 
                        text="Add The Path:", 
                        font=("TW cen MT", 18), 
                        text_color='white', 
                        fg_color=background_color, 
                        bg_color=background_color)
add_path.place(x=33, y=11)

#### LINES ####
line1 = ctk.CTkCanvas(window, 
                      width=545, height=2, 
                      bg='#404040', bd=0, 
                      highlightthickness=0, 
                      relief='ridge')
line1.place(x=40, y=49)

line2 = ctk.CTkCanvas(window, 
                      width=545, height=2, 
                      bg='#404040', bd=0, 
                      highlightthickness=0, 
                      relief='ridge')
line2.place(x=40, y=299)

line3 = ctk.CTkCanvas(window, 
                      width=545, height=2, 
                      bg='#404040', bd=0, 
                      highlightthickness=0, 
                      relief='ridge')
line3.place(x=40, y=550)

line4 = ctk.CTkCanvas(window, 
                      width=545, height=2, 
                      bg='#404040', bd=0, 
                      highlightthickness=0, 
                      relief='ridge')
line4.place(x=40, y=411)


#### FILE OR FOLDER ####
radio_frame = ctk.CTkFrame(window, 
                           bg_color=background_color, 
                           fg_color=background_color, 
                           width=410, height=40)
radio_frame.place(x=33, y=165)

file_folder_values = ['          File            ', '           Folder          ']
file_folder_btn = ctk.CTkSegmentedButton(radio_frame, 
                                         values=file_folder_values, 
                                         font=("TW cen MT", 20, 'bold'), 
                                         corner_radius=10, 
                                         fg_color='#3b3b3b', 
                                         selected_color=secondry_color,
                                         text_color='white',
                                         selected_hover_color=hover_color, 
                                         command=file_folder,)
file_folder_btn.place(x=0, y=0)

#### DROP DOWN FOR FILE TYPE ####
select_file_type_label = ctk.CTkLabel(window, 
                                      text="Select File Type:", 
                                      font=("TW cen MT", 18), 
                                      text_color='white', 
                                      fg_color=background_color, 
                                      bg_color=background_color)
select_file_type_label.place(x=33, y=210)

select_type_dd = ctk.CTkOptionMenu(window, 
                                   width=120, height=26,
                                   font=("TW cen MT", 18), 
                                   text_color='white', 
                                   bg_color=background_color, 
                                   values=('All', 'Video', 'Image', 'Audio', 'Document', 'Archive'), 
                                   dynamic_resizing=False, 
                                   fg_color='#404040', 
                                   button_color='#303030', 
                                   button_hover_color='#1a1a1a', 
                                   dropdown_font=("TW cen MT", 18), 
                                   dropdown_fg_color='#303030', 
                                   corner_radius=10,
                                   command=file_type)
select_type_dd.place(x=33, y=250)

#### DESTINATION FOLDER ####
destination_label = ctk.CTkLabel(window, 
                                 text="Select Destination:", 
                                 font=("TW cen MT", 18), 
                                 text_color='white', 
                                 fg_color=background_color, 
                                 bg_color=background_color)
destination_label.place(x=33, y=410)

destination_entry = ctk.CTkEntry(window, 
                                 font=("TW cen MT", 15), 
                                 height=40, width=436, 
                                 bg_color=background_color, 
                                 corner_radius=7)
destination_entry.place(x=33, y=455)

destination_locate = ctk.CTkButton(window, 
                                   text="Add Destination", 
                                   font=("TW cen MT", 24, 'bold'), 
                                   text_color='white',
                                   bg_color=background_color,
                                   fg_color=secondry_color, 
                                   width=436, height=40, 
                                   hover_color=hover_color,
                                   command=destination)
destination_locate.place(x=33, y=505)

#### RIGHT PART ####


######### IMAGE ########


r_frame = ctk.CTkFrame(window, 
                       width=480, height=600)
r_frame.place(x=495, y=20)


#### DELETE OR MOVE ####
method_label = ctk.CTkLabel(window,
                             text="Select Method:",
                             font=("TW cen MT", 18),
                             text_color='white',
                             fg_color=background_color)

method_label.place(x=33, y=300)

method_values = ['          Delete           ', '           Move          ']
method = ctk.CTkSegmentedButton(window, 
                                values=method_values, 
                                font=("TW cen MT", 25, 'bold'), 
                                corner_radius=10, 
                                fg_color='#3b3b3b', 
                                text_color='white', 
                                selected_color=secondry_color,
                                selected_hover_color=hover_color,
                                height=50, 
                                command=method)
method.place(x=33, y=343)
method.set(value=method_values[1])

######## HELP #########
ques_img = Image.open(r"images\question.png")
ques_img = ques_img.resize((25, 25))
ques = ImageTk.PhotoImage(ques_img)

help_btn = ctk.CTkButton(window,
                         text="Help",
                         font=("TW cen MT", 20, 'underline'),
                         image=ques,
                         fg_color=background_color,
                         text_color='white',
                         width=20, height=20,
                         hover_color=background_color,
                         command=help)
help_btn.place(x=0, y=610)

def on_enter(e):
    help_btn.configure(text_color='#42f55a')
def on_leave(e):
    help_btn.configure(text_color='white')
def tap(e):
    help_btn.configure(text_color='white')
def untap(e):
    help_btn.configure(text_color='#42f55a')
help_btn.bind('<Enter>', on_enter)
help_btn.bind('<Leave>', on_leave)
help_btn.bind('<Button-1>', tap)
help_btn.bind('<ButtonRelease-1>', untap)

########## EMPTY GRAPH ################## 

labels = '', '', '', '', '', '', ''
sizes = [1, 1, 1, 1, 1, 1, 1]
explode = (0, 0, 0, 0, 0, 0, 0) 

fig = Figure(figsize=(5, 5), dpi=90)
fig.patch.set_facecolor('#2b2b2b')  

ax = fig.add_subplot(111)
ax.set_facecolor('#2b2b2b')  

colors = [ '#9ccf76', '#e3e353', '#fec749', '#f48a63', '#e37d93', '#ba95c2', '#8ea7d2']

wedges, texts= ax.pie(sizes, explode=explode, labels=labels,
                                    shadow=True, startangle=90, wedgeprops=dict(width=0.3, edgecolor='white'),
                                    colors=colors, textprops={'color': 'white'})
ax.axis('equal')

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()

canvas.get_tk_widget().place(x=640, y=2000)
heading = ctk.CTkLabel(window,
                    text="File Distribution Visualisor ", 
                    text_color='white', 
                    font=("TW cen MT", 30, 'bold'), 
                    bg_color='#2b2b2b')
heading.place(x=570, y=30)

##################### TABLE PLOTTING #######################
table = Image.open(r"images\color_table.png")
table = table.resize((170, 280),) 
table= ImageTk.PhotoImage(table)
table_label = ctk.CTkLabel(window, image=table, text='', bg_color='#2b2b2b')
table_label.place(x=500, y=2000)

video_num = ctk.CTkLabel(window, 
                         text=str(0), 
                         text_color='white', 
                         font=("TW cen MT", 16, 'bold'), 
                         bg_color='#2b2b2b')
video_num.place(x=607, y=2000)

image_num = ctk.CTkLabel(window, 
                         text=str(0), 
                         text_color='white', 
                         font=("TW cen MT", 16, 'bold'), 
                         bg_color='#2b2b2b')
image_num.place(x=612, y=2000)

folder_num = ctk.CTkLabel(window, 
                         text=str(0), 
                         text_color='white', 
                         font=("TW cen MT", 16, 'bold'), 
                         bg_color='#2b2b2b')
folder_num.place(x=610, y=2000)

audio_num = ctk.CTkLabel(window, 
                         text=str(0), 
                         text_color='white', 
                         font=("TW cen MT", 16, 'bold'), 
                         bg_color='#2b2b2b')
audio_num.place(x=608, y=2000)

document_num = ctk.CTkLabel(window, 
                         text=str(0), 
                         text_color='white', 
                         font=("TW cen MT", 16, 'bold'), 
                         bg_color='#2b2b2b')
document_num.place(x=641, y=2000)

archives_num = ctk.CTkLabel(window, 
                         text=str(0), 
                         text_color='white', 
                         font=("TW cen MT", 16, 'bold'), 
                         bg_color='#2b2b2b')
archives_num.place(x=622, y=2000)

others_num = ctk.CTkLabel(window,
                        text=str(0),
                        text_color='white',
                        font=("TW cen MT", 16, 'bold'),
                        bg_color='#2b2b2b')
others_num.place(x=607, y=2000)


icon = Image.open(r"images\folder.png")

icon = ImageTk.PhotoImage(icon)
window.wm_iconbitmap()
window.iconphoto(False, icon)
window.mainloop()



################## CREATED BY SAYAN OWNER OF ECHO SCRIPTS ###########################
