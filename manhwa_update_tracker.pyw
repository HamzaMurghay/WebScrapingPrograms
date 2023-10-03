# This program will check through a list of URLs that lead to the manhwas(which explained in the most simple way, are comics that update weekly) that I read and see if it has updated, if it has, it emails me to notify me (also maybe maybeeee planning to maybe make a pdf file with the chapter, mostly not tho, at least not now)

# Knowledge and Modules used: Web Scraping, handling and performing operations on date and time,Email messaging from python, finding error specifics using sys module, very basic HTML

from bs4 import BeautifulSoup  # From here
import requests
import datetime
import time  # To here is all the modules needed to carry out web extraction of data and time values in order to accurately make an update report

from email.message import EmailMessage  # From here to the next line is all modules to help carry out emailing
import smtplib

import sys  # This is to catch the line at which error has happened and return that value along with the reason, in the email that is sent regarding exception occurrence

manhwa_links = {'https://chapmanganato.com/manga-lm989347': ('https://www.mangago.me/read-manga/weak_hero/', 'https://i.pinimg.com/736x/cd/a0/89/cda089e15665ba44679530d800909c08.jpg'),
                'https://chapmanganato.com/manga-mp990098': ('https://www.mangago.me/read-manga/infinite_level_up_in_murim/', 'https://static.wikia.nocookie.net/koreanwebtoons/images/a/ae/Infinite_Leveling_Murim.jpg/revision/latest/scale-to-width-down/330?cb=20211112132206'),
                'https://chapmanganato.com/manga-de980813': ('https://www.mangago.me/read-manga/eleceed/', 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx106929-flAUvHZDUz5v.jpg'),
                'https://manganato.com/manga-sq995625': ('https://www.mangago.me/read-manga/juvenile_offender/', 'https://cdn.manhuaus.org/juvenile-offender/chapter-3/001.webp'),
                'https://chapmanganato.com/manga-mx989506': ('https://www.mangago.me/read-manga/the_knight_of_embers/', 'https://preview.redd.it/the-ember-knight-any-manhwa-manga-manhua-that-has-an-mc-v0-ltx33iqmyvmb1.png?width=640&crop=smart&auto=webp&s=9f38870bbaad7a2184c702129a44adae0a96f074'),
                'https://chapmanganato.com/manga-em981495': ('https://www.mangago.me/read-manga/spy_x_family/', 'https://resizing.flixster.com/oKZx6R0LR26Hy_-BwPxj05F3dsg=/ems.cHJkLWVtcy1hc3NldHMvdHZzZWFzb24vYWZmMjgxMzYtMjg5Yi00ZmVhLWEwYjctYmEyMmI4MTFjNzBjLnBuZw==')}

# This dictionary stores the links of 6 manhwa which I regularly follow and web scrapes the sites every day to see if it has updated or not, the key value contains the scrape link, where the info about the manhwa in specific is scraped, while the value tuple contains the link to the site where I usually read from and the image address to be used in the email when an update notification is sent
#  You can replace these links with manhwas of your own if you want to try this program out or if you have specific ones you want to track

present_month_abbrev, present_hour, present_min = datetime.datetime.now().strftime(
    "%b"), datetime.datetime.now().strftime("%H"), datetime.datetime.now().strftime(
    "%M")  # NOTE the strftime() works well, but it returns the time/date in the form of a string and not a datetime object, I'm mentioning this cuz I didn't realise at first
# Also "%b" gives you the abbreviated form of the month in text, as in "Sep" from "September", while "%B" would give you the whole "September", "%d" give you the date, but tbh you don't need to use datetime.now() for that, date.today().day works just as fine, but I used the former because it would be in the same format as the other two, so yeah...

present_datetime = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                     datetime.datetime.now().day, datetime.datetime.now().hour,
                                     int(datetime.datetime.now().strftime('%M')))

email_sender = "EMAIL_YOU_WANT_TO_SEND_UPDATES_FROM@examplesite.com"  # this can be a regularly used account or even a specially made account for you python emailing purposes
email_password = "IORU YWIU NCIU NOIU"  # This password is the app password of your email sending account that you need to specially get and put in this string, it is a 16-letter lowercase code generated only for the sending account specifically, you can find out how to make it by searching up yt videos (DISCLAIMER: the 16-letter code I've put in the string is not an actual code for someone, it is a placeholder and will not work, so please don't use it
email_receiver = "EMAIL_YOU_WANT_TO_RECIEVE_UPDATES_ON@examplesite.com"  # This would usually be your main account on which you want to receive updates


