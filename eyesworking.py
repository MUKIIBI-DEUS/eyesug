
# imports-----------------------------------------------------
import os
import customtkinter as css
import screen_brightness_control as sbc
import datetime
import sqlite3
from tkinter import messagebox
from plyer import notification
from functions_m import deadline
from functions_m import mill_minutes

#colour variables to use throughout the Application
background_colour="#017bf5"
fore_colour="#017bf5"
light="gray"

connection = sqlite3.connect("dope.db")
cursor = connection.cursor()
cursor.execute(
    '''create table  IF NOT EXISTS deadline(courseName text,Deadline_date text,SetDate text,remindermin 
    integer)''')


# GLOBALS-----------------------------------------------------
j=1
d=j
s=j




# dayslefts = deadline(20, 5)
# # to remind the user throughout the day
# # remind_hr=mill_minutes(int(input("reminding time in hours :")))
# remind_min = mill_minutes(int(input("reminding time in minutes :")))
# print(remind_min)

# GLOBALS-----------------------------------------------------

year=None

day=None

month=None



# FUNCTION-----------------------------------------------------
def display():
    display_frame.grid()
    display_frame.grid_propagate(False)
    others_frame.grid_forget()
    coursework_frame.grid_forget()
    power_btn.configure(fg_color="#017bf5")
    display_btn.configure(fg_color="#434344")
    coursework_btn.configure(fg_color="#017bf5")


# changing brightness of the screen
def change_brightness(value):
    right_frame.update()
    sbc.set_brightness(round(value))
    # print(value)


# changing the gamma of the screen
def change_sharpness(value):
    right_frame.update()
    sbc.fade_brightness(round(value))


# COURSE WORK BTN
#-----------------------------------------------------------------------------------------------------------------------
def coursework():
    coursework_frame.grid()
    coursework_frame.grid_propagate(False)
    coursework_btn.configure(fg_color="#434344")
    display_frame.grid_forget()
    others_frame.grid_forget()
    power_btn.configure(fg_color="#017bf5")
    display_btn.configure(fg_color="#017bf5")
    about_us_btn.configure(fg_color="#017bf5")


# >>>>>>>>>>>>>>>>>>>>>>
# A function to pick all details from a coursework pad1 and
#-----------------------------------------------------------------------------------------------------------------------
def getDeadlineDetailsPad1():
    data_view_section.update()
    count=0


    # accessing the datetime module
    x = datetime.datetime.now()

    current_year = int(x.strftime("%Y"))
    current_month = int(x.strftime("%m"))
    current_day = int(x.strftime("%d"))

    # Getting user input(ALL details of the deadline a)
    # using N will be used to verify if the deadline is not less than current day(AVOIDING NEGATIVE VALUES)
    course = courseUnitInput.get()

    year = deadline_yearInput.get()



    month = deadline_monthInput.get()



    day = deadline_dayInput.get()



    reminder_min1 = reminder_minute_Input.get()

    # ERROR HANDLING>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # error handling deadline cant be less than the current day



    if course and year and month and day and reminder_min1:
        try:
            # adding a number to reminder time to avoid collision
            reminder_min = int(reminder_min1) + 2
            # converting the current day to string format>>>>>>>>>>

            current_date = str(current_year) + "/" + str(current_month) + "/" + str(current_day)
            deadline_date = year + "/" + month + "/" + day
            # coverting to date format>>>>>>>>>>>>>>>>>>>>>>
            deadl_fin = x.strptime(deadline_date, "%Y/%m/%d")

            current_datefin = x.strptime(current_date, "%Y/%m/%d")

            # getting days left after subtracting the  current date from the deadline

            daysleft = deadl_fin - current_datefin

            print(daysleft.days - 1)

            # DATABASE CREATION----------------------------------------------


            cursor.execute(
                '''create table  IF NOT EXISTS deadline(courseName text,Deadline_date text,SetDate text,remindermin 
                integer)''')
            cursor.execute("insert into deadline values(:courseName,:Deadline_date,:SetDate,:remindermin)",
                           {'courseName': course, 'Deadline_date': deadline_date, 'SetDate': current_date,
                            'remindermin': reminder_min})
            # adding imput data  to the database>>>>>>>>>>>>>>>>>>>>
            #error handling before data is casted to the database deadeline cant be behind the current date
            inte_value=0

            #Confirmation for saving the deadline and data verification>>>>>>>>>>>>>>>>>>>>>>>>>>>





                #if the daysleft of the dealine are greater than 0 then commit changes to the database
            if daysleft.days>inte_value:

                if messagebox.askokcancel("Saving", "Do you want to save the deadline"):
                        connection.commit()
                        messagebox.showinfo("Success", "Deadline set successfully! Thanks we shall remind you .")
                else:
                        print("Not saved")



            else:
                    messagebox.showerror("error", "Data not saved Deadline date cannot be behind the current date ")



            # the code to fetch all information from the data base
            row = cursor.fetchall()
            for row in cursor.execute("select * from deadline"):
                print(row)

            # closing the database connecion


            # showing the dialog /message box after data completion and correctness

        except ValueError:


                messagebox.showerror("Error", "Please enter valid details.")
    else:
        messagebox.showerror("Error", "Please fill all entries.  Note:Data must be correct.")
