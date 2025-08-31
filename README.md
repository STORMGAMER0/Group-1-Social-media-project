# Social Media App
Hello, this is Backend Rest API for a simple ***social media app*** where users can 
- *post messages*
- *optionally upload images*
- *like other users's posts*.

## API Endpoints
Bellow is the API routes in this app:
*`POST /users/`
* `POST /posts/`
* `GET /posts/`
* `GET /users/{username}/posts`
* `POST /posts/{post_id}/like`

### To Run This Program 
Run this program in your local machine without problem using the following procedures:
+ Clone this repository to your local machine
+ In the repository root folder create a virtual environment using `python3 -m venv myenv`
+ Activate the venv using `source myenv/bin/activate` on macOS/linux <br>
  OR
+ Use `myenv\Scripts\activate.bat` & `myenv\Scripts\Activate.ps1` for windows C.prompt and powershell respectively
+ install requirements 
+ create a .env file and add your postgreSQL URL (e.g `postgresql://user:password@localhost:port/database`)
+ Then run `uvicorn app.main:app --reload`
  follow the prompt to the app.

***TADAAH!***

  
