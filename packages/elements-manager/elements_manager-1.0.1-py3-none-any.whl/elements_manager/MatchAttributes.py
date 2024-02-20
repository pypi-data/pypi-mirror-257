import itertools
try:
    from .Compare_Xpath import compare_by_xpath,edit_xpath
except: 
    from Compare_Xpath import compare_by_xpath,edit_xpath
def MakeDicOrdered(findingorder,event_data):
    new_dic=event_data.copy()
    new_event_data={}
    for attribute in findingorder:
        try:
            new_event_data[attribute]=new_dic[attribute]
            del new_dic[attribute]
        except Exception as e:
            pass
    for attribute in new_dic:
        new_event_data[attribute]=new_dic[attribute]
    return new_event_data
 
def CheckForOrder(event_data):
    new_dic=event_data
    try:
        findingorder=event_data['orderofelement']
        if(type(findingorder)==list):
            new_dic=MakeDicOrdered(findingorder,event_data)
    except:
        pass
    return new_dic
    
def FindXLengthreq(Xpath):
    XpathList= Xpath.split("/")
    SubString = "html".upper()
    if SubString in XpathList[1].upper():
        length= len(XpathList)-1
    else:
        length= len(XpathList)
    return length
def listToString(list1):  
    string = ""  
    for item in list1:  
        string = string+" "+item  
    return string 
def TagMatchreq(ElementFoundList ,tagname):
    elmlist=[]
    for elm in ElementFoundList:
        try:
            if(elm.name == tagname):
                elmlist.append(elm)
        except Exception as e:
            pass   
    if(len(elmlist)==0 ):
        elmlist=elmlist+ElementFoundList
    else:
        pass
    return elmlist   
def TextMatchreq(ElementFoundList ,tagtext,isrepeat):
    elmlist=[]
    for elm in ElementFoundList:
        try:
            if(elm.getText() == tagtext and tagtext!=""):
                elmlist.append(elm)
        except Exception as e:
            pass     
    if(len(elmlist)==0 and isrepeat==False):
        elmlist=elmlist+ElementFoundList
    else:
        pass
    return elmlist
def AttributeMatchreq(ElementFoundList ,attribute , value):
    try:
        value=value.strip()
    except:
        pass
    elmlist=[]
    count =0
    for elm in ElementFoundList:
        attval=elm.get(attribute)
        if(attribute=="class" and type(attval)==list):
            attval=listToString(elm.get(attribute))
            try:
                attval=attval.strip()
            except:
                pass
        try:
            if(attval == [value] or attval==value):
                count=count+1
                elmlist.append(elm)
        except Exception as e:
            pass
    if(len(elmlist)==0 ):
        elmlist=elmlist+ElementFoundList
    else:
        pass
    return elmlist
