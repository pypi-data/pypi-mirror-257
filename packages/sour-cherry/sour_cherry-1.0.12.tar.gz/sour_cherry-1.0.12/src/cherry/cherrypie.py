import click, os
from .source import virtual, folders, files

@click.group()
def cherrypie():
    pass

# new_path = r'c:\Users\limzy\OneDrive\Desktop\Projects\trial'
dest_path = os.getcwd()


@cherrypie.command()
@click.option('-n', '--name', type=click.STRING, default='venv', show_default=True, help='The name of the virtual environment')
@click.option('-a', '--activate', type=click.Choice(['y', 'n']), required= False, default='y', show_default=True, help='Allow virtual environment to be activated.')
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
    
def paint(name, path, activate):
    try:
        virtual.create_venv(name, path)
        click.echo("Success!!")
        if activate == 'y':
            virtual.activate_venv(name, path)
    except Exception as e:
        click.echo(f'I need virtual succour: {e}')
    
    try:
        virtual.install_depend(path=path, name=name)
    except Exception as e:
        click.echo(f'I need virtual succour: {e}')
        
        
        
map_dict = {
    'root': [
        '.env',
        '.gitignore',
        'requirements.txt',
        {
            'app': [
                {
                    'routers': ['route.py']
                },
                'config.py',
                'db.py',
                'main.py',
                'models.py',
                'schemas.py',
                'utils.py',
            ]
        },
        {
            'scripts': ['script1.py']
        },
        {
            'tests': ['test_example.py']
        }
    ]
}

def unpacker(dictio, path):
    for k, v in dictio.items():
        curr_path = path
        if k != 'root':
            curr_path = os.path.join(path, k)
        for content in v:
            if isinstance(content, dict):
                unpacker(content, curr_path)
            else:
               files.create_file(content, curr_path)
    return "Created!"
    
        

@cherrypie.command()
def blossom():
    try:
        directories = ['scripts', 'tests']
        for fol in directories:
            folders.folder(fol, dest_path)
        # folders.folder('scripts')
        folders.create_subfolder(dest_path, 'app', 'routers')
        click.echo("All done!!")
    except Exception as e:
        click.echo(f'I need folder succour: {str(e)}')   
    
    # Create files
    try:
        unpacker(map_dict, dest_path)
    except Exception as e:
        click.echo(f'I need files succour: {str(e)}')
        
if __name__=="__main__":
    cherrypie()