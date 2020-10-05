from typing import Any
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
import os
from datetime import datetime
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
from PIL import ImageFont
import random
import stat
import tempfile
from itertools import chain
import re

app = Flask(__name__,static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = 's3cr3t'
app.debug = True

FILE_SYSTEM_ROOT = "/Users/enrique/code/work/python/chess/web/tarea1/position"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getPosition/<fenfile>', methods=['GET'])
def results(fenfile):
    title = 'Result'
    data = []
    newfen = get_file_content(fenfile).rstrip()
    data.append(newfen)
    fontFile = convertToFontFile(newfen)
    data.append(fontFile)
    renderer = DrawChessPosition()
    board = renderer.draw(newfen)
    board.show()
    img = chess_position_using_font(newfen, "fonts/chess_merida_unicode.ttf", 18)
    img2 = img.convert('RGB')
    nal = random.randint(0, 1022)
    name= 'boardpos_'+str(nal)+'_'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
    img3 = img2.save("static/img/"+name)
    data.append(name)
    return render_template('position.html', title=title, data = data )

@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    jsdata = request.form['fen_data']
    fen_id = create_position(jsdata)
    params = { 'fen' : fen_id }
    return jsonify(params)

@app.route('/getFenPosition/<uri>', methods = ['GET'])
def get_fen_data(uri):
    data = get_file_content(uri)
    params = { 'data' : data }
    return jsonify(params)

@app.route('/browser')
def browse():
    itemList = os.listdir(FILE_SYSTEM_ROOT)
    return render_template('browse.html', itemList=itemList)

@app.route('/browser/<path:urlFilePath>')
def browser(urlFilePath):
    nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, urlFilePath)
    if os.path.isdir(nestedFilePath):
        itemList = os.listdir(nestedFilePath)
        fileProperties = {"filepath": nestedFilePath}
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return render_template('browse.html', urlFilePath=urlFilePath, itemList=itemList)
    if os.path.isfile(nestedFilePath):
        fileProperties = {"filepath": nestedFilePath}
        sbuf = os.fstat(os.open(nestedFilePath, os.O_RDONLY)) #Opening the file and getting metadata
        fileProperties['type'] = stat.S_IFMT(sbuf.st_mode)
        fileProperties['mode'] = stat.S_IMODE(sbuf.st_mode)
        fileProperties['mtime'] = sbuf.st_mtime
        fileProperties['size'] = sbuf.st_size
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return render_template('file.html', currentFile=nestedFilePath, fileProperties=fileProperties)
    return 'something bad happened'

def create_position(text):
    unique_id = 'position_'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.txt'
    with open('position/'+unique_id, 'a') as file:
        file.write(text[1:-1]+"\n")
    return unique_id

def get_file_content(fenf):
    with open('position/'+fenf, 'r') as file:
        nfile = file.read()
        file.close()
        return nfile

def convertToFontFile(myfen):
    colors = '*+*+*+*++*+*+*+**+*+*+*++*+*+*+**+*+*+*++*+*+*+**+*+*+*++*+*+*+*'
    fontFile = []
    even_cell_start = "*"
    fp = FenParser(myfen)
    ary = fp.parse()
    i = 0
    j = 0
    fontFile.append('!""""""""#')
    for row in ary:
        for n, i in enumerate(row):
            if i == ' ':
                row[n] = colors[j]
            if i == 'p':
                if colors[j] == "*":
                    row[n] = 'o'
                else:
                    row[n] = 'O'
            if i == 'P':
                if colors[j] == "*":
                    row[n] = 'p'
            if i == 'r':
                if colors[j] == "*":
                    row[n] = 't'
                else:
                    row[n] = 'T'
            if i == 'R':
                if colors[j] == "*":
                    row[n] = 'r'
            if i == 'n':
                if colors[j] == "*":
                    row[n] = 'm'
                else:
                    row[n] = 'M'
            if i == 'N':
                if colors[j] == "*":
                    row[n] = 'n'
            if i == 'b':
                if colors[j] == "*":
                    row[n] = 'v'
                else:
                    row[n] = 'V'
            if i == 'B':
                if colors[j] == "*":
                    row[n] = 'b'
            if i == 'q':
                if colors[j] == "*":
                    row[n] = 'w'
                else:
                    row[n] = 'W'
            if i == 'Q':
                if colors[j] == "*":
                    row[n] = 'q'
            if i == 'k':
                if colors[j] == "*":
                    row[n] = 'l'
                else:
                    row[n] = 'L'
            if i == 'K':
                if colors[j] == "*":
                    row[n] = 'k'
            j = j + 1
        fontFile.append("$" + row[0] + row[1] + row[2] + row[3] + row[4] + row[5] + row[6] + row[7] + '%')

    fontFile.append('/(((((((()#')
    return fontFile

class BadChessboard(ValueError):
    pass

def expand_blanks(feno):
    '''Expand the digits in an FEN string into spaces

    >>> expand_blanks("rk4q3")
    'rk    q   '
    '''

    def expand(match):
        return ' ' * int(match.group(0))

    return re.compile(r'\d').sub(expand, feno)


