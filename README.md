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

## 🖥 How to Run the Project

### ⚙️ Setup via Windows Terminal

1. **Download the repository** from [GitHub](https://github.com/Meta-Dusk/CPE106L-Group10-Project) by clicking **`<> Code` → `Download ZIP`** or choose **`Open with Visual Studio Code`** *(recommended)*.

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
- Alternatively, manually install modules:

  ```bash
  pip install flet pymongo bcrypt cryptography
  ```

##### 🔜 Upcoming Launcher Features

- Auto-install libraries on prompt.
- Relaunch script after successful installation.

---

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

> ⚠️ Code structure is actively evolving as new features are added.

### 🚧 Pending Features (May or May Not Be Included)

- **Scheduling Algorithms**: Optimization with Dijkstra, A*, etc.
- **Google Maps API**: Routing and distance calculations.
- **Matplotlib**: Data visualization (e.g., ride frequency, wait times).
- **FastAPI**: Backend API for ride matching and notifications.

---

## 🔄 Scope Alterations / Additions

### ✅ Finished Implementation

- **Tkinter / ttkbootstrap**: Fallback GUI alternatives if Flet is not used.
- **BCrypt**: Secure password hashing.
- **MongoDB Atlas**: Cloud-based MongoDB support.
- **SQLite**: Local database alternative; toggle via login screen.

### 🚧 Pending Integrations (Optional)

- **Render (Cloud Deployment)**: For future deployment of the live app.

---

> 📎 **Note**: This README will be periodically updated alongside development.
