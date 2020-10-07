import requests
import pprint
from bs4 import BeautifulSoup as bs4
import re

fetchingAddress = "https://www.datawallet.com/"
infoSupport = fetchingAddress + "/whats-a-datawallet/"
pagescrapped = requests.get(fetchingAddress)
#print(pagescrapped.content)
subscriptionExists = ['PRICING', 'SUBSCRIPTION']
pageSoup = bs4(pagescrapped.content, "html.parser")
#print(pageSoup.prettify)
routeAddress = [a.get("href") for a in pageSoup.find_all("a")]
#print(routeAddress)

for i in routeAddress:
    val = re.match("^https:.*?\/careers$", i)
    if val:
        careerRoute = val.group(0)

# supporting email address
#pageSupport = bs4((requests.get(careerRoute)).content, "html.parser")
# if loop condition
companyName = pageSoup.find("meta", property="og:site_name")["content"]
#print(companyName)
pageTitle = pageSoup.find("meta", property="og:title")["content"]
#print(pageTitle)
shortDescription = pageSoup.find("meta", property="og:description")["content"]
#print(shortDescription)
pageSupport = bs4((requests.get(infoSupport)).content, "html.parser")
summaryData = (pageSupport.find_all("main"))[0].get_text()
with open("summary1.txt", "w") as file:
    file.write(summaryData)
#print(summaryData)
headerMenu = pageSoup.find_all("a", {'href': '/pricing'})[-1].get_text()
checkPaidService = ""
for i in subscriptionExists:
    if re.match(i, headerMenu, re.IGNORECASE):
        checkPaidService = "Paid"
print(checkPaidService)
exit()
contactEmail = (pageSupport.find_all("div", class_="icon envelope-icon"))[0].get_text()
contactEmail = contactEmail.strip()
print(contactEmail)
#print(summaryData)




