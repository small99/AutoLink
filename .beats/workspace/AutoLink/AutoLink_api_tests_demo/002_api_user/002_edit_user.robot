*** Settings ***
Resource	./000_public_user_resources.txt

Test Teardown	Delete All Sessions


*** Variables ***
${method}    edit
${edit_success}    用户信息修改成功
${edit_fail_wrong_password}    原始密码错误
${edit_not_exist_user}    用户不存在


*** Test Cases ***
Edit Exists User Success
    ${result}=    Edit User Session   testchen_e    testchen11    123456    123@33.com    123456
    Dictionary Should Contain Value		${result}    ${edit_success}

Edit User Fail With Import Wrong Password
    ${result}=    Edit User Session    testchen_e    testchen11    1234567    123@33.com    123456
    Dictionary Should Contain Value		${result}    ${edit_fail_wrong_password}
    
Edit Not Exists User
    ${result}=    Edit User Session    testchen    testchen11_not_exists    1234567    123@33.com    123456
    Dictionary Should Contain Value		${result}    ${edit_not_exist_user}
    