#ALL ERROR HANDLING, VERIFICATION AND DATA ENTRY TO THE DATA BASE IS ACCOMPOLISHED *******************************************


# add days left in the data base but remenber the
# ----------------------
#SEARCH ENGINE FUNCTION
def search_courseWork(event):
    try:
        search_input=search_entry.get()
        data_view_section = css.CTkScrollableFrame(master=coursework_frame,
                                                   fg_color="#434344",
                                                   height=290,
                                                   width=710,

                                                   )
        data_view_section.grid(row=2, column=0, columnspan=2, pady=10, padx=3)
        # Entity Labels of the dataview(HEADERS)>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # courseName label in dataviewsction

        course_name_h = css.CTkLabel(master=data_view_section,
                                     text="Course Name",
                                     fg_color="purple",
                                     text_color="white",

                                     height=50,
                                     width=150
                                     )
        course_name_h.grid(row=0, column=0, pady=2, padx=1)

        # courseName from database:
        course = []
        cursor.execute(f"select courseName from deadline where courseName like '%{search_input}%' ")
        rows = cursor.fetchall()
        for i, row in enumerate(rows, start=1):
            for j, value in enumerate(row):
                l = css.CTkLabel(master=data_view_section,
                                 text=value,
                                 fg_color="#017bf5",
                                 text_color="white",
                                 height=50,
                                 width=150
                                 )
                l.grid(row=i, column=j, pady=2, padx=1)
            print(value)

        deadline_label_h = css.CTkLabel(master=data_view_section,
                                        text="Deadline Date",
                                        fg_color="purple",
                                        text_color="white",
                                        height=50,
                                        width=146
                                        )
        deadline_label_h.grid(row=0, column=1)

        # deadline label in dataviewsction
        cursor.execute(f"select Deadline_date from deadline where courseName like '%{search_input}%'")
        rows = cursor.fetchall()
        for i, row in enumerate(rows, start=1):
            for j, value in enumerate(row, start=1):
                l = css.CTkLabel(master=data_view_section,
                                 text=value,
                                 fg_color="#017bf5",
                                 text_color="white",
                                 height=50,
                                 width=146
                                 )
                l.grid(row=i, column=j, pady=2, padx=1)
            print(value)

        # SetDate label in dataviewsection

        setDate_label_h = css.CTkLabel(master=data_view_section,
                                       text="Set Date",
                                       fg_color="purple",
                                       text_color="white",
                                       height=50,
                                       width=146
                                       )
        setDate_label_h.grid(row=0, column=2, pady=2, padx=1)

        cursor.execute(f"select SetDate from deadline where courseName like '%{search_input}%'")
        rows = cursor.fetchall()
        for i, row in enumerate(rows, start=1):
            for j, value in enumerate(row, start=2):
                l = css.CTkLabel(master=data_view_section,
                                 text=value,
                                 fg_color="#017bf5",
                                 text_color="white",
                                 height=50,
                                 width=146
                                 )
                l.grid(row=i, column=j, pady=2, padx=1)
            print(value)

        # Reminder time
        reminder_label_h = css.CTkLabel(master=data_view_section,
                                        text="Remind",
                                        fg_color="purple",
                                        text_color="white",
                                        height=50,
                                        width=80
                                        )
        reminder_label_h.grid(row=0, column=3, pady=2, padx=1)

        cursor.execute(f"select remindermin from deadline where courseName like '%{search_input}%'")
        rows = cursor.fetchall()
        for i, row in enumerate(rows, start=1):
            for j, value in enumerate(row, start=3):
                l = css.CTkLabel(master=data_view_section,
                                 text=value,
                                 fg_color="#017bf5",
                                 text_color="white",
                                 height=50,
                                 width=80
                                 )
                l.grid(row=i, column=j, pady=2, padx=1)
            print(value)

        # DAYS left label in the dataview
        daysleft_h = css.CTkLabel(master=data_view_section,
                                  text="Days left",
                                  fg_color="purple",
                                  text_color="white",
                                  height=50,
                                  width=100
                                  )
        daysleft_h.grid(row=0, column=4, pady=2, padx=1)

        cursor.execute(f"select Deadline_date from deadline where courseName like '%{search_input}%' ")
        rows = cursor.fetchall()

        # accessing the datetime module
        x = datetime.datetime.now()

        current_year = int(x.strftime("%Y"))
        current_month = int(x.strftime("%m"))
        current_day = int(x.strftime("%d"))

        colour = "#121312"
        for i, row in enumerate(rows, start=1):
            for j, value in enumerate(row, start=4):
                current_date = str(current_year) + "/" + str(current_month) + "/" + str(current_day)
                print(value)

                # coverting to date format>>>>>>>>>>>>>>>>>>>>>>
                deadl_fin = x.strptime(value, "%Y/%m/%d")

                current_datefin = x.strptime(current_date, "%Y/%m/%d")

                # getting days left after subtracting the  current date from the deadline

                daysleft = deadl_fin - current_datefin
                cl = daysleft.days
                if cl > 3:
                    colour = light
                elif cl >= 1 and cl <= 3:
                    colour = "#9c4141"
                elif cl < 1 and cl <= -1:
                    colour = "red"
                    cl = str(daysleft.days) + " past"

                else:
                    print("hello")

                l = css.CTkLabel(master=data_view_section,
                                 text=cl,
                                 fg_color=colour,
                                 text_color="white",
                                 height=50,
                                 width=100
                                 )
                l.grid(row=i, column=j, pady=2, padx=1)
    except ValueError:
        messagebox.showerror("Not found!","coursework not found try again")
        print("not found")
