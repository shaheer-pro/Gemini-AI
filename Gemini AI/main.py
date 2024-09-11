import tkinter as tk
import google.generativeai as ai  # type: ignore

# Initialize global variables
chat = None
API_KEY = ""

def configure_api_key():
    global API_KEY, chat
    API_KEY = api_key_entry.get().strip()
    
    if not API_KEY:
        status_label.config(text="API Key cannot be empty.", fg='red')
        return

    try:
        ai.configure(api_key=API_KEY)
        model = ai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        status_label.config(text="API Key configured successfully.", fg='green')
        api_key_entry.config(state=tk.DISABLED)
        configure_button.config(state=tk.DISABLED)
    except Exception as e:
        status_label.config(text=f"Error configuring API Key: {e}", fg='red')

def send_message(event=None):
    if chat is None:
        status_label.config(text="API Key not set. Please configure it.", fg='red')
        return

    user_message = entry.get().strip()
    if user_message == "":
        return  # Do nothing if the user input is empty
    
    if user_message.lower() == "quit":
        chat_window.config(state=tk.NORMAL)  # Allow text editing
        chat_window.insert(tk.END, "Chatbot: Bye\n")
        chat_window.config(state=tk.DISABLED)  # Disable text editing
        return

    chat_window.config(state=tk.NORMAL)  # Allow text editing
    chat_window.insert(tk.END, "You: " + user_message + "\n")
    
    try:
        response = chat.send_message(user_message)
        chat_window.insert(tk.END, "Chatbot: " + response.text + "\n")
    except Exception as e:
        chat_window.insert(tk.END, "Chatbot: Sorry, an error occurred.\n")
        print(f"Error sending message: {e}")

    chat_window.config(state=tk.DISABLED)  # Disable text editing
    entry.delete(0, tk.END)  # Clear the entry widget

# Create the main window
root = tk.Tk()
root.title("Chatbot GUI")
root.geometry("800x600")
root.configure(bg='black')

# Create and pack the title label at the top
title_label = tk.Label(root, text="Gemini AI", font=("Arial", 16), bg='black', fg='white')
title_label.pack(pady=10)

# Frame for API key entry
api_key_frame = tk.Frame(root, bg='black')
api_key_frame.pack(pady=10)

# API Key entry widget
api_key_label = tk.Label(api_key_frame, text="Enter API Key:", bg='black', fg='white')
api_key_label.pack(side=tk.LEFT, padx=(10, 5))
api_key_entry = tk.Entry(api_key_frame, width=40, bg='white', fg='black', insertbackground='black')
api_key_entry.pack(side=tk.LEFT, padx=(0, 10))

# Configure button to set the API Key
configure_button = tk.Button(api_key_frame, text="Configure", command=configure_api_key, bg='grey', fg='white')
configure_button.pack(side=tk.LEFT)

# Status label
status_label = tk.Label(root, text="", bg='black', fg='white')
status_label.pack(pady=5)

# Create and pack the chat window (text area)
chat_window = tk.Text(root, height=20, width=50, state=tk.DISABLED, bg='white', fg='black', insertbackground='black')
chat_window.pack(padx=10, pady=10)

# Create a frame to hold the entry widget and send button
input_frame = tk.Frame(root, bg='black')
input_frame.pack(pady=10)

# Create and pack the entry widget (text box for user input) within the frame
entry = tk.Entry(input_frame, width=40, bg='white', fg='black', insertbackground='black')
entry.pack(side=tk.LEFT, padx=(0, 10))

# Create and pack the send button next to the entry widget within the frame
send_button = tk.Button(input_frame, text="Send", command=send_message, bg='grey', fg='white')
send_button.pack(side=tk.LEFT)

# Bind the Enter key to the send_message function
entry.bind("<Return>", send_message)

# Run the Tkinter event loop
root.mainloop()
