@echo off
echo Copying Frontend_eqverse-master to current frontend folder...
echo.

REM Backup current frontend
if exist "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend_backup" (
    echo Removing old backup...
    rmdir /s /q "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend_backup"
)
echo Creating backup of current frontend...
xcopy "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend" "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend_backup\" /E /I /H /Y

REM Copy Frontend_eqverse-master contents
echo Copying Frontend_eqverse-master files...
xcopy "c:\Users\heyia\OneDrive\Desktop\Frontend_eqverse-master\*" "c:\Users\heyia\OneDrive\Desktop\New folder (2)\frontend\" /E /I /H /Y

echo.
echo Done! Your old frontend is backed up in frontend_backup folder
echo Now run: cd frontend && npm install
pause
