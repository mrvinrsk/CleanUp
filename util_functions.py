import os
import shutil


def delete_files(path):
    bytesize = 0
    deleted_files = 0

    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
            bytesize += os.path.getsize(path)
        elif os.path.isdir(path):
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)

                try:
                    if os.path.isfile(filepath) or os.path.islink(filepath):
                        fsize = os.path.getsize(filepath)
                        os.unlink(filepath)

                        if not os.path.exists(filepath):
                            bytesize += fsize
                            deleted_files += 1
                            print("File '" + filepath + "' deleted.")
                    elif os.path.isdir(filepath):
                        fsize = os.path.getsize(filepath)
                        shutil.rmtree(filepath)

                        if not os.path.exists(filepath):
                            bytesize += fsize
                            deleted_files += 1
                            print("Folder '" + filepath + "' deleted.")
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (filepath, e))

        return [bytesize, deleted_files]
    else:
        print("'" + path + "' couldn't be deleted, since it doesn't exist")
    return 0


def readable_bytes(size, decimals=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimals}f} {unit}"
