# -*- coding: utf-8 -*-

from lxml import etree
import zipfile
from pydoc import deque

nsprefixes = {
    # Text Content
    'mv':'urn:schemas-microsoft-com:mac:vml',
    'mo':'http://schemas.microsoft.com/office/mac/office/2008/main',
    've':'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'o':'urn:schemas-microsoft-com:office:office',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'v':'urn:schemas-microsoft-com:vml',
    'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w10':'urn:schemas-microsoft-com:office:word',
    'wne':'http://schemas.microsoft.com/office/word/2006/wordml',
    # Drawing
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture',
    # Properties (core and extended)
    'cp':"http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    'dc':"http://purl.org/dc/elements/1.1/",
    'dcterms':"http://purl.org/dc/terms/",
    'dcmitype':"http://purl.org/dc/dcmitype/",
    'xsi':"http://www.w3.org/2001/XMLSchema-instance",
    'ep':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties',
    # Content Types (we're just making up our own namespaces here to save time)
    'ct':'http://schemas.openxmlformats.org/package/2006/content-types',
    # Package Relationships (we're just making up our own namespaces here to save time)
    'pr':'http://schemas.openxmlformats.org/package/2006/relationships'
    }


def markdownify(file,salt):
    return convert_to_markdown(opendocx(file),salt)

def opendocx(file):
    '''Open a docx file, return a document XML tree'''
    f = open("test.tmp",'w')
    f.write("la")
    f.close()
    mydoc = zipfile.ZipFile(file)
    xmlcontent = mydoc.read('word/document.xml')
    document = etree.fromstring(xmlcontent)
    media = [];
    for item in mydoc.namelist():
        if "word/media" in item:
            media.append(item)
    doc = {
           "media":deque(sorted(media)),
           "doc":document,
           "file":file
        }
    return doc


def convert_to_markdown(document,name):
    blocks = "";
    for element in document['doc'].getchildren()[0].getchildren():
        # a new paragraph
        if element.tag == "{%s}p" % nsprefixes['w']:
            blocks+=(parse_paragraph(element,document,name))+"\n\n"
        
        # a table
        if element.tag == "{%s}tbl" % nsprefixes['w']:
            blocks+=parse_table(element,document,name)+"\n\n"
            
            
    return blocks

def parse_table(table,document,name):
    table_string = ""
    table_data = []
    col_count=0
    
    for element in table.getchildren():
        #specification of grid size
        if element.tag == "{%s}tblGrid" % nsprefixes['w']:
            col_count += len( element.getchildren())
        #a new row
        if element.tag == "{%s}tr" % nsprefixes['w']:
            row_data = []
            for cols in element.getchildren():
                if cols.tag =="{%s}tc" % nsprefixes['w']:
                    cell_data= []
                    for el in cols.getchildren():
                        #the paragraphs inside the cell
                        if el.tag =="{%s}p" %nsprefixes['w']:
                            cell_data.append(parse_paragraph(el,document,name))
                    cell = {
                        "span":len(cell_data),#for merged cells
                        "data":"/".join(cell_data)
                        }
                    row_data.append(cell)
            table_data.append(row_data)
    biggest_col_widths = [0]*col_count
    for i in xrange(len(table_data)):
        #iterate over all the rows, counting the width of each cell
        #find the widest nth cell for all rows
        col_index = 0
        while col_index<col_count:
            #can't use a for loop because some rows have fewer columns(merged)
            
            #this cell is merged from 2+ cells
            if table_data[i][col_index]['span']>1:
                col_index+=table_data[i][col_index]['span']
                continue;
            
            #if this cell is wider than all the other cells in its column
            if len(table_data[i][col_index]['data'])>biggest_col_widths[col_index]:
                biggest_col_widths[col_index] = len(table_data[i][col_index]['data'])
            
            col_index+=1
            
    for i in xrange(len(table_data)):
        col_index = 0
        row_string_data = []
        while col_index<col_count:
            cell_span = table_data[i][col_index]['span']
            #generalized so it will find the widths of a cell regardless of how many columns it spans
            width = sum(biggest_col_widths[col_index:col_index+cell_span])+(cell_span-1)
            row_string_data.append(table_data[i][col_index]['data'])
            col_index+=cell_span            
        table_string+="|".join(row_string_data)+"\n"
        if i==0:
            empty_row = []
            for j in xrange(col_count):
                empty_row.append("-"*biggest_col_widths[j])
            table_string+="|".join(empty_row)+"\n"
    return table_string


