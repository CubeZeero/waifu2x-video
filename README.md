<p align="center">
  <img width="250px" src="icon.png">
</p>


# waifu2x-video

waifu2x-caffeとffmpegを用いて動画のアップコンバートを行うツールソフト

Video-only upconverter using waifu2x-caffe and ffmpeg

# 概要

waifu2x-videoはwaifu2x-caffe([https://github.com/lltcggie/waifu2x-caffe](https://github.com/lltcggie/waifu2x-caffe))とffmpegを用いて動画のアップコンバートを行うツールソフトです。

ffmpegで連番画像へ解体、連番画像をwaifu2x-caffeでアップコンバートしffmpegで動画へ変換するフローを自動で行います。

# 使用方法

ffmpegをダウンロードし、パスを通してコマンドプロンプトから利用できるようにします。

waifu2x-caffeをダウンロードし、詳細設定から`waifu2x-caffe-cui.exe`を指定してください。

waifu2x-caffeに関する仕様はwaifu2x-caffeの[Readme](https://github.com/lltcggie/waifu2x-caffe/blob/master/README.md)を御覧ください。

## 入力パス、出力パス

それぞれ変換する動画、変換後に出力する動画ファイルを指定してください

## 出力プリセット

ffmpegの出力プリセットを指定できます。

品質固定モードの場合出来上がる品質は同じですが、速度が速くなるほどファイルサイズは大きくなります。

時間がある限り速度が遅いプリセットを使うと、より小さいファイルにすることができます。

ビットレート一定の場合は同じファイルサイズでも、時間をかけた分品質が向上します。

## crf

crf (品質固定モード) を指定できます。

小さい値になればなるほど品質は向上しますが、その分ファイルサイズは増幅します。

## crfを使用する

チェックを入れるとcrfを使用できます。

チェックを外した場合、指定したビットレート一定でエンコードを行います。

## 音声もコピー

チェックを入れると音声もコピーして結合します。

## コーデック

コーデックを選択できます。

`./w2xv_data/lists/ffmpeg_codecs.txt`を編集することで、項目を追加することもできます。

## 画像フォーマット

連番解体時、waifu2x-caffeでの拡大時で使用される画像フォーマットを選択できます。

`./w2xv_data/lists/ffmpeg_formats.txt`を編集することで、項目を追加することもできます。

## ビットレート

動画エンコード時のビットレートを指定できます。

`crfを使用する`のチェックを外した場合のみ、この設定が使用されます。

## パス

1パス、2パスエンコードを指定できます。

2パスの場合、1パス目で動画を解析し、2パス目で解析結果を基に最適な動画を作成します。

なお、品質固定モードの場合は使用されません。
