from selenium import webdriver
import time
import sys
# Import smtplib for the actual sending function
import smtplib

print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])
print(sys.argv[4])


class CourtBooker:
    driver = None

    def __init__(self, username=sys.argv[1], password=sys.argv[2], email=sys.argv[3], epassword=sys.argv[4]):
        self.username = username
        self.password = password
        self.email = email
        self.epassword = epassword
        self.set_up()
        self.log_in(self.username, self.password)
        self.find_court()
        self.clean_up()

    def set_up(self):
        self.driver = webdriver.Chrome()

    def clean_up(self):
        self.driver.close()

    def log_in(self, username, password):
        self.driver.get('https://www.smartclubcloud.com')
        elem = self.driver.find_element_by_xpath("//form[@class='form-vertical login-form']//input[@name='username']")
        elem.clear()
        elem.send_keys(username)
        elem2 = self.driver.find_element_by_xpath("//form[@class='form-vertical login-form']//input[@name='password']")
        elem2.clear()
        elem2.send_keys(password)

        button = self.driver.find_element_by_xpath("//button[@id='loginButton']")
        button.click()
        self.driver.implicitly_wait(3)

    def find_court(self):

        bookings_tab = self.driver.find_element_by_xpath('//a[contains(text(), \'Bookings\')]')
        bookings_tab.click()

        self.driver.implicitly_wait(3)

        book_now = self.driver.find_element_by_xpath('//input[@value=\'Book Now\']')
        book_now.click()

        self.driver.implicitly_wait(3)

        date_selector = self.driver.find_element_by_xpath(
            '//input[@class=\'BookingDateTextBox ui-rangepicker-input ui-widget-content\']')
        date_selector.click()
        day = self.driver.find_element_by_xpath('//a[contains(text(), \'Thursday\')]')
        day.click()

        time.sleep(5)

        view_courts = self.driver.find_element_by_xpath("//input[@value=\"View Courts\"]")

        courtA = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[11]/div[9]")
        titleA = courtA.get_attribute("title")
        print("Court A: " + titleA)

        court5 = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[7]/div[9]")
        title5 = court5.get_attribute("title")
        print("Court 5: " + title5)

        while titleA == 'This slot falls outside of the booking window.' \
                or title5 == 'This slot falls outside of the booking window.':
            courtA = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[11]/div[9]")
            titleA = courtA.get_attribute("title")
            print("Court A: " + titleA)
            court5 = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[7]/div[9]")
            title5 = court5.get_attribute("title")
            print("Court 5: " + title5)
            if titleA != 'This slot falls outside of the booking window.' \
                    and title5 != 'This slot falls outside of the booking window.':
                break
                print("Courts open")
            else:
                print('Trying again')
                view_courts.click()
                time.sleep(5)

        courtC = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[13]/div[9]")
        titleC = courtC.get_attribute("title")
        print("Court C: " + titleC)

        court6 = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[8]/div[9]")
        title6 = court6.get_attribute("title")
        print("Court 6: " + title6)

        court5 = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[7]/div[9]")
        title5 = court5.get_attribute("title")
        print("Court 5: " + title5)

        courtB = self.driver.find_element_by_xpath("//*[@id=\"CourtsGrid\"]/div[12]/div[9]")
        titleB = courtB.get_attribute("title")
        print("Court B: " + titleB)

        if 'Book this slot' in titleA:
            courtA.click()
            time.sleep(3)
            self.make_booking('court A')
        elif 'Book this slot' in titleC:
            courtC.click()
            time.sleep(3)
            self.make_booking('court C')
        elif 'Book this slot' in title6:
            court6.click()
            time.sleep(3)
            self.make_booking('court 6')
        elif 'Book this slot' in title5:
            court5.click()
            time.sleep(3)
            self.make_booking('court 5')
        elif 'Book this slot' in titleB:
            courtB.click()
            time.sleep(3)
            self.make_booking('court B')
        else:
            print(titleA)
            print(titleB)
            print(titleC)
            print(title5)
            print(title6)
            print('No courts available')
            self.send_email('No courts available to be', self.email, self.epassword)

    def make_booking(self, string):

        status = self.driver.find_element_by_xpath("//div[@id=\"AllocationSummaryDetailsDiv\"]").text

        if "Invalid" not in status:
            select_players = self.driver.find_element_by_xpath(
                "//div[@id='PlayerDropDownDiv']//button[@class=\"ui-multiselect ui-multiselect-selectionsummary ui-corner-all\"]")
            select_players.click()
            time.sleep(1)
            brian = self.driver.find_element_by_xpath("//input[@title='Brian Macartney']")
            brian.click()
            campbell = self.driver.find_element_by_xpath("//input[@title='Campbell Dunn']")
            campbell.click()
            robert = self.driver.find_element_by_xpath("//input[@title='Robert Bell']")
            robert.click()
            print("Booked!!!")
            self.send_email(string, self.email, self.epassword)
        else:
            print("Court already booked")
            self.send_email('Court already', self.email, self.epassword)

    @staticmethod
    def send_email(string, email, epassword):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(email, epassword)
        s.sendmail(email, email, string + ' booked')
        s.quit()


CourtBooker()
