# -*- coding: utf-8 -*-
#!/usr/bin/python

import urllib, sys, os, codecs
from re import compile as _Re
from lxml import html
from os import listdir, makedirs
from os.path import isfile, join, exists

#http://stackoverflow.com/questions/3797746/how-to-do-a-python-split-on-languages-like-chinese-that-dont-use-whitespace
_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split

img_directory_path = "./stroke_img"

def split_unicode_chrs(text):
  # added check for kanji characters only
  return [chr for chr in _unicode_chr_splitter(text) if chr and ord(chr) >= 0x4E00 and ord(chr) <= 0x9FBF]

def main():

  kanji_input = codecs.open("kanji_list", encoding="utf-8", mode="a+")
  kanji_input.seek(0)

  kanji_list = []

  for line in kanji_input.readlines():
    kanji_list += line.strip()

  kanji_add = []

  if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
      for kan_input in sys.argv[i].decode("utf-8"):
        kanji_add += split_unicode_chrs(kan_input)

  if not exists(img_directory_path):
    makedirs(img_directory_path)

  onlyfiles = [f.rstrip(".png").decode("utf-8") for f in listdir(img_directory_path) if isfile(join(img_directory_path,f))]

  updated = []

  for kanji in kanji_list:
    if kanji not in onlyfiles:
      updated.append(kanji)
      get_stroke_img(kanji)

  if updated:
    print "The following {} kanji were added or updated:".format(len(updated))
    for kanji in updated:
      print kanji,
    print
  else:
    print "All kanji in the main list up to date"

  added = []

  for kanji in kanji_add:
    if kanji not in onlyfiles and kanji not in kanji_list:
      get_stroke_img(kanji)
      added.append(kanji)
    if kanji not in kanji_list:
      kanji_input.write(kanji,)

  if added:
    print "The following {} kanji were added:".format(len(added))
    for kanji in added:
      print kanji,
  else:
    print "No new kanji added"

  kanji_input.close()
  return

def get_stroke_img(kanji):
  url = "http://jisho.org/kanji/details/" + kanji.encode('utf-8')
  page = html.fromstring(urllib.urlopen(url).read())
  xpath = page.xpath('//div[@class="stroke_diagram"]/img/@src')
  if xpath:
    print "Getting {}...".format(kanji.encode("utf-8"))
    image_url = xpath[0]
    urllib.urlretrieve("http://jisho.org" + image_url, img_directory_path + "/" + kanji + ".png")

if __name__ == "__main__":
  main()
