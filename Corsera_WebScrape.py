# This is a program that will return all the courses related to Data Engineering in Coursera in the form of a text file on your computer,it will run once every 24 hours once started, you are also given the ability to filter the courses based on the skills you specifically want to learn

from bs4 import BeautifulSoup
import requests
import time

print("The skills you enter will all be taken into consideration, so if you put two skills this program will return the courses where BOTH of those skills are taught\n")
# also be wary for typos while entering skill names, this program does not counter skill typos
# you can even enter a word of the skill you have so like, just "machine" can give you courses which have 'machine learning' in them, however only do this if you are sure that that word is a certainty to be there in the skills taught, as in if machine learning was possible to be said in another way without the word 'machine' then this is not advised

skills_sought = []  # List that will store all the skills that the user is looking to learn
skill_sought = ''  # This will be our input variable, we will take inputs and store it in the above list and then change this variable again when asking for new input
while not skill_sought == 'none':
    skill_sought = input("(If nothing more then type 'none') What skill do you seek to learn? >").lower()
    skills_sought.append(skill_sought)
print()  # in order to leave one line of space between input and output, USED ONLY IF YOU WANT TO PRINT OUTPUT IN TERMINAL AND NOT IN TEXT FILE


def get_courses():
    page_info_raw = requests.get('https://www.coursera.org/courses?query=data%20engineering').text  # Notice how we put the page request after the input, this is to ensure that if the user inputs their skills late by mistake, the information on the requested page is not outdated, cuz if we request data first and then ask user, then say after 5 hours that info will be outdated
    page_info_souped = BeautifulSoup(page_info_raw, "lxml")
    courses_list = page_info_souped.find_all('li', class_='cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76')

    for course in courses_list:
        skill_in_course_count = 0
        course_skills_gained = course.find('p', class_='cds-119 css-dmxkm1 cds-121').text.split(':')[1].strip().split(',')
        for skill_want in skills_sought:
            if skill_want == 'noen':  # used to remove any typos made while typing "none", it happened to me quite a lot while typing, so I put it in
                skills_sought.remove('noen')
                break
            elif len(skills_sought) == 1:
                break
            else:
                for skill_present in course_skills_gained:
                    if skill_want in skill_present.lower():
                        skill_in_course_count += 1
                        break
                    # print(skills_sought,skill_in_course_flag,skill_want,skill_present,course_skills_gained)  # you can use this to understand the functionality of this whole nested for loop and if shit

        if skill_in_course_count == len(skills_sought) - 1 or len(skills_sought) == 1:
            course_name = course.h3.text

            course_infocard_RR = course.find('div', class_='cds-CommonCard-ratings')  # Extracts info card containing reviews and ratings
            course_rating = course_infocard_RR.find('p', class_='cds-119 css-11uuo4b cds-121').text
            course_reviews = course_infocard_RR.find('p', class_='cds-119 css-dmxkm1 cds-121').text

            course_infocard_LD = course.find('div', class_='cds-CommonCard-metadata').text  # Gets the info card of the course containing course level and duration

            course_level, course_duration = course_infocard_LD.split("Â·")[0], course_infocard_LD.split("Â·")[2]  # The reason we have put "Â·" as the split argument is because when
            # we extract course.info card_LD and print it for a given course, the output comes out as this: Beginner Â· Professional Certificate Â· 3 - 6 Months, so that's why we put "Â·"
            # Also we are multi-defining here since we are basically getting the values from same place, so for better code readability and shit we define both variables at once

            course_link = course.find('a')['href']
            course_link = "https://www.coursera.org" + course_link

            with open(f"Courses_WebScraped/{course_name}.txt", 'w') as c:
                c.write(f"Course Name: {course_name} \n \n")
                c.write(f"Course Rating: {course_rating}/5 [Reviewed by {course_reviews.split()[0].strip('(')} Users] \n")  # we put split here because the original course reviews is in the form of "(10k Reviews)", so we remove the 'Reviews' word using split, and we remove the hanging "(" bracket by using strip, otherwise the print comes as "Reviewed by (10k Users", see the hanging bracket?
                c.write(f"Suited for: {course_level}level\n")
                c.write(f"Duration:{course_duration} \n \n")
                c.write("Skills to be Gained:\n")
                for i in range(len(course_skills_gained)):
                    if i % 3 == 0:
                        c.write("\n")
                    if i == len(course_skills_gained) - 1:
                        c.write(f"{course_skills_gained[i].strip()} \n")
                        break
                    c.write(f"{course_skills_gained[i].strip()},")
                c.write(f"\nCourse link: {course_link}\n")
                c.write("-----------------------------------------------------------------------------------------")
            print(f"Course Found: {course_name}")
        else:
            continue

    if skill_in_course_count != len(skills_sought) - 1:
        print("\nNo Such Courses Found!")


if __name__ == '__main__':
    while True:
        get_courses()
        wait_minutes = 3600
        print(f"\nWaiting for one day to scrape again....")
        time.sleep(wait_minutes * 24)
