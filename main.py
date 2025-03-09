import random
import time
import os
import sys
import tkinter as tk
from tkinter import scrolledtext
import glob
import math
from datetime import datetime

class UdonOS:
    def __init__(self):
        self.root = tk.Tk()
        # Set application name to "Udon" instead of "Python"
        self.root.createcommand('tk::mac::OpenApplication', self.root.lift)
        self.root.tk.call('tk', 'windowingsystem')  # Initialize windowing system
        self.root.createcommand('::tk::mac::OnMenuBar', True)  # Enable menu bar
        self.root.createcommand('::tk::mac::Quit', self.root.quit)
        self.root.tk.call('global', 'auto_path', '[list' + '{' + self.root.tk.call('set', 'auto_path') + '}]')
        self.root.tk.call('global', 'tcl_pkgPath', '[list' + '{' + self.root.tk.call('set', 'tcl_pkgPath') + '}]')
        self.root.tk.call('package', 'require', 'Tk')
        self.root.tk.call('set', '::tk::mac::useCompatibility', '0')
        self.root.tk.call('tk', 'scaling', '1.0')
        self.root.tk.call('wm', 'class', '.', 'Udon')  # Set application name
        
        self.root.title("UDON OS Terminal 🍜")
        self.root.geometry("800x600")
        
        try:
            icon = tk.PhotoImage(file='/Users/itamar/udon-os/assets/icons8-steaming-bowl-48.png')
            self.root.iconphoto(True, icon)
        except:
            pass  # Continue without icon
        
        # Initialize basic properties
        self.current_dir = os.getcwd()
        self.username = os.getlogin()
        self.is_admin = False
        self.admin_password = "(_))0N05"
        
        # Terminal setup
        self.terminal = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='green')
        self.terminal.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Input field setup
        self.input_field = tk.Entry(self.root, bg='black', fg='green')
        self.input_field.pack(fill='x', padx=10, pady=5)
        self.input_field.bind('<Return>', lambda e: self.on_enter())
        self.input_field.focus()
        
        # Welcome message
        self.print_to_terminal(f"Welcome to UDON OS v1.0\n")
        self.print_to_terminal(f"Logged in as: {self.username}\n")
        self.print_to_terminal("Type 'help' for available commands\n")
    
    def print_to_terminal(self, text):
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)
    
    def on_enter(self):
        command = self.input_field.get().strip()
        if command:
            self.process_command(command)
        self.input_field.delete(0, tk.END)
        self.input_field.focus()
        return 'break'
    
    def process_command(self, command):
        self.print_to_terminal(f"{self.username}@udon:{self.current_dir}$ {command}\n")
        
        parts = command.lower().split()
        cmd = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == "help":
            commands = {
                "help": "Show this help message",
                "clear": "Clear terminal",
                "time": "Show current time",
                "date": "Show current date",
                "echo [text]": "Display text",
                "calc [expr]": "Calculate expression",
                "ls": "List files",
                "pwd": "Print working directory",
                "cd [path]": "Change directory (use '..' for parent directory)",
                "whoami": "Show current user",
                "touch [name]": "Create new file",
                "cat [file]": "Display file contents",
                "admin [password]": "Enter admin mode",
                "exit": "Close UDON OS"
            }
            
            if self.is_admin:
                admin_commands = {
                    "shutdown": "Shutdown the system",
                    "delete [file]": "Delete a file",
                    "rename [old] [new]": "Rename a file",
                    "changepw [new_password]": "Change admin password"
                }
                commands.update(admin_commands)
            
            for cmd, desc in commands.items():
                self.print_to_terminal(f"- {cmd}: {desc}\n")
        
        elif cmd == "clear":
            self.terminal.delete(1.0, tk.END)
        
        elif cmd == "time":
            current_time = time.strftime("%H:%M:%S")
            self.print_to_terminal(f"Current time: {current_time}\n")
        
        elif cmd == "date":
            current_date = time.strftime("%Y-%m-%d")
            self.print_to_terminal(f"Current date: {current_date}\n")
        
        elif cmd == "echo":
            text = " ".join(args)
            self.print_to_terminal(f"{text}\n")
        
        elif cmd == "calc":
            try:
                result = eval(" ".join(args))
                self.print_to_terminal(f"Result: {result}\n")
            except:
                self.print_to_terminal("Invalid expression\n")
        
        elif cmd == "ls":
            try:
                files = os.listdir(self.current_dir)
                for file in files:
                    self.print_to_terminal(f"{file}\n")
            except:
                self.print_to_terminal("Error listing directory\n")
        
        elif cmd == "cd":
            try:
                if not args:
                    new_dir = os.path.expanduser("~")
                elif args[0] == "..":
                    new_dir = os.path.dirname(os.path.abspath(self.current_dir))
                else:
                    new_dir = os.path.abspath(os.path.join(self.current_dir, args[0]))
                
                if os.path.exists(new_dir) and os.path.isdir(new_dir):
                    os.chdir(new_dir)
                    self.current_dir = new_dir
                    self.print_to_terminal(f"Changed to: {self.current_dir}\n")
                else:
                    self.print_to_terminal("Directory not found\n")
            except Exception as e:
                self.print_to_terminal(f"Error changing directory: {str(e)}\n")
        
        elif cmd == "pwd":
            self.print_to_terminal(f"{self.current_dir}\n")
        
        elif cmd == "whoami":
            self.print_to_terminal(f"{self.username}\n")
        
        elif cmd == "touch":
            if args:
                try:
                    file_path = os.path.join(self.current_dir, args[0])
                    with open(file_path, 'a'):
                        self.print_to_terminal(f"Created file: {args[0]}\n")
                except Exception as e:
                    self.print_to_terminal(f"Error creating file: {str(e)}\n")
            else:
                self.print_to_terminal("Please specify filename\n")

        elif cmd == "admin":
            if not self.is_admin:
                if len(args) == 1 and args[0] == self.admin_password:
                    self.is_admin = True
                    self.print_to_terminal("Admin access granted!\n")
                else:
                    self.print_to_terminal("Invalid password\n")
            else:
                self.print_to_terminal("Already in admin mode\n")

        elif cmd == "shutdown" and self.is_admin:
            self.print_to_terminal("Shutting down...\n")
            self.root.after(2000, self.root.quit)

        elif cmd == "delete" and self.is_admin:
            if args:
                try:
                    file_path = os.path.join(self.current_dir, args[0])
                    os.remove(file_path)
                    self.print_to_terminal(f"Deleted file: {args[0]}\n")
                except Exception as e:
                    self.print_to_terminal(f"Error deleting file: {str(e)}\n")
            else:
                self.print_to_terminal("Please specify filename\n")

        elif cmd == "rename" and self.is_admin:
            if len(args) == 2:
                try:
                    old_path = os.path.join(self.current_dir, args[0])
                    new_path = os.path.join(self.current_dir, args[1])
                    os.rename(old_path, new_path)
                    self.print_to_terminal(f"Renamed {args[0]} to {args[1]}\n")
                except Exception as e:
                    self.print_to_terminal(f"Error renaming file: {str(e)}\n")
            else:
                self.print_to_terminal("Please specify old and new filenames\n")

        elif cmd == "changepw" and self.is_admin:
            if len(args) == 1:
                self.admin_password = args[0]
                self.print_to_terminal("Admin password changed successfully\n")
            else:
                self.print_to_terminal("Usage: changepw [new_password]\n")

        elif cmd in ["shutdown", "delete", "rename", "changepw"] and not self.is_admin:
            self.print_to_terminal("This command requires admin privileges\n")
        
        elif cmd == "cat":
            if args:
                try:
                    file_path = os.path.join(self.current_dir, args[0])
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            content = f.read()
                            self.print_to_terminal(f"{content}\n")
                    else:
                        self.print_to_terminal(f"File not found: {args[0]}\n")
                except Exception as e:
                    self.print_to_terminal(f"Error reading file: {str(e)}\n")
            else:
                self.print_to_terminal("Please specify filename\n")

        elif cmd == "exit":
            self.root.quit()
        
        else:
            self.print_to_terminal("Unknown command. Type 'help' for available commands.\n")

if __name__ == "__main__":
    app = UdonOS()
    app.root.mainloop()