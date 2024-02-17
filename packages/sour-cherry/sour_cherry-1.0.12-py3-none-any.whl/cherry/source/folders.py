import click, subprocess, os
path = os.getcwd()


def folder(name, path):
    path = os.path.join(path, name)
    try:
        result = subprocess.run(['mkdir', path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            click.echo('Command run successfully.')
            click.echo(result.stdout)
        else:
            click.echo(f'Command failed with error: {result.stderr}')
    except Exception as e:
        click.echo(f'An error occured: {str(e)}')


def create_subfolder(path, folder_name, subfolder_name):
    """
    Create a subfolder within a specified directory.
    """
    try:
        # Combine the provided directory and subfolder names to create the full path
        subfolder_path = os.path.join(path, folder_name, subfolder_name)

        # Use os.makedirs to create the subfolder (including any necessary parent folders)
        os.makedirs(subfolder_path)

        click.echo(f"Subfolder '{subfolder_name}' created in '{folder_name}'.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    folder()

    