# __________________________________________________________________________________________________________________________________________________________________________________________

# The button command that will refresh the data view section after new data entry
#-----------------------------------------------------------------------------------------------------------------------
def refresh_data_view_section_coursework():
    data_view_section = css.CTkScrollableFrame(master=coursework_frame,
                                               fg_color="#434344",
                                               height=290,
                                               width=710,



                                               )
    data_view_section.grid(row=2, column=0, columnspan=2, pady=10, padx=3)
    # Entity Labels of the dataview(HEADERS)>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # courseName label in dataviewsction

    course_name_h = css.CTkLabel(master=data_view_section,
                                 text="Course Name",
                                 fg_color="purple",
                                 text_color="white",

                                 height=50,
                                 width=150
                                 )
    course_name_h.grid(row=0, column=0, pady=2, padx=1)

    # courseName from database:
    course = []
    cursor.execute("select courseName from deadline")
    rows = cursor.fetchall()
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row):
            l = css.CTkLabel(master=data_view_section,
                             text=value,
                             fg_color="#017bf5",
                             text_color="white",
                             height=50,
                             width=150
                             )
            l.grid(row=i, column=j, pady=2, padx=1)
        print(value)

    deadline_label_h = css.CTkLabel(master=data_view_section,
                                    text="Deadline Date",
                                    fg_color="purple",
                                    text_color="white",
                                    height=50,
                                    width=146
                                    )
    deadline_label_h.grid(row=0, column=1)

    # deadline label in dataviewsction
    cursor.execute("select Deadline_date from deadline")
    rows = cursor.fetchall()
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row, start=1):
            l = css.CTkLabel(master=data_view_section,
                             text=value,
                             fg_color="#017bf5",
                             text_color="white",
                             height=50,
                             width=146
                             )
            l.grid(row=i, column=j, pady=2, padx=1)
        print(value)

    # SetDate label in dataviewsection

    setDate_label_h = css.CTkLabel(master=data_view_section,
                                   text="Set Date",
                                   fg_color="purple",
                                   text_color="white",
                                   height=50,
                                   width=146
                                   )
    setDate_label_h.grid(row=0, column=2, pady=2, padx=1)

    cursor.execute("select SetDate from deadline")
    rows = cursor.fetchall()
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row, start=2):
            l = css.CTkLabel(master=data_view_section,
                             text=value,
                             fg_color="#017bf5",
                             text_color="white",
                             height=50,
                             width=146
                             )
            l.grid(row=i, column=j, pady=2, padx=1)
        print(value)

    # Reminder time
    reminder_label_h = css.CTkLabel(master=data_view_section,
                                    text="Remind",
                                    fg_color="purple",
                                    text_color="white",
                                    height=50,
                                    width=80
                                    )
    reminder_label_h.grid(row=0, column=3, pady=2, padx=1)

    cursor.execute("select remindermin from deadline")
    rows = cursor.fetchall()
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row, start=3):
            l = css.CTkLabel(master=data_view_section,
                             text=value,
                             fg_color="#017bf5",
                             text_color="white",
                             height=50,
                             width=80
                             )
            l.grid(row=i, column=j, pady=2, padx=1)
        print(value)

    # DAYS left label in the dataview
    daysleft_h = css.CTkLabel(master=data_view_section,
                              text="Days left",
                              fg_color="purple",
                              text_color="white",
                              height=50,
                              width=100
                              )
    daysleft_h.grid(row=0, column=4, pady=2, padx=1)

    cursor.execute("select Deadline_date from deadline")
    rows = cursor.fetchall()

    # accessing the datetime module
    x = datetime.datetime.now()

    current_year = int(x.strftime("%Y"))
    current_month = int(x.strftime("%m"))
    current_day = int(x.strftime("%d"))

    colour = "#121312"
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row, start=4):
            current_date = str(current_year) + "/" + str(current_month) + "/" + str(current_day)
            print(value)

            # coverting to date format>>>>>>>>>>>>>>>>>>>>>>
            deadl_fin = x.strptime(value, "%Y/%m/%d")

            current_datefin = x.strptime(current_date, "%Y/%m/%d")

            # getting days left after subtracting the  current date from the deadline

            daysleft = deadl_fin - current_datefin
            cl = daysleft.days
            if cl > 3:
                colour = light
            elif cl >= 1 and cl <= 3:
                colour = "#9c4141"
            elif cl < 1 and cl <= -1:
                colour = "red"
                cl = str(daysleft.days) + " past"

            else:
                print("hello")

            l = css.CTkLabel(master=data_view_section,
                             text=cl,
                             fg_color=colour,
                             text_color="white",
                             height=50,
                             width=100
                             )
            l.grid(row=i, column=j, pady=2, padx=1)

    # Ellapsed label in the




