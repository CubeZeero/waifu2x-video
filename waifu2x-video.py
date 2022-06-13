# coding: utf-8

import PySimpleGUI as sg
import os
import configparser
import shutil
import time
import subprocess
import threading
import ffmpeg
from ffmpeg_progress_yield import FfmpegProgress as fmpg

import version
import window_layout

software_version = version.VERSION()
window_title = 'waifu2x-video v' + software_version

icon_path = 'w2xv_data/img/icon.ico'

current_path = os.getcwd()

config_ini = configparser.ConfigParser()
config_ini.read('w2xv_data/config.ini', encoding = 'utf-8')

waifu2x_cui_path = config_ini['DEFAULT']['waifu2x_path']

sg.LOOK_AND_FEEL_TABLE['white'] = {
    'BACKGROUND': '#ffffff',
    'TEXT': 'black',
    'INPUT': '#eeeeee',
    'SCROLL': '#4169e1',
    'TEXT_INPUT': '#4169e1',
    'BUTTON': ('white', '#4169e1'),
    'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 0,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

sg.theme('white')

with open('w2xv_data/lists/ffmpeg_codecs.txt') as fm_codecs:
    ffmpeg_codec_list = fm_codecs.read().splitlines()

with open('w2xv_data/lists/ffmpeg_formats.txt') as fm_formats:
    img_format_list = fm_formats.read().splitlines()

ffmpeg_preset_list = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow', 'placebo']
waifu2x_model_list = ['2次元イラスト(UpRGBモデル)', '写真・アニメ(UpPhotoモデル)', '2次元イラスト(RGBモデル)', '写真・アニメ(Photoモデル)', '2次元イラスト(Yモデル)', '2次元イラスト(UpResNet10)', '2次元イラスト(CUnet)']
separate_list = ['64', '100', '128', '240', '256', '384', '432', '480', '512']

waifu2x_model_dict = {
    '2次元イラスト(UpRGBモデル)': 'upconv_7_anime_style_art_rgb',
    '写真・アニメ(UpPhotoモデル)': 'upconv_7_photo',
    '2次元イラスト(RGBモデル)': 'anime_style_art_rgb',
    '写真・アニメ(Photoモデル)': 'photo',
    '2次元イラスト(Yモデル)': 'anime_style_art_y',
    '2次元イラスト(UpResNet10モデル)': 'upresnet10',
    '2次元イラスト(CUnetモデル)': 'cunet'}

def disabled_object(sw_disabled):
    #crap code :(
    main_window['-ffmpeg_presets_combo-'].update(disabled = sw_disabled)
    main_window['-ffmpeg_codecs_combo-'].update(disabled = sw_disabled)
    main_window['-img_format_combo-'].update(disabled = sw_disabled)
    main_window['-ffmpeg_pass_combo-'].update(disabled = sw_disabled)
    main_window['-ffmpeg_codecs_combo-'].update(disabled = sw_disabled)
    main_window['-ffmpeg_bitrate-'].update(disabled = sw_disabled)
    main_window['-inputfile_path-'].update(disabled = sw_disabled)
    main_window['-input_browse_button-'].update(disabled = sw_disabled)
    main_window['-outputfile_path-'].update(disabled = sw_disabled)
    main_window['-output_browse_button-'].update(disabled = sw_disabled)
    main_window['-crf_checkbox-'].update(disabled = sw_disabled)
    main_window['-audio_copy_checkbox-'].update(disabled = sw_disabled)
    main_window['-cm_00_radio-'].update(disabled = sw_disabled)
    main_window['-cm_01_radio-'].update(disabled = sw_disabled)
    main_window['-cm_02_radio-'].update(disabled = sw_disabled)
    main_window['-scale_w-'].update(disabled = sw_disabled)
    main_window['-scale_h-'].update(disabled = sw_disabled)
    main_window['-nl_00_radio-'].update(disabled = sw_disabled)
    main_window['-nl_01_radio-'].update(disabled = sw_disabled)
    main_window['-nl_02_radio-'].update(disabled = sw_disabled)
    main_window['-nl_03_radio-'].update(disabled = sw_disabled)
    main_window['-model_list_combo-'].update(disabled = sw_disabled)
    main_window['-seperate_list_combo-'].update(disabled = sw_disabled)
    main_window['-batch_list_combo-'].update(disabled = sw_disabled)
    main_window['-tta_checkbox-'].update(disabled = sw_disabled)
    main_window['-pm_00_radio-'].update(disabled = sw_disabled)
    main_window['-pm_01_radio-'].update(disabled = sw_disabled)
    main_window['-start_button-'].update(disabled = sw_disabled)
    main_window['-cancel_button-'].update(disabled = not sw_disabled)
    main_window['-open_setting_button-'].update(disabled = sw_disabled)
    main_window['-crf_spin-'].update(disabled = sw_disabled)

def convert_long_task():

    global current_step
    global task_cancel_flag

    if main_values['-audio_copy_checkbox-'] == True:
        current_step += 1
        main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Audio extraction' + task_cancel_msg)

        fmac_cmd = ['ffmpeg', '-y', '-i', input_video_path, '-vn', current_path + '\w2xv_tmp\\audio_tmp.mp3']

        fmac = fmpg(fmac_cmd)
        for fmac_progress in fmac.run_command_with_progress():
            main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Audio extraction' + task_cancel_msg)
            main_window['-pb-'].update(current_count = fmac_progress)
            main_window.refresh()

        time.sleep(1)

    if task_cancel_flag == 1:
        main_window['-status_text-'].update(value = 'on Standby...')
        main_window['-pb-'].update(current_count = 0, max = 100)
        shutil.rmtree(current_path + '\w2xv_tmp')
        disabled_object(False)
        return

    current_step += 1
    main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Dismantle to image sequence' + task_cancel_msg)

    fmis_cmd = ['ffmpeg', '-y', '-i', input_video_path, '-r', str(video_info_fps), current_path + '\w2xv_tmp\\img_sequence\\img_tmp_%05d.' + img_format]

    fmis = fmpg(fmis_cmd)
    for fmis_progress in fmis.run_command_with_progress():
        main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Dismantle to image sequence' + task_cancel_msg)
        main_window['-pb-'].update(current_count = fmis_progress)
        main_window.refresh()

    if task_cancel_flag == 1:
        main_window['-status_text-'].update(value = 'on Standby...')
        main_window['-pb-'].update(current_count = 0, max = 100)
        disabled_object(False)
        shutil.rmtree(current_path + '\w2xv_tmp')
        return

    imgs_files_sum = int(sum(os.path.isfile(os.path.join(current_path + '\\w2xv_tmp\\img_sequence', name)) for name in os.listdir(current_path + '\\w2xv_tmp\\img_sequence')))

    main_window['-pb-'].update(current_count = 0, max = imgs_files_sum)
    current_step += 1

    for cnt in range(imgs_files_sum):

        if task_cancel_flag == 1:
            main_window['-status_text-'].update(value = 'on Standby...')
            main_window['-pb-'].update(current_count = 0, max = 100)
            shutil.rmtree(current_path + '\w2xv_tmp')
            disabled_object(False)
            break

        main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Waifu2x up convert... ' + str(cnt) + '/' + str(imgs_files_sum))
        main_window['-pb-'].update(current_count = cnt)

        waifu2x_res = subprocess.run([waifu2x_cui_path,
                                    '-i', str(current_path + '\w2xv_tmp\\img_sequence\\img_tmp_' + str(cnt).zfill(5) + '.' + img_format),
                                    '-o', str(current_path + '\w2xv_tmp\\img_sequence_us\\img_tmp_' + str(cnt).zfill(5) + '.' + img_format),
                                    '-m', str(convert_mode),
                                    '-n', str(noise_level),
                                    '-w', str(scale_level_w),
                                    '-h', str(scale_level_h),
                                    '-p', str(proseccor_mode),
                                    '-c', str(waifu2x_separate),
                                    '-y', str(waifu2x_model),
                                    '-b', str(waifu2x_batch),
                                    '-t', str(tta_mode)], shell = True, capture_output = True)

        main_window.refresh()

    if task_cancel_flag == 1: return

    current_step += 1
    main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Converting to video' + task_cancel_msg)
    main_window['-pb-'].update(current_count = 0, max = 100)

    if main_values['-crf_checkbox-'] == True:
        if main_values['-audio_copy_checkbox-'] == True:
            fmcv_cmd = ['ffmpeg', '-y', '-r', str(video_info_fps), '-i', current_path + '\w2xv_tmp\\img_sequence_us\\img_tmp_%05d.' + img_format, '-i', current_path + '\w2xv_tmp\\audio_tmp.mp3', '-vcodec', str(ffmpeg_codec), '-crf', str(ffmpeg_crf), '-pix_fmt', 'yuv420p', '-preset', str(ffmpeg_preset), '-r', str(video_info_fps), str(output_video_path)]
        else:
            fmcv_cmd = ['ffmpeg', '-y', '-r', str(video_info_fps), '-i', current_path + '\w2xv_tmp\\img_sequence_us\\img_tmp_%05d.' + img_format, '-vcodec', str(ffmpeg_codec), '-crf', str(ffmpeg_crf), '-pix_fmt', 'yuv420p', '-preset', str(ffmpeg_preset), '-r', str(video_info_fps), str(output_video_path)]
    else:
        if main_values['-audio_copy_checkbox-'] == True:
            fmcv_cmd = ['ffmpeg', '-y', '-r', str(video_info_fps), '-i', current_path + '\w2xv_tmp\\img_sequence_us\\img_tmp_%05d.' + img_format, '-i', current_path + '\w2xv_tmp\\audio_tmp.mp3', '-vcodec', str(ffmpeg_codec), '-b:v', str(ffmpeg_bitrate), '-pix_fmt', 'yuv420p', '-pass', str(ffmpeg_pass), '-preset', str(ffmpeg_preset), '-r', str(video_info_fps), str(output_video_path)]
        else:
            fmcv_cmd = ['ffmpeg', '-y', '-r', str(video_info_fps), '-i', current_path + '\w2xv_tmp\\img_sequence_us\\img_tmp_%05d.' + img_format, '-vcodec', str(ffmpeg_codec), '-b:v', str(ffmpeg_bitrate), '-pix_fmt', 'yuv420p', '-pass', str(ffmpeg_pass), '-preset', str(ffmpeg_preset), '-r', str(video_info_fps), str(output_video_path)]

    fmcv = fmpg(fmcv_cmd)
    for fmcv_progress in fmcv.run_command_with_progress():
        main_window['-status_text-'].update(value = 'Step ' + str(current_step) + '/' + pg_step_max + ': Converting to video' + task_cancel_msg)
        main_window['-pb-'].update(current_count = fmcv_progress)
        main_window.refresh()

    main_window.write_event_value('-endtask-', 'DONE')

    return



main_window = window_layout.lo_main_window(sg, window_title, icon_path, ffmpeg_preset_list, ffmpeg_codec_list, img_format_list, waifu2x_model_list, separate_list)

while True:
    main_event, main_values = main_window.read()

    if main_event == sg.WIN_CLOSED:
        break

    if main_event == '-open_setting_button-':
        setting_window = window_layout.lo_setting_window(sg, window_title, icon_path, waifu2x_cui_path)

        while True:
            setting_event, setting_values = setting_window.read()

            if setting_event == sg.WIN_CLOSED or setting_event == '-setting_cancel_button-':
                break

            if setting_event == '-setting_ok_button-':
                config_ini['DEFAULT']['waifu2x_path'] = setting_values['-w2x_path-']
                waifu2x_cui_path = setting_values['-w2x_path-']

                with open('w2xv_data/config.ini', 'w', encoding = 'utf-8') as cf_file:
                    config_ini.write(cf_file)

                break

        setting_window.close()

    if main_event == '-cancel_button-':
        task_cancel_flag = 1
        task_cancel_msg = ' (This step runs to the end)'

    if main_event == '-endtask-':
        main_window['-status_text-'].update(value = 'on Standby...')
        main_window['-pb-'].update(current_count = 0, max = 100)
        shutil.rmtree(current_path + '\w2xv_tmp')
        disabled_object(False)

    if main_event == '-start_button-':

        if os.path.exists(waifu2x_cui_path) == True:

            if main_values['-inputfile_path-'] != '' and main_values['-outputfile_path-'] != '':

                os.mkdir(current_path + '\w2xv_tmp')
                os.mkdir(current_path + '\w2xv_tmp\img_sequence')
                os.mkdir(current_path + '\w2xv_tmp\img_sequence_us')
                disabled_object(True)

                input_video_path = main_values['-inputfile_path-']
                output_video_path = main_values['-outputfile_path-']

                img_format = main_values['-img_format_combo-']
                ffmpeg_preset = main_values['-ffmpeg_presets_combo-']
                ffmpeg_codec = main_values['-ffmpeg_codecs_combo-']
                ffmpeg_crf = main_values['-crf_spin-']
                ffmpeg_bitrate = main_values['-ffmpeg_bitrate-']
                ffmpeg_pass = main_values['-ffmpeg_pass_combo-']

                for cnt in range(4):
                    if main_values['-nl_0' + str(cnt) + '_radio-'] == True: noise_level = cnt

                if main_values['-cm_00_radio-'] == True: convert_mode = 'scale'
                if main_values['-cm_01_radio-'] == True: convert_mode = 'noise_scale'
                if main_values['-cm_02_radio-'] == True: convert_mode = 'auto_scale'

                if main_values['-pm_00_radio-'] == True: proseccor_mode = 'cpu'
                if main_values['-pm_01_radio-'] == True: proseccor_mode = 'gpu'

                waifu2x_model = waifu2x_model_dict[main_values['-model_list_combo-']]
                waifu2x_separate = main_values['-seperate_list_combo-']
                waifu2x_batch = main_values['-batch_list_combo-']

                scale_level_w = main_values['-scale_w-']
                scale_level_h = main_values['-scale_h-']

                tta_mode = int(bool(main_values['-tta_checkbox-']))

                probe = ffmpeg.probe(input_video_path)
                video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
                video_info_fps = int(video_info['r_frame_rate'].split('/')[0])

                current_step = 0
                task_cancel_flag = 0
                task_cancel_msg = ''

                pg_step_max = '4' if main_values['-audio_copy_checkbox-'] == True else '3'

                threading.Thread(target = convert_long_task, daemon = True).start()

            else:
                main_window['-status_text-'].update(value = 'ERROR: 入出力パスを指定してください')

        else:
            main_window['-status_text-'].update(value = 'ERROR: waifu2x-caffe-cui.exe のパスを指定してください')
