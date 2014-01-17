import ConfigParser 
from datetime import datetime, timedelta
from scraper import Scraper
yesterday = datetime.now() - timedelta(hours=12)

config = ConfigParser.RawConfigParser()
config.read('../setup.cfg')

def print_board(board):
    for row in board:
        for item in row:
            print('%s' % item),
        print ""

def date_string(date):
    return datetime.strftime(date, '%B %d %Y')

def string_date(string_date):
    return datetime.strptime(string_date, '%B %d %Y')

def adjust_gmt(date):
    GMT_string = config.get('drawingboard', 'GMT') 
    return datetime.now() - timedelta(hours=abs(int(GMT_string)))
    

class TomorrowFactory():

    def __init__(self, today):
        self.today = today

    def tomorrow(self):
        tomorrow_date = self.today + timedelta(days=1)
        self.today = tomorrow_date
        return tomorrow_date

    def generate_key(self):
        return date_string(self.tomorrow())


class DrawingBoard():

    def __init__(self):
        self.board = []
        self.build_canvas()

    def build_canvas(self):
        NUM_COLUMNS = 52
        NUM_ROWS = 7
        for row in range(0, NUM_ROWS):
            row = []
            for column in range(0, NUM_COLUMNS):
                row.append("0 ")
            self.board.append(row)
        self.board = []
        painting_file_name = config.get('drawingboard', 'painting_file')
        with open(painting_file_name) as canvas:
            for line in canvas:
                row = []
                items = line.split()
                if items != []:
                    for item in items:
                        if item == '0':
                            row.append(None)
                        else:
                            row.append('x')
                    self.board.append(row)

    def create_date_map(self, start_index, start_date):
        if self.is_too_late(start_index):
            raise DrawingBoard.TooLateToStart("It's too late to start building your board this week, let's start next week.")
        date_map = {}
        tomorrow = TomorrowFactory(start_date)
        length = len(self.board)
        width = len(self.board[0])
        for i in range(0, width):
            start = 0
            if i == 0:
                start = start_index
            for k in range(start, length):
                date_map.update({tomorrow.generate_key(): (k, i, self.board[k][i])})
        return date_map

    def is_too_late(self, current_index):
        length = len(self.board)
        for i in range(0, length):
            if self.board[i][0] is not None and i < current_index:
                return True
        return False

    def coordinates_to_date(self, row, column):
        for key in date_map:
            item = date_map.get(key)
            if item[0] == row and item[1] == column:
                return string_date(key) 
            return None

    class TooLateToStart(Exception):
        pass

class Oracle():            
    def_start_date = datetime.now()

    def __init__(self, start_index, start_date):
        self.drawing_board = DrawingBoard()
        self.start_index = start_index 
        self.start_date = start_date 

    def is_parteh_time(self, date):
        try:
            date_map = self.drawing_board.create_date_map(self.start_index, self.def_start_date)
            date_value = date_map.get(date_string(date))
            if not start_date:
                config.set('drawingboard', 'start_date', start_date)
                config.set('drawingboard', 'start_index', start_index)
        except DrawingBoard.TooLateToStart, e:
            date_value = None
        return date_value is not None


scraper = Scraper()
start_date = string_date(config.get('drawingboard', 'start_date'))
# adjust GMT since GitHub commit history is basing itself on GMT 0
start_date = adjust_gmt(start_date)
oracle = Oracle(start_index=scraper.get_today_y(), start_date=start_date)
oracle.is_parteh_time(datetime.now())
