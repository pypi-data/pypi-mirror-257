import click, os, subprocess

folder_path = os.path.dirname(__file__)

# @click.command()
# @click.argument('name', type=click.STRING, required=True)
# @click.argument('path', type=click.Path(exists=True))
def create_file(name, path):

    try:
        if not os.path.exists(path):
            raise click.BadParameter(f'{path} does not exist')
        
        # if not name.endswith(".py"):
        #     name += ".py"
        
        new_folder_path = os.path.join(path, f'{name}')
        
        txt_file = rf'{folder_path}\utils\{name}.txt'
        py_file = rf'{new_folder_path}'
        
        res = subprocess.run(['echo', '', '>', new_folder_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        with open(txt_file, 'r') as t, open(py_file, 'w') as p:
            txt_contents = t.read()
            p.write(txt_contents)
            
        if res.returncode == 0:
            click.echo(f"Successfully created {name} in the {new_folder_path} directory")
            
        else:
            click.echo(res.stderr)
    except Exception as e:
        click.echo(f'Ran an error: {str(e)}')
    
@click.command()
# @click.argument('content', type=click.STRING, metavar='CONTENT')
def edit_file():
    txt_file = rf'{folder_path}\imports.txt'
    py_file = rf'{folder_path}\app\all.py'
    try:
        with open(txt_file, 'r') as t, open(py_file, 'w') as p:
            txt_contents = t.read()
            p.write(txt_contents)
            # click.echo("Content copied successfully")
    except Exception as e:
        click.echo(f'Failed: {str(e)}')
    
    
if __name__=="__main__":
    edit_file()