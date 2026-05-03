# FigureSkatingStudioApp
The application is created for Figure Skating CLub. In the application, users can search for and register for individual or group figure skating training sessions. Group training sessions are classified based on the type (off-ice/on-ice), specialization, format, and level.

Specialization is an optional category. For example, individual training sessions do not need to have predefined specializations. A user first registers for the session, and then the training focus is discussed with the coach. 

User Roles

The application has three types of users: Admin (Head Coach), Coaches and Clients.

- Both clients and coaches can create an account and log in to the application.
- Only coaches can add, edit, and delete training notifications (training announcements).
- Clients and other coaches can view all training notifications posted in the application.
- Users/clients can search for training sessions using keywords. Clients can also search for training sessions using one or more classifications, for example:
Level (e.g., intermediate)
Training type (e.g., stretching or jumps training)
- Clients can register for training sessions. Each training notification displays the list of users who have registered.
- Both clients and coaches can add profile picture for their own profile 

Additional Admin Features

The following actions are available only to administrators:
- Create training sessions for coaches and assign a coach to each session
- Edit training sessions created by other coaches
- Delete or manage existing training sessions created by coaches
- Add or update profile pictures for coaches
- Profile picture management is only allowed for coaches (clients cannot have their images modified by admins)

User Pages
- Each user profile page displays the user’s role next to their name (e.g. Coach, Client, Head coach)
The coach profile page shows:
- The total number of training notifications created by the coach
- A list of those notifications
The client profile page shows:
-The total number of training sessions the client has registered for
-A list of those registrations

The primary data item in the system is the training notification. The secondary data item is the registration.

Follow these steps to run the app locally on your computer.

1. Clone the repository
```bash
git clone https://github.com/Verona363/FigureSkatingStudioApp
cd FigureSkatingStudioApp
```
2. Create a virtual environment
```bash
python -m venv venv
```
3. Activate it
```bash
source venv/bin/activate
```
4. Install dependencies
```bash
pip install flask
```
6. Set up the database
```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```
7. Run the flask app
```bash
flask run
```
5. Go to
```bash
http://127.0.0.1:5000
```