#--------------------------------------------------------------------------------------------------------------------



#A Function that clears all data in entries to null

def clear_entries():

    courseUnitInput.delete(0,15)

    deadline_yearInput.delete(0,15)



    deadline_monthInput.delete(0,15)



    deadline_dayInput.delete(0,15)



    reminder_minute_Input.delete(0,15)

#-----------------------------------------------------------------------------------------------------------------------

# swapping to options of shutting down the computer
def power():
    coursework_frame.grid_forget()
    display_frame.grid_forget()
    others_frame.grid()
    others_frame.grid_propagate(False)
    power_btn.configure(fg_color="#434344")
    display_btn.configure(fg_color="#017bf5")
    about_us_btn.configure(fg_color="#017bf5")
    coursework_btn.configure(fg_color="#017bf5")


#-----------------------------------------------------------------------------------------------------------------------


def shutdown():
    return os.system("shutdown /s /hybrid")


def restart():
    return os.system("shutdown /r /t 1")


def hibernate():
    # return os.system("shutdown /h")
    return os.system("dxdiag")

#-----------------------------------------------------------------------------------------------------------------------
# NOTIFICATION
# Notify the user about the deadline of any course work
# def notify():
#     notification.notify(
#         title="      Networking course work    ",
#         message=f"""
#                 daysleft : {daysleft}     Hon Deus
#
#
#                 """
#     )
#     win.after(remind_min, notify)
#

