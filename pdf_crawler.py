from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import platform, time

EXE_PATH_OS={'Windows':'./lib/chromedriver.exe', 'Darwin':'./lib/chromedriverMac'}
DIR_TMP_PDF='./tmp_pdf/'
lib_path=EXE_PATH_OS[platform.system()]

course_link = 'https://performancemanager.successfactors.eu/sf/learning?destUrl=https%3a%2f%2fsaplearninghub%2eplateau%2ecom%2flearning%2fuser%2fdeeplink%5fredirect%2ejsp%3flinkId%3dITEM%5fDETAILS%26componentID%3dCP100%5fEN%5fCol04%26componentTypeID%3de%2dbook%26revisionDate%3d1357992000000%26fromSF%3dY&company=learninghub'
explicit_wait_time = 30
implicit_wait_time = 30

def log_in(driver, wait_time):
    #log in the elearing system, only works for SSO user
    li = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
    )
    li.click()
    button = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.ID, "subBtn"))
    )
    button.click()

def initilize(course_link, exe_path, wait_time):
    driver = webdriver.Chrome(executable_path=exe_path)
    driver.get(course_link)
    driver.implicitly_wait(wait_time)
    return driver

def open_book(driver, wait_time):
    iframe_outter = driver.find_element_by_xpath("//iframe[@name='iframelearning']")
    driver.switch_to.frame(iframe_outter)
    print("Swith to iframelearing")
    button_continue = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,':_button')]"))
    )
    print("Click on button conitnue")
    driver.execute_script("arguments[0].click();", button_continue)
    

    driver.switch_to.default_content()
    iframe_outter = driver.find_element_by_xpath("//iframe[@name='iframelearning']")
    driver.switch_to.frame(iframe_outter)
    print("Switch to iframe frmpmod")
    WebDriverWait(driver, wait_time).until(EC.frame_to_be_available_and_switch_to_it("frmpmod"))
    #Switch to the iframe twice to ensure that they are selected
    driver.switch_to.frame("iframelearning")
    driver.switch_to.frame("frmpmod")

    div = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.ID, "placemat"))
    )
    print("Find the placement div")
   
    link = div.find_element_by_xpath("//span/a")
    link.click()
    #Wait for the new window open
    for x in range(0, 10):
        if len(driver.window_handles) > 1:
            break
        time.sleep((wait_time / 10))
    driver.switch_to.window(driver.window_handles[1])

    try:
        button_cancel = driver.find_element_by_id('btnCancel-content')
        button_cancel.click()
    except:
        pass

def merge_pdfs(basedir, pages, output):
    #make sure the base dir exsits
    if not os.path.exists(basedir):
        os.mkdir(dir)

    pages = pages + 1
    paths = list(map(lambda x:str(basedir + str(x) + '.pdf'), range(1, pages)))

    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def clear_tmp_dir(basedir):
    for filename in os.listdir(basedir):
        if filename.endswith('.pdf'):
            os.unlink(filename)

if __name__ == '__main__':
    try:
        driver = initilize(course_link, lib_path, implicit_wait_time)
        log_in(driver, explicit_wait_time)
        open_book(driver, explicit_wait_time)
        
        page = driver.find_element_by_id("inputPageNo-inner")
        page.clear()
        page = driver.find_element_by_id("inputPageNo-inner")
        page.send_keys('50')
        page.send_keys(Keys.RETURN)
    finally:
        #driver.quit()
        print('Please quit manually')
