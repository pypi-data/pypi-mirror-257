import os
from gxl_ai_utils.utils import utils_file
if __name__ == '__main__':
    base_url = "/home/work_nfs7/tyxu/peoples_speech"
    final_tar_dir = "/home/backup_nfs5/xlgeng/data/shard_asr/peoples_speech"
    utils_file.makedir_sil(final_tar_dir)
    raw_dir = "/home/work_nfs8/xlgeng/data/raw/peoples_speech"
    utils_file.makedir_sil(raw_dir)
    all_part = ['test', 'train', 'validation']
    all_part = ['validation']
    for part in all_part:
        temp_part = os.path.join(base_url, part)
        utils_file.logging_print(f"开始处理如下目录 {temp_part}")
        temp_raw_dir = os.path.join(raw_dir, part)
        temp_final_tar_dir = os.path.join(final_tar_dir, part)
        # 得到所有tar_path list
        tar_path_dict = utils_file.get_file_path_list_for_wav_dir(temp_part, suffix=".tar", recursive=True)
        utils_file.print_list(tar_path_dict)
        for i, tar_path in enumerate(tar_path_dict):
            utils_file.logging_print(f"处理第 {i} 个 {tar_path}")
            utils_file.do_decompression_tar(tar_path=tar_path, output_dir=temp_raw_dir)