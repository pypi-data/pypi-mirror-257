import shutil

def zip_directory(source_directory = 'folder-to-zip',output_zip_file='filename.zip'):
    # Create a zip file containing the contents of the source directory
    shutil.make_archive(output_zip_file, 'zip', source_directory)
    # print(f"Zipped directory '{source_directory}' to '{output_zip_file}'")
    return source_directory,output_zip_file