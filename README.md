# CPE106L-Group10-Project

![Insert Mapua Logo Here](https://malaya.com.ph/wp-content/uploads/2024/11/Mapua.png)

## Project ATS (Accessible Transportation Scheduler)

## Members and Roles

#### Dayag Jr., Vicente Nigel S.

> Project Member

#### Dela Cruz, John Andrei M.

> Project Manager

#### Regalado, John Seth B.

> Project Member

## Community Need

Help elderly or individuals with accessibility needs schedule rides with local volunteers or services.

## How to Run the Project

### Setup and Open with Windows Terminal

1. Download repository in [GitHub](https://github.com/Meta-Dusk/CPE106L-Group10-Project) by clicking `<> Code` then selecting `Local` and `Download ZIP` or `Open with Visual Studio` (Recommended Visual Studio Code).
> #### After Downloading
> Unzip if you downloaded ZIP file into a folder, then navigate to it by doing `cd "path/to/folder/"`, make sure you navigate to the project folder, which contains the `./launch.py`.
> If the downloaded file is stored in a different drive, you can switch to it by doing `d:` and just replace the letter to whatever drive letter you want to switch to (make sure it is in lowercase).
2. Once you have navigated to the folder containing the project files, you can then just simply type in the terminal `py launch.py`. To make sure that the launch script is accessible, you can check the files in the current directory (folder) by doing `dir` in the terminal.
3. Once you have entered `py launch.py` wait a bit, and it will open the launcher for you, which will contain options for you to run.
> #### Missing Libraries?
> The launcher has a feature for missing libraries; as of now, it will only show you the missing libraries in a UI made using tkinter. The module names of these dependencies are type-sensitive, therefore you can just copy and paste the listed module names in the UI and just install by doing `pip install {module name}`, make sure to replace `{module name}` with the module name.
> ##### Features to be added:
> - Auto-install missing libraries by prompting the user during launch.
> - Relaunch after auto-install has been chosen.

### Ubuntu Virtual Machine (VM)

> Pending :P <br>
> ![Sad Penguin](https://openclipart.org/image/800px/178504)

## Original Project Scope

### Already Implemented

**Database**: Use MongoDB for flexible ride and user data.

**Flet Desktop App**: Interface for booking rides and managing schedules.

**MVC Design Pattern**: Modular structure for maintainability.

**Object Oriented Design**: Classes for users, drivers, ride requests, and schedules.

> #### Disclaimer
> Code structure will be frequently updated/refactored depending on the amount of features implemented.

### Pending Implementations (May or May Not be Included)

**Python Data Structures & Optimization Algorithms**: Use scheduling and route optimization algorithms (e.g., Dijkstra, A*).

**API Integration**: Google Maps API for routing and distance calculation.

**Matplotlib**: Visualize ride frequency, wait times, and service coverage.

**FastAPI**: Backend for ride matching, scheduling, and notifications.

## Scope Alterations/Additions

### Already Implemented

**Tkinter and/or ttkbootstrap**: For testing/fallback GUIs in the desktop application version of the project (Only if Flet will not be used).

**BCrypt**: Password hashing for relatively safe storage of user's passwords.

**MongoDB Atlas**: You know what's even better than a NoSQL database? A NoSQL database on the cloud. Connect to a MongoDB Atlas cluster for user authentication for a non-local database implementation.

**SQlite**: Having two databases just in case the other fails. You can easily switch between these two by just clicking a button in the login screen.

### Pending Implementations (May or May Not be Included)

**Render (Cloud Application Platorm)**: For when the project is ready to be deployed.
