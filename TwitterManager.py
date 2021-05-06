from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
import datetime

hashtag="request for startup"


class Twitter:
    def __init__(self, hashtag):
        self.profile=webdriver.ChromeOptions()
        self.profile.add_experimental_option('prefs',{'intl.accept_languages':'en,en_US'})
        self.browser=webdriver.Chrome("chromedriver.exe",chrome_options=self.profile)
        self.browser.maximize_window()
  
        self.hashtag=hashtag
        self.tweetlist=[]
        self.datelist=[]
        self.usernamelist=[]
        self.likelist=[]
        self.retweetlist=[]
        self.discussionlist=[]



        

    def searchKey(self,hashtag):
        self.browser.get("https://twitter.com/explore")
        time.sleep(5)
        keySearch=self.browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input')
        keySearch.send_keys(hashtag)
        time.sleep(1)
        keySearch.send_keys(Keys.ENTER)
        time.sleep(5)

    def webPage(self):
        tweet= self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[1]/div[1]") 
            
        for tweets in tweet: 
                
            self.tweetlist.append(tweets.text)

                
        date=self.browser.find_elements_by_xpath('//div[@data-testid="tweet"]/div[2]/div[1]/div[1]/div[1]/div[1]/a/time')
            
        for dates in date :
            self.datelist.append(dates.get_attribute('datetime'))
    
        username=self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/a/div[1]/div[2]/div[1]/span")
            
        for usernames in username:
            self.usernamelist.append(usernames.text)

        like=self.browser.find_elements_by_xpath('//div[@data-testid="like"]/div[1]/div[2]/span')
            
        for likes in like :
            self.likelist.append(likes.text)
            
        retweet=self.browser.find_elements_by_xpath('//div[@data-testid="retweet"]/div[1]/div[2]/span')

        for retweets in retweet:
            self.retweetlist.append(retweets.text)

        discussions=self.browser.find_elements_by_xpath('//div[@data-testid="reply"]/div[1]/div[2]/span')

        for discussion in discussions:
            self.discussionlist.append(discussion.text)




    def getTweet(self):

        Twitter.webPage(self)

        last = self.browser.execute_script("return document.documentElement.scrollHeight")

        self.browser.implicitly_wait(5)

 
        while True:
    
            self.browser.execute_script("window.scrollTo(0,(document.documentElement.scrollHeight));")
            time.sleep(5)
        
            Twitter.webPage(self)
        

        
            self.browser.implicitly_wait(5)

            new = self.browser.execute_script("return document.documentElement.scrollHeight")


            if last == new:
                break

            last = new
       




    def logger(self):
    
        data = []
        for i  in  range(len(self.usernamelist)):

            if (self.likelist[i]==""):
                self.likelist[i]=0
            elif "K" in self.likelist[i]:
                self.likelist[i]=float(self.likelist[i].replace("K"," "))*1000
            elif "M" in self.likelist[i]:
                self.likelist[i]=float(self.likelist[i].replace("M"," "))*1000000
            else:
                self.likelist[i]=float(self.likelist[i])

            if self.retweetlist[i]=="":
                self.retweetlist[i]=0
            elif "K" in self.retweetlist[i]:
                self.retweetlist[i]=float(self.retweetlist[i].replace("K"," "))*1000
            elif "M" in self.retweetlist[i]:
                self.retweetlist[i]=float(self.retweetlist[i].replace("M"," "))*1000000
            else:                
                self.retweetlist[i]=float(self.retweetlist[i])

            if  self.discussionlist[i]=="":
                self.discussionlist[i]=0
            elif "K" in self.discussionlist[i]:
                self.discussionlist[i]=float(self.discussionlist[i].replace("K"," "))*1000
            elif "M" in self.discussionlist[i]:
                self.discussionlist[i]=float(self.discussionlist[i].replace("M"," "))*1000000
            else:
                self.discussionlist[i]=float(self.discussionlist[i])



            


            self.datelist[i]=datetime.datetime.strptime(self.datelist[i],'%Y-%m-%dT%H:%M:%S.000Z')


            dictdate = {'id':i+1,'tweet':self.tweetlist[i],'date':self.datelist[i], 
            'username':self.usernamelist[i], 'like':self.likelist[i],
            'retweet':self.retweetlist[i], 'discussion':self.discussionlist[i]}
            data.append(dictdate)
        
        data1=sorted(data, key=lambda d: d["like"],reverse=True)
        data2=sorted(data, key=lambda d: d["retweet"],reverse=True)
        data3=sorted(data, key=lambda d: d["discussion"],reverse=True)
        data4=sorted(data, key=lambda d: d["date"],reverse=True)
        
        with open ("tweetlist.json", "w" ,encoding="utf-8")  as f:
            json.dump(data,f,ensure_ascii=False ,indent=4,default=str)

        with open ("tweetlistlike.json", "w" ,encoding="utf-8")  as f:
            json.dump(data1,f,ensure_ascii=False ,indent=4,default=str)

        with open ("tweetlistretweet.json", "w" ,encoding="utf-8")  as f:
            json.dump(data2,f,ensure_ascii=False ,indent=4,default=str)
            
        with open ("tweetlistdiscussion.json", "w" ,encoding="utf-8")  as f:
            json.dump(data3,f,ensure_ascii=False ,indent=4,default=str)

        with open ("tweetlistdate.json", "w" ,encoding="utf-8")  as f:
            json.dump(data4,f,ensure_ascii=False ,indent=4,default=str)
            
            
        


