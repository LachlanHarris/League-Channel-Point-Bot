from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
#importing my files
import paths,streams,webscraping

def webdriver_setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir=" + paths.Paths["chromeProfile"])
    driver = webdriver.Chrome(executable_path = paths.Paths["chromeDriver"],chrome_options=chrome_options)
    return driver

#creates the driver browser with all streams opened 
def initial_web_setup(driver):
    for x in streams.Streams:
        driver.switch_to.new_window('tab')
        driver.get("https://www.twitch.tv/popout/" + x + "/chat?popout=")
        elem = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, paths.Paths["pointButton"] )))
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

def get_and_format_points(button):
    points = button.text
    #formats points from 1k to 1000 etc.
    if "K" in points:
        points = (float(points.split("K")[0])) * 1000
    elif "M" in points:
        points = (float(points.split("M")[0])) * 1000000
    #I do not handle Billion formatting because idk if you get a B also if you have a billion points just stop    
    return int(points)
    
def prediction_time_formatter(time):
    # Split the time into hours, minutes, and seconds
    minutes, seconds = time.split(":")

    # Convert the time to seconds
    total_seconds = int(minutes) * 60 + int(seconds)

    return total_seconds

#check if the current bet has a live prediction
def check_live_prediction(driver):
    try:
        button = driver.find_element(By.XPATH,paths.Paths["predictionButton"])
    except Exception as e: 
        print("there is no active prediction")
        print("causing the following exception (this is expected):")
        print(e)
        return False
    else:
        print("there is an active prediction")
        return True
    
def live_prediction_data_scraper(driver, predictionButton):
    predictionButton.click()
    title = driver.find_element(By.XPATH,paths.Paths["predictionTitle"])
    status = driver.find_element(By.XPATH,paths.Paths["predictionStatus"])
    option1 = driver.find_element(By.XPATH,paths.Paths["predictionOption1"])
    option2 = driver.find_element(By.XPATH,paths.Paths["predictionOption2"])
    return title.text, status.text, option1.text, option2.text
    
#defines if the prediction falls into a few categories we bet for
#win/loss , amount of deaths, amount of kills
#more should be added but for now this is all we will handle

#TODO: implement amount of deaths, amount of kills
def prediction_classifier(title, option1, option2):
    #WIN LOSS HANDLERS
    #if win is either option
    if "win" in option1.lower() or "win" in option2.lower():
        return "win/loss"
    #if win is in the title
    if "win" in title.lower():
        return "win/loss"

def scraper(driver):
    url = driver.current_url()
    url = url.split("/")
    streamer = url[-2]

    driver.get(streams.Streams[streamer])
    elem = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, paths.Paths["opggTable"])))

    html = driver.page_source
    soup = BeautifulSoup(html)
    data = pd.read_html(html)
    blue_team = data[0]
    red_team = data[1]

    driver.close()

    IGN = streams.Streams[streamer].split("/")
    IGN = IGN [-2]
    winner = webscraping.find_winner(blue_team, red_team)
    teamOfStreamer = webscraping.find_team_of_streamer(blue_team, red_team, IGN)

    if winner == teamOfStreamer:
        return True
    else:
        return False


    
def main():
    driver = webdriver_setup()
    initial_web_setup(driver)
    try:
        while True:
            
            for window_handle in driver.window_handles:
                driver.switch_to.window(window_handle)
                #sits for 2 seconds at a tab before starting
                time.sleep(2)
                button = driver.find_element(By.XPATH, paths.Paths["pointButton"])
                channelPoints = get_and_format_points(button)
                button.click()
                
                #if there is a prediction field active (if check_live_prediction returned true)
                if check_live_prediction(driver):
                    predictionButton = driver.find_element(By.XPATH,paths.Paths["predictionButton"])
                    title, status, option1, option2 = live_prediction_data_scraper(driver, predictionButton)
                    
                    #if the bet is Currently open
                    if "Submissions closing in" in status:
                        #classify what kind of prediction we have
                        predictionType = prediction_classifier(title, option1, option2)
                        #select bet with a custom amount
                        custom_prediction = driver.find_element(By.XPATH,paths.Paths["predictionCustomAmount"])
                        custom_prediction.click()
                        
                        #THIS SECTION IS ABLE TO CALCULATE SECONDS LEFT IF WE WANT TO SLEEP THE PROGRAM AND WAIT TILL THE LAST SECOND TO BET
                        #CURRENTLY NOT IMPLEMENTED 
                        #gets the time string
                        #prediction_remaining_time = status.split("Submissions closing in")[1]
                        #turns the time string from MM:SS to just seconds
                        #prediction_remaining_time = prediction_time_formatter(prediction_remaining_time)
                        #print(prediction_remaining_time)
                        
                        
                        
                        if predictionType == "win/loss":
                            #find_winner()
                            #TESTING ALWAYS BETTING ON OPTION 1 WITH 100 points

                            result = scraper(driver)
                            #THIS RETURNS TRUE IF YOU SHOULD VOTE YES FALSE IF NO
                            #THIS IS WHERE I WAS UP TO 
                            #IMPLEMENT CHECKING OPTIONS AND BETTING
                            
                            option1Field = driver.find_element(By.XPATH,paths.Paths["predictionInput1"])
                            option1Field.send_keys('100')
                            
                            option1SubmitButton = driver.find_element(By.XPATH,paths.Paths["predictionOption1Button"])
                            option1SubmitButton.click()
                            
                        elif predictionType == "deaths":
                            print("asdasd")
                        elif predictionType == "kills":
                            print("asdasd")
                        
                    
                    #else the bet is closed or is awaiting results
                    else:
                        print("status of the bet is not currently open: " + status)
            #once it finishes checking each channel for a prediction it will rest for 2 minutes
            time.sleep(120)
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        driver.close()

if __name__ == "__main__":
    main()