#import dependancies
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

#importing my files
import paths,streams,webscraping

#sets up the webdriver
def webdriver_setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("user-data-dir=" + paths.Paths["chromeProfile"])
    driver = webdriver.Chrome(executable_path = paths.Paths["chromeDriver"],chrome_options=chrome_options)
    return driver


#creates the driver browser with all streams opened 
def initial_web_setup(driver):
    #opens all streams detailed in the streams tab
    for streamer in streams.Streams:
        driver.switch_to.new_window('tab')
        driver.get("https://www.twitch.tv/popout/" + streamer + "/chat?popout=")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, paths.Paths["pointButton"])))
    #closes the initial tab created as a consequence of our loop    
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

#formats points from 1k to 1000 etc.
def get_and_format_points(button):
    points = button.text
    if "K" in points:
        points = (float(points.split("K")[0])) * 1000
    elif "M" in points:
        points = (float(points.split("M")[0])) * 1000000 
    return int(points)

def get_stream_name_from_URL(driver):
    url = str(driver.current_url)
    url = url.split("/")
    streamer = url[-2]  
    return streamer

#check if there is an active prediction event by searching for button xpath
def check_active_prediction(driver):
    try:
        streamer = get_stream_name_from_URL(driver)
        button = driver.find_element(By.XPATH,paths.Paths["predictionButton"])
    except Exception as e: 
        print("there is no active prediction on " + streamer)
        return False
    else:
        print("there is an active prediction on "+ streamer)
        return True

    
def live_prediction_data_scraper(driver, predictionButton):
    try:
        predictionButton.click()
        title = driver.find_element(By.XPATH,paths.Paths["predictionTitle"])
        status = driver.find_element(By.XPATH,paths.Paths["predictionStatus"])
        option1 = driver.find_element(By.XPATH,paths.Paths["predictionOption1"])
        option2 = driver.find_element(By.XPATH,paths.Paths["predictionOption2"])
    except Exception as e:
        print("could not resolve prediction values")
        print("prediction may have closed or may have more than 2 fields")
        return False
    else:
        return title.text, status.text, option1.text, option2.text
    
#defines if the prediction falls into a few categories we bet for
#win/loss , amount of deaths, amount of kills
def prediction_classifier(title, option1, option2):
    #checks for "win" in title or options
    if "win" in option1.lower() or "win" in option2.lower():
        return "win/loss"
    if "win" in title.lower():
        return "win/loss"

def data_scraper(driver):
    streamer = get_stream_name_from_URL(driver)
    try:
        driver.switch_to.new_window('tab')
        driver.get(streams.Streams[streamer])
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, paths.Paths["opggTable"])))
        time.sleep(5)
        html = driver.page_source 
        data = pd.read_html(html)
        blue_team = data[0]
        red_team = data[1]

    except Exception as e:
        print("FAILED TO FIND OPGG TABLES IN SCRAPING ATTEMPT")
        print("following exception was raised: ")
        print(e)
        driver.close()
        return False
    else:
        driver.close()
        return blue_team, red_team, streamer


def check_for_term_in_option(terms, option):
    for x in terms():
        if x in option.lower():
            return True
    return False

#this checks which option contains the yes or win option to the win loss bet
# returning 1 means option 1 is the "win" string or yes to the question do they win
def win_option_finder(driver):
    option1 = driver.find_element(By.XPATH,paths.Paths["predictionOption1"]).text
    option2 = driver.find_element(By.XPATH,paths.Paths["predictionOption2"]).text

    #return option 1 contains yes
    if check_for_term_in_option(paths.accepted_terms_yes, option1):
        return "1"
    if check_for_term_in_option(paths.accepted_terms_no, option2):
        return "1"
    #return option 2 contains yes
    if check_for_term_in_option(paths.accepted_terms_yes, option2):
        return "2"
    if check_for_term_in_option(paths.accepted_terms_no, option1):
        return "2"

    #return false if the parser cannot resolve the nature of the options
    return False

#returns 1 or 2 depending on what option should be bet on
def compare_results(predictionBool, win_option):
    if predictionBool:
        return win_option
    else:
        if win_option == 1:
            return "2"
        if win_option == 2:
            return "1"

def cast_prediction(driver, option, bet_amount):
    option1Field = driver.find_element(By.XPATH,paths.Paths["predictionInput" + option])
    option1Field.send_keys(bet_amount)
    option1SubmitButton = driver.find_element(By.XPATH,paths.Paths["predictionOption" + option + "Button" ])
    option1SubmitButton.click()
    print("BET PLACED ON OPTION " + option +  "FOR " + bet_amount )


def main():
    driver = webdriver_setup()
    initial_web_setup(driver)
    try:
        while True:
            for window_handle in driver.window_handles:
                driver.switch_to.window(window_handle)
                
                button = driver.find_element(By.XPATH, paths.Paths["pointButton"])
                channelPoints = get_and_format_points(button)
                button.click()

                #if there is a prediction field active (if check_live_prediction returned true)
                if check_active_prediction(driver):
                    predictionButton = driver.find_element(By.XPATH,paths.Paths["predictionButton"])
                    
                    #check to see if the prediction data scraping failed
                    if live_prediction_data_scraper(driver, predictionButton) == False:
                        continue
                    title, status, option1, option2 = live_prediction_data_scraper(driver, predictionButton)
                    
                    #if the prediction is currently open
                    if "Submissions closing in" in status:

                        #classify what kind of prediction we have
                        predictionType = prediction_classifier(title, option1, option2)
                        #select bet with a custom amount
                        custom_prediction = driver.find_element(By.XPATH,paths.Paths["predictionCustomAmount"])
                        custom_prediction.click()
                        
                        #if the prediction is of type win/loss
                        if predictionType == "win/loss":
                            scraping_result = data_scraper(driver)
                            win_option = win_option_finder(driver)

                            #guard clauses for if either scraping operator fails
                            if scraping_result == False:
                                button.click()
                                continue
                            if win_option == False:
                                print("the options could not be understood resulting in the bet being skipped")
                                continue

                            blue_team = scraping_result[0]   
                            red_team = scraping_result[1]
                            streamer = scraping_result[2]
                            predictionBool = webscraping.win_loss_prediction_answer(blue_team,red_team,streamer)

                            #guard clause to prevent non parsed result

                            bet_amount = "100"
                            optionToBet = compare_results(predictionBool, win_option)
                            cast_prediction(driver, optionToBet, bet_amount)

                    #else the prediction is closed or is awaiting results
                    else:
                        print("status of the bet is not currently open: " + status)

                #click the points button again to close it so the next loop can open it again
                driver.switch_to.window(window_handle)
                button = driver.find_element(By.XPATH, paths.Paths["pointButton"])
                button.click()

            #once it finishes checking each channel for a prediction it will rest for 45 seconds
            time.sleep(45)

    except KeyboardInterrupt:
        print("interrupted")
    finally:
        driver.close()

if __name__ == "__main__":
    main()