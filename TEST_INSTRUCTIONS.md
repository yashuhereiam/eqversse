# Testing Instructions

## Issues Found and Fixed

### 1. Sound File Location
**Problem**: Sound files (boom.wav, ambient.wav) are in root directory but need to be in Frontend_eqverse-master/public/
**Fix**: Run `copy_sounds_to_eqverse.bat`

### 2. Sound Playback in App.js
**Status**: ✅ FIXED - Added sound effect mapping to actual file paths

### 3. Frontend Integration
**Status**: ✅ COMPLETE - Integrated with Frontend_eqverse-master (Vite + React)

## Setup Steps

### Backend Setup
1. Install Python dependencies:
   ```
   pip install flask flask-cors google-generativeai pyttsx3
   ```

2. Start backend server:
   ```
   python backend_api.py
   ```
   Should see: "Running on http://127.0.0.1:5000"

### Frontend Setup (Frontend_eqverse-master)
1. Copy sound files to public directory:
   ```
   copy_sounds_to_eqverse.bat
   ```

2. Navigate to frontend directory:
   ```
   cd c:\Users\heyia\OneDrive\Desktop\Frontend_eqverse-master
   ```

3. Install dependencies (if not done):
   ```
   npm install
   ```

4. Start frontend:
   ```
   npm run dev
   ```
   Should open browser at http://localhost:5173

## Testing Checklist

1. [ ] Backend starts without errors
2. [ ] Frontend starts and opens in browser
3. [ ] Register new user with child age < 18
4. [ ] Login with registered username
5. [ ] Select mood on mood page
6. [ ] Navigate to home and see three game islands
7. [ ] Play all three mini-games
8. [ ] Complete all games
9. [ ] "Generate Your Personalized Story!" button appears
10. [ ] Click button to start interactive story
11. [ ] Story episodes load with sound effects and TTS
12. [ ] Make choices through all 5 episodes
13. [ ] XP counter updates correctly
14. [ ] Conclusion shows based on XP earned
15. [ ] "Back to Home" button returns to home page

## New Features Added

- Login/Register integration with backend API
- Age validation (must be under 18, ages 3-17)
- Interactive story page with 5 episodes
- Sound effects and text-to-speech
- XP system based on choices
- Personalized conclusion based on performance

## API Endpoints Used

- POST /register - Create new user account
- POST /login - Authenticate user
- POST /start_story - Initialize story session
- GET /get_episode?session_id=X - Get current episode
- POST /make_choice - Submit choice and advance

## Files Modified

- Frontend_eqverse-master/src/pages/LoginPage.jsx
- Frontend_eqverse-master/src/pages/RegisterPage.jsx  
- Frontend_eqverse-master/src/pages/HomePage.jsx
- Frontend_eqverse-master/src/App.jsx

## Files Created

- Frontend_eqverse-master/src/pages/StoryPage.jsx
- Frontend_eqverse-master/src/pages/StoryPage.css
- copy_sounds_to_eqverse.bat

