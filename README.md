# 🚗 CPE106L-Group10-Project

![Mapúa Logo](https://malaya.com.ph/wp-content/uploads/2024/11/Mapua.png)

## 🛠 Project ATS: Accessible Transportation Scheduler

---

## 👨‍💻 Members and Roles

| Name                          | Role            |
|-------------------------------|-----------------|
| Dayag Jr., Vicente Nigel S.   | Project Member  |
| Dela Cruz, John Andrei M.     | Project Manager |
| Regalado, John Seth B.        | Project Member  |

---

## 💡 Community Need

To assist elderly individuals or those with accessibility challenges in scheduling transportation with local volunteers or service providers.

---
## 📦 Pre-requisites

- You must have `python>=3.13.5` (or just any latest version of Python), for compatibility.
- As for the dependencies _(modules/libraries)_ used, refer to the launcher (when running `launch.py`).

## 💭 Additional Notes

1. **Running the Application in Web Mode**
   - Yes, the application can run in a web browser. Simply set the launcher to **Web Mode**, and it will open the app in your system's default browser.
   - **Note**: Closing the browser tab **does not** stop the application. You must also close the terminal or command prompt that launched it.

2. **Accessing the App on Mobile Devices**
   - While the app isn't optimized for mobile screens, it can still be accessed via a mobile browser on the same local network.
   - To do so:
     1. Launch the app in **Web Mode** on your PC.
     2. In the terminal, look for an address like `http://127.0.0.1:xxxxx` or similar.
     3. Get your actual IP address:
        - On **Windows**, open a new terminal and run:
          ```bash
          ipconfig
          ```
        - Find your **IPv4 Address** (e.g., `192.168.0.123`).
     4. Replace the `127.0.0.1` in the earlier address with your IPv4 address. For example:
        ```
        http://192.168.0.123:xxxxx
        ```
     5. Open this address in your mobile browser while connected to the same Wi-Fi.
   - **Note**: Due to limited screen space, some UI elements may not be fully visible or usable on mobile.

3. **Launcher Configuration**
   - The launcher supports multiple **Window Modes** and **Launch Modes**:

     - **Window Modes**:
       - **Windowed**: Default mode with a standard window frame.
       - **Full Screen**: Occupies the entire screen (only works with *Native* launch mode).
       - **Borderless**: Custom frameless window (useful for aesthetic flexibility).

     - **Launch Modes**:
       - **Native (Default)**: Runs as a desktop application.
       - **Web**: Opens the app in your web browser. Only supports *Windowed* mode.
       - **Run Setup**: Initializes connection settings for MongoDB Atlas (username, password, and host). Optional, but recommended to run once.
      
## 📃 Main Features (as of now)

1. **Missing modules auto-download**
   - Can be triggered via launcher.
2. **Sensitive data setup handler**
   - This is triggered once the `run setup` option has been selected in the launcher. This will then run a separate script for setting up sensitive data, such as configuring the MongoDB connection string.
3. **Dual-database system**
   - The application can simply switch between using **MongoDB** and **SQLite** based on the user. The default database is MongoDB, and if the application can't connect to MongoDB, you can switch to use the local database instead, which is what SQLite is used for.
4. **Profile Setup**
   - The user can make an account in the login screen (which will make an account based on the current database), and the profile setup is optional. You can fill in your details after the login, by clicking the `Profile` button.
5. **Admin Controls**
   - Users can become admins, but the only method to become an admin, is through manipulating the user's details in the database itself (as of now, this value field is simply a boolean named `op`).
6. **Booking Simulation**
   - Since this application is not yet deployed, the user can just simulate what the booking would look like. A map view is provided, in which the user can navigate with the controls shown above the map view.
7. **Music and SFX**
   - While this feature may be unnecessary, the application does have music playing, and also have sound effects. This feature can be disabled in the settings menu, by navigating via the dashboard, to your profile, then click the settings button at the top-right of the screen.
8. **API Config, View Graphs**
   - As of now, these features won't do much, but you can navigate to them via the dashboard to see what's currently implemented.

## 🖥 How to Run the Project

### ⚙️ Setup via Windows Terminal

1. **Download the repository** from [GitHub](https://github.com/Meta-Dusk/CPE106L-Group10-Project) by clicking **`<> Code` → `Download ZIP`** *(recommended)* or choose **`Open with Visual Studio Code`**.

2. **Navigate to the project folder**:
   - If ZIP file was downloaded, extract it.
   - Open Terminal and run:

     ```bash
     cd "path/to/project/folder"
     ```

   - If the folder is on a different drive, switch drives by typing:

     ```bash
     d:
     ```

3. **Launch the app** by running:

   ```bash
   py launch.py
   ```

   - Ensure `launch.py` exists by listing files:

     ```bash
     dir
     ```

4. **Wait for the launcher interface to appear**, which provides options to run the project.

#### 🧩 Missing Libraries?

- The launcher will detect missing modules and prompt to install them automatically.
- Alternatively, manually install modules listed in the launcher:

  ```bash
  pip install flet pymongo bcrypt cryptography ...
  ```

- The launcher saves user configs, such as window type and launch mode.

### 🐧 Ubuntu Virtual Machine (VM)

⚠️ *Currently Pending* 😅  
![Sad Penguin](https://openclipart.org/image/800px/178504)

---

## 📌 Original Project Scope

### ✅ Already Implemented

- **MongoDB**: NoSQL database for ride and user data.
- **Flet Desktop App**: Modern UI for scheduling and ride management.
- **MVC Pattern**: Modular design for scalability and maintainability.
- **Object-Oriented Design**: Classes for users, drivers, and rides.

### ☑️ Partially Implemented

- **Matplotlib**: Data visualization (e.g., ride frequency, wait times).
- **FastAPI**: Backend API for ride matching and notifications.
- **Google Maps API**: Routing and distance calculations.

> ⚠️ Code structure is actively evolving as new features are added.

### 🚧 Pending Features (May or May Not Be Included)

- **Scheduling Algorithms**: Optimization with Dijkstra, A*, etc.

---

## 🔄 Scope Alterations / Additions

### ✅ Finished Implementation

- **Tkinter / ttkbootstrap**: Fallback GUI alternatives if Flet is not used.
- **BCrypt**: Secure password hashing.
- **MongoDB Atlas**: Cloud-based MongoDB support.
- **SQLite**: Local database alternative; toggle via login screen.
- **PyGame**: Music and SFX; 'cuz why not (optional, can be disabled).
- **GeoPy**: For functions concerning geological data.
- **Httpx + Aiohttp**: For URL related functionality.

### 🚧 Pending Integrations (Optional)

- **Render (Cloud Deployment)**: For future deployment of the live app.

---

> 📎 **Note**: This README will be periodically updated alongside development.
