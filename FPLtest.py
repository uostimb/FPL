from selenium import webdriver
from twilio.rest import Client
import secrets  # Comment this out if not using separate secrets file!

# Change debug = True to show browser (False hides it offscreen) and prevent sending an twilio SMS on error
debug = False

# Change the below to test a winning postcode, we'll still try to login using the real "our_postcode"
debug_winning_postcode = None

our_postcode = secrets.postcode # Your FPL postcode
our_email = secrets.email # Your FPL email address

account_sid = secrets.account_sid # Your twilio account SID
auth_token = secrets.auth_token # Your twilio auth token
number_from = secrets.number_from # Your twilio number from
number_to = secrets.number_to # Your twilio number to

client = Client(account_sid, auth_token)

if debug_winning_postcode:
    our_postcode = debug_winning_postcode

print("Postcode = {}".format(our_postcode))

def open_and_login():
    browser = webdriver.Firefox()
    if debug:
        browser.set_window_position(2000, 0) # put browser on second monitor for dev and test
        our_postcode = secrets.postcode # Need to use our real postcode to log in, regardless of debug_winning_postcode
    else:
        browser.set_window_position(-2000, 0) # put browser offscreen for production
    browser.implicitly_wait(70) # Need to wait this long for the 1min video draw advert to finish
    browser.get("https://freepostcodelottery.com")

    # Looks like FPL are A/B Testing a new front page!
    try:
        print("Attempting to login to new front page")
        openloginform = browser.find_element_by_link_text("Sign in")
        openloginform.click()
        email = browser.find_element_by_xpath("/html/body/div[@id='modal-signin']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body']/section[@id='sign-in']/div[@class='sign-in']/form[@class='ui-form']/div[@class='email form-group']/input[@id='confirm-email']")
        email.send_keys(our_email)
        postcode = browser.find_element_by_xpath("/html/body/div[@id='modal-signin']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body']/section[@id='sign-in']/div[@class='sign-in']/form[@class='ui-form']/div[@class='postcode form-group']/input[@id='confirm-ticket']")
        postcode.send_keys(our_postcode)
        submit_button = browser.find_element_by_xpath("/html/body/div[@id='modal-signin']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body']/section[@id='sign-in']/div[@class='sign-in']/form[@class='ui-form']/button[@class='btn btn-info btn-loader']")
        submit_button.click()
        print("Logged in OK")

    except:
        print("Couldn't login to new front page")
        print("Attempting to login to old front page")
        login_postcode = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='landing-wrapper']/div[@class='ui-curve'][1]/section[@class='sign-in']/form[@id='signup-top']/div[@class='form-group '][1]/input[@id='postcode']")
        login_postcode.send_keys(our_postcode)
        login_email = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='landing-wrapper']/div[@class='ui-curve'][1]/section[@class='sign-in']/form[@id='signup-top']/div[@class='form-group '][2]/input[@id='email']")
        login_email.send_keys(our_email)
        form = browser.find_element_by_id("signup-top")
        form.submit()
        print("Logged in OK")

    finally:
        return browser


def main_draw(browser):
    maindraw_postcode = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/div[@class='main-content']/div[@class='main-content-inner']/main[@class='content-centered']/section[@id='result']/div[@class='result ui-box box-info box-result no-radius-xs-down']/div[@class='ui-box-header result-header']/p[@class='postcode']").text
    print()
    print("Main draw: {}".format(maindraw_postcode))
    if our_postcode in maindraw_postcode:
        wintext = "**WINNER WINNER CHICKEN DINNER!!** Won FreePostCodeLottery Main Draw! {}".format(maindraw_postcode)
        print(wintext)
    else:
        wintext = ""
    return wintext


def video_draw(browser):
    browser.get("https://freepostcodelottery.com/video")
    video_click = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/div[@class='main-content']/div[@class='main-content-inner']/main[@class='content-centered']/section[@id='result']/div[@class='result ui-box box-info box-result no-radius-xs-down']/div[@class='video-container loaded']/div[@id='jwPlayer']//div[@class='jw-controls jw-reset']/div[@class='jw-display jw-reset']/div[@class='jw-display-container jw-reset']/div[@class='jw-display-controls jw-reset']/div[@class='jw-display-icon-container jw-display-icon-display jw-reset']")
    video_click.click()
    videodraw_postcode = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/div[@class='main-content']/div[@class='main-content-inner']/main[@class='content-centered']/section[@id='result']/div[@class='result ui-box box-info box-result no-radius-xs-down']/div[@id='result-header']/div[@class='ui-box-header result-header']/p[@class='postcode']").text
    print()
    print("Video draw: {}".format(videodraw_postcode))
    if our_postcode in videodraw_postcode:
        wintext = "**WINNER WINNER CHICKEN DINNER!!** Won FreePostCodeLottery Video Draw! {}".format(videodraw_postcode)
        print(wintext)
    else:
        wintext = ""
    return wintext


