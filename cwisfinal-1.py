"""
Smart Study Planner
A console program to log, review and analyse study sessions.
Data is saved to study_log.txt so it persists between runs.
"""


def classify_session(duration):
    """Classify a session by its duration in minutes."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session(sessions):
    """Ask the user for session details and add it to the list."""
    subject = input("Subject: ").strip()
    topic = input("Topic: ").strip()
    date = input("Date/day: ").strip()

    # Keep asking until a valid positive number is entered
    while True:
        raw = input("Duration in minutes: ").strip()
        try:
            duration = float(raw)
            if duration > 0:
                break
            print("Duration must be a positive number. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    sessions.append({
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    })
    print("Session added!\n")


def view_sessions(sessions):
    if not sessions:
        print("No sessions logged yet.\n")
        return

    print("┌" + "─"*12 + "┬" + "─"*15 + "┬" + "─"*8 + "┬" + "─"*10 + "┬" + "─"*8 + "┐")
    print(f"│{'Subject':<12}│{'Topic':<15}│{'Date':<8}│{'Duration':<10}│{'Type':<8}│")
    print("├" + "─"*12 + "┼" + "─"*15 + "┼" + "─"*8 + "┼" + "─"*10 + "┼" + "─"*8 + "┤")
    for s in sessions:
        label = classify_session(s["duration"])
        print(f"│{s['subject']:<12}│{s['topic']:<15}│{s['date']:<8}│{str(s['duration']):<10}│{label:<8}│")
    print("└" + "─"*12 + "┴" + "─"*15 + "┴" + "─"*8 + "┴" + "─"*10 + "┴" + "─"*8 + "┘")


def search_by_subject(sessions, subject):
    """Show sessions for one subject (case-insensitive) and total time."""
    matches = [s for s in sessions if s["subject"].lower() == subject.lower()]

    if not matches:
        print(f"No sessions found for '{subject}'.\n")
        return

    total = 0
    for s in matches:
        label = classify_session(s["duration"])
        print(f"{s['topic']} | {s['date']} | {s['duration']} min | {label}")
        total += s["duration"]
    print(f"Total time on {subject}: {total} minutes\n")


def study_statistics(sessions):
    """Compute and display overall study statistics."""
    if not sessions:
        print("No data to show statistics for.\n")
        return

    # Group total minutes by subject
    totals_by_subject = {}
    for s in sessions:
        subj = s["subject"]
        totals_by_subject[subj] = totals_by_subject.get(subj, 0) + s["duration"]

    total_minutes = sum(totals_by_subject.values())
    print(f"Total hours studied: {total_minutes / 60:.2f}")

    print("\nHours per subject:")
    for subj, mins in totals_by_subject.items():
        print(f"  {subj}: {mins / 60:.2f} hours")

    weakest = min(totals_by_subject, key=totals_by_subject.get)
    print(f"\nWeakest area (least total time): {weakest}")

    longest = max(sessions, key=lambda s: s["duration"])
    print(f"Longest session: {longest['subject']} - {longest['duration']} min\n")


def save_sessions(sessions):
    """Save all sessions to study_log.txt."""
    with open("study_log.txt", "w") as f:
        for s in sessions:
            f.write(f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n")


def load_sessions():
    """Load sessions from study_log.txt if it exists."""
    sessions = []
    try:
        with open("study_log.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                subject, topic, date, duration = line.split("|")
                sessions.append({
                    "subject": subject,
                    "topic": topic,
                    "date": date,
                    "duration": float(duration)
                })
    except FileNotFoundError:
        pass  # No file yet on first run - that's fine
    return sessions


def main():
    sessions = load_sessions()

    while True:
        print("=== Smart Study Planner ===")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject = input("Enter subject to search: ").strip()
            search_by_subject(sessions, subject)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Sessions saved. Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()

