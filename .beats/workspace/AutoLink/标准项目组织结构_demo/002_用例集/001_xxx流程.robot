*** Settings ***
Library    SeleniumLibrary
Resource   ../001_资源集/元素对象.txt


*** Test Cases ***
搜索1
    Open Browser    ${HOME}    ${BROWSER}
    Input Text    id=${kw_id}    ${SEARCH_WORD}
    Sleep	5s
    Close All Browsers
    
    
搜索2
    Open Browser    ${HOME}    ${BROWSER}
    Input Text    id=${kw_id}    ${SEARCH_WORD}
    Sleep	5s
    Close All Browsers   
    
    Log		12312313123