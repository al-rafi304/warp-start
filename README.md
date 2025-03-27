# 🚀 WarpStart

**WarpStart** is a terminal-based utility that helps you quickly launch all the tools and commands you need to get started on a project — all from a friendly interactive interface.

## ✨ Features

- 📁 Create named "project" profiles  
- ✅ Select multiple apps to open (VS Code, terminal, browser, etc.)
- 💻 Define project-specific commands to run automatically
- 📂 Open terminals in specific directories and run commands
- 🌎 Navigate to specified websites on browser launch
- 🔁 Reusable setup: open your saved project anytime with a few keystrokes

## 🧑‍💻 Usage

Run the script (Python required)

```bash
python warp-start.py
```
Make sure you have the required libraries installed:
```bash
pip install typer InquirerPy
```
## 📦 Build a Standalone Executable

You can turn warp-start.py into a standalone executable using PyInstaller:

 - Step 1: Install PyInstaller
   
   ```bash
   pip install pyinstaller
   ```
 - Step 2: Build the executable
   ```bash
   pyinstaller --onefile warp-start.py
   ```
This will create a single binary in the dist/ folder.

## 🛠️ Install Globally (Optional)

To make warpstart accessible from anywhere:

 - Step 1: Move the binary to a folder in your PATH
   ```bash
   mv dist/warp-start ~/.bin/
   ```
 - Step 2: Ensure ~/bin is in your PATH (add to ~/.bashrc or ~/.zshrc if needed)
   ```bash
   export PATH="$HOME/.bin:$PATH"
   ```
Now you can simply run:
```bash
warp-start
```
## 📁 Project Data

Project configurations are stored in:
```bash
~/.warpstart/projects.json
```
You can edit or remove saved projects from there if needed.
