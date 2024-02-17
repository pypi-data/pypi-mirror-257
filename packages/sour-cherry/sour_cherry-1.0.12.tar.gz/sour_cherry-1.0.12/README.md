# Cherry
This is a Python based CLI tool to create essentials for FastAPI backend development.

# Introduction 
 - Built with Python Click, you can easily create and activate virtual environments, insall some of the popular and necessary libraries and dependencies all with one command. 
 - Additionally, you can create files and directories in a specified hierachical order to ease project clutter also with one single command.
 - All python files are initiated with some boilerplate code and examples that you can customize according to your project needs.

# Usage
> [!IMPORTANT]
> Cherry is compatible with windows systems. UNIX support to be added soon.

 - **Install cherry** Run the pip command as shown above.
 - Cherry has two commands: `paint` & `blossom`.
 - **Paint:** `cherry paint` creates a virtual environment, activates it and installs some of the required dependencies. It accepts one argument, `name`, flagged as `-n` which will be used as the name of your virtual environment. Default is 'venv' if -n is not provided. For example `cherry paint -n example` will create a virtual environment called 'example'.
 - **Blossom:** running `cherry blossom` creates the necessary files and directories.
 - After running the two commands, switch to your new virtual environment by clicking on the pop-up vscode message and starting a new console window or running `name-of-your-virtual-environment\Scripts\activate`. For e.g., if you created a virtual environment called 'example', run `example\Scripts\activate`.
  - **You're now ready to start developing!!**