def parse_math_block(element):
    block_text = ""
    parse_matrix= {
        "limLow":parse_math_limit,
        "d":parse_math_parenthesis,
        "nary":parse_math_nary,
        "func":parse_math_function,
        "rad":parse_math_rad,
        "sSub":parse_math_subscript,
        "sSup":parse_math_supscript,
        "groupChr":parse_math_group,
        "m":parse_math_matrix,
        "f":parse_math_fraction,
        "box":parse_math_block,
        "sSubSup":parse_math_subsupscript,
        "e":parse_math_block
        }
    for child in element.getchildren():
        tag_type = child.tag.split("}")[1]
        
        #it's a text block
        if child.tag == "{%s}r" % nsprefixes['m']:
            style = ""
            text = ""
            for el in child.getchildren():
                #font style
                if el.tag == "{%s}rPr" % nsprefixes['m']:
                    for s in el.getchildren():
                        if s.tag == "{%s}sty" %nsprefixes['m']:
                            if(s.values()[0]=='p'):
                                style = "rm"
                            if(s.values()[0]=='bi'):
                                style = "bf"
                #actual text of the block
                if el.tag == "{%s}t" % nsprefixes['m']:
                    text = el.text
            if len(style)>0:
                block_text+="{\%s %s}"%(style,text)
            else:
                block_text+=text
        
        if tag_type in parse_matrix:
            block_text+=parse_matrix[tag_type](child)   
    return "{"+block_text+"}"

def parse_math_matrix(element):
    block_text = ""
    rows = []
    for child in element.getchildren():
        if child.tag == "{%s}mr" % nsprefixes['m']:
            row = []
            for s in child.getchildren():
                row.append(parse_math_block(s))
            rows.append(" & ".join(row))
    row_str = "\\\\".join(rows)
    block_text = "\\begin{array}{cc}%s \\\\\\end{array}"%row_str
    return block_text

def parse_math_function(element):
    block_text = ""
    function_name = ""
    function_arg = ""
    for child in element.getchildren():
        if child.tag == "{%s}fName" % nsprefixes['m']:
            function_name = parse_math_block(child)
        if child.tag == "{%s}e" % nsprefixes['m']:
            function_arg = parse_math_block(child)
    block_text = "%s\,%s" % (function_name,function_arg)
    return block_text

def parse_math_subscript(element):
    block_text = ""
    text = ""
    sub = ""
    for child in element.getchildren():
        if child.tag == "{%s}e" % nsprefixes['m']:
            text = parse_math_block(child)
        if child.tag == "{%s}sub" % nsprefixes['m']:
            sub = parse_math_block(child)
    block_text = "%s_{%s}" % (text,sub)
    return block_text

def parse_math_group(element):
    block_text = ""
    mode = ""
    text = ""
    for child in element.getchildren():
        if child.tag == "{%s}groupChrPr" % nsprefixes['m']:
            for el in child.iter():
                if el.tag == "{%s}chr" % nsprefixes['m']:
                    val = el.values()[0]
                    if val == u'←' or val == u'⇐':
                        mode = "xleftarrow"
                    if val == u'→' or val == u'⇒':
                        mode = "xrightarrow"
                        
        if child.tag == "{%s}e" % nsprefixes['m']:
            text = parse_math_block(child)
    block_text = "\%s %s"%(mode,text)
    return block_text

def parse_math_subsupscript(element):
    block_text = ""
    return block_text

def parse_math_supscript(element):
    block_text = ""
    text = ""
    sup = ""
    for child in element.getchildren():
        if child.tag == "{%s}e" % nsprefixes['m']:
            text = parse_math_block(child)
        if child.tag == "{%s}sup" % nsprefixes['m']:
            sup = parse_math_block(child)
    block_text = "%s^{%s}" % (text,sup)
    return block_text

def parse_math_parenthesis(element):
    return "\left("+parse_math_block(element)+"\\right)"

def parse_math_limit(element):
    block_text = ""
    limit = ""
    for child in element.getchildren():
        if child.tag == "{%s}lim" % nsprefixes['m']:
            limit = parse_math_block(child)
    block_text = "\lim_%s" % limit
    return block_text

def parse_math_fraction(element):
    block_text = ""
    num = ""
    denom = ""
    for child in element.getchildren():
        if child.tag == "{%s}num" % nsprefixes['m']:
            num = parse_math_block(child)
        if child.tag == "{%s}den" % nsprefixes['m']:
            denom = parse_math_block(child)
    block_text = "\\frac{%s}{%s}" % (num,denom)
    return block_text

def parse_math_nary(element):
    block_text = ""
    type = "int"
    lower = ""
    upper = ""
    main = ""
    for child in element.getchildren():
        if child.tag == "{%s}naryPr" % nsprefixes['m']:
            for s in child.getchildren():
                if s.tag == "{%s}chr" % nsprefixes['m']:
                    char = s.values()[0]
                    if  char == u'∏':
                        type = "prod"
                    if char == u'∬':
                        type = "iint"
                    if char == u'∭':
                        type = 'iiint'
                    if char == u'∑':
                        type = 'sum'
        
        #lower bound
        if child.tag == "{%s}sub" % nsprefixes['m']:
            lower = parse_math_block(child)
            
        #upper bound
        if child.tag == "{%s}sup" % nsprefixes['m']:
            upper = parse_math_block(child)
            
        #main text
        if child.tag == "{%s}e" % nsprefixes['m']:
            main = parse_math_block(child)
    
    block_text = "\%s_%s^%s%s" % (type,lower,upper,main)
    return block_text

