*** Settings ***
Library           ../000_resource/commonLibrary.py
Library           String

*** Variables ***


*** Test Cases ***
generateUserInfo
    [Documentation]    描述：随机生成手机号码，身份证，姓名，银行卡号
	[tags]    valid
    ${phone}    create_Phone
    ${idcard}    gennerator
    ${bankNO}    create_BankCard    62162610
    ${username}    create UserName
    ${username}    Decode Bytes To String    ${username}    UTF-8