import re
import csv
import sys
import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from fb_common_friends_secrets import FB_USR, FB_PWD, CSV_FILE, GECKO_PATH

VERSION = "0.1"
BANNER = """
fffffff.py v. {0} - Banner
by sowdust
""".format(VERSION)


def pause(min=2,max=5):
    return round(random.uniform(min,max),1)


def check_login(driver,usr,pwd):
    driver.get('https://www.facebook.com/settings')

    if 'login' in driver.current_url:

        print('[!] Not logged in.')
        driver.get("http://www.facebook.org")
        assert "Facebook" in driver.title
        print('[*] Trying to log in with user %s' % usr)
        elem = driver.find_element_by_id("email")
        elem.send_keys(usr)
        elem = driver.find_element_by_id("pass")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        print(driver.current_url)
        print('[*] Logged in')


def get_friends(driver,usr1,usr2, url='https://www.facebook.com/browse/mutual_friends/?uid=%s&node=%s'):

    friends = []
    final_url = url % (usr1,usr2)
    print('[*] Trying to retrieve url %s' % final_url)
    time.sleep(pause())
    driver.get(final_url)
    
    try:
        users = driver.find_elements_by_css_selector("div[class='fsl fwb fcb']")
        for user in users:
            s = user.get_attribute('innerHTML')
            uid = re.findall('/ajax/hovercard/user.php\?id=([0-9]*)(?:"|&amp;)',s)
            url = re.findall('href=[\'"]?([^\'" >]+)',s)
            name = re.findall('>[.*]?([^<]+)',s)
            friend = {}
            friend['name'] = name[0]
            friend['id'] = uid[0]
            friend['url'] = url[0]
            if friend not in friends:
                friends.append(friend)
            else:
                print('[*] User %s already in friends' % name)
    except Exception as ex:
        print('[!] Error! %s' % ex)

    return friends


def parse_args():

    parser = argparse.ArgumentParser(description='Recursively build friend list of Facebook users using the "common friends" utility.')
    parser.add_argument('-t', '--target', metavar='target', type=int, help='facebook id of target', required=True)
    parser.add_argument('-f','--friends', nargs='+', type=int, help='initial friends or users to start with', required=True)
    parser.add_argument('-u', '--user', metavar='user', type=str, help='facebook username')
    parser.add_argument('-p', '--password', metavar='password', type=str, help='facebook password')
    parser.add_argument('-c','--csv-output', metavar='output', type=str, help='output csv file path', required=True)
    #parser.add_argument('-j','--json-output', metavar='output', type=str, help='output csv file path')
    parser.add_argument('-d','--driver-path', metavar='output', type=str, help='path to geckodriver.exe')
    parser.add_argument('-q', '--headless', action='store_true', help='headless browser mode')
    args = parser.parse_args(args=None if len(sys.argv) > 1 else ['--help'])

    return args


def main():

    print(BANNER)
    args = parse_args()

    # read and set main variables

    if not args.target:
        print('[!] Error. You must specify the ID of the target Facebook profile')
        sys.exit(0)

    driver_path = args.driver_path if args.driver_path  else GECKO_PATH
    usr = args.user if args.user else FB_USR
    pwd = args.password if args.password else FB_PWD
    csv_file_path = args.csv_output if args.csv_output else CSV_FILE
    target = args.target

    # output and working vars
    friends_found = []
    tested = []
    to_test = args.friends # [] # TODO: read from input

    # start browser
    options = Options()
    if args.headless: options.add_argument("-headless")
    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(executable_path=driver_path)

    check_login(driver,usr,pwd)
    
    # fetch and write friends
    print('[*] Fetching friends of target user %d' % target)
    start = time.time()

    with open(csv_file_path, mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        fieldnames = ['id', 'name', 'url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while to_test:
            fid = to_test.pop()

            count_new = 0
            count_old = 0

            for g in get_friends(driver,target,fid):

                # add all new friends to pivot points
                if g['id'] not in tested and g['id'] not in to_test:
                    to_test.append(g['id'])

                # add all new friends to the complete list 
                if g not in friends_found:
                    count_new += 1
                    friends_found.append(g)
                    writer.writerow(g)

            csv_file.flush()

            tested.append(fid)
            print("[*] Found %d new and %d old friends pivoting on %s" % (count_new,count_old,fid))
            print(" ")
            print("    Tested:   %d" % len(tested))
            print("    Found:    %d" % len(friends_found))
            print("    To test:  %d" % len(to_test))
            print(" ")

    end = time.time()
    print(end - start)

    print(' ')
    print('[*] Found a total of %d friends in %.2f' % ( len(friends_found), (end-start)*1000))
    for f in friends_found:
        print('[%s]\t%s\t%s' % (f['id'],f['name'],f['url']))


if __name__ == '__main__':
    main()




