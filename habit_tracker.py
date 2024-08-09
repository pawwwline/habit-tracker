from datetime import date

class Habit:
    def __init__(self, habit_name: str):
        self.habit_name = habit_name
        self.records = {}
    
    def record(self, record_date: str, complete: bool):
        self.records[record_date] = complete
    
    def get_status(self, record_date: date):
        return self.records.get(record_date.isoformat(), False)


class HabitManager:
    def __init__(self):
        self._habits = {}
    
    def add_habit(self, habit: Habit):
        self._habits[habit.habit_name] = habit

    def delete_habit(self, habit_name):
        habit = self._habits.get(habit_name)
        if habit:
            today = date.today().isoformat()
            habit.records = {d: v for d, v in habit.records.items() if d < today}
            if not habit.records:
                self._habits.pop(habit_name)

    def record_habit(self, habit_name: str, completed: bool):
        record_date = date.today().isoformat()
        habit = self._habits.get(habit_name)
        if habit:
            habit.record(record_date, completed)
       
    def get_habits_today(self):
        today = date.today()
        habits_status = {}
        for habit_name, habit in self._habits.items():
            status = habit.get_status(today)
            habits_status[habit_name] = status
        return habits_status
        

class HabitCLI:
    def __init__(self, habit_manager: HabitManager):
        self.habit_manager = habit_manager

    def run(self):
        while True:
            print("1. Add habit")
            print("2. Record habit")
            print("3. View habits for today")
            print("4. Delete habit")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_habit()
            elif choice == '2':
                self.record_habit()
            elif choice == '3':
                self.view_habits_for_today()
            elif choice == '4':
                self.delete_habit()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_habit(self):
        habit_name = input("Enter habit name: ")
        habit = Habit(habit_name)
        self.habit_manager.add_habit(habit)
        print(f"Habit '{habit_name}' added.")

    def record_habit(self):
        habit_name = input("Enter habit name: ")
        completed = input("Completed? (y/n): ").lower() == 'y'
        self.habit_manager.record_habit(habit_name, completed)
        print(f"Habit '{habit_name}' recorded as {'completed' if completed else 'not completed'}.")

    def view_habits_for_today(self): #TODO: debug complete status
        habits_status = self.habit_manager.get_habits_today()
        if not habits_status:
            print("No habits for today.")
        else:
            for habit_name, status in habits_status.items():
                print(f"{habit_name}: {'Completed' if status else 'Not completed'}")

    def delete_habit(self):
        habit_name = input("Enter habit name to delete: ")
        if self.habit_manager.delete_habit(habit_name):
            print(f"Habit '{habit_name}' deleted.")
        else:
            print(f"Habit '{habit_name}' not found.")



if __name__ == "__main__":
    habit_manager = HabitManager()
    cli = HabitCLI(habit_manager)
    cli.run()
 