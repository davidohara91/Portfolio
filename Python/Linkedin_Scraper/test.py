from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = "davidohara91@gmail.com"
password = "hRElp1eDF#UYSFkK$1cOMufi0Up2nc"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
job = Job("https://www.linkedin.com/jobs/search/?currentJobId=3829279648&f_E=2%2C3%2C4&geoId=104738515&location=Ireland&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&spellCorrectionEnabled=true", driver=driver, close_on_complete=False)