# FUNCTION-----------------------------------------------------
win = css.CTk()
win.geometry("900x500")
win.title("Eyes Ug")
win.resizable(False, False)
# icons and images


# set Left side MASTER frame with options***************************************************
side_frame = css.CTkFrame(master=win, width=160, height=500, fg_color="white", corner_radius=0)
side_frame.configure(width=160, height=500)
side_frame.grid(row=0, column=0)
side_frame.columnconfigure(0, weight=1)
side_frame.rowconfigure(0, weight=1)
# side_frame.grid_propagate(False)
# widgets on the Left side frame
# display button
display_btn = css.CTkButton(master=side_frame, text="Display", corner_radius=0, width=160, height=120,
                            fg_color="#434344",
                            text_color="white",
                            hover_color="#272727",
                            # image=icon
                            command=display,
                            hover=False

                            )

# Course Work
coursework_btn = css.CTkButton(master=side_frame, text="Coursework", width=160, height=120,

                               text_color="white",
                               hover=False,
                               corner_radius=0,
                               command=coursework

                               )

# Power button
power_btn = css.CTkButton(master=side_frame, text="Power Options", width=160, height=120,
                          hover=False,
                          corner_radius=0,
                          command=power
                          )

# About us button
about_us_btn = css.CTkButton(master=side_frame, text="About us", width=160, height=141,
                             hover=False,
                             corner_radius=0)

# END OF LEFT SIDE FRAME***************************************************


# grid geometry for options of left side frame
display_btn.grid(row=0, column=0)
coursework_btn.grid(row=1, column=0)
power_btn.grid(row=2, column=0)
about_us_btn.grid(row=3, column=0)

# SET Right side MASTER frame with options***************************************
right_frame = css.CTkFrame(master=win, width=900, height=500, corner_radius=0)

# DISPLAY FRAME--------------------------------------------------DISPLAY FRAME
display_frame = css.CTkFrame(master=right_frame, width=800, height=500, fg_color="#434344", corner_radius=0)

# brightness label and slider>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
bright_label = css.CTkLabel(master=display_frame, text="Brightness", width=100, height=100, corner_radius=0,
                            text_color="white",
                            font=('Arial', 20)
                            )
bright_slider = css.CTkSlider(master=display_frame, height=20, from_=0, to=100, width=400,
                              hover=False,
                              command=change_brightness,

                              )

# sharpness label and slider>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
sharpness_label = css.CTkLabel(master=display_frame, text="Sharpness", width=100, height=100, corner_radius=0,
                               text_color="white",
                               font=("Apple", 20)
                               )
sharpness_slider = css.CTkSlider(master=display_frame, height=20, from_=0, to=100, width=400,
                                 # command=change_sharpness
                                 )

# Developer Name:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
dev_name_label = css.CTkLabel(master=display_frame, text="Developer : MUKIIBI DEUS ",
                              font=("Arial", 20),

                              text_color="#fff",
                              height=20)

# developer Contact>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
dev_no_label = css.CTkLabel(master=display_frame, text="Contact:+256702917121", height=20,
                            text_color="#fff"
                            )

# developer University
dev_university_label = css.CTkLabel(master=display_frame, text="University:Uganda Martyrs",
                                    text_color="#fff",
                                    height=20)

