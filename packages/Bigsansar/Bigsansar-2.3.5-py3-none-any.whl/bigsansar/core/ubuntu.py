
import os
import shutil
from bigsansar.core.pip_package import copy_file_from_pip_lib

from bigsansar.core.setup_linux_server import deploy_server


def deploy():

    print('RE-Configuring now')
    print('removing related file and folider')
    os.system('sudo rm -v /etc/ssh/sshd_config')
    source_ssh = copy_file_from_pip_lib('etc/sshd_config')
    os.system('sudo cp -v %s /etc/ssh/' % (source_ssh))
    print('re installing internal package')

    file_path = "www/settings.py"
        # Text to be deleted
    text_to_delete = '''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
        # Read the content of the file
    with open(file_path, 'r') as file:
            content = file.read()

        # Remove the specified text
    modified_content = content.replace(text_to_delete, '')

        # Write the modified content back to the file
    with open(file_path, 'w') as file:
            file.write(modified_content)

    print("Text removed successfully.")


    
