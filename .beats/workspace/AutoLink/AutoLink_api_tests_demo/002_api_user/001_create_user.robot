*** Settings ***
Resource	../000_resources/所有用例公用变量和关键字.txt

Test Teardown	Delete All Sessions

*** Variables ***
${method}    create


*** Test Cases ***
Create User Success
    Create User    testchen    testchen11    123456    123@33.com

Get User List
    Create Session for User


*** Keywords ***
Create User
    [Arguments]    ${fullname}    ${username}    ${password}    ${email}
    Create Session    ${ALIAS}        ${BASE_URL}
    ${data}=    Create Dictionary    method=${method}    fullname=${fullname}    username=${username}    password=${password}    email=${email}
    ${headers}=    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    ${resp}=    Post Request    ${ALIAS}    ${USER_PATH}    data=${data}     headers=${headers}
    Should Be Equal As Strings      ${resp.status_code}     201
    
Create Session for User
    Create Session    ${ALIAS}        ${BASE_URL}
    ${resp}=    Get Request    ${ALIAS}    ${USER_PATH}
    Should Be Equal As Strings      ${resp.status_code}     200
   
    
   