# COURSE WORK FRAME AND OPTIONS--------------------------------------------
coursework_frame = css.CTkFrame(master=right_frame,
                                fg_color=light,
                                width=900,
                                height=500,
                                corner_radius=False

                                )

# PAD ONE IN COURSE WORK >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
cousre_pad1 = css.CTkFrame(master=coursework_frame,
                           width=204,
                           height=180,
                           corner_radius=10,
                           fg_color="#434344"
                           )
cousre_pad1.grid(row=0, column=0, padx=20)
cousre_pad1.grid_propagate(False)
# Pad1 Title for Course work>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
cWorkTitle1 = css.CTkLabel(master=cousre_pad1,
                           text="Set deadline",
                           width=204,
                           height=30,
                           corner_radius=1,
                           fg_color="#017bf5",
                           text_color="white"
                           )
cWorkTitle1.grid(row=0, column=0, columnspan=4)
# COURSE UNIT NAME
course_unit_label = css.CTkLabel(master=cousre_pad1,
                                 fg_color="white",
                                 width=60,
                                 text="Course"
                                 )
course_unit_label.grid(row=1, column=0, pady=6)
# reminder input>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
courseUnitInput = css.CTkEntry(master=cousre_pad1, fg_color="white",
                               text_color="black",
                               width=142,
                               placeholder_text="course Name",
                               height=30
                               )
courseUnitInput.grid(row=1, column=1, padx=1, columnspan=3)
# pad deadline label for deadline inputs>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
deadline_label = css.CTkLabel(master=cousre_pad1,
                              width=60,
                              fg_color="white",
                              text="Deadline",
                              )
deadline_label.grid(row=2, column=0)

# DEAD LINE INPUTS ONE***********************************************SUBHEADING
# deadline year input>>>>>>>>>>>>>>>
deadline_yearInput = css.CTkEntry(master=cousre_pad1, fg_color="white",
                                  text_color="black",
                                  placeholder_text="year",
                                  width=50,
                                  height=30
                                  )
deadline_yearInput.grid(row=2, column=1)
# deadline month input>>>>>>>>>>>>>>>
deadline_monthInput = css.CTkEntry(master=cousre_pad1, fg_color="white",
                                   text_color="black",
                                   placeholder_text="month",
                                   width=49,
                                   height=30
                                   )
deadline_monthInput.grid(row=2, column=2)
# deadline month input>>>>>>>>>>>>>>>
deadline_dayInput = css.CTkEntry(master=cousre_pad1, fg_color="white",
                                 text_color="black",
                                 placeholder_text="day",
                                 width=40,
                                 height=30
                                 )
deadline_dayInput.grid(row=2, column=3)
# DEALINE REMINDER*******************************************SUBHEADING
reminder_label = css.CTkLabel(master=cousre_pad1,
                              fg_color="white",
                              width=60,
                              text="Reminder"
                              )
reminder_label.grid(row=3, column=0)
# reminder input>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
reminder_minute_Input = css.CTkEntry(master=cousre_pad1, fg_color="white",
                                     text_color="black",
                                     width=142,
                                     placeholder_text="minutes",
                                     height=30
                                     )
reminder_minute_Input.grid(row=3, column=1, pady=10, padx=1, columnspan=3)
# SAVE BUTTON>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
save_coursework_changes = css.CTkButton(master=cousre_pad1,
                                        text="Save",
                                        width=50,
                                        fg_color="#017bf5",
                                        command=getDeadlineDetailsPad1

                                        )
save_coursework_changes.grid(row=4, column=1)
# CANCEL BUTTON>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
exit_btn = css.CTkButton(master=cousre_pad1,
                         text="clear",
                         width=87,
                         fg_color="#017bf5",
                         command=clear_entries

                         )
exit_btn.grid(row=4, column=2, columnspan=2)
# CANCEL BUTTON>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#COURSE WORKPAD DONE***********************************************************************


#SEARCH FRAME
search_frame=css.CTkFrame(master=coursework_frame,
                          width=300,
                          height=100,
                          fg_color="gray"
                          )
