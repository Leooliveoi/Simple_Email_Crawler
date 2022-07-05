''' Email Crawler :) using BeautifulSoup and Regular Expression '''

import sys
import re
import requests # pip install requests
from bs4 import BeautifulSoup # pip install bs4

TO_CRAWL = []
CRAWLED = set()
EMAILS = []
URL_INIT = ""
FILENAME = "_Emails.txt"

def saveFile():
    try:
        '''EMAIL SAVE'''
        count = 0
        print("\nDONE, THE EMAIL CRAWLING IS FINISHED")
        with open(FILENAME, "a") as file:
            file.write("===> " + URL_INIT + " <===\n")
            for email in EMAILS:
                line = "\nEmail: {}; \n".format(email)
                file.write(line)
                count += 1

            file.write("\n\n")
            if count != 0 :
                print("Find {} E-mails".format(count))
            else:
                print("no E-mail Found")
        print("File save as: "+FILENAME)
    except Exception as e:
        print("Error in saveFile(),", e)


def urlVerify(url):
    try:
        if url[:7] == "http://":
            first = url[:7]
            second = url[7:]
        elif url[:8] == "https://":
            first = url[:8]
            second = url[8:]
        elif url[:8] != "https://" or url[:7] != "http://":
            url = "http://"+url

        URL_INIT = url

        return url
    except Exception as e:
        print("Error in urlVerify(),", e)


def requestVerify(url):

    try:
        urlfinal = urlVerify(url)

        header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
        response = requests.get(urlfinal, headers=header)
        html = response.text
        return html

    except KeyboardInterrupt:
        print("======= User Interrupt =======")
        saveFile()
        sys.exit(0)

    except:
        pass


def getEmail(html):
    try:
        #Regex101.com
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", html)
        return emails
    except TypeError:
        print("Error in getEmail(), Verify Your URL sintax")
        pass

    except Exception as e:
        print("Error in getEmail(),", e)


def emailCraw(emails):
    try:
        for email in emails:
            if email not in EMAILS:
                EMAILS.append(email)
                print(email)
    except Exception as e:
        print("Error in emailCraw(),",e)
        pass


def getLinks(html):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tag_a = soup.findAll("a", href=True)
        for tag in tag_a:
            link = tag["href"]
            if link.startswith("http"):
                links.append(link)

        return links
    except TypeError:
        print("Error in getLinks(), Verify Your URL sintax")
        pass
    except Exception as e:
        print("Error in getLink(),", e)


def linkCraw(links):
    try:
        for link in links:
            if link not in CRAWLED and link not in TO_CRAWL:
                TO_CRAWL.append(link)
    except Exception as e:
        print("Error in linkCraw(),",e)
        pass


def craw():
    while True:
        try:
            if TO_CRAWL:
                url = TO_CRAWL.pop()
                html = requestVerify(url)
                links = getLinks(html)
                emails = getEmail(html)

                if links:
                    linkCraw(links)
                if emails:
                    emailCraw(emails)

                CRAWLED.add(url)
                print("Crawling {}".format(url))

            else:
                saveFile()
                break
        except Exception as e:
            print("Error in Craw(),", e)
            sys.exit(0)


if __name__ == "__main__":
    try:

        if len(sys.argv) >= 2:
            url = sys.argv[1]
            URL_INIT = url
            TO_CRAWL.append(url)
            craw()
        else:
            url = "example.com"
            URL_INIT = url
            TO_CRAWL.append(url)
            craw()
    except Exception as e:
        print(e)

