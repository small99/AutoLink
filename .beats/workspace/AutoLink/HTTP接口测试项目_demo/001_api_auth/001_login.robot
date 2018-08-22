*** Settings ***
Resource	../000_resources/所有用例公用变量和关键字.txt

Test Teardown	Delete All Sessions


*** Variables ***
${login_result}		login success
${logout_result}	logout success


*** Test Cases ***  
Valid Login 
    Login       AutoLink    123456
    
Valid Logout
    Logout

*** Keywords ***
Open Home Page
		Create Session	${ALIAS}        ${BASE_URL}
		${resp}=		Get Request		${ALIAS}	/
		Should Be Equal As Strings      ${resp.status_code}     200
    
Login   
    [Arguments]     ${username}     ${password}
    Create Session  ${ALIAS}        ${BASE_URL}
    ${data}=        Create Dictionary   username=${username}    password=${password}
    ${headers}=			Create Dictionary	 Content-Type=application/x-www-form-urlencoded
    ${resp}=        Post Request    ${ALIAS}        ${LOGIN_PATH}       data=${data}    headers=${headers}
    Should Be Equal As Strings      ${resp.status_code}     201
    Dictionary Should Contain Value		${resp.json()}    ${login_result}

Logout
    Create Session  ${ALIAS}        ${BASE_URL}
    ${resp}=        Get Request     ${ALIAS}    ${LOGIN_PATH}
    Should Be Equal As Strings      ${resp.status_code}     201
    Dictionary Should Contain Value		${resp.json()}    ${logout_result}

       


