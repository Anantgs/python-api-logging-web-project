# Linux Log Management Project

Complete the following tasks manually. Students should research and determine the required commands.

## 1. User and Group Management

1. Create a user named `logadmin` and a group named `logmanager`.
2. Add `logadmin` to the `logmanager` group.
3. Create `/opt/log-management-project` and clone the repository into it.
4. Assign `logmanager` as the project directory's group and enable SGID.
5. Log in as `logadmin` and verify that the user can access and modify the project.

## 2. `vi` Editor

1. Use `vi` to read the project's `README.md`.
2. Locate the application port and log-directory configuration in `app.py`.
3. Create a `student-details.txt` file containing the student's name, date, hostname, and username.
4. Use `vi` to search the application log for a specified word or log level.
5. Make a backup of a project file, modify it with `vi`, and verify the change.

## 3. File Management

1. Create `backup`, `reports`, and `archive` directories inside the project.
2. Assign the `logmanager` group and appropriate permissions to these directories.
3. Copy `/var/log/python-api-logging/app.log` into the `backup` directory while preserving its metadata.
4. Create a compressed archive containing the backup and reports.
5. Create a symbolic link named `current-app.log` pointing to the active application log.

## 4. SSH Management

1. Verify that the SSH service is installed and running.
2. Generate an SSH key pair for `logadmin`.
3. Configure key-based SSH authentication for `logadmin`.
4. Log in to the server remotely as `logadmin` and verify the user's group membership.
5. Transfer a log report between the server and another machine using a secure SSH-based utility.

## 5. Log Management

1. Run the application and generate logs using its API.
2. Monitor `/var/log/python-api-logging/app.log` in real time.
3. Count entries for instructor-specified log levels or keywords.
4. Save matching log entries in the project's `reports` directory.
5. Inspect the automatically rotated files and identify the largest log file.

## 6. Process Management

1. Start the application manually as `logadmin`.
2. Find its PID, owner, parent PID, CPU usage, and memory usage.
3. Determine which process is listening on port `8080`.
4. Stop the application gracefully, verify that it stopped, and start it again.
5. Run the application in the background with its terminal output redirected to a file.

## Final Verification

Demonstrate that:

- The application runs as `logadmin`.
- Shared files inherit the `logmanager` group.
- The API responds on port `8080`.
- Logs are written to `/var/log/python-api-logging/app.log`.
- The application can be accessed and managed through SSH.
- The application process can be located, monitored, stopped, and restarted.
