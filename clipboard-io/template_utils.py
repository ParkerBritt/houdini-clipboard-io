import subprocess, os

def list_templates():
    pass

def unpack_template(cpio_path: str,
                    output: None | str = None):
    # verify output exists
    if output and not os.path.exists(output):
        raise Exception("Output directory doesn't exist: "+output)

    # verify path exists and is cpio file
    if not os.path.exists(cpio_path):
        raise Exception("File doesn't exist: "+cpio_path)
    if not os.path.splitext(cpio_path)[1]==".cpio":
        print(os.path.splitext(cpio_path))
        raise Exception("Can't unpack. File doesn't have .cpio file extension: "+cpio_path)

    # change working directory to output extractred files appropriately
    old_wd = None
    if output:
        old_wd = os.getcwd()
        os.chdir(output)

    subprocess.run(["hexpand", cpio_path])
    
    # restore working directory
    if old_wd:
        os.chdir(old_wd)

    print("Finished unpacking:", cpio_path)
    

def unpack_all():
    pass
