#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import io
import re
import codecs

# カレントディレクトリのディレクトリ名
DIRECTORY_NAME = os.path.split(os.getcwd())[1]

# 
def write_base_lyx_code(wf):
    wf.write("""#LyX 2.2 created this file. For more info see http://www.lyx.org/
\\lyxformat 508
\\begin_document
\\begin_header
\\save_transient_properties true
\\origin unavailable
\\textclass jsbook
\\begin_preamble
\\usepackage{pxrubrica}
\\usepackage[dvipdfmx, bookmarkstype=toc, colorlinks=true, urlcolor=black, linkcolor=blue, citecolor=black, linktocpage=true, bookmarks=true]{hyperref}
\\usepackage{pxjahyper}
\\end_preamble
\\use_default_options true
\\maintain_unincluded_children false
\\language japanese
\\language_package default
\\inputencoding utf8-platex
\\fontencoding global
\\font_roman "default" "default"
\\font_sans "default" "default"
\\font_typewriter "default" "default"
\\font_math "auto" "auto"
\\font_default_family default
\\use_non_tex_fonts false
\\font_sc false
\\font_osf false
\\font_sf_scale 100 100
\\font_tt_scale 100 100
\\graphics default
\\default_output_format default
\\output_sync 0
\\bibtex_command default
\\index_command default
\\paperfontsize default
\\spacing single
\\use_hyperref false
\\pdf_bookmarks true
\\pdf_bookmarksnumbered true
\\pdf_bookmarksopen false
\\pdf_bookmarksopenlevel 1
\\pdf_breaklinks false
\\pdf_pdfborder false
\\pdf_colorlinks false
\\pdf_backref false
\\pdf_pdfusetitle true
\\papersize default
\\use_geometry false
\\use_package amsmath 1
\\use_package amssymb 1
\\use_package cancel 1
\\use_package esint 1
\\use_package mathdots 1
\\use_package mathtools 1
\\use_package mhchem 1
\\use_package stackrel 1
\\use_package stmaryrd 1
\\use_package undertilde 1
\\cite_engine basic
\\cite_engine_type default
\\biblio_style plain
\\use_bibtopic false
\\use_indices false
\\paperorientation portrait
\\suppress_date false
\\justification true
\\use_refstyle 1
\\index Index
\\shortcut idx
\\color #008000
\\end_index
\\secnumdepth -2
\\tocdepth 2
\\paragraph_separation indent
\\paragraph_indentation default
\\quotes_language english
\\papercolumns 1
\\papersides 1
\\paperpagestyle default
\\tracking_changes false
\\output_changes false
\\html_math_output 0
\\html_css_as_file 0
\\html_be_strict false
\\end_header

\\begin_body\n""")
    wf.write("\\begin_layout Title\n" + DIRECTORY_NAME + "\n\\end_layout\n")
    wf.write("""\\begin_layout Standard
\\begin_inset CommandInset toc
LatexCommand tableofcontents
\\end_inset
\\end_layout\n\n""")
    write_body(wf)
    wf.write("""\\end_body
\\end_document""")

# 本文の作成
def write_body(wf):
    count = 0
    while True:
        count += 1
        path = DIRECTORY_NAME + "-" + str(count) + ".txt";
        if not os.path.exists(path):
            break
        txt2lyx(wf, path)

# 水平線の作成
def write_horizon(wf):
    wf.write("""\\begin_layout Standard
\\begin_inset CommandInset line
LatexCommand rule
offset "0.5ex"
width "100col%"
height "1pt"
\\end_inset
\\end_layout\n""")

# ルビの作成
def write_ruby(wf):
    wf.write("""\\begin_inset ERT
status open
\\begin_layout Plain Layout
\\backslash\n""")
    wf.write("ruby[g]{" + body + "}{" + ruby + "}\n")
    wf.write("""\\end_layout
\\end_inset""")

# 
def write_line(wf, line):
    wf.write("%s\n"%line)

# 
def write_text(wf, line, bl_count):
    # 空行処理
    if (not line) or re.match(r"^[\s\u3000]+$", line):
        bl_count += 1
        return bl_count
    if bl_count > 0:
        wf.write("\\begin_layout Standard\n")
        for i in range(0, bl_count):
            wf.write("\\begin_inset VSpace defskip\n")
            wf.write("\\end_inset\n")
        wf.write("\\end_layout\n")
        bl_count = 0
    
    # 段落の作成
    if line.startswith('　'):
        #-- 段落（行下げあり）
        wf.write("\\begin_layout Standard\n")
        write_line(wf, line[1:])
        wf.write("\\end_layout\n")
    else:
        #-- 段落（行下げなし）
        wf.write("\\begin_layout Standard\n\\noindent\n")
        write_line(wf, line)
        wf.write("\\end_layout\n")
    
    wf.write("\n")
    return bl_count

# 
def txt2lyx(wf, path):
    line_num = 0
    with codecs.open(path, 'r', encoding='utf-8') as f:
        lines = re.split('\r\n|\r|\n', f.read())
        preface_end_line = 0
        for i,line in enumerate(lines):
            if line == "********************************************":
                preface_end_line = i
                break
        
        #Chapter Title
        if preface_end_line > 0:
            line_num = preface_end_line + 1
        wf.write("\\begin_layout Chapter\n")
        wf.write("%s\n"%lines[line_num])
        wf.write("\\end_layout\n")
        wf.write("\n")
        
        # まえがき
        bl_count = 0
        for line_num in range(0, preface_end_line):
            line = lines[line_num]
            bl_count = write_text(wf, line, bl_count)
        if preface_end_line > 0:
            write_horizon(wf)
        
        # 本文および後書き
        bl_count = 0
        is_start = True
        for line in lines[preface_end_line + 2:]:
            # あとがき
            if line == "************************************************":
                bl_count = 0
                write_horizon(wf)
                continue
            
            # 本文
            bl_count = write_text(wf, line, bl_count)
            if is_start:
                if bl_count > 0:
                    bl_count = 0
                else:
                    is_start = False



# main
with io.open(DIRECTORY_NAME + '.lyx', mode='w', encoding='utf-8', newline='\n') as f:
    write_base_lyx_code(f)
