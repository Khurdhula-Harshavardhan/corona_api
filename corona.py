#Import the library files we need.
import urllib.request,urllib.error 
import requests
import re
from string import punctuation
from datetime import date
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


#the main class that will do web scraping for us.
class Corona_data :
    url=str()
    response=dict()
    place=str()
    states=list()
    data=str()
    core=list()
    mapper=dict()
    result=dict()
    #Will use constructor to initialize required features/parameters.
    def __init__(self):
        self.url="https://www.mohfw.gov.in/"
        self.response["Source"]="Govt.OF IND"
        self.response["API HOST"]="Khurdhula Harshavardhan"
        self.response["Status"]="Success"
        self.states=[
            "Andaman and Nicobar Islands",
            "Andhra Pradesh",
            "Arunachal Pradesh",
            "Assam",
            "Bihar",
            "Chandigarh",
            "Chhattisgarh",
            "Dadra and Nagar Haveli and Daman and Diu",
            "Delhi",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jammu and Kashmir",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Ladakh",
            "Madhya Pradesh",
            "Maharashtra",
            "Manipur",
            "Meghalaya",
            "Mizoram",
            "Nagaland",
            "Odisha",
            "Puducherry",
            "Punjab",
            "Rajasthan",
            "Sikkim",
            "Tamil Nadu",
            "Telangana",
            "Tripura",
            "Uttarakhand",
            "Uttar Pradesh",
            "West Bengal"
        ]


        #creating mapper :
        for state in self.states :
            self.mapper[state.replace("\t","")]=state.lower().replace(" ","").replace("\t","")

    #function of manipulate and check the validity of the input to get correct results.
    def search(self,location) :
        if  " " in location and location.strip(" ").isalnum() :
            e={"Status":"Failed","Error":"Invalid State"}
            return e
        elif " " in location or "%20" in location :
                
                #cross check the gaurdian pattern.
                if "%20" in location:
                    location=location.replace("%20", " ")

                #irrespective of %20 due to browser the following code should work.
                words = list()
                words=location.split(" ")
                for word in words :
                    if word.lower() != "and" :
                        index = words.index(word)
                        words.remove(word)
                        word=word.strip(punctuation).capitalize()
                        words.insert(index,word)
                    self.place=" ".join(words)
                if self.place in self.states :
                    ans=self.download()
                    return ans
                else :
                    e={"Status":"Failed","Error":"Invalid State"}
                    return e
        else :
                #this logic is for states which dont have spaces or such characters in b/w.
                self.place=location.capitalize()
                if self.place in self.states :
                    ans=self.download()
                    return ans
                else :
                    e={"Status":"Failed","Error":"Invalid State"}
                    return e

    #i had to write this for some reason strip and re.sub were not doing the job for me..
    def clean(self,data):
        cleaned = data.replace(" ","")
        cleaned = cleaned.replace("\n","")
        cleaned=cleaned.replace("\t","")
        del data
        return cleaned

    #Fucntion to download and parse html code.
    def download(self) :
        #Downloading to Required page onto our API
        try :
            self.data=urllib.request.urlopen(self.url,context=ctx).read().decode()
            features = re.findall("<tr>(.+)</tr>",self.clean(self.data))
            ans=self.structure(features[0])
            return ans
        except Exception as e :
            ex={"Status":"Failed","Error":str(e)}
            return ex

    def structure(self,raw_table) :
        try :
            raw_table=raw_table.replace("<td>"," ")
            raw_table=raw_table.replace("</td>"," ")
            raw_table=raw_table.replace("<tr>"," ")
            raw_table=raw_table.replace("<tbody>","\n")
            raw_table=raw_table.replace("</tr>","\n")
        
            #now have to split it.
            self.core=raw_table.split("\n")

            #Further filtering, the data.
            for line in self.core :
                if " " in line and not 'strong' in line :
                    register = line.lower().replace("\t","").split(" ")
                    for element in register :
                        if len(element) == 0  :
                            index = register.index(element)
                            register.pop(index)
                    self.result[register[1]]=register[2:]

            ans=self.buildResponse()
            return ans
        except :
            e={"Status":"Failed","Error":"Failed to filter data to extract core."}
            return e

    #final function to build response.
    def buildResponse(self) :
        try :
            #build place
            self.response["Place"]=self.place

            #build active cases
            self.response["Active Cases"]=(self.result[self.mapper[self.place]])[0]

            #build recovered cases
            self.response["Recovered Cases"]=(self.result[self.mapper[self.place]])[1]

            #build deaths
            self.response["Deaths"]=(self.result[self.mapper[self.place]])[2]


            #build total confirmed cases
            self.response["Total Cases"]=(self.result[self.mapper[self.place]])[3]
            

            #build updated date 
            self.response["Last Updated"]=date.today()

            #finally we have our required request.
            return self.response
        except:
            e={"Status":"Failed","Error":"Failed to build a response."}
            return e

    #this function is used to test the accuracy of the api.
    def test(self) :
        count=0
        Failures=0
        Successes=0

        while count!=1000 :
            for item in self.states :
                count+=1
                if count==1000 :
                    break
                if (self.search(item))["Status"] is "Failed" :
                    print("Response : ",(self.search(item))["Status"])
                    print("Place stored : ",self.place)
                    print("Mapper stored it as : ",self.mapper.get(item,"Mapper is failing you"))
                    #print("Result stored it as : ",self.result.get(item, "Result is failing you"))
                    print("\n\n")
                    Failures+=1
                else :
                    if count==1000 :
                        break
                    Successes+=1
                    print("SUCCESSFUL ATTEMPT : %d"%(count))
                    print(self.response,"\n")
                
        
        print("COMPLETED TEST : \nTotal Requests Made : %d\nTotal Failed Requests : %d\nTotal Successful Requests : %d\nAPI Accuracy= %f percent!"%(count,Failures,Successes,float((Successes/count)*100)))


            
    


            
            