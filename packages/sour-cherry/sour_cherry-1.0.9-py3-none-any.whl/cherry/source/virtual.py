import os, subprocess, click

def create_venv(name, path):
    """Creates a python virtual environment.

    Args:
        name (_str_): This will be the name of your virtual environment.
    """
    try:
        subprocess.run(['virtualenv', '-p', 'python3', rf'{path}\{name}'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        click.echo(f'Successfully created virtual environment: {name}')
    except Exception as e:
        click.echo(f'Failed to create virtual environment. Error: {str(e)}')
    
    # try:
    #     subprocess.run(['pip', 'install', '-r', rf'C:\Users\limzy\OneDrive\Desktop\Projects\cherry\utils\requirements.txt.txt', '--target', f'{path}\{name}\Lib\site-packages'])
    #     click.echo(f'Successfully installed all the required dependencies.')
    # except Exception as e:
    #     click.echo(f'Failure!!! Failure!!: {e}')



    
def activate_venv(name, path):
    try:
        activation_script_path = os.path.join(rf'{path}', f'{name}', 'Scripts', 'activate.bat')
        click.echo(activation_script_path)
        subprocess.run([activation_script_path], check=True, shell=(os.name=='nt'))
        click.echo(f'Successfully activated virtual environment: {name}')
    except Exception as e:
        click.echo(f'Failed to activate virtual environment. Error: {str(e)}')

def install_depend(path, name):
    try:
        subprocess.run(['pip', 'install', '-r', rf'{os.path.dirname(__file__)}\utils\requirements.txt.txt', '--target', f'{path}\{name}\Lib\site-packages'])
        click.echo(f'Successfully installed all the required dependencies.')
    except Exception as e:
        click.echo(f'Failure!!! Failure!!: {e}')
    