def xpath_soupreq(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
def CompareParentDictreq(FinalParentMatchDict , ParentSoupDict , count ):
    for attribute in FinalParentMatchDict:
        try:
            if(FinalParentMatchDict[attribute] == ParentSoupDict[attribute]):
                count=count+1
        except Exception as e:
            pass
    return count
def XpathSeleniumreq(ElementFoundList):
    SoupList=[]
    for element in ElementFoundList:
        try:
            SoupDict={}
            Xpath =xpath_soupreq(element)
            length = FindXLengthreq(Xpath)
            SoupDict['element']=element
            SoupDict['xlength']=length
            SoupList.append(SoupDict)
        except Exception as e:
            pass
    return SoupList
def CompareXpathreq(ElementFoundList , xlength):
    XpathCountList = XpathSeleniumreq(ElementFoundList)
    taglist=[]
    for ele_dic in XpathCountList:
        if(ele_dic['xlength'] == xlength):
            taglist.append(ele_dic['element'])
    if(len(taglist)==0 ):
        taglist=taglist+ElementFoundList
    else:
        pass
    return taglist
def MaxParentValuereq(FinalList):
    MaxCountList=[]
    for parent_dict in FinalList:
        MaxCountList.append(parent_dict['count'])
    MaxValue = max(MaxCountList)
    MatchList=[]
    for parent_dict in FinalList:
        if(parent_dict['count'] == MaxValue):
            MatchList.append(parent_dict['element'])
    return MatchList
def CompareMatchDictreq(Event_Dic, ElementFoundList,isrepeat):
    #Event_Dic={"tag": "img", "tagtext": "", "class": "img", "alt": "", "style": "opacity: 1;", "xlength": 13}
    for attribute in Event_Dic:
        if(attribute=='orderofelement'):
            pass
        elif(attribute == 'tag'):
            ElementFoundList = TagMatchreq(ElementFoundList ,Event_Dic['tag'])
        elif(attribute =="tagtext"):
            ElementFoundList = TextMatchreq(ElementFoundList ,Event_Dic['tagtext'],isrepeat)
        elif(attribute == 'xlength'):
            ElementFoundList = CompareXpathreq(ElementFoundList ,Event_Dic['xlength'] )
        else:
            ElementFoundList = AttributeMatchreq(ElementFoundList,attribute ,Event_Dic[attribute] )
    return ElementFoundList

def GetParentSoupDic(element):
    """It finds the parent of element and then fetches its attributes and create a dic having parent's atts.

    Args:
      element: bs element

    Returns:
      ParentSoupDict: parent attribute dic {"tag":"div","xlength":3,"tagtext":""}
      
    """
    Xpath =xpath_soupreq(element)
    length = FindXLengthreq(Xpath)
    parent=element.find_parent()
    ParentSoupDict={}
    ParentSoupDict['tag'] = parent.name
    text=parent.getText()
    ParentSoupDict['tagtext']=text
    attributes=parent.attrs
    for attribute in attributes:
        if(attribute=="class"):
            attval=listToString(attributes[attribute])
            try:
                ParentSoupDict[attribute] = attval.strip()
            except:
                ParentSoupDict[attribute] = attval
        else:
            ParentSoupDict[attribute] = attributes[attribute]
    ParentSoupDict['xlength']=length -1
    return ParentSoupDict
def CompareWithParentreq(ElementFoundList , FinalParentMatchDict):
    """It finds the parent of elements and then the matching count bw parent and original parent dic. Then it filters the elements who have maximum parent matching count.

    Args:
      ElementFoundList: list of bs elements
      FinalParentMatchDict: Parent Attribute Dic e.g {"tag":"div","xlength":3,"tagtext":""}

    Returns:
      FinalSoupList2:filtered list of elements 
      
    """
    FinalSoupList=[]
    FinalSoupList2=[]
    for element in ElementFoundList:
        FinalSoupDict={}
        ParentSoupDict=GetParentSoupDic(element)
        checkadd=False
        count= 0
        count  = CompareParentDictreq(FinalParentMatchDict , ParentSoupDict , count)
        if(count > 0):
            FinalSoupDict["element"]=element
            FinalSoupDict["count"]=count
            FinalSoupDict['json'] = ParentSoupDict
            FinalSoupList.append(FinalSoupDict)
    if(len(FinalSoupList) == 0):
        FinalSoupList =FinalSoupList + ElementFoundList
        return FinalSoupList
    else:
        FinalSoupList2 = MaxParentValuereq(FinalSoupList)
        return FinalSoupList2
def FindElementreq(EventMatchDict,soup,isrepeat):
    """It finds the elements who have attributes passed in EventMatchDict. 

    Args:
      soup: bs page source object
      EventMatchDict: Event Attribute Dic e.g {"tag":"div","xlength":3,"tagtext":""}

    Returns:
      ElementFoundList:elements found list
      
    """
    #FinalEventDict={"tag": "img", "tagtext": "", "class": "img", "alt": "", "style": "opacity: 1;", "xlength": 13}
    for attribute in EventMatchDict:
        ElementFoundList=soup.find_all(EventMatchDict["tag"],{attribute:EventMatchDict[attribute]})
        break
    if(len(ElementFoundList)<1):
        try:
            tag_name = EventMatchDict['tag']
            ElementFoundList = soup.find_all(tag_name)
        except Exception as e:
            ElementFoundList = soup.find_all()
    ElementFoundList = CompareMatchDictreq(EventMatchDict, ElementFoundList,isrepeat)
    return ElementFoundList
    
def find_by_all_attrributes(event_dic,reqsoup,xpath):
    attributes={}
    for attribute in event_dic:
        if(attribute in ["xlength","tag","orderofelement","tagtext"] or event_dic[attribute]==""):
            pass
        else:
            attributes[attribute]=event_dic[attribute]
    try:
        FinalSoupList=reqsoup.find_all(event_dic["tag"], attrs=attributes)
    except:
        FinalSoupList=reqsoup.find_all()
    return FinalSoupList
def CopyEventCode(reqsoup,analysis_dict):
    try:
        isrepeat=analysis_dict["isrepeat"]
    except:
        isrepeat=False
    try:
        xpath=analysis_dict["xpath"]
    except:
        xpath=""
    event_dic=analysis_dict["Event"]
    parent_dic=analysis_dict["Parent"]
    FinalSoupList=find_by_all_attrributes(analysis_dict["Event"],reqsoup,xpath)
    done=False
    if(len(FinalSoupList)>0):
        done=True
    if(done==False):
        event_dic=CheckForOrder(event_dic)
        ElementFoundList = FindElementreq(event_dic,reqsoup,isrepeat)
        FinalSoupList = CompareWithParentreq(ElementFoundList, parent_dic)
    else:
        try:
            ElementFoundList = CompareXpathreq(FinalSoupList ,event_dic['xlength'])
        except:
            ElementFoundList=FinalSoupList
        if(isrepeat==True and "tagtext" in event_dic):
            if("tagtext" in event_dic):
                if(event_dic["tagtext"].strip()!=""):
                    ElementFoundList=TextMatchreq(ElementFoundList ,event_dic["tagtext"],True)
        FinalSoupList = CompareWithParentreq(ElementFoundList, parent_dic)
    if(True):
        if(isrepeat==True):
            repeat=True
        else:
            repeat=False
        if(xpath.strip()!=""):
            text,element,FinalSoupList=compare_by_xpath(FinalSoupList,xpath,repeat)
    return FinalSoupList
def find_the_elements_by_event(reqsoup,page,analysis_dict):
    FinalSoupList=CopyEventCode(reqsoup,analysis_dict)
    return FinalSoupList
'''
from bs4 import BeautifulSoup
true=True
false=False
analysis_dict={
                "tabid": "659186544",
                "isrepeat": false,
                "xpath": "/div/ul",
                "tabevent": {
                    "class": "_abpo"
                },
                "tabpevent": {
                    "class": "_ac2d"
                },
                "submit": false,
                "Parent": {
                    "style": "background: rgba(0, 0, 0, 0.3);",
                    "tag": "div",
                    "xlength": "21",
                    "tagtext": "6411",
                    "class": "_ac2d"
                },
                "Event": {
                    "tag": "ul",
                    "xlength": "22",
                    "tagtext": "6411",
                    "class": "_abpo"
                },
                "url": "https://www.instagram.com/p/CinH89oqrjT/"
            }
with open("page.txt",encoding="utf-8") as d:
    page_source=d.read()
reqsoup=BeautifulSoup(page_source,'html.parser')
FinalSoupList=find_the_elements_by_event(reqsoup,page_source,analysis_dict)
print(len(FinalSoupList))

analysis_dict={
                "Event": {
                    "aria-hidden": "true",
                    "xlength": "24",
                    "tag": "span"
                },
                "isrepeat": true,
                "xpath": "/html/body/div[7]/div[3]/div/div/div/div[2]/div/div/main/section[7]/div[3]/div[4]/div/ul/li/div/div[2]/div/a/div/span/span",
                "Parent": {
                    "xlength": "23",
                    "class": "mr1 hoverable-link-text t-bold",
                    "tag": "span"
                }
            }
for ele in FinalSoupList:
    #eles=find_the_elements_by_event(ele,page_source,analysis_dict)
    #print(ele)
    print(ele.text)
'''