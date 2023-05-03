import sys
import os
import io

OUTPUT_DIR = "./models"

def main():
    create_output_dir()

    args = sys.argv[1:]
    if len(args) <= 0:
        print("Missing file to parse, please provide at least one file.")
        return
    
    for filepath in args:
        with open(filepath, "rb") as f:
            print("file opened: {}".format(filepath))
            model_index = 0
            motion_model_index = 0
            motion_index = 0
            while (text := f.read(4)):
                match text:
                    case b"NJCM":
                        parse_model_data(f, filepath, model_index)
                        model_index += 1
                    case b"MIXL":
                        f.seek(4, os.SEEK_CUR)
                        motion_model_index = int.from_bytes(f.read(1), byteorder='little', signed=False)
                        # reset motion index for new model
                        motion_index = 0
                        f.seek(3, os.SEEK_CUR)
                    case b"NMDM":
                        parse_motion_data(f, filepath, motion_model_index, motion_index)
                        motion_index += 1

def parse_model_data(reader: io.BufferedReader, filepath: str, model_index: int) -> None:
    write_filename = write_model_filename(filepath, model_index)
    print("writing model: {}".format(write_filename))
    with open(write_filename, "wb") as writer:
        bytes_to_read = int.from_bytes(reader.read(4), byteorder='little', signed=False)
        data = reader.read(bytes_to_read)
        writer.write(b"NJCM")
        writer.write(bytes_to_read.to_bytes(4, byteorder='little', signed=False))
        writer.write(data)

def parse_motion_data(reader: io.BufferedReader, filepath: str, motion_model_index: int, motion_index: int) -> None:
    write_filename = write_motion_filename(filepath, motion_model_index, motion_index)
    print("writing motion: {}".format(write_filename))
    with open(write_filename, "wb") as writer:
        bytes_to_read = int.from_bytes(reader.read(4), byteorder='little', signed=False)
        data = reader.read(bytes_to_read)
        writer.write(b"NMDM")
        writer.write(bytes_to_read.to_bytes(4, byteorder='little', signed=False))
        writer.write(data)

def write_model_filename(filepath: str, model_index: int) -> str:
    return "{}/{}_model_{}.nj".format(OUTPUT_DIR, get_file_name(filepath), model_index)

def write_motion_filename(filepath: str, motion_model_index: int, motion_index: int) -> str:
    return "{}/{}_model_{}_motion_{}.njm".format(OUTPUT_DIR, get_file_name(filepath), motion_model_index, motion_index)

def get_file_name(filepath: str) -> str:
    return os.path.basename(filepath)

def create_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":
    main()