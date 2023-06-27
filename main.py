import requests
from bs4 import BeautifulSoup

default_url = "https://artsci.calendar.utoronto.ca/search-courses?course_keyword=&field_breadth_requirements_value=All&field_distribution_requirements_value=All&field_prerequisite_value=&field_section_value=All&page="
num_range = 169  # change back to 169


course_objects = []


class Course:  # to create a new course object that stores code, course name, and reverse prerequisites
    def __init__(self, course_code, course_name, rev_prereq):
        self.course_code = course_code
        self.course_name = course_name
        self.rev_prereq = rev_prereq

    def __repr__(self):  # gives class objects a name
        return self.course_code


for num in range(num_range + 1):
    soup = BeautifulSoup(requests.get(default_url + str(num)).content,
                         'html.parser')
    title = soup.find_all('h3')
    for item in title:
        # course_names.append(item.find("div").text[13:])  # course names
        # course_codes.append(item.find("div").text[2:8])  # course codes

        course_code = item.find("div").text[2:8]
        course_name = item.find("div").text[13:]

        course_objects.append(Course(course_code, course_name, []))

# print(course_codes)
# print(course_names)

# print(soup.prettify())  to make the html stuff more readable


default_url_prereq = "https://artsci.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=All&field_prerequisite_value=&field_breadth_requirements_value=All&field_distribution_requirements_value=All"

for course in course_objects:  # loop through every course
    url = default_url_prereq[:116] + course.course_code + default_url_prereq[116:]  # update url for course code
    soup = BeautifulSoup((requests.get(url)).content, 'html.parser')
    title = soup.find_all('h3')  # gives me a list of all tags containing h3

    prereqs = []  # to store the reverse prereqs for this course

    link = None  # initiate link with none

    # check if there are more pages
    find_last_button = soup.find('li', {'class': 'w3-button pager__item pager__item--last'})  # operates on 'url'.
    if find_last_button is not None:
        title_1 = find_last_button
        link = title_1.find('a')['href']
        # if valid, link will store: ?course_keyword=&field_section_value=All&field_prerequisite_value=MAT137&field_breadth_requirements_value=All&field_distribution_requirements_value=All&page=1

    if link is None:  # if there are no more new pages (there only exists one page of prerequisites)

        for item in title:  # loop through every prerequisite
            find_div = item.find("div")
            if find_div is not None:
                course_code = find_div.text[2:8]
                course_name = find_div.text[13:]

                for courses in course_objects:  # loop through every course object. If course object matches, append it to the courses
                    if courses.course_code == course_code:
                        prereqs.append(courses)  # append course object

            # save prereqs to course object prereq parameter

    else:  # there exists an additional page of prerequisites, we need to loop through every page
        number = int(link[-1])

        # number will start with 0.
        for num in range(number + 1):

            # update url from 'url'.
            new_url = url + '&page=' + str(num)

            soup = BeautifulSoup((requests.get(new_url)).content, 'html.parser')
            title = soup.find_all('h3')  # gives me a list of all tags containing h3

            for item in title:  # loop through every prerequisite
                find_div = item.find("div")
                if find_div is not None:
                    course_code = find_div.text[2:8]
                    course_name = find_div.text[13:]

                    for courses in course_objects:  # loop through every course object. If course object matches, append it to the courses
                        if courses.course_code == course_code:
                            prereqs.append(courses)  # append course object

    course.rev_prereq = prereqs

    print(course.course_code)
    print(course.course_name)
    print(course.rev_prereq)


# # finding the last page:
# a_url = "https://artsci.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=All&field_prerequisite_value=MAT137&field_breadth_requirements_value=All&field_distribution_requirements_value=All"
# soup = BeautifulSoup((requests.get(a_url)).content, 'html.parser')
# # print(soup.prettify())
# find_last_button = soup.find('li', {'class': 'w3-button pager__item pager__item--last'})
# if find_last_button is not None:
#     title = find_last_button
#     print(title.find('a')['href'])
#
# # prints: ?course_keyword=&field_section_value=All&field_prerequisite_value=MAT137&field_breadth_requirements_value=All&field_distribution_requirements_value=All&page=1
