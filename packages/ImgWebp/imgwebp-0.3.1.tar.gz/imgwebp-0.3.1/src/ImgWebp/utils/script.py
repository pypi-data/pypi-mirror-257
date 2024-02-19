import os
import subprocess
import logging

from ImgWebp.utils.path import get_unpack_path,get_tmp_path,remove_tmp
from PIL import Image


def resize_image(input_image_path, output_image_path, size):
    with Image.open(input_image_path) as image:
        resized_image = image.resize(size)
        resized_image.save(output_image_path)


class CommandParameter:
    option = "-o"
    loop = "-loop"
    quality = {"混合": "-mixed", "无损": "-lossless", "有损": "-lossy"}
    time = "-d"

    def __init__(self, command, input_path, output_path):
        self.height_value = None
        self.width_value = None
        self.time_value = None
        self.quality_value = None
        self.loop_value = None
        self.output_type = None
        self.command = command
        self.input_path = input_path
        self.output_path = output_path

    def set_output_type(self, output_type):
        self.output_type = output_type
        return self

    def set_loop_value(self, loop_value):
        self.loop_value = loop_value

    def set_quality_value(self, quality_value):
        self.quality_value = self.quality[quality_value]

    def set_time_value(self, time_value):
        self.time_value = time_value
    def set_width_and_height(self,width_value,height_value):
        self.width_value = width_value
        self.height_value = height_value

    def get_args(self):
        if self.command == "cwebp":
            return self.cwebp()
        elif self.command == "dwebp":
            return self.dwebp()
        elif self.command == "gif2webp":
            return self.gif2webp()
        elif self.command == "img2webp":
            return self.img2webp()

    def img2webp(self):
        self.output_type = "webp"
        args =[]
        args0 = [self.loop,str(self.loop_value),self.quality_value,self.time,str(self.time_value)]
        args1 = self.get_input_file()
        args2 = [self.option,self.get_output_path(args1[0])]
        args4 = args0+args1+args2
        args.append(",".join(args4))
        return args

    def get_input_file(self) -> list:
        if os.path.isdir(self.input_path):
            files = [os.path.join(self.input_path, entry) for entry in os.listdir(self.input_path) if
                     os.path.isfile(os.path.join(self.input_path, entry))]
        else:
            files = self.input_path.split(",")

        if self.width_value and self.height_value:
            tmp_files=[]
            for file in files:
                tmp_file = os.path.join(get_tmp_path(),os.path.basename(file))
                resize_image(file, tmp_file, (int(self.width_value), int(self.height_value)))
                tmp_files.append(tmp_file)
            return tmp_files

        return files

    def gif2webp(self):
        self.output_type = "webp"
        args = []
        if os.path.isdir(self.input_path):
            files = [os.path.join(self.input_path, entry) for entry in os.listdir(self.input_path) if
                     os.path.isfile(os.path.join(self.input_path, entry)) and entry.lower().endswith(".gif")]
            for file in files:
                str_list = self.get_str_list(file)
                args.append(",".join(str_list))
        else:
            str_list = self.get_str_list(self.input_path)
            args.append(",".join(str_list))
        return args

    def dwebp(self):
        args = []
        if os.path.isdir(self.input_path):
            files = [os.path.join(self.input_path, entry) for entry in os.listdir(self.input_path) if
                     os.path.isfile(os.path.join(self.input_path, entry)) and entry.lower().endswith(".webp")]
            for file in files:
                str_list = self.get_str_list(file)
                args.append(",".join(str_list))
        else:
            str_list = self.get_str_list(self.input_path)
            args.append(",".join(str_list))
        return args

    def cwebp(self):
        self.output_type = "webp"
        args = []
        if os.path.isdir(self.input_path):
            files = [os.path.join(self.input_path, entry) for entry in os.listdir(self.input_path) if
                     os.path.isfile(os.path.join(self.input_path, entry))]
            for file in files:
                str_list = self.get_str_list(file)
                args.append(",".join(str_list))
        else:
            str_list = self.get_str_list(self.input_path)
            args.append(",".join(str_list))
        return args

    def get_str_list(self, input_path):
        output_path = self.get_output_path(input_path)
        return [input_path, self.option, output_path]

    def get_output_path(self,input_path):
        filename = os.path.basename(input_path).split(".")[0]
        return f"{self.output_path}/{filename}.{self.output_type}"


class LibWebp:
    def __init__(self, command, parameter: CommandParameter):
        self.success = False
        self.command = command
        self.parameter = parameter

    def run(self):
        arg_list = self.parameter.get_args()
        for param in arg_list:
            self.execute(param.split(","))

    def execute(self, args):
        script_path = os.path.join(get_unpack_path(), "bin", self.command)
        try:
            result = subprocess.run([script_path] + args, capture_output=True, text=True)
            if result.returncode == 0:
                self.success = True
                remove_tmp()
                msg = f"{self.command}执行成功，执行参数：{[script_path] + args}"
                logging.info(msg)

        except Exception as e:
            raise e


if __name__ == "__main__":
    commandParameter = CommandParameter(
        "opt/siteImg/img/AI/",
        "opt/siteImg/webp/AI")
    lw = LibWebp("cwebp", commandParameter)
    lw.run()
