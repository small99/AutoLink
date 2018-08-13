*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${BROWSER}    Chrome
${HOME}    http://www.baidu.com
${SEARCH_WORD}    开源优测
${kw_id}	kw

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

搜索3
    Open Browser    ${HOME}    ${BROWSER}
    Input Text    id=${kw_id}    ${SEARCH_WORD}
    Sleep	5s
    Close All Browsers
    
    