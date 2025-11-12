from tkinter import BOTH, END, WORD, Button, Label, Text, Toplevel


class Suggestion_Window(Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        #title, icon, size
        self.title('Smart Suggestions')
        self.geometry("700x500")
        self.configure(bg='teal')

        Label(self, text="Smart Suggestions", font=('Helvetica', 20), bg='teal', fg='white').pack(pady=20)

        # Suggestions display
        self.suggestions_text = Text(self, wrap=WORD, width=60, height=15, font=("Arial", 12), bg='lightcyan')
        self.suggestions_text.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Refresh button
        Button(self, text="Refresh Suggestions", command=self.refresh_suggestions,font=("Arial", 12), bg='#00a0a0', fg='white').pack(pady=10)

        # Load initial suggestions
        self.refresh_suggestions()

    def refresh_suggestions(self):
        #Refresh suggestions based on current weather and tasks
        self.suggestions_text.delete(1.0, END)

        # Get current weather data for suggestions
        weather_data = self.get_weather_data_for_suggestions()

        if weather_data:
            # Generate suggestions using your SuggestionEngine
            suggestions = self.master.suggestion_engine.generate_suggestions(weather_data, self.master.task_manager)

            # Display suggestions
            if suggestions:
                for suggestion in suggestions:
                    self.suggestions_text.insert(END, f"• {suggestion}\n\n")
            else:
                self.suggestions_text.insert(END, "Get weather data and add tasks to see personalized suggestions!")
        else:
            self.suggestions_text.insert(END, "Please get weather data first to see suggestions!")

    def get_weather_data_for_suggestions(self):
        #Convert current weather to SuggestionEngine format
        try:
            # Check both possible weather data locations
            if hasattr(self.master, 'current_weather_data') and isinstance(self.master.current_weather_data, dict):
                weather_data = self.master.current_weather_data
                return {
                    'description': weather_data.get('weather', '').lower(),
                    'temperature': weather_data.get('temp', 72),
                    'conditions': weather_data.get('weather', '').lower(),
                    'location': weather_data.get('location', 'Current Location')
                }
            elif hasattr(self.master, 'forecast') and isinstance(self.master.forecast, dict):
                weather_data = self.master.forecast
                return {
                    'description': weather_data.get('weather', '').lower(),
                    'temperature': weather_data.get('temp', 72),
                    'conditions': weather_data.get('weather', '').lower(),
                    'location': weather_data.get('location', 'Current Location')
                }
        except Exception as e:
            print(f"Error getting weather data for suggestions: {e}")
        return None