def establish_server_connection(sub, bod):
    email_message_info = EmailMessage()
    email_message_info['From'] = email_sender
    email_message_info['To'] = email_receiver
    email_message_info['Subject'] = sub
    email_message_info.set_content(bod, subtype='html')

    with smtplib.SMTP('smtp.gmail.com',
                      587) as smtp_server:  # essentially creates a smtp server for you to login and send emails from inputted account
        smtp_server.starttls()
        smtp_server.login(email_sender, email_password)
        smtp_server.sendmail(email_sender, email_receiver, email_message_info.as_string())


def check_for_update():
    for scrape_link, info_tuple in manhwa_links.items():
        page_raw = requests.get(scrape_link).text
        page_souped = BeautifulSoup(page_raw, 'lxml')

        manhwa_name = page_souped.find('div', class_="story-info-right").h1.text
        manhwa_new_chapter = page_souped.find('li', class_="a-h").a.text

        datetime_last_updated = page_souped.find('span', class_='chapter-time text-nowrap')['title']
        time_last_updated_dtobject = datetime.datetime.strptime(datetime_last_updated, '%b %d,%Y %H:%M')
        time_since_updated = present_datetime - time_last_updated_dtobject
        max_time_left_unchecked = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 23, 00, 00) - datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 11, 00, 00)

        hour_min_seconds_when_last_updated_list = str(time_since_updated).split(',')[len(str(time_since_updated).split(','))-1].split(':')  # Stores the hours and minutes ago when the manhwa was updated in the form of a list, so if manhwa was updated 5 hours 37 minutes ago then the list is in the form of ['05', '37', '00']
        if time_since_updated <= max_time_left_unchecked:  # Checks if the manhwa was updated more than 12 hours ago,(Its physically not possible for the manhwa to go unchecked if the program has run every 12 hours, that's why max time is 12 hrs) and since if it was it will not say it has a new update because if it did then it would repeat what it already said in the previous check 12 hours ago
            print(f"\nNew update for '{manhwa_name}' [{hour_min_seconds_when_last_updated_list[0].strip()} hours {hour_min_seconds_when_last_updated_list[1]} minutes ago]")
            subject = f'{manhwa_name} Update Notice'
            body = f'''
<!DOCTYPE html>
    <html>
        <body>
            <div style="background-color:#eee;padding:10px 20px;">
                <center>
                    <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349,text-align:center;">{manhwa_name} Has Updated!</h2>
                <center>
            </div>
            <div style="padding:20px 0px">
                <div style="height: 500px;width:400px">
                    <center>
                        <img src={info_tuple[1]} style="height: 300px;">
                    </center>
                    <div style="text-align:left;">
                        <p>This email is to notify you that <strong>{manhwa_name}</strong> has updated with <strong>{manhwa_new_chapter}</strong> of its publication as of <br>[{hour_min_seconds_when_last_updated_list[0].strip()} hours {hour_min_seconds_when_last_updated_list[1]} minutes] since the sending of this email!!</p>
                        <a href="{info_tuple[0]}">Click Here To Read</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
'''
            establish_server_connection(subject, body)
            print("Email Sent!\n")
        else:
            print(f'No new updates for "{manhwa_name}" yet')


if __name__ == '__main__':
    while True:
        try:
            check_for_update()
        except:
            exception_occurrence_line = sys.exc_info()[2].tb_next.tb_lineno  # Finds the last line due to which exception occurred
            exception_occurred_reason = sys.exc_info()[1]
            subject_err = "Program Exception Occurrence"
            body_err = f"""
<!DOCTYPE html>
    <html>
        <body>
            <p>This email is to notify you that your Manga Update Tracking Program has returned an error on line no. {exception_occurrence_line}!</p><br>         
            <p>The reason for error is as follows: <br>{exception_occurred_reason}</p>
        </body>
    </html>
"""
            establish_server_connection(subject_err, body_err)
            print(f"An Exception has Occurred! on line {exception_occurrence_line}")
            print("Email regarding error has been sent!\n")

        one_hour = 3600
        print(f"\nWaiting for 12 hours to scrape again....[Last checked at {present_hour}:{present_min}]\n")
        time.sleep(one_hour * 12)

# Still debating to add the ability for it to be an extension

# from time import strptime
# strptime('Feb','%b').tm_mon  # Returns the month number of the specific month abbreviation entered as first argument
