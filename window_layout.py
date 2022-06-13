def lo_main_window(sg, window_title, icon_path, ffmpeg_preset_list, img_format_list, waifu2x_model_list, separate_list):

        ffmpeg_presets = [[sg.Combo(ffmpeg_preset_list, ffmpeg_preset_list[5], font = ['Meiryo',8], size = (10,1), readonly = True, key = '-ffmpeg_presets_combo-')]]

        #ffmpeg_codecs = [[sg.Combo(ffmpeg_codec_list, ffmpeg_codec_list[0], font = ['Meiryo',8], size = (10,1), readonly = True, key = '-ffmpeg_codecs_combo-')]]

        img_formats = [[sg.Combo(img_format_list, img_format_list[1], font = ['Meiryo',8], size = (10,1), readonly = True, key = '-img_format_combo-')]]

        ffmpeg_bitrate = [[sg.Input('30000000', font = ['Meiryo',8], size = (20,1), key = '-ffmpeg_bitrate-'), sg.Text(text = 'bps', font = ['Meiryo',8])]]

        #ffmpeg_pass = [[sg.Combo(['1', '2'], '1', font = ['Meiryo',8], size = (6,1), readonly = True, key = '-ffmpeg_pass_combo-')]]

        crf_set = [[sg.Spin([num for num in range(52)], 23, font = ['Meiryo',8], readonly = True, key = '-crf_spin-')]]

        fileinout_lo = [[sg.Text(text = '入力パス', font = ['Meiryo',8], pad = ((10,0),(10,0))), sg.Input(font = ['Meiryo',8], size = (100,1), pad = ((20,0),(10,0)), key = '-inputfile_path-'),
                         sg.FileBrowse(button_text = '参照', target = "-inputfile_path-", file_types=(("Video file", ""),), font = ['Meiryo',8], size = (10,1), pad = ((20,10),(10,0)), key = '-input_browse_button-')],

                        [sg.Text(text = '出力パス', font = ['Meiryo',8], pad = ((10,0),(10,10))), sg.Input(font = ['Meiryo',8], size = (100,1), pad = ((20,0),(10,10)), key = '-outputfile_path-'),
                         sg.FileSaveAs(button_text = '参照', target = "-outputfile_path-", file_types=(("Video file", ""),), font = ['Meiryo',8], size = (10,1), pad = ((20,10),(10,10)), key = '-output_browse_button-')],

                        [sg.Frame('出力プリセット', ffmpeg_presets, font = ['Meiryo',8], border_width = 1, pad = ((10,0),(0,10))), sg.Frame('crf', crf_set, font = ['Meiryo',8], pad = ((10,0),(0,10)), border_width = 1),
                         sg.Checkbox(text = 'crfを使用する', default = True, font = ['Meiryo',8], pad = ((10,0),(7,0)), key = '-crf_checkbox-'),
                         sg.Checkbox(text = '音声もコピー', default = True, font = ['Meiryo',8], pad = ((10,0),(7,0)), key = '-audio_copy_checkbox-'),
                         sg.Frame('画像フォーマット', img_formats, font = ['Meiryo',8], border_width = 1, pad = ((10,0),(0,10))),
                         sg.Frame('ビットレート', ffmpeg_bitrate, font = ['Meiryo',8], border_width = 1, pad = ((10,0),(0,10))), sg.Text(text = 'コーデック: h264(libx264)', font = ['Meiryo',8], pad = ((30,0),(0,0)))]]

        convert_mode = [[sg.Radio('拡大', 'convert_mode_grp', default = True, font = ['Meiryo',8], key = '-cm_00_radio-')], [sg.Radio('ノイズ除去と拡大', 'convert_mode_grp', default = False, font = ['Meiryo',8], key = '-cm_01_radio-')],
                        [sg.Radio('ノイズ除去(自動判別)と拡大', 'convert_mode_grp', default = False, font = ['Meiryo',8], key = '-cm_02_radio-')],
                        [sg.Text(text = '拡大', font = ['Meiryo',8], pad = ((10,0),(0,0))),
                         sg.Input('1920', font = ['Meiryo',8], size = (6,1), pad = ((10,0),(10,10)), key = '-scale_w-'), sg.Text(text = 'x', font = ['Meiryo',8], pad = ((10,0),(0,0))), sg.Input('1080', font = ['Meiryo',8], size = (6,1), pad = ((10,0),(10,10)), key = '-scale_h-')]]

        convert_noiselevel = [[sg.Radio('レベル0', 'convert_noiselevel_grp', default = True, font = ['Meiryo',8], key = '-nl_00_radio-')], [sg.Radio('レベル1', 'convert_noiselevel_grp', default = False, font = ['Meiryo',8], key = '-nl_01_radio-')],
                              [sg.Radio('レベル2', 'convert_noiselevel_grp', default = False, font = ['Meiryo',8], key = '-nl_02_radio-')], [sg.Radio('レベル3', 'convert_noiselevel_grp', default = False, font = ['Meiryo',8], key = '-nl_03_radio-')]]

        waifu2x_sets = [[sg.Combo(waifu2x_model_list, waifu2x_model_list[0], font = ['Meiryo',8], size = (25,1), pad = ((10,10),(10,0)), readonly = True, key = '-model_list_combo-')],
                        [sg.Text(text = '分割サイズ', font = ['Meiryo',8], pad = ((10,0),(10,0))), sg.Combo(separate_list, separate_list[2], font = ['Meiryo',8], size = (6,1), pad = ((10,0),(10,0)), readonly = True, key = '-seperate_list_combo-')],
                        [sg.Text(text = 'バッチサイズ', font = ['Meiryo',8], pad = ((10,0),(10,10))), sg.Combo([num for num in range(1,21)], 1, font = ['Meiryo',8], size = (6,1), pad = ((10,0),(10,10)), readonly = True, key = '-batch_list_combo-')],
                        [sg.Checkbox(text = 'TTAモード使用', default = True, font = ['Meiryo',8], pad = ((10,0),(0,0)), key = '-tta_checkbox-')]]

        convertset_lo = [[sg.Frame('変換モード・拡大率', convert_mode, font = ['Meiryo',8], border_width = 1, pad = ((10,0),(0,10))), sg.Frame('ノイズ除去レベル', convert_noiselevel, font = ['Meiryo',8], border_width = 1, pad = ((10,0),(0,10))),
                          sg.Frame('Waifu2x設定', waifu2x_sets, font = ['Meiryo',8], border_width = 1, pad = ((10,10),(0,10)))]]

        proseccor_mode = [[sg.Radio('CPU', 'proseccor_mode_grp', default = False, font = ['Meiryo',8], key = '-pm_00_radio-')], [sg.Radio('GPU(cuDNN)', 'proseccor_mode_grp', default = True, font = ['Meiryo',8], key = '-pm_01_radio-')]]

        pm_button_column = [[sg.Frame('プロセッサー', proseccor_mode, font = ['Meiryo',8], border_width = 1)],
                            [sg.Button(button_text = '実行', font = ['Meiryo',8], size = (10,1), pad = ((20,10),(10,0)), key = '-start_button-')],
                            [sg.Button(button_text = 'キャンセル', font = ['Meiryo',8], size = (10,1), pad = ((20,10),(10,0)), key = '-cancel_button-', disabled = True)]]

        w2xv_set_column = [[sg.Image(source = 'w2xv_data/img/logo_mini.png', pad = ((50,0),(20,0)))],
                           [sg.Button(button_text = '詳細設定', font = ['Meiryo',8], size = (10,1), pad = ((62,0),(10,0)), key = '-open_setting_button-')]]

        main_layout = [[sg.Frame('入出力設定', fileinout_lo, font = ['Meiryo',10], border_width = 1)],
                       [sg.Frame('変換画質・処理設定', convertset_lo, font = ['Meiryo',10], border_width = 1), sg.Column(pm_button_column), sg.Column(w2xv_set_column)],
                       [sg.ProgressBar(100, size_px = (870,20), pad = ((6,0),(10,0)), key = '-pb-')],
                       [sg.Text(text = 'on Standby...', font = ['Meiryo',8], pad = ((10,0),(10,0)), key = '-status_text-')]]

        return sg.Window(window_title, main_layout, icon = icon_path, size = (900,430), font = ['Meiryo',12])