search_frame.grid(row=0,column=1)
search_frame.grid_propagate(False)

#search Entry>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
search_entry=css.CTkEntry(master=search_frame,
                          placeholder_text="search course work",
                          height=30,
                          width=199,

                          )
search_entry.grid(row=0,column=0,pady=10)
#search Entry button in search frame
search_button=css.CTkButton(master=search_frame,
                            height=30,
                            width=80,
                            text="search"

                            )
search_button.grid(row=0,column=1,pady=10,padx=5)
search_entry.bind("<Key>",search_courseWork)

#Refresh button in coursework frame to repick data from the datbase implement new changes if present
refresh_data_view_section_coursework=css.CTkButton(master=search_frame,
                                                   text="Refresh",
                                                   command=refresh_data_view_section_coursework,
                                                   hover_color="#434344",
                                                   fg_color="purple",
                                                   width=80,
                                                   height=30

                                                   )
refresh_data_view_section_coursework.grid(row=1,column=1,pady=20)


# DATA VIEW FROM THE DATABASE____________________________





data_view_section=css.CTkScrollableFrame(master=coursework_frame,
                                         fg_color="#434344",
                                         height=290,
                                         width=710



                                 )
data_view_section.grid(row=2,column=0,columnspan=2,pady=10,padx=3)
#Entity Labels of the dataview(HEADERS)>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#courseName label in dataviewsction

course_name_h=css.CTkLabel(master=data_view_section,
                                text="Course Name",
                                fg_color="purple",
                                text_color="white",

                                height=50,
                                width=120
                                )
course_name_h.grid(row=0,column=0,pady=2,padx=1)


#courseName from database:
course=[]
cursor.execute("select courseName from deadline")
rows=cursor.fetchall()
for i,row in enumerate(rows,start=1):
    for j,value in enumerate(row):

        l = css.CTkLabel(master=data_view_section,
                         text=value,
                         fg_color="#017bf5",
                         text_color="white",
                         height=50,
                         width=120
                         )
        l.grid(row=i, column=j, pady=2,padx=1)
    print(value)




deadline_label_h=css.CTkLabel(master=data_view_section,
                              text="Deadline Date",
                              fg_color="purple",
                              text_color="white",
                              height=50,
                              width=146
                              )
deadline_label_h.grid(row=0,column=1)


#deadline label in dataviewsction
cursor.execute("select Deadline_date from deadline")
rows=cursor.fetchall()
for i,row in enumerate(rows,start=1):
    for j,value in enumerate(row,start=1):

        l = css.CTkLabel(master=data_view_section,
                         text=value,
                         fg_color="#017bf5",
                         text_color="white",
                         height=50,
                         width=146
                         )
        l.grid(row=i, column=j, pady=2,padx=1)
    print(value)

#SetDate label in dataviewsection

setDate_label_h=css.CTkLabel(master=data_view_section,
                                text="Set Date",
                                fg_color="purple",
                                text_color="white",
                                height=50,
                                width=146
                                )
setDate_label_h.grid(row=0,column=2,pady=2,padx=1)


cursor.execute("select SetDate from deadline")
rows=cursor.fetchall()
for i,row in enumerate(rows,start=1):
    for j,value in enumerate(row,start=2):

        l = css.CTkLabel(master=data_view_section,
                         text=value,
                         fg_color="#017bf5",
                         text_color="white",
                         height=50,
                         width=146
                         )
        l.grid(row=i, column=j, pady=2,padx=1)
    print(value)


#Reminder time
reminder_label_h=css.CTkLabel(master=data_view_section,
                                text="Remind",
                                fg_color="purple",
                                text_color="white",
                                height=50,
                                width=80
                                )
reminder_label_h.grid(row=0,column=3,pady=2,padx=1)


cursor.execute("select remindermin from deadline")
rows=cursor.fetchall()
for i,row in enumerate(rows,start=1):
    for j,value in enumerate(row,start=3):

        l = css.CTkLabel(master=data_view_section,
                         text=value,
                         fg_color="#017bf5",
                         text_color="white",
                         height=50,
                         width=80
                         )
        l.grid(row=i, column=j, pady=2,padx=1)
    print(value)





