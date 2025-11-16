@echo off
echo Creating assets folder and copying background image...

REM Create assets folder if it doesn't exist
if not exist "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend\src\assets" (
    mkdir "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend\src\assets"
    echo Assets folder created!
)

REM Copy background image
if exist "c:\Users\heyia\OneDrive\Desktop\Frontend_eqverse-master\src\assets\home-background.png" (
    copy "c:\Users\heyia\OneDrive\Desktop\Frontend_eqverse-master\src\assets\home-background.png" "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend\src\assets\home-background.png"
    echo Background image copied successfully!
) else (
    echo ERROR: home-background.png not found in Frontend_eqverse-master
    echo Please check if the file exists at: c:\Users\heyia\OneDrive\Desktop\Frontend_eqverse-master\src\assets\
)

echo.
echo Done! Refresh your browser to see the changes.
pause