def lo_setting_window(sg, window_title, icon_path, waifu2x_cui_path, final_enc_cmd, tmp_folder_chk):

        setting_layout = [[sg.Text(text = 'waifu2x-caffe-cuiの場所', font = ['Meiryo',8], pad = ((0,0),(10,0))), sg.Input(waifu2x_cui_path, font = ['Meiryo',8], size = (70,1), pad = ((20,0),(10,0)), key = '-w2x_path-'),
                           sg.FileBrowse(button_text = '参照', target = "-w2x_path-", file_types=(("waifu2x-caffe-cui", "*.exe"),), font = ['Meiryo',8], size = (10,1), pad = ((20,0),(10,0)), key = '-w2x_browse_button-')],
                          [sg.Text(text = '最終書き出し用コマンド', font = ['Meiryo',8], pad = ((0,0),(10,0))), sg.Input(final_enc_cmd, font = ['Meiryo',8], size = (85,1), pad = ((20,0),(10,0)), key = '-final_enc_cmd-')],
                          [sg.Text(text = '入力パス: {input_path} 結合用音声ファイルパス: {audio_path} fps値: {fps} 出力先パスは指定しないでください', font = ['Meiryo',8], pad = ((0,0),(10,0)))],
                          [sg.Checkbox(text = '生成されたテンポラリフォルダを残す', default = tmp_folder_chk, font = ['Meiryo',8], pad = ((10,0),(7,0)), key = '-tmp_checkbox-')],
                          [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((0,0),(10,0)), key = '-setting_ok_button-'),
                           sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((20,0),(10,0)), key = '-setting_cancel_button-')]]

        return sg.Window(window_title + ' - 詳細設定', setting_layout, icon = icon_path, size = (800,180), font = ['Meiryo',12], element_justification = 'c', modal = True)
