# To-do-list
  A desktop GUI application that focuses on to-do management and task flow organization for individuals and small teams.
  
# Graphical Abstract:
![image](https://github.com/user-attachments/assets/13098e85-e0c6-4a4a-9dae-80b515ce9ba2)

# Software type: Command line (CLI) task management application.
   This software is a lightweight, offline-first desktop to-do management tool that focuses on providing efficient and flexible task life-cycle management solutions for individuals and small teams. Different from complex enterprise-level project management tools or online to-do applications that rely on the cloud, its core value lies in:
1. Lightweight design: Focus only on the core functions of task management, avoid redundant modules, reduce learning costs, and allow users to get started quickly; 
2. Offline autonomy: It can be used without network connection, and task data is stored locally and persistently (JSON file) to ensure privacy and data control ability;
3. Full process coverage: from task creation, editing, priority setting, due reminders to status tracking, screening and sorting, forming a complete closed loop to help users manage daily affairs in a systematic way.

# Target market (possible usage)
1. Knowledge Workers and Professionals: 
  This type of user faces complex daily tasks that need to be handled efficiently according to priorities and deadlines to avoid missing key matters;
  Function matching:
- The label system ("study", "homework", "paper") supports task grouping, and with status tracking (completed/uncompleted), it visualizes learning progress;
- Task details record (creation time, completion time, description) to facilitate time allocation review and optimize learning efficiency;
- Offline use feature, suitable for stable operation in scenarios without network, such as libraries and classrooms.
2. Students and researchers:
  The learning plans, homework submissions, literature reading and other tasks of this type of users need to be managed by categories to balance the progress of multiple tasks;
  Function matching:
- The label system ("study", "homework", "paper") supports task grouping and status tracking (completed/uncompleted) to visualize learning progress;
- Task details record (creation time, completion time, description) to facilitate time allocation review and optimize learning efficiency;
- Offline use feature, suitable for stable operation in scenarios without network, such as libraries and classrooms.
3. Small teams and sole proprietors:
  This type of user needs a simple but fully functional task management tool to facilitate basic task allocation and collaboration, without the need for complex permission management, and to avoid paying for "excessive features";
  Function matching:
- Lightweight task sharing through file copying or simple collaborative processes supports multiple people to share data on the same device or LAN;
- Simple filtering and sorting functions quickly synchronize team task status and reduce communication costs;
- Low resource consumption,it is suitable for running on low-end devices or old computers.
4. Personal life management user:
  This type of user will use it to manage various to-do items in their personal lives, such as household affairs, shopping lists, health plans, and other fragmented tasks.
  Function matching:
- Flexible labels ("Family", "Shopping", "Health") and custom descriptions are suitable for various life scenarios;
- One-click switching of task status (completed/uncompleted) intuitively presents the progress of life tasks and enhances the sense of achievement;
- Local storage ensures privacy and avoids the security risks of uploading personal data to the cloud.

# Core functions
1. Task management: add, edit, view, delete tasks
2. Task status tracking: mark tasks as completed/incomplete
3. Task filtering and sorting:
- Filter by status (all, incomplete, completed, due today)
- Filter by tag
- Sort by different conditions (creation time, due date, priority, task name)
4. Search function; text search by task name or description
5. Task priority: supports high, medium, and low priority settings
6. Due date setting: can set a due date for tasks
7. Task tags: supports multiple types of tags ( work, study, personal, urgent)
8. Task details: contains detailed information such as creation time,completion time, description, etc.
9. Persistent storage: save task data to JSON files

# The software process
## Specification
Requirements elicitation and analysis: Agile Requirements Engineering
1. Step 1: User story development
* Prior To the formal development of the project, we conduct competitive product analysis and market research on the To-Do list (e.g. task management pain points for students and small teams).
* After market research, we found that many users still have some shortcomings when using similar software, such as the need for complete networking, product functions are too complex. In addition, few of the existing products can really meet the needs of users, such as project prioritization.
* Activities: Use a user story template to describe requirements (e.g., "As a student, I want to filter tasks by the 'homework' TAB so that I can focus on academic tasks"), following a role-goal-scenario structure.
* Output: List of user stories with priority.
* Agile principles: Practice "customer collaboration" and identify needs through continuous interaction.
2. Step 2: Requirements refinement and acceptance criteria definition
* Activity: Segmentation (decomposition) of advanced user stories (such as "Task filtering" divided into "status filtering", "label filtering", "date filtering" subtasks).
* Define Acceptance criteria (AC, Acceptance criteria) for each user story, such as:
AC1: When the "unfinished" button is clicked, only the tasks whose status is "unfinished" are displayed;
AC2: The filtering operation should respond within 1 second (performance constraint).
* Output: Refined user stories (including AC) for inclusion in the current Sprint Backlog.
3. Step 3: Minimize the specification document
<img width="689" alt="1" src="https://github.com/user-attachments/assets/e31762eb-fe0c-4836-a537-f6dea53608c9" />

* Use Figma or click sketch to show UI interaction, corresponding to the PPT "prototyping support requirements verification".
(It has been released in the graphical abstarct)

* A prioritized backlog of work (functionality to be implemented) to-do list.
<img width="771" alt="2" src="https://github.com/user-attachments/assets/fe46fe51-7e2e-454e-b7f4-50a0be9e0561" />

## Design & Implementation: Iterative Development
Architecture Design (Evolutionary Design)
* Step 1: Initial Architecture Definition (Sprint 0)
Activities: (GUI layer, business logic layer, data layer), define core modules and interfaces:
GUI layer: Tkinter components (Main Window, Task Treeview, Dialog window, Context Menu), relying on ttk to achieve the theme;
Business logic layer: TodoAppGUI class encapsulates task management methods (add_task(), filter_tasks());
Data layer: JSON file persistence (load_tasks(), save_tasks()), reserved extension interface (support SQLite or cloud synchronization in the future).
* Step 2: Iterative design optimization
Perform local design for the current user story (e.g., when implementing "priority tags", design color coding rules: high priority → red, medium → yellow, low → green)
Use refactoring technology to avoid code bloat
* Step 3: Sprint planning and task allocation
Before each sprint (2 weeks as an example), the team selects high-priority user stories from the Product Backlog and breaks them down into technical tasks
Pay attention to the to-do list and record the task status in real time: to-do → in progress → to be tested → completed.
* Step 4: Incremental coding and integration
Follow test-driven development (TDD): first write unit tests (such as verifying due_date format verification logic), then implement the code to ensure coverage ≥ 80%
Perform continuous integration (CI) daily: merge code through Github, use automation tools to automatically run unit tests, and avoid integration conflicts. Output: runnable incremental versions (e.g. Sprint 1 delivers basic task CRUD functions, Sprint 2 adds filtering/sorting).

## Validation and Testing
1. Unit testing: verifying a single component (such as the set_priority() method of the Task data model);
2. Integration testing: verifying component interactions (such as whether the UI correctly updates the color code after modifying the task priority);
3. System testing: end-to-end testing (such as creating a task → setting a deadline → filtering "due today" tasks and checking whether they are displayed correctly);
4. User acceptance testing (UAT): We will invite real users (such as students and corporate users) to verify with actual data.
## Evolution: Continuous Improvement and Iteration
After the verification activities in the previous step, we will release the verified and tested version and invite users to use our soft.

# Software development plan
1. Development process: We choose agile development.
  Agile development is flexible and adaptable, allowing incremental and iterative development to quickly respond to changing requirements, making it particularly suitable for to-do list managers, as user requirements for task management features may evolve over time. Unlike the rigid, sequential waterfall model, agile development supports continuous feedback and improvement, ensuring that the software remains relevant and user-friendly.
* Modular design - The program is organized into a class, in which each function (add, view, complete, delete tasks) is relatively independent, can be independently developed and tested.
* Iterative possibilities - This simple program can be used as a minimum viable product (MVP), after which more features can be gradually added, such as task prioritization, deadlines, categories, etc.
* User feedback oriented - The design of the program allows for adjustment and improvement according to the user experience during use.
* Flexibility - Code structure allows functionality to be added or modified without redesigning the entire system.
  
While waterfall models typically require all requirements analysis and design to be done before coding, the structure of this small application is more in line with the characteristics of agile development - you can start with simple features and then gradually add features based on needs and feedback.
If this is a larger project, Agile methods might involve Sprint planning, daily standing meetings, retrospective meetings, and more agile practices.

2. Members
<img width="613" alt="Member" src="https://github.com/user-attachments/assets/cad1ab54-287d-4826-9f95-c26edb107dad" />

3. Schedule
Our project schedule is divided into three phases：
* Phase 1:
Week1 (3.20 - 3.26): 
Complete requirements gathering and architecture design, define core functionality and outline initial user interface layout.
Week2 & 3 (3.27- 4.9): 
Developed core functionality including adding, deleting, and modifying tasks, as well as basic GUI components such as the main window and task tree view.
* Phase 2: 
Week4(4.10 - 4.16): 
Comprehensive testing, performance optimization, and bug fixes.
* Phase 3:
Week5(4.17 - 4.20): 
Complete document writing and video recording, ready for delivery.
4. Current status of my software
- Task Addition: Users can add new tasks, including task title, description, priority, due date, and label.
- Task editing: Existing tasks can be edited to modify their details.
- Task deletion: Users can delete tasks that are no longer needed.
- Tasks can be marked as completed and the completion time recorded.
- Task filtering: Supports task filtering by task status (All, incomplete, completed, expired today) and label.
- Task sorting: You can sort by creation time, expiration date, priority, or task name.
- Task search: Supports keyword search tasks.
- Task export: You can export tasks to a text file.
- Menu system: Contains menu options for exporting tasks, exiting applications, and so on.
- About: Displays the version and brief description of the application.
8. Future plan
- Enhanced user interface:
Improve user experience with a more modern UI design.Add more customization options such as theme color, font size, etc.
- Data storage optimization:
Consider using a database (such as SQLite) instead of a JSON file for more efficient data management.Realize data encryption and enhance security.
- Notification function:
Added a reminder function for expired tasks, supporting pop-up window or email notification.You can set a periodic reminder.
- Collaboration features:
Supports multi-user login to achieve task sharing and collaboration.You can set task permissions to control who can view or edit tasks.
- Mobile support:
Develop mobile app versions for iOS and Android platforms.Implement cross-platform data synchronization.
- Extended features:
The repeated task function is added to support periodic tasks such as daily and weekly tasks.Supports task dependencies, showing connections between tasks.
- Performance optimization:
Optimize the code structure to improve the response speed and stability of the application.Use asynchronous processing to improve the efficiency of export and import tasks.

# Demo (Youtube URL)
https://youtu.be/W4Mf_KZ0zcI?si=JnTnv6IS5wTHJiFe

# Environments of the software development and running
1. Programming Language: Python
2. GUI Library: Tkinter
3. Additional Packages:
ttk: Part of Tkinter for themed widgets.  Usually included with Python.
tkcalendar: For date selection.  Install using pip install tkcalendar.
4. Minimum H/W Requirements:
Processor: Any modern processor capable of running Python.
RAM: 128MB.
Storage: 50MB.
5. Minimum S/W Requirements:
Operating System: Windows, macOS, or Linux.
Python: 3.6 or higher.
6. Setup Instructions:
Install Python: Download and install Python from the official website (https://www.python.org/).
Install Required Packages: Open a terminal or command prompt and run pip install tkcalendar.
Run the Script: Navigate to the directory containing the script and run it using python your_script_name.py.
