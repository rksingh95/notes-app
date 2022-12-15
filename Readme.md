### Django Notes Application


### Run the application using make file
- Clone the project on your machine
- Open the project makefile
- Run `make start_container` on your machine
- The app to edit notes will start to run on http://0.0.0.0:8000 (If not found simply change the host to http://localhost:8000)
- Create user using the signup button (Provide username and password)
-  ![Use the signup form](https://github.com/rksingh95/notes-app/blob/master/DjangoNotesApp/app_images/Screenshot%202022-12-15%20at%2022.00.49.png)
- Basic user, password email validations are in place so if any errors you will be given correct message
- ![Use Login form](https://github.com/rksingh95/notes-app/blob/master/DjangoNotesApp/app_images/Screenshot%202022-12-15%20at%2022.03.31.png)
- Provide the user credentials to login without logging in you cant make any notes
- Once logged in the view represents all the functionality that we can handle on the note taking app.
- ![Notes App Overview](https://github.com/rksingh95/notes-app/blob/master/DjangoNotesApp/app_images/Screenshot%202022-12-15%20at%2022.09.10.png)
- We can Add, Edit, Update and Delete notes using the view provided.
- The search bar is not active for the note.
- #### We have the search functionality implemented in the backend side the api for which is `search/note/<str:tag>`
- this api provides user with the notes created by the authenticated user.
- ![Project test coverage is about 85 %](https://github.com/rksingh95/notes-app/blob/master/DjangoNotesApp/app_images/Screenshot%202022-12-15%20at%2022.15.46.png)
- #### RUN Tests (Once the container is up and running simply execute `make test` to run all 19 tests)
### -------------------------------------------------------------------------------------------------------------------
### API Documentation
- `profile/signup` -> Allows user to setup the profile (:Method: `POST` :Payload: `username`, `email`, `password` and `repeat_password` )
- `profile/login` -> Logins the user post authenticating the token (:Method: `POST` :Payload: `username`, and `password` )
- `logout` -> Logout the user (:Method: `GET` )
- `addnote` -> Allows authenticated user to add notes (:Method: `POST` :Payload: `notestitle`, `notesbody` and `notestag` )
- `edit/note/<str:note_id>` -> Allows authenticated user to edits notes based on note id (:Method: `GET` and `POST` :Parms: `note_id`)
- `update/note/<str:note_id>` -> Allows authenticated user to update notes based on note id (:Method: `POST` :Parms: `note_id`
- :Payload: `notestitle`, `notesbody` and `notestag`)
- `search/note/<str:note_id>` -> Allows authenticated user to search notes based on note id (:Method: `GET` :Parms: `note_id`)
- `delete/note/<str:note_id>` -> Allows authenticated user to delete notes based on note id (:Method: `GET`, `DELETE` :Parms: `note_id`)

### -------------------------------------------------------------------------------------------------------------------
