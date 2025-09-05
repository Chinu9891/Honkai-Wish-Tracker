A project for tracking wishes in the game Honkai Star Rail.

It works by detecting a mouse click on the wish button while on the summon screen. This is done via the help of win32 api and OpenCV for template matching.
After the initial click, the app enters a continious loop to capture pre-defined portions of the frames and perform OCR on them to extract item names.

Also includes a mostly done FastAPI backend to support the web application that I am aiming to build with React. This web app would provide a UI for the user's wish history and an analytics dashboard.
