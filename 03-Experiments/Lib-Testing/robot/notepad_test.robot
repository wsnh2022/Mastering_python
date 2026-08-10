*** Settings ***
Library    RPA.Desktop

*** Tasks ***
Open Notepad And Type Text
    Open Application    notepad.exe
    Sleep    2s
    Type Text    Hello Robot RPA
    Sleep    3s
    Open Application    notepad.exe    D:\\Library\\Desktop\\BEST-DAILY-USER-PROMPTS.txt
