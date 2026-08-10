*** Settings ***
Library    Browser
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}         https://the-internet.herokuapp.com/login
${USERNAME}    tomsmith
${PASSWORD}    SuperSecretPassword!

*** Test Cases ***
Login Then Interact With Dropdown Then Logout
    [Documentation]    Same multi-step flow as the Selenium version, using Playwright.

    # Step 1 - Fill in login form
    Fill Text    id=username    ${USERNAME}
    Fill Secret    id=password    $PASSWORD

    # Step 2 - Submit login
    Click    css=button[type='submit']
    Sleep    3s
    # Step 3 - Verify login succeeded
    Get Text    css=.flash.success    contains    You logged into a secure area
    Sleep    3s
    # Step 4 - Navigate to a different page
    Go To    https://the-internet.herokuapp.com/dropdown
    Sleep    3s
    # Step 5 - Interact with a dropdown
    Select Options By    id=dropdown    label    Option 2
    Sleep    3s
    # Step 6 - Verify the dropdown selection stuck
    Get Selected Options    id=dropdown    label    ==    Option 2
    Sleep    3s
    # Step 7 - Go back and log out
    Go To    https://the-internet.herokuapp.com/secure
    Click    text="Logout"
    Get Text    css=.flash.success    contains    You logged out of the secure area

*** Keywords ***
Open Browser To Login Page
    New Browser    chromium    headless=False
    New Page    ${URL}