def parse_math_rad(element):
    block_text = ""
    deg = ""
    main = ""
    for child in element.getchildren():
        if child.tag == "{%s}deg" % nsprefixes['m']:
            deg = parse_math_block(child)
        if child.tag == "{%s}e" % nsprefixes['m']:
            main = parse_math_block(child)
    block_text = "\sqrt[%s]{%s}" % (deg,main)
    return block_text


def parse_paragraph(paragraph,document,name):
    #print "new paragraph"
    paragraph_style = ""
    plaintext = ""
    bold = False
    italics = False
    underline = False;
    avg_size = 0
    block_count = 0
    for element in paragraph.iter():
       
        #style for the entire paragraph
        if element.tag == "{%s}pPr" % nsprefixes['w']:
    
            for child in element.getchildren():
                #a heading style is found
                if child.tag =="{%s}pStyle" % nsprefixes['w']:
                    if len(child.values())>0:
                        style = child.values()[0]
                        if "Heading" in style:
                            heading_level = int(style[-1])
                            paragraph_style=("#"*heading_level)
                            
                #list style is found
                if child.tag =="{%s}numPr"%nsprefixes['w']:
                    type="1."
                    level=0
                    for el in child.getchildren():
                        if el.tag=="{%s}ilvl"%nsprefixes['w']:
                            level = int(el.values()[0])
                        if el.tag=="{%s}numId"%nsprefixes['w']:
                            if el.values()[0] == '1':
                                type = "*"
                    paragraph_style=("    "*level)+type+" "
                    
        # a text block
        if element.tag =="{%s}r"%nsprefixes['w']:
            cur_bold = False
            cur_italics = False
            block_count +=1
            text = ""
            for child in element.getchildren():
                #the style for the block
                if child.tag == "{%s}rPr" % nsprefixes['w']:
                    for el in child.getchildren():
                        if el.tag=="{%s}sz":
                            avg_size+= int(el.values()[0])/2
                        if el.tag=="{%s}i" % nsprefixes['w']:
                            cur_italics=True
                        if el.tag=="{%s}b" % nsprefixes['w']:
                            cur_bold=True
                        if el.tag=="{%s}u" %nsprefixes['w']:
                            cur_italics=True
                            
                #the actual text
                if child.tag =="{%s}t" % nsprefixes['w']:
                    if child.text:
                        text = child.text
                
                #HOLY SHIT A PICTURE
                #or a chart
                if child.tag =="{%s}drawing" % nsprefixes['w']:
                    for el in child.iter():
                        if el.tag == "{%s}pic"%nsprefixes['pic']:
                            #i'm leaving this parser cos i'm a picture
                            text=parse_picture(child,document,name)
                        
            #if the boldness/italicness changed
            if bold ^ cur_bold:
                text = "**" + text
            if italics ^ cur_italics:
                text = "*"+text
            
            bold = cur_bold
            italics = cur_italics
            plaintext+=text
            
        #it's a math equation
        if element.tag=="{%s}oMath"%nsprefixes['m']:
            math = parse_math_block(element)
            plaintext+="$$"+math+"$$"
            
    if bold and plaintext[-1]!="*":
        plaintext+="**"
    if italics and plaintext[-1]!="*":
        plaintext+="*"
    if block_count >0:
        avg_size /= block_count
        if 12<avg_size<14:
            if len(paragraph_style)==0:
                paragraph_style = "###"
        if 14<avg_size<16:
            if len(paragraph_style)==0:
                paragraph_style = "##"
        if 16<avg_size:
            if len(paragraph_style)==0:
                paragraph_style = "#"
        
                
                
    return paragraph_style+plaintext

def parse_picture(pic,document,name):
    picture_link=""
    current_picture = document['media'].popleft();
    #look to see if the picture originally came from a remote url
    for el in pic.iter():
        if el.tag == "{%s}docPr" % nsprefixes['wp']:
            if el.values()[2][0:4] == "http":
                #great we already have our picture
                url =  el.values()[2]
                picture_link = '![alt](%s "")' % url
                return picture_link
            
    #if we're here it means the pic isn't already online
    #TODO: figure out how/where to store the image
    """
    file = document['file']
    mydoc = zipfile.ZipFile(file)
    mydoc.extract(current_picture, "temp/"+name)
    #print current_picture
    img = open("temp/"+name+"/"+current_picture,"rb")
    img_data = img.read()
    base64_data = base64.b64encode(img_data)
    print upload_image(img_data);
    print base64_data
    """
   # print current_picture
    return "#a picture link#"

#print markdownify("test.docx","name")

