import os
import io
from pathlib import Path

OUTPUT_DIR = "./models"

def main():
    create_output_dir()

    root_dir = Path("./content/data/afs")
    file_list = [f for f in root_dir.glob('**/*') if f.is_file()]
    for file in file_list:
        parse_file(file)

def parse_file(filepath: str):
    with open(filepath, "rb") as f:
        model_index = 0
        motion_model_index = 0
        motion_index = 0
        while (text := f.read(4)):
            match text:
                case b"GIXL":
                    parse_global_texture_list_data(f, filepath, model_index)
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

def parse_global_texture_list_data(reader: io.BufferedReader, filepath: str, model_index: int) -> None:
    create_output_dir(get_file_name(filepath))
    write_filename = write_gixl_filename(filepath, model_index)
    print("writing GIXL: {}".format(write_filename))
    with open(write_filename, "wb") as writer:
        bytes_to_read = int.from_bytes(reader.read(4), byteorder='little', signed=False)
        data = reader.read(bytes_to_read)
        writer.write(b"GIXL")
        writer.write(bytes_to_read.to_bytes(4, byteorder='little', signed=False))
        writer.write(data)

def parse_model_data(reader: io.BufferedReader, filepath: str, model_index: int) -> None:
    create_output_dir(get_file_name(filepath))
    write_filename = write_model_filename(filepath, model_index)
    print("writing model: {}".format(write_filename))
    with open(write_filename, "wb") as writer:
        bytes_to_read = int.from_bytes(reader.read(4), byteorder='little', signed=False)
        data = reader.read(bytes_to_read)
        writer.write(b"NJCM")
        writer.write(bytes_to_read.to_bytes(4, byteorder='little', signed=False))
        writer.write(data)
        parse_pointer_definition_data(reader, writer)
        parse_mcs_definition_data(reader, writer)

def parse_motion_data(reader: io.BufferedReader, filepath: str, motion_model_index: int, motion_index: int) -> None:
    create_output_dir(get_file_name(filepath))
    write_filename = write_motion_filename(filepath, motion_model_index, motion_index)
    print("writing motion: {}".format(write_filename))
    with open(write_filename, "wb") as writer:
        bytes_to_read = int.from_bytes(reader.read(4), byteorder='little', signed=False)
        data = reader.read(bytes_to_read)
        writer.write(b"NMDM")
        writer.write(bytes_to_read.to_bytes(4, byteorder='little', signed=False))
        writer.write(data)
        parse_pointer_definition_data(reader, writer)
        parse_gamt_definition_data(reader, writer)

def parse_mcs_definition_data(reader: io.BufferedReader, writer: io.BufferedWriter) -> None:
    generic_read_definition_data(reader, writer, b"MCS_")
    
def parse_pointer_definition_data(reader: io.BufferedReader, writer: io.BufferedWriter) -> None:
    generic_read_definition_data(reader, writer, b"POF0")

def parse_gamt_definition_data(reader: io.BufferedReader, writer: io.BufferedWriter) -> None:
    generic_read_definition_data(reader, writer, b"GAMT")

def generic_read_definition_data(reader: io.BufferedReader, writer: io.BufferedWriter, magic: bytes) -> None:
    text = reader.read(4)
    if text == magic:
        bytes_to_read = int.from_bytes(reader.read(4), byteorder='little', signed=False)
        data = reader.read(bytes_to_read)
        writer.write(magic)
        writer.write(bytes_to_read.to_bytes(4, byteorder='little', signed=False))
        writer.write(data)
    else:
        reader.seek(-4, os.SEEK_CUR)

def write_gixl_filename(filepath: str, model_index: int) -> str:
    return "{}/{}/{}_model_{}_gixl.dat".format(OUTPUT_DIR, get_file_name(filepath), get_full_file_name(filepath), model_index)

def write_model_filename(filepath: str, model_index: int) -> str:
    return "{}/{}/{}_model_{}.nj".format(OUTPUT_DIR, get_file_name(filepath), get_full_file_name(filepath), model_index)

def write_motion_filename(filepath: str, motion_model_index: int, motion_index: int) -> str:
    return "{}/{}/{}_model_{}_motion_{}.njm".format(OUTPUT_DIR, get_file_name(filepath), get_full_file_name(filepath), motion_model_index, motion_index)

def get_full_file_name(filepath: str) -> str:
    return os.path.basename(filepath)

def get_file_name(filepath: str) -> str:
    return os.path.splitext(get_full_file_name(filepath))[0]

def create_output_dir(extension: str = None):
    os.makedirs("{}/{}".format(OUTPUT_DIR, (extension or "")), exist_ok=True)

if __name__ == "__main__":
    main()