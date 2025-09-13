# Set the second parameter of core() 'False' to make it CLI based.
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Auto-installation of the chromedriver.


def convert_durations_to_seconds(values):
    result = []
    for v in values:
        v = v.strip()  # remove leading/trailing spaces
        parts = v.split(":")

        # handle mm:ss vs hh:mm:ss
        if len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        else:
            total_seconds = None  # invalid format

        result.append(total_seconds)
    return result


def target_count(driver_):
    """Gets the total number of videos in the playlist using X-Path"""
    videos_count = driver_.find_element(
        By.XPATH, "//span[@role='text' and normalize-space()='Playlist']/following::span[@role='text'][1]"
    )
    return int(videos_count.text.split(" ")[0])


def scroll_until_videos_loaded(driver_, tc=-1, pause=3):
    # jugaad as we weren't able to use tc=target(driver) in the parameters itself
    if tc == -1:
        tc = target_count(driver_)
    last_count = 0
    while True:
        # find all current durations
        elems_ = driver_.find_elements(By.CSS_SELECTOR, "#time-status span#text")

        # break if we reached target
        if len(elems_) >= tc:
            return elems_, tc

        # scroll down a bit more
        ActionChains(driver_).scroll_by_amount(0, 100000).perform()
        time.sleep(pause)

        # if no new videos were loaded after scrolling, break
        if len(elems_) == last_count:
            print("No more new videos are loading.")
            return elems_, tc
        last_count = len(elems_)


def core(user_input, print_to_console=False):
    """Set the argument to True to make it print the information to the CLI"""

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    # Automatically downloads & uses the right ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.youtube.com")
    time.sleep(3)
    # Searches the query
    search_bar = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
    search_bar.send_keys(user_input)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)

    # Clicks on the top playlist
    top_playlist = driver.find_element(By.XPATH, "//yt-lockup-view-model//a[text() = 'View full playlist']")
    url = top_playlist.get_attribute('href')
    top_playlist.click()  # Way 1, or we can directly get the playlist url using get_attribute('href') then open a new browser, hectic....
    time.sleep(3)
    title = driver.find_element(By.CSS_SELECTOR, "h1.dynamicTextViewModelH1 span").text
    creator = driver.find_element(By.CSS_SELECTOR, ".yt-page-header-view-model__page-header-headline-info .yt-core-attributed-string__link").get_attribute("textContent")

    time.sleep(3)

    output = scroll_until_videos_loaded(driver)
    elems = output[0]
    total_videos = int(output[1])

    # Very important as we're using the search technique instead of directly passing the video link, due to that, we are
    # getting some extra values, be it using any selector. In order to filter those extra values, I am using split_index
    # It subtracts the extra valued list with the actual, to get the exact number of extras (initials only), Finally indexing from the trues values only.

    split_index = len(elems) - total_videos

    texts = [i.get_attribute("textContent").split("\n")[1].strip() for i in elems[split_index:]]
    result = round(sum(convert_durations_to_seconds(texts)) / 3600, 2)

    driver.quit()

    if print_to_console:
        print(f"Top Playlist Name: {title} | Creator: {creator} |  URL: {url}")
        print(f"Total number of videos {len(texts)}")
        print(texts)
        print(f"Total Duration of the course: {result} hours.")


    return title, creator, url, texts, result


if __name__ == "__main__":
    try:
        core(input("Enter your course query: "), True)
    except:  # Too broad exception term.
        print("Sorry, some problem occurred, please check your inputs. ")
    finally:
        print("----------------------------End-------------------------------")
