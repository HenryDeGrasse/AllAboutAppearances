import os
import datetime
import random
from tkinter import Tk, Label, Button, filedialog, messagebox

try:
    from tkcalendar import Calendar
except ImportError as e:
    print(f"Error: Failed to import tkcalendar: {e}")
    print("Install it with: pip install tkcalendar")
    exit(1)

try:
    from git import Repo
except ImportError as e:
    print(f"Error: Failed to import GitPython: {e}")
    print("Install it with: pip install GitPython")
    exit(1)

# Initialize Tkinter window
app = Tk()
app.title("Git Commit Creator")
app.geometry("400x600")  # Set window size

# Print Tk version for debugging
print("TCL/TK Version:", app.tk.call('info', 'patchlevel'))

# Start Date Calendar
Label(app, text="Select Start Date:").pack(pady=5)
start_calendar = Calendar(app, selectmode="day")
start_calendar.pack(pady=5)

# End Date Calendar
Label(app, text="Select End Date:").pack(pady=5)
end_calendar = Calendar(app, selectmode="day")
end_calendar.pack(pady=5)

# Select Directory Button
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        repo_label.config(text=f"Selected Repo: {directory}")
        app.repo_path = directory

Button(app, text="Select GitHub Repo Directory", command=select_directory).pack(pady=10)
repo_label = Label(app, text="No directory selected")
repo_label.pack(pady=5)

# Create Commits Function with Randomness
def create_commits_action():
    # Get the selected dates
    start_date_str = start_calendar.get_date()
    end_date_str = end_calendar.get_date()

    # Convert to datetime.date objects
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%y").date()
    except ValueError:
        start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y").date()

    try:
        end_date = datetime.datetime.strptime(end_date_str, "%m/%d/%y").date()
    except ValueError:
        end_date = datetime.datetime.strptime(end_date_str, "%m/%d/%Y").date()

    # Validate inputs
    if end_date < start_date:
        messagebox.showerror("Error", "End date must be after start date.")
        return

    if not hasattr(app, "repo_path") or not app.repo_path:
        messagebox.showerror("Error", "Please select a Git repository directory.")
        return

    try:
        # Initialize the Git repository
        repo = Repo(app.repo_path)
        current_date = start_date

        while current_date <= end_date:
            # Introduce randomness for commits per day
            # 30% chance of 0 commits, 70% chance of 1–11 commits
            commit_count = 0 if random.random() < 0.3 else random.randint(1, 11)

            for _ in range(commit_count):
                # Create a dummy file for each commit
                file_name = f"file_{current_date.strftime('%Y%m%d')}_{random.randint(1000, 9999)}.txt"
                file_path = os.path.join(app.repo_path, file_name)
                with open(file_path, "w") as f:
                    f.write(f"Commit for {current_date}")

                # Stage the file
                repo.index.add([file_name])

                # Set the commit date and time (randomize time slightly)
                commit_time = current_date.strftime("%Y-%m-%d 12:00:00")
                os.environ["GIT_AUTHOR_DATE"] = commit_time
                os.environ["GIT_COMMITTER_DATE"] = commit_time

                # Commit changes
                repo.index.commit(f"Commit for {current_date}")
                print(f"Committed {file_name} on {commit_time}")

                # Remove the file
                os.remove(file_path)
                print(f"Removed {file_name}")

            # Move to the next day
            current_date += datetime.timedelta(days=1)

        print("Commits created Successfully!")
        messagebox.showinfo("Success", f"Created commits from {start_date} to {end_date}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create commits: {e}")
        print(f"Commit error: {e}")

# Create Commits Button
Button(app, text="Create Commits", command=create_commits_action).pack(pady=10)

# Run the Tkinter event loop
app.mainloop()
