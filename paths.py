#these are all the Xpath values for the html elements needed to access to place twitch predictions
#also 2 physical location paths
Paths= {
    "chromeProfile": 'C:/Users/Lachl/AppData/Local/Google/Chrome/User Data',
    "chromeDriver": 'C:/Users/Lachl/Desktop/Twitch_Channel_Point_bot/chrome/chromedriver.exe',
    
    "pointsClaim": '//*[@id="root"]/div/div[1]/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button',
    "pointButton": '//*[@id="root"]/div/div[1]/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[1]/div[2]/button',
    "predictionButton": '//*[@id="channel-points-reward-center-body"]/div/div/div[1]/div/button',
    "predictionTitle": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[1]/p[1]',
    "predictionStatus": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[1]/p[2]',
    "predictionOption1": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/p',
    "predictionOption2": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/p',
    "predictionCustomAmount": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[3]/div[2]/button',
    "predictionInput1": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[3]/div[1]/div/div/div[1]/div/div/div/input',
    "predictionInput2": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/input',
    "predictionOption1Button": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[3]/div[1]/div/div/div[1]/div/div/button',
    "predictionOption2Button": '//*[@id="channel-points-reward-center-body"]/div/div/div/div/div/div/div[3]/div[1]/div/div/div[2]/div/div/button',

    "opggTable": "/html/body/div[1]/div[6]/div",
}

accepted_terms_yes = ["win", "yes", "yeah", "ye", "ofc", "ofcourse","yep", "yup", "surely"]
accepted_terms_no = ["loss", "lose", "no","nah","noppers", "nop"]