def survey_draw(browser):
    browser.get("https://freepostcodelottery.com/survey-draw/")
    try:
        surveydraw_postcode = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/div[@class='main-content']/div[@class='main-content-inner']/main[@class='content-centered']/section[@id='result']/div[@class='result ui-box box-info box-result no-radius-xs-down']/div[@id='result-header']/div[@class='ui-box-header result-header']/p[@class='postcode']").text
    except:
        show_postcode = browser.find_element_by_link_text("No thanks, show me the winning postcode")
        show_postcode.click()
        surveydraw_postcode = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/div[@class='main-content']/div[@class='main-content-inner']/main[@class='content-centered']/section[@id='result']/div[@class='result ui-box box-info box-result no-radius-xs-down']/div[@id='result-header']/div[@class='ui-box-header result-header']/p[@class='postcode']").text
    print()
    print("Survey draw: {}".format(surveydraw_postcode))
    if our_postcode in surveydraw_postcode:
        wintext = "**WINNER WINNER CHICKEN DINNER!!** Won FreePostCodeLottery Survey Draw! {}".format(surveydraw_postcode)
        print(wintext)
    else:
        wintext = ""
    return wintext


def stackpot_draw(browser):
    browser.get("https://freepostcodelottery.com/stackpot/")
    stackpot_postcodes = browser.find_elements_by_class_name("postcode")
    print()
    wintext = ""
    for i in stackpot_postcodes:
        print("Stackpot draw: {}".format(i.text))
        if our_postcode in i.text:
            wintext = "**WINNER WINNER CHICKEN DINNER!!** Won FreePostCodeLottery Stackpot! {}".format(i.text)
            print(wintext)
    return wintext


def bonus_draw(browser):
    browser.get("https://freepostcodelottery.com/your-bonus/")
    ten_pound = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/section[@id='banner-bonus']/div[@class='banner-inner']/div[@class='draws']/div[@class='draw-five draw draw-result']/div[@class='draw-inner']/div[@class='ui-box-header result-header']/p[@class='postcode']").text
    twenty_pound = browser.find_element_by_xpath("/html/body/div[@class='main-container']/div[@id='main-wrapper']/section[@id='banner-bonus']/div[@class='banner-inner']/div[@class='draws']/div[@class='draw-ten draw draw-result']/div[@class='draw-inner']/div[@class='ui-box-header result-header']/p[@class='postcode']").text
    print()
    print("bonus draw: {}".format(ten_pound))
    print("bonus draw: {}".format(twenty_pound))
    if our_postcode in ten_pound or our_postcode in twenty_pound:
        wintext = "**WINNER WINNER CHICKEN DINNER!!** Won FreePostCodeLottery Bonus Draw! {} {}".format(ten_pound, twenty_pound)
        print(wintext)
    else:
        wintext = ""
    return wintext


try:
    browser = open_and_login()
    won_text = main_draw(browser)
    won_text += video_draw(browser)
    won_text += survey_draw(browser)
    won_text += stackpot_draw(browser)
    won_text += bonus_draw(browser)

    print()

    if won_text:
        print("WINNER!! - Sending SMS Notification: {}".format(won_text))
        # send twilio SMS
        message = client.messages.create(
            to=number_to,
            from_=number_from,
            body=won_text)
        print(message.sid)
    else:
        print("No winners for {} today :(".format(our_postcode))

except Exception as e:
    fail_text = "Error in FPL Selenium Script! - '{}' Line#:{}".format(e, e.__traceback__.tb_lineno)
    print("ERROR! Sending Error SMS - {}".format(fail_text))
    if not debug:
        # send twilio SMS
        message = client.messages.create(
            to=number_to,
            from_=number_from,
            body=fail_text)
        print(message.sid)

finally:
    if browser:
        browser.quit()
