from bs4 import BeautifulSoup
from .MatchAttributes import find_the_elements_by_event,xpath_soupreq
from .FindXpath import *
import requests
import json
import sys
def get_the_analysis(bot_id,multiple_element):
    found=False
    message=""
    send_bot_id=bot_id
    if(multiple_element==True):
        send_bot_id=send_bot_id+"_repeat"
    response=requests.post("https://jpzu5bjwzg.execute-api.us-east-2.amazonaws.com/default/read_bot_analysis",data=json.dumps({"bot_id":send_bot_id,"from":"element_manager"}),headers={"content-type":"application/json"}).json()
    found=response["status"]
    analysis=response["analysis"]
    if(found==False):
        try:
            message=response["message"]
        except:
            message="Not Found"
    return analysis,found,message
def change_analysis(analysis,multiple_element):
    new_analysis={}
    for event_number in analysis:
        event_name=list(analysis[event_number].keys())[0]
        new_analysis=analysis[event_number][event_name]
        break
    try:
        new_analysis["Event"]["xlength"]=int(new_analysis["Event"]["xlength"])
    except:
        pass
    try:
        new_analysis["Parent"]["xlength"]=int(new_analysis["Parent"]["xlength"])
    except:
        pass
    if(multiple_element==False):
        new_analysis["isrepeat"]=False
    return new_analysis
def get_the_front_xpath(element):
    global_driver=get_global_driver()
    front_xpath=JavaScriptXpath(global_driver,element)
    return front_xpath
def send_the_log(bot_id,multiple_element,browser):
    log="get_xpath called"
    if(multiple_element==True):
        log="get_xpaths called"
    log=log+" for bot:-"+str(bot_id)
def check_if_svg_tag(element):
    if(element.name not in ["svg","path"]):
        return element
    parent=element
    for i in range(0,10):
        parent= parent.find_parent()
        if(parent.name not in ["svg","path"]):
            return parent
    return element
def get_element_xpath(driver,bot_id,multiple_element):
    xpath=None
    try:
        send_the_log(bot_id,multiple_element,"")
        typee="driver"
        front_xpath=""
        if("webdriver.remote.webelement.WebElement" in str(type(driver))):
            typee="element"
            front_xpath=get_the_front_xpath(driver)
        analysis,found,message=get_the_analysis(bot_id,multiple_element)
        if(found==False):
            raise RuntimeError("ID not Found")
        analysis=change_analysis(analysis,multiple_element)
        if(typee=="driver"):
            page_source=driver.page_source
        else:
            page_source=driver.get_attribute("innerHTML")
        reqsoup=BeautifulSoup(page_source,'html.parser')
        elements=find_the_elements_by_event(reqsoup,page_source,analysis)
        if(multiple_element==False):
            el2=check_if_svg_tag(elements[0])
            xpath=xpath_soupreq(el2)
        else:
            xpath=[]
            for el in elements:
                el=check_if_svg_tag(el)
                xpath.append(xpath_soupreq(el))
    except Exception as e:
        raise RuntimeError(str(e))
    return xpath
def get_xpath(driver,bot_id):
    return get_element_xpath(driver,bot_id,False)
def get_xpaths(driver,bot_id):
    return get_element_xpath(driver,bot_id,True)