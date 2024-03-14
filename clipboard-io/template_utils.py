import subprocess, os

def list_templates():
    pass

def unpack_template(cpio_path: str,
                    output: str | None = None,
                    make_dirs: bool = False):
    # it is up to the user to make sure the output dir is clear

    # create intermediate directories
    if output and make_dirs:
        os.makedirs(output, exist_ok=True)

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
    if not output:
        output = os.getcwd()
    else:
        old_wd = os.getcwd()

    _, cpio_path_tail = os.path.split(cpio_path)
    cpio_out_dir = os.path.join(output, cpio_path_tail+".dir")
    cpio_out_contents = os.path.join(output, cpio_path_tail+".contents")
    os.mkdir(cpio_out_dir)
    os.chdir(cpio_out_dir)
    print("writing out files to:", cpio_out_dir)
    subprocess.run(["hcpio", "-idI", cpio_path])

    print("wiriting contents index to:", cpio_out_contents)
    with open(cpio_out_contents, "w") as f:
        subprocess.run(["hcpio", "-itI", cpio_path], stdout=f) 
    
    # restore working directory
    if old_wd:
        os.chdir(old_wd)

    print("Finished unpacking:", cpio_path)
    

def unpack_all():
    pass
