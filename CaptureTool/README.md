A python script that continously captures the user's screen to detect in game summon events.

Utilizes the win32 API to detect mouse clicks at predefined regions of interests. These mouse clicks then serve as a signal to start the OCR process on another region of interest.

The above tries to minimize the GPU usage by only processing mouse clicks and doing OCR when the user is on the summon screen (done via OpenCV template matching).

The next step is to expand this project into a web application, where the python script sends the results to a backend server which would then communicate with the frontend to display user's summon results and an analytics dashboard.