def check_valid(expanded_fen):
    '''Asserts an expanded FEN string is valid'''
    match = re.compile(r'([KQBNRPkqbnrp ]{8}/){8}$').match
    if not match(expanded_fen + '/'):
        raise BadChessboard()


def expand_fen(fenn):
    '''Preprocesses a fen string into an internal format.

    Each square on the chessboard is represented by a single
    character in the output string. The rank separator characters
    are removed. Invalid inputs raise a BadChessboard error.
    '''
    expanded = expand_blanks(fenn)
    check_valid(expanded)
    return expanded.replace('/', '')


def draw_board(n=8, sq_size=(20, 20)):
    '''Return an image of a chessboard.

    The board has n x n squares each of the supplied size.'''
    from itertools import cycle
    def square(i, j):
        return i * sq_size[0], j * sq_size[1]

    opaque_grey_background = 192, 255
    board = Image.new('LA', square(n, n), opaque_grey_background)
    draw_square = ImageDraw.Draw(board).rectangle
    whites = ((square(i, j), square(i + 1, j + 1))
              for i_start, j in zip(cycle((0, 1)), range(n))
              for i in range(i_start, n, 2))
    for white_square in whites:
        draw_square(white_square, fill='white')
    return board


class DrawChessPosition(object):
    '''Chess position renderer.

    Create an instance of this class, then call
    '''

    def __init__(self):
        '''Initialise, preloading pieces and creating a blank board.'''
        self.n = 8
        self.create_pieces()
        self.create_blank_board()

    def create_pieces(self):
        '''Load the chess pieces from disk.

        Also extracts and caches the alpha masks for these pieces.
        '''
        whites = 'KQBNRP'
        piece_images = dict(
            zip(whites, (Image.open('pieces/w%s.png' % p) for p in whites)))
        blacks = 'kqbnrp'
        piece_images.update(dict(
            zip(blacks, (Image.open('pieces/%s.png' % p) for p in blacks))))
        piece_sizes = set(piece.size for piece in piece_images.values())
        # Sanity check: the pieces should all be the same size
        assert len(piece_sizes) == 1
        self.piece_w, self.piece_h = piece_sizes.pop()
        self.piece_images = piece_images
        self.piece_masks = dict((pc, img.split()[3]) for pc, img in
                                self.piece_images.items())

    def create_blank_board(self):
        '''Pre-render a blank board.'''
        self.board = draw_board(sq_size=(self.piece_w, self.piece_h))

    def point(self, i, j):
        '''Return the top left of the square at (i, j).'''
        w, h = self.piece_w, self.piece_h
        return i * h, j * w

    def square(self, i, j):
        '''Return the square at (i, j).'''
        t, l = self.point(i, j)
        b, r = self.point(i + 1, j + 1)
        return t, l, b, r

    def draw(self, fen_):
        '''Return an image depicting the input position.

        fen - the first record of a FEN chess position.
        Clients are responsible for resizing this image and saving it,
        if required.
        '''
        board = self.board.copy()
        pieces = expand_fen(fen_)
        images, masks, n = self.piece_images, self.piece_masks, self.n
        pts = (self.point(i, j) for j in range(n) for i in range(n))

        def not_blank(pt_pc):
            return pt_pc[1] != ' '

        for pt, piece in filter(not_blank, zip(pts, pieces)):
            board.paste(images[piece], pt, masks[piece])
        return board


unichr_pieces = dict(
    zip("KQRBNPkqrbnp",
        (chr(uc) for uc in range(0x2654, 0x2660))))


def chess_position_using_font(nfen, font_file, sq_size):
    '''Return a chess position image.

    font_file - the name of a font file
    sq_size - the size of each square on the chess board
    '''
    font = ImageFont.truetype(font_file, sq_size)
    pieces = expand_fen(nfen)
    board = draw_board(sq_size=(sq_size, sq_size))
    put_piece = ImageDraw.Draw(board).text

    def point(i, j):
        return i * sq_size, j * sq_size

    def not_blank(pt_pce):
        return pt_pce[1] != ' '

    pts = (point(i, j) for j in range(8) for i in range(8))
    for pt, piece in filter(not_blank, zip(pts, pieces)):
        put_piece(pt, unichr_pieces[piece], fill='black', font=font)
    return board

class FenParser():
  def __init__(self, fen_str):
    self.fen_str = fen_str

  def parse(self):
    ranks = self.fen_str.split(" ")[0].split("/")
    pieces_on_all_ranks = [self.parse_rank(rank) for rank in ranks]
    return pieces_on_all_ranks

  def parse_rank(self, rank):
    rank_re = re.compile("(\d|[kqbnrpKQBNRP])")
    piece_tokens = rank_re.findall(rank)
    pieces = self.flatten(map(self.expand_or_noop, piece_tokens))
    return pieces

  def flatten(self, lst):
    return list(chain(*lst))

  def expand_or_noop(self, piece_str):
    piece_re = re.compile("([kqbnrpKQBNRP])")
    retval = ""
    if piece_re.match(piece_str):
      retval = piece_str
    else:
      retval = self.expand(piece_str)
    return retval

  def expand(self, num_str):
    return int(num_str)*" "

if __name__ == '__main__':
    app.run(port=8080, debug=True)