#DAYS left label in the dataview
daysleft_h=css.CTkLabel(master=data_view_section,
                                text="Days left",
                                fg_color="purple",
                                text_color="white",
                                height=50,
                                width=100
                                )
daysleft_h.grid(row=0,column=4,pady=2,padx=1)


cursor.execute("select Deadline_date from deadline")
rows=cursor.fetchall()

# accessing the datetime module
x = datetime.datetime.now()

current_year = int(x.strftime("%Y"))
current_month = int(x.strftime("%m"))
current_day = int(x.strftime("%d"))



colour="#121312"
for i,row in enumerate(rows,start=1):
    for j,value in enumerate(row,start=4):
        current_date = str(current_year) + "/" + str(current_month) + "/" + str(current_day)
        print(value)

        # coverting to date format>>>>>>>>>>>>>>>>>>>>>>
        deadl_fin = x.strptime(value,"%Y/%m/%d")

        current_datefin = x.strptime(current_date, "%Y/%m/%d")

        # getting days left after subtracting the  current date from the deadline

        daysleft = deadl_fin - current_datefin
        cl = daysleft.days
        if cl > 3:
            colour = light
        elif cl >= 1 and cl<=3:
            colour = "#9c4141"
        elif cl<1 and cl<=-1:
            colour = "red"
            cl=str(daysleft.days)+" past"

        else:
            print("hello")



        l = css.CTkLabel(master=data_view_section,
                         text=cl,
                         fg_color=colour,
                         text_color="white",
                         height=50,
                         width=100
                         )
        l.grid(row=i, column=j, pady=2,padx=1)


#Ellapsed label in the

#END OF THE COURSE WORK FRAME
#-----------------------------------------------------------------------------------------------------------------------



















# Grid geometry for right side frame with options


# OTHERS  BTN FRAME-------------------------------------------------------------------------------
others_frame = css.CTkFrame(master=right_frame,
                            width=700,
                            height=500,
                            fg_color="#191c1f",
                            corner_radius=False)

# others frame options
shutdwon_btn = css.CTkButton(master=others_frame, height=100, width=100, text="Shutdown",
                             fg_color="#ffd901",
                             text_color="black",
                             hover=False,

                             command=shutdown

                             )
restart_btn = css.CTkButton(master=others_frame, height=100, width=100, text="Restart",
                            fg_color="#036630", hover=False,
                            command=restart
                            )
hibernate_btn = css.CTkButton(master=others_frame, height=100, width=100, text="Hibernate",
                              fg_color="#032e66",
                              hover=False,
                              command=hibernate
                              )

# grid geometry options for the right side frame
# ---------------------------------------
right_frame.grid(row=0, column=1)
right_frame.grid_propagate(False)
# ---------------------------------------
# ---------------------------------------
display_frame.grid()
display_frame.grid_propagate(False)
# ----------------------------------------
bright_label.grid(row=0, column=0)
bright_slider.grid(row=0, column=1)
sharpness_label.grid(row=1, column=0)
sharpness_slider.grid(row=1, column=1)
dev_name_label.grid(row=2, column=0, columnspan=3, sticky="W", padx=40, pady=20)
dev_no_label.grid(row=3, column=0, columnspan=3, sticky="W", padx=40, pady=20)
dev_university_label.grid(row=4, column=0, columnspan=3, sticky="W", padx=40, pady=20)
# COURSE WORK FRAME AND OPTIONS--------------------------------------------
coursework_frame.grid()
# coursework_frame.grid_propagate(False)
# -----------------------------------------
others_frame.grid()
others_frame.grid_propagate(False)
# -----------------------------------------
shutdwon_btn.grid(row=1, column=0, padx=30, pady=160)
restart_btn.grid(row=1, column=1, padx=20, pady=160)
hibernate_btn.grid(row=1, column=2, padx=20, pady=160)

# NOTIFY FUNCTIONS
# notify()


win.mainloop()
connection.close()

