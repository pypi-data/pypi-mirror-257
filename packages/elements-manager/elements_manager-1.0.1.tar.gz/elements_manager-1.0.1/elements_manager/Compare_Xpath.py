import itertools
def xpath_soupreq(element):
    """It finds the xpath of the bs4 element.

    Args:
      element: bs4 element

    Returns:
      xpath e.g "/html/div/span"
      
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        #components.append('%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
def is_substr(find, data):
    """It checks if the string is substring in all keys or not.

    Args:
      find:"string"
      data: ["string1","string2"]

    Returns:
      True : if subtring present in all data values
      
    """
    if len(data) < 1 and len(find) < 1:
        return False
    for i in range(len(data)):
        if find not in data[i]:
            return False
    return True
def long_substr(data):
    """It finds the longest substring between list values.

    Args:
      data: ["html/body/div/div/div","html/body/div/div2/div"]

    Returns:
      substr : longest substring e.g "html/body/div/div"
      
    """
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and is_substr(data[0][i:i+j], data):
                    substr = data[0][i:i+j]
    return substr
def clean_substring(substring):
    """It checks if the substring found is not starting with "/" or "]" as we are comparing xpaths so they should be identical in format.

    Args:
      substring: "[2]/div"

    Returns:
      new_substring : "/div"
      
    """
    new_substring=substring
    if(substring[0]=="/"):
        return substring
    substring_frst=substring.split("/")[0]
    init=len(substring_frst)
    if("]" in substring_frst):
        new_substring=new_substring[init:]
    return new_substring
def get_match_count(org_xpath,xpath,count,repeat):
    """It takes original xpath and found xpath and then finds the longest substring length bwteen them and returns the matching count. If repeat is True then it goes to one iteration only, otherwise till substring is ""

    Args:
      substring: "[2]/div"

    Returns:
      count : longest substring count
      
    """
    substring=long_substr([org_xpath,xpath])
    try:
        substring=clean_substring(substring)
    except: 
        pass
    if(len(substring.split("/"))>=2):
        temp_count=len(substring)-1
        if("[[" in substring[-1]):
            temp_count=temp_count-1
        try:
            last=substring.split("/")[-1]
            last=last.split("[")[1]
            f=int(last[-1])
            temp_count=temp_count-len(last)
        except:
            pass
        done=False
    else:
        temp_count=0
        done=True
    count=count+temp_count
    new_org_xpath=org_xpath.replace(substring,"")
    new_xpath=xpath.replace(substring,"")
    if(repeat==True):
        return count
    if(done==False):
        count=get_match_count(new_org_xpath,new_xpath,count,repeat)
    return count
def get_match_count_repeat(xpath,element_xpath):
    count=0
    xpath_list=xpath.split("/")
    element_xpath_list=element_xpath.split("/")
    for i in range(1,len(xpath_list)):
        pass
    return count
def edit_xpath(xpath):
    """It edits the xpath and attaches the tag number with each tag e.g "/html/body" will be converted to "/html[1]/body[1]". It was done as the xpath found from analysis and from bs code are different as string but are same.

    Args:
      xpath: element xpath e.g "/html/body"

    Returns:
      new_xpath : new xpath e.g "/html[1]/body[1]"
      
    """
    new_xpath=""
    xpath_list=xpath.split("/")
    for i in range(1,len(xpath_list)):
        tag=xpath_list[i]
        new_xpath=new_xpath+"/"+tag
        if(tag.endswith("]")):
            pass
        else:
            new_xpath=new_xpath+"[1]"
    return new_xpath
def get_maximum_count_element(match_count_dic,repeat):
    """It finds the elements list who have maximum count. If repeat is True then second maximum count is considered otherwise first maximum.

    Args:
      match_count_dic: dic containing match count and element e.g {"element":4,"elemen2":5}
      repeat: is True if isrepeat is True in analysis dic

    Returns:
      element_found : 0th element found from all_elements
      all_elements: elements found list having max matching count with xpath
      
    """
    all_elements=[]
    list_of_count=list(match_count_dic.values())
    maximum_count=max(list_of_count)
    if(repeat==True):
        list_of_count=list(set(list_of_count))
        list_of_count.sort()
        try:
            maximum_count=list_of_count[-2]
        except:
            maximum_count=max(list_of_count)
    for element in match_count_dic:
        if(match_count_dic[element]>=maximum_count):
            all_elements.append(element)
            element_found=element
    return element_found,all_elements

def compare_by_xpath(FinalSoupList,xpath,repeat):
    """It filters the elements by xpath. It first fetches the xpath of all elements and then find the elements having maximum matching count with original xpath.

    Args:
      FinalSoupList: list of elements
      xpath: original xpath
      repeat: is True if isrepeat is True in analysis dic

    Returns:
      text: text of final element found
      element : 0th element found from all_elements
      all_elements: elements found list having max matching count with xpath
      
    """
    match_count_dic={}
    xpath=edit_xpath(xpath)
    for element in FinalSoupList:
        element_xpath=xpath_soupreq(element)
        element_xpath=edit_xpath(element_xpath)
        count=get_match_count(xpath,element_xpath,0,repeat)
        match_count_dic[element]=count
    element,all_elements=get_maximum_count_element(match_count_dic,repeat)
    try:
        text=element.get_text()
    except:
        text=FinalSoupList[0].get_text()
    if(repeat==True and len(all_elements)<2):
        all_elements=FinalSoupList
    else:
        new_eles=[]
        for el in FinalSoupList:
            if(el in all_elements):
                new_eles.append(el)
        all_elements=new_eles
    return text,element,all_elements
