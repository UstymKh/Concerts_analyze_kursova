import pygame, pyautogui, calendar, datetime, glob
from search_for_result.main import find_best_results
from pygame import mixer
from download_from_youtube import download
from request_for_video import make_url
from lastfm_ask import get_top_track

mixer.init()
# creating display
pygame.init()
WIDTH, HEIGHT = pyautogui.size()
WIDTH, HEIGHT = round(WIDTH * 0.8), round(HEIGHT * 0.8)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mustrip")
background = pygame.image.load("images/Mustrip.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
second_backround = pygame.image.load("images/ask_user_page.jpg")
second_backround = pygame.transform.scale(second_backround, (WIDTH, HEIGHT))
third_backround = pygame.image.load("images/calendar_background.jpg")
third_backround = pygame.transform.scale(third_backround, (WIDTH, HEIGHT))
button_image = pygame.image.load("images/button.png")


def message_start(msg, size_of_font, position, color=(0, 0, 0),
                  need_size=False):
    """showing given message"""
    font = pygame.font.SysFont(None, size_of_font)
    screen_text = font.render(msg, True, color)
    if need_size:
        return font.size(msg)
    SCREEN.blit(screen_text, position)


# variable to create a blink
check = 0


def welcome_page():
    """drawing welcome page"""
    global check
    SCREEN.blit(background, (0, 0))
    check += 1
    if check % 5 < 3:
        msg = "Click anywhere to start!"
        message_start(msg, round(HEIGHT * 0.035), (
            WIDTH // 2 - (round(HEIGHT * 0.035) * len(msg) // 8),
            HEIGHT * 0.2))


class FieldToWrite:
    def __init__(self, name_of, size, size_of_font, position, color,
                 msg="",
                 color_of_font=(0, 0, 0)):
        self.size = size
        self.position = position
        self.msg = msg
        self.color = color
        self.size_of_font = size_of_font
        self.area = (position[0] + size[0], position[1] + size[1])
        self.color_of_font = color_of_font
        self.msg_to_show = ""
        self.position_of_font = (
            position[0] + size_of_font // 2, position[1] + size_of_font // 2)
        self.name_of = name_of
        self.name_coordinates = (
            self.position_of_font[0] - size_of_font * len(name_of) // 1.5,
            self.position_of_font[1])

    def add_letter(self, letter):
        self.msg += letter
        if message_start(self.msg_to_show + "ww", self.size_of_font,
                         self.position_of_font, need_size=True)[0] < self.size[
            0]:
            self.msg_to_show += letter

    def backspace(self):
        if len(self.msg) > 0:
            if self.msg_to_show == self.msg:
                self.msg_to_show = self.msg_to_show[:-1]
            self.msg = self.msg[:-1]

    def draw(self, line_size=0):
        if not line_size:
            line_size = self.size[0] // 100
        pygame.draw.rect(SCREEN, self.color, (
            self.position[0], self.position[1], self.size[0], self.size[1]))
        pygame.draw.lines(SCREEN, (0, 0, 0), True, [self.position, (
            self.position[0] + self.size[0], self.position[1]),
                                                    (self.position[0] +
                                                     self.size[0],
                                                     self.position[1] +
                                                     self.size[1]), (
                                                        self.position[0],
                                                        self.position[1] +
                                                        self.size[1])],
                          line_size)
        message_start(self.msg_to_show, self.size_of_font,
                      self.position_of_font,
                      self.color_of_font)
        message_start(self.name_of, round(1.5 * self.size_of_font),
                      self.name_coordinates,
                      self.color_of_font)

    def mouse_on(self):
        if pygame.mouse.get_pressed()[0] and (
                self.position[0] < pygame.mouse.get_pos()[0] < \
                self.position[0] + \
                self.size[0]) and (self.position[1] < \
                                   pygame.mouse.get_pos()[1] <
                                   self.position[1] + \
                                   self.size[1]):
            return True
        return False

    def druc(self, r, l):
        next_one = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                key = pygame.key.name(event.key)
                if len(key) == 1:
                    if l:
                        key = cyrillic_keys[key]
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.add_letter(key.upper())
                    else:
                        self.add_letter(key)
                elif key == "space":
                    self.add_letter(" ")
                elif key == "caps lock":
                    l = not l
                elif key == "backspace":
                    self.backspace()
                elif key == "return":
                    next_one = True
        return r, l, next_one


def Page_ask_user():
    global run, language, city, country, artist
    SCREEN.blit(second_backround, (0, 0))
    end = False
    if city_field.mouse_on():
        city = True
        country = False
        artist = False
    if country_field.mouse_on():
        city = False
        country = True
        artist = False
    if artist_field.mouse_on():
        city = False
        country = False
        artist = True
    if city:
        run, language, country = city_field.druc(run, language)
    if country:
        city = False
        run, language, artist = country_field.druc(run, language)
    if artist:
        country = False
        run, language, end = artist_field.druc(run, language)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    city_field.draw()
    country_field.draw()
    artist_field.draw()
    return end


class DayNode:
    CORNER = 0
    SIZE = (2 * HEIGHT + 2 * WIDTH) // 44
    WEEK = ["MON", "TUE", "WED", 'THU', 'FRI', 'SAT', "SUN"]

    def __init__(self, meaning, coordinates, next_one=None):
        self.number = meaning[0]
        self.weekday = meaning[1]
        self.coordinates = coordinates
        self.next_one = next_one
        self.is_chosen = False

    def make_next(self):
        addition = [(self.SIZE * (11.5 / 10) // 1, 0),
                    (0, self.SIZE * (11.5 / 10) // 1),
                    (-self.SIZE * (11.5 / 10) // 1, 0),
                    (0, -self.SIZE * (11.5 / 10) // 1)]
        new_coordinates = (self.coordinates[0] + addition[DayNode.CORNER][0],
                           self.coordinates[1] + addition[DayNode.CORNER][1])
        if (new_coordinates[0] > WIDTH - self.SIZE) or (
                new_coordinates[0] < 0) or (
                new_coordinates[1] > HEIGHT - self.SIZE) or (
                new_coordinates[1] < 0):
            DayNode.CORNER += 1
            new_coordinates = (
                self.coordinates[0] + addition[DayNode.CORNER][0],
                self.coordinates[1] + addition[DayNode.CORNER][1])
        new_meaning = (self.number + 1, self.WEEK[
            self.WEEK.index(self.weekday) + 1 - len(self.WEEK)])
        self.next_one = DayNode(new_meaning, new_coordinates)

    def choose(self):
        self.is_chosen = not self.is_chosen

    def mouse_on(self):
        mouse_position = pygame.mouse.get_pos()
        if (self.coordinates[0] < mouse_position[0] < self.coordinates[
            0] + self.SIZE) and (
                self.coordinates[1] < mouse_position[1] < self.coordinates[
            1] + self.SIZE):
            return True
        return False

    def draw(self):
        color = (0, 255, 0) if self.is_chosen else (255, 0, 0)
        pygame.draw.rect(SCREEN, color, (
            self.coordinates[0], self.coordinates[1], self.SIZE,
            self.SIZE))
        message_start(str(self.number), self.SIZE // 2, (
            self.coordinates[0] + self.SIZE // 4,
            self.coordinates[1] + self.SIZE // 4), (0, 0, 0))
        message_start(self.weekday, self.SIZE // 8, (
            self.coordinates[0] + (2 * self.SIZE) // 3,
            self.coordinates[1] + (2 * self.SIZE) // 3), (0, 0, 0))


class MonthNode:
    MONTHS = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November",
              "December"]

    def __init__(self, month, year, next_one=None):
        self.month = month
        self.year = year
        self.name = self.MONTHS[month - 1]
        inf_month = calendar.monthrange(year, month)
        self.first_day = DayNode.WEEK[inf_month[0]]
        self.amount_of_days = inf_month[1]
        self.root = DayNode((1, self.first_day), (0, 0))
        self.days = [self.root]
        self.fill_days()
        self.next_one = next_one
        self.mouse_free = True
        self.where = DayNode((0, 0), (WIDTH, HEIGHT))

    def fill_days(self):
        current = self.root
        for i in range(self.amount_of_days - 1):
            current.make_next()
            current = current.next_one
            self.days.append(current)

    def make_next(self):
        DayNode.CORNER = 0
        new = (1, self.year + 1) if self.month == 12 else (
            self.month + 1, self.year)
        new_month, new_year = new
        self.next_one = MonthNode(new_month, new_year)

    def draw(self):
        if self.mouse_free:
            for day in self.days:
                if day.mouse_on():
                    day.choose()
                    self.mouse_free = False
                    self.where = day
        elif not self.where.mouse_on():
            self.mouse_free = True
        pygame.Surface.fill(SCREEN, (255, 255, 255))
        current = self.root
        current.draw()
        while current.next_one is not None:
            current = current.next_one
            current.draw()


class Butoon:
    def __init__(self, name, position, height):
        self.name = name
        self.position = position
        self.size = (len(name) * height // 4, height)
        self.image = pygame.transform.scale(button_image,
                                            self.size)

    def mouse_on(self):
        if pygame.mouse.get_pressed()[0] and (
                self.position[0] < pygame.mouse.get_pos()[0] < self.position[
            0] + self.size[0]) and (
                self.position[1] < pygame.mouse.get_pos()[1] < self.position[
            1] + self.size[1]):
            return True
        return False

    def draw(self):
        SCREEN.blit(self.image, self.position)
        message_start(self.name, self.size[1] // 2, (
            self.position[0] + self.size[1] // 3,
            self.position[1] + self.size[1] // 3))


month = MonthNode(datetime.datetime.now().month, datetime.datetime.now().year)
current = month
for i in range(11):
    current.make_next()
    current = current.next_one
current_month = month
button_all_days = Butoon("MARK ALL FUTURE YEAR",
                         (WIDTH // 3 - HEIGHT // 7, HEIGHT // 3 + HEIGHT // 7),
                         HEIGHT // 10)
button_next_month = Butoon("NEXT MONTH", (
    button_all_days.position[0],
    button_all_days.position[1] - button_all_days.size[1] - HEIGHT // 15),
                           HEIGHT // 10)
button_finish = Butoon("FINISH CHOOSING", (
    button_next_month.position[0] + button_next_month.size[0] + HEIGHT // 15,
    button_next_month.position[1]), HEIGHT // 10)
MON = DayNode(("ALL", "MON"), (button_all_days.position[0],
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))
TUE = DayNode(("ALL", "TUE"), (button_all_days.position[0] + DayNode.SIZE,
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))
WED = DayNode(("ALL", "WED"), (button_all_days.position[0] + 2 * DayNode.SIZE,
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))
THU = DayNode(("ALL", "THU"), (button_all_days.position[0] + 3 * DayNode.SIZE,
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))
FRI = DayNode(("ALL", "FRI"), (button_all_days.position[0] + 4 * DayNode.SIZE,
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))
SAT = DayNode(("ALL", "SAT"), (button_all_days.position[0] + 5 * DayNode.SIZE,
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))
SUN = DayNode(("ALL", "SUN"), (button_all_days.position[0] + 6 * DayNode.SIZE,
                               button_all_days.position[1] +
                               button_all_days.size[1] + HEIGHT // 15))


def calendar_page_show():
    global all_weekday, run, language, current_month
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    current_month.draw()
    button_all_days.draw()
    for name in DayNode.WEEK:
        eval(name + ".draw()")
    if not current_month.next_one is None:
        button_next_month.name = current_month.next_one.name
        button_next_month.draw()
    button_finish.draw()
    if button_next_month.mouse_on():
        current_month = current_month.next_one
    if button_all_days.mouse_on():
        current = current_month
        while not current is None:
            for day in current.days:
                day.choose()
            current = current.next_one
    if button_finish.mouse_on():
        return True
    return False


cyrillic_keys = {"q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н",
                 "u": "г", "i": "ш", "o": "щ", "p": "з", "[": "х", "]": "ї",
                 "a": "ф", "s": "і", "d": "в", "f": "а", "g": "п", "h": "р",
                 "j": "о", "k": "л", "l": "д", ";": "ж", "'": "є", "z": "я",
                 "x": "ч", "c": "с", "v": "м", "b": "и", "n": "т", "m": "ь",
                 ",": "б", ".": "ю", }

welcome_menu = True
city_field = FieldToWrite("City :", (WIDTH // 2, HEIGHT // 8), HEIGHT // 16,
                          (WIDTH // 4, HEIGHT // 4), (255, 255, 255))
country_field = FieldToWrite("Country :", (WIDTH // 2, HEIGHT // 8),
                             HEIGHT // 16,
                             (WIDTH // 4, HEIGHT // 4 + HEIGHT // 4),
                             (255, 255, 255))
artist_field = FieldToWrite("Artist :", (WIDTH // 2, HEIGHT // 8),
                            HEIGHT // 16,
                            (WIDTH // 4, HEIGHT // 4 + HEIGHT // 2),
                            (255, 255, 255))
ask_user_page = False
finish = False
city = False
country = False
artist = False
calendar_page = False
all_weekday = False
language = False
run = True
result_page = False
information = {"city": 0, "country": 0, "artist": 0, "free_dates": [],
               "adults": 1}
while run:

    pygame.time.delay(100)
    if welcome_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        welcome_page()
        if pygame.mouse.get_pressed()[0]:
            welcome_menu = False
            ask_user_page = True
    if ask_user_page:
        calendar_page = Page_ask_user()
        if calendar_page:
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
            ask_user_page = False
            information["city"] = city_field.msg
            information["country"] = country_field.msg
            information["artist"] = artist_field.msg
    if calendar_page:
        finish = calendar_page_show()
    if finish:
        calendar_page = False
        current = month
        while not current is None:
            for day in current.days:
                if day.is_chosen:
                    d = str(day.number)
                    if len(d) == 1:
                        d = "0" + d
                    m = str(current.month)
                    if len(m) == 1:
                        m = "0" + m
                    y = str(current.year)
                    information["free_dates"].append(d + "/" + m + "/" + y)
            current = current.next_one
        print("downloading")
        track = get_top_track(information["artist"])
        download(make_url(track))
        filename = glob.glob("*.wav")[0]
        mixer.music.load(filename)
        mixer.music.play()
        best_event = find_best_results(information)
        if best_event is None:
            best_event = {"total price": None}
            best_event["venue"] = {"city": None}
        finish = False
        result_page = True
    if result_page:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.blit(second_backround, (0, 0))
        message_start(
            "Predictable price of trip for concert of {} to {} is {}".format(
                information["artist"], best_event["venue"]["city"],
                best_event["total_price"]), HEIGHT // 20, (0, 0))
    pygame.display.update()
pygame.quit()
