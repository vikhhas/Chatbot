import telebot
import config
import datetime
import random
import re
import math
import re
from telebot import types
class CorgiBot:
    def __init__(self, token):
        self.vector_1_coords = None  # Координати першої точки вектора
        self.vector_2_coords = None  # Координати другої точки вектора
        self.bot = telebot.TeleBot(token)
        self.start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Клавіатура з кнопками
        self.start_item = types.KeyboardButton("📚 Теми")  # Кнопка "Теми"
        self.exit_item = types.KeyboardButton("🚪 Вихід")  # Кнопка "Вийти"
        self.help_item = types.KeyboardButton("🆘 Допомога")  # Кнопка "Допомога"
        self.start_markup.add(self.start_item, self.help_item)  # Додавання кнопок до клавіатури
        self.start_markup.add(self.exit_item)  # Додавання кнопок до клавіатури
        self.topics = {
            "📏 Математика": ["Скалярний добуток векторів", "Площа прямокутника", "Число π"],
            "🌍 Географія": ["5 найвищих гір", "Країна з найбільшої кількістю озер", "Місто з найбільшою кількістю населення", "Знайти азимут", "Відстань між двома точками"],
            "🤮 Фізика": ["Закон Ньютона", "Закон Кулона", "Стала Планка", "Кулонівська стала"],
            "💫 Філологія": ["Як утворити пасив в англійській мові?", "Як утворити форму множини в українській мові?"],
            "📃 Робота з текстом": ["Слова з певною літерою", "Найдовше речення", "Алфавітний порядок",
                                   "Видалити слова з цифрами", "Найдовші слова без голосних"],
            "🤓 Загальні": ["Днів у році", "Заспівай колядку", "Гра історія", "Найпоширеніша мова", "Найбільша тварина",
                           "Найвища будівля", "Найвідоміша нагорода у кіноіндустрії", "Найбільш відома статуя",
                           "Найшвидша тварина", "Найбільш відомий музичний фестиваль"]
        }  # Словник з темами та підтемами
        self.state = {}  # Стан розмови
        self.log_file = "dialog.txt"  # Ім'я файлу для запису журналу розмови
        self.log_filename = None
    def format_user_message(self, message):
        """
        Форматує повідомлення користувача.

        Args:
            message (str): Повідомлення користувача.

        Returns:
            str: Форматоване повідомлення з позначкою користувача.
        """
        return f"<b>👤 Пользователь:</b> {message}"
    def format_bot_message(self, message):
        """
        Форматує повідомлення бота.

        Args:
            message (str): Повідомлення бота.

        Returns:
            str: Форматоване повідомлення з позначкою бота.
        """
        return f"<b>🤖 Бот:</b> {message}"
    def log_message(self, chat_id, message_text):
        """
        Записує повідомлення у журнал розмови.

        Args:
            chat_id (int): Ідентифікатор чату.
            message_text (str): Текст повідомлення.

        """
        log_entry = f"{datetime.datetime.now()}: {message_text}\n"
        if self.log_filename:
            with open(self.log_filename, "a", encoding="utf-8") as f:
                f.write(log_entry)
        else:
            self.create_log_file(chat_id, log_entry)

    def remove_digit_words(self, text):
        """
        Видаляє з тексту всі слова, які містять цифри.

        Args:
            text (str): Вихідний текст.

        Returns:
            str: Текст з видаленими словами, що містять цифри.
        """
        words = self.get_words(text)
        filtered_words = [word for word in words if not any(char.isdigit() for char in word)]
        return ' '.join(filtered_words)

    def get_sentences(self, text):
        sentences = []
        for line in text:
            line = line.strip()
            if line:
                line_sentences = line.split('.')  # Разделение строки на предложения по символу точки
                sentences.extend(line_sentences)
        return sentences

    def process_text_file(self, input_file_path, output_file_path):
        """
        Обробляє текстовий файл.

        Args:
            input_file_path (str): Шлях до вхідного файлу.
            output_file_path (str): Шлях до файлу для запису результату.
        """
        # Відкриває вхідний файл для прочитання
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            text = input_file.read()

        # Обробка тексту та запис рез-ів у вихідний файл
        processed_text = self.process_text(text)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(processed_text)
    def calculate_distance(self, point1, point2):
        """
        Обчислює відстань між двома точками.

        Args:
            point1 (tuple): Координати першої точки.
            point2 (tuple): Координати другої точки.

        Returns:
            float: Відстань між точками.
        """
        if len(point1) != len(point2):
            raise ValueError("Довжини точок повинні бути однаковими.")
        distance = sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5
        return distance
    def calculate_coulomb_law(self, charge1, charge2, distance):
        """
        Обчислює електричну силу за законом Кулона.

        Args:
            charge1 (float): Заряд першого об'єкту.
            charge2 (float): Заряд другого об'єкту.
            distance (float): Відстань між об'єктами.

        Returns:
            float: Електрична сила.
        """
        k = 9e9  # Електростатична стала
        electric_force = k * abs(charge1) * abs(charge2) / (distance ** 2)
        return electric_force

    def get_words(self, text):
        words = text.split()
        return words
    def calculate_newton_law(self, mass1, mass2, distance):
        """
        Обчислює гравітаційну силу за законом Ньютона.

        Args:
            mass1 (float): Маса першого об'єкту.
            mass2 (float): Маса другого об'єкту.
            distance (float): Відстань між об'єктами.

        Returns:
            float: Гравітаційна сила.
        """
        G = 6.67430e-11  # Гравітаційна постійна
        gravitational_force = G * abs(mass1) * abs(mass2) / (distance ** 2)
        return gravitational_force

    def get_plank_constant(self):
        """
        Повертає значення сталої Планка.

        Returns:
            float: Значення сталої Планка.
        """
        plank_constant = 6.62607015e-34  # Значення сталої Планка
        return plank_constant
    def get_coulomb_constant(self):
        """
        Повертає значення кулонівської постійної.

        Returns:
            float: Значення кулонівської постійної.
        """
        coulomb_constant = 8.9875517923e9  # Значення кулонівської сталої
        return coulomb_constant
    def get_pi_constant(self):
        """
        Повертає значення числа пі.

        Returns:
            float: Значення числа пі.
        """
        pi_constant = 3.141592  # Значення числа пі
        return pi_constant

    def create_log_file(self, chat_id, log_entry):
        """
        Створює файл журналу з діалогом.

        Args:
            chat_id (int): ID чату.
            log_entry (str): Запис журналу для збереження.

        Returns:
            None
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_filename = f"dialog_{timestamp}.txt"
        with open(self.log_filename, "w", encoding="utf-8") as f:
            f.write(f"Chat ID: {chat_id}\n")
            f.write(f"Start Time: {timestamp}\n")
            f.write(log_entry)

    def find_longest_words(self, text):
        sentences = self.get_sentences(text)
        words = self.get_words(text)
        longest_words = []
        max_length = 0
        vowels = ['а', 'е', 'и', 'і', 'ї', 'о', 'у', 'ю', 'я', 'є', 'ї']
        for word in words:
            has_vowels = False
            for vowel in vowels:
                if vowel in word:
                    has_vowels = True
                    break
            if not has_vowels:
                word_length = len(word)
                if word_length > max_length:
                    max_length = word_length
                    longest_words = [word]
                elif word_length == max_length:
                    longest_words.append(word)
        return longest_words

    def find_longest_words(self, text):
        words = self.get_words(text)
        longest_words = []
        max_length = 0

        for word in words:
            word = word.strip()
            if self.has_vowels(word):
                continue

            length = len(word)
            if length > max_length:
                max_length = length
                longest_words = [word]
            elif length == max_length:
                longest_words.append(word)

        return longest_words

    def has_vowels(self, word):
        vowels = ['а', 'е', 'и', 'і', 'ї', 'о', 'у', 'ю', 'я', 'є', 'ї']
        for vowel in vowels:
            if vowel in word:
                return True
        return False
    def contains_vowel(self, word):
        """
        Перевіряє, чи містить слово голосну літеру.

        Args:
            word (str): Слово для перевірки.

        Returns:
            bool: True, якщо слово містить голосну літеру, інакше False.
        """
        vowels = ['a', 'e', 'i', 'o', 'u']
        for vowel in vowels:
            if vowel in word.lower():
                return True
        return False

    def calculate_days_in_year(self, year):
        """
        Обчислює кількість днів у році.

        Args:
            year (int): Рік для обчислення.

        Returns:
            int: Кількість днів у році (365 або 366).
        """
        if year % 400 == 0:
            return 366
        elif year % 100 == 0:
            return 365
        elif year % 4 == 0:
            return 366
        else:
            return 365
    def calculate_azimuth(self, point1_coords, point2_coords):
        """
        Обчислює азимут між двома точками.

        Args:
            point1_coords (tuple): Координати першої точки у вигляді кортежу (x1, y1).
            point2_coords (tuple): Координати другої точки у вигляді кортежу (x2, y2).

        Returns:
            float: Значення азимуту між точками в градусах.
        """
        x1, y1 = point1_coords
        x2, y2 = point2_coords
        dx = x2 - x1
        dy = y2 - y1
        # Розрахунок азимуту за допомогою функції atan2
        azimuth_rad = math.atan2(dy, dx)
        azimuth_deg = math.degrees(azimuth_rad)
        # Коригування азимуту до діапазону 0-360 градусів
        if azimuth_deg < 0:
            azimuth_deg += 360
        return azimuth_deg

    def get_most_spoken_language(self):
        """
        Отримує найпоширеніші мови та їх описи.

        Returns:
            str: Форматований текст з переліком мов та їх описами.
        """
        languages = {
            "· Англійська": " Англійська мова - міжнародна мова спілкування, яка використовується в багатьох країнах світу.",
            "· Китайська": " Китайська мова - найпоширеніша мова серед населення Китаю та китайської діаспори.",
            "· Іспанська": " Іспанська мова - друга за популярністю мова у світі після китайської.",
            "· Арабська": " Арабська мова - мова, якою говорять у більшості арабських країн.",
            "· Французька": " Французька мова - одна з офіційних мов ООН та міжнародного співтовариства."
        }

        descriptions = []
        used_descriptions = set()  # Множина для відстеження вже використаних описів
        for language, description in languages.items():
            if description not in used_descriptions:
                descriptions.append(f"{language}: {description}")
                used_descriptions.add(description)

        formatted_text = "\n".join(descriptions)
        return formatted_text
    def get_largest_animal_description(self):
        return "Найбільша тварина - синій кит. Вага синього кита може досягати близько 200 тонн, а його довжина може перевищувати 30 метрів."

    def get_tallest_building_description(self):
        return "Найвища будівля - Бурдж Халіфа. Загальна висота Бурдж Халіфа становить близько 828 метрів, що робить його найвищою будівлею у світі."

    def get_most_famous_movie_award_description(self):
        return "Найвідоміша нагорода у кіноіндустрії - премія Оскар. Премія Оскар є однією з найпрестижніших нагород у кіноіндустрії і вручається щорічно в Голлівуді."

    def get_most_famous_statue_description(self):
        return "Найбільш відома статуя - Статуя Свободи. Розташована на острові Ліберті в Нью-Йоркській гавані, Статуя Свободи є одним із найвідоміших символів США."

    def get_fastest_animal_description(self):
        return "Найшвидша тварина - гепард. Гепард може розвивати швидкість до 110 кілометрів на годину протягом короткого періоду часу."

    def get_most_famous_music_festival_description(self):
        return "Найбільш відомий музичний фестиваль - фестиваль Гластонбері. Фестиваль Гластонбері вважається одним з найбільших і найвідоміших музичних фестивалів у світі."

    def find_words_with_letter(self, letter):
        """
        Знаходить слова, які містять певну літеру.

        Args:
            letter (str): Літера для пошуку.

        Returns:
            list: Список слів, які містять задану літеру.
        """
        words = []
        for word in self.word_list:
            if letter in word.lower():
                words.append(word)
        return words

    def find_longest_sentence(self, text):
        sentences = text.split('.')
        longest_sentence = ''
        max_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            length = len(sentence)
            if length > max_length:
                max_length = length
                longest_sentence = sentence
        return longest_sentence

    def sort_words_alphabetically(self, words):
        """
        Сортує слова в алфавітному порядку.

        Args:
            words (list): Список слів для сортування.

        Returns:
            list: Відсортований список слів.
        """
        words.sort()  # Сортування слів
        return words
    def remove_words_with_digits(self, text1):
        """
        Видаляє слова, які містять цифри, з тексту.

        Args:
            text1 (str): Початковий текст.

        Returns:
            str: Текст, в котором видалені слова, які містять цифри.
        """
        words = text1.split()
        cleaned_words = []
        for word in words:
            if not re.search(r'\d', word):
                cleaned_words.append(word)
        cleaned_text = ' '.join(cleaned_words)
        return cleaned_text

    def calculate_rectangle_area(self, length, width):
        """
        Рахую площу прямокутника.

        Args:
            length (float): Довжина прямокутника.
            width (float): Ширина прямокутника.

        Returns:
            float: Площа прямокутника.
        """
        return length * width

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            self.bot.send_message(
                message.chat.id,
                "Ласкаво просимо, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, створений для експериментів.".format(
                    message.from_user, self.bot.get_me()),
                parse_mode='html', reply_markup=self.start_markup
            )

        @self.bot.message_handler(content_types=['text'])
        def handle_message(message):
            if message.chat.type == 'private':
                self.log_message(message.chat.id, message.text)

                if message.from_user.id == self.bot.get_me().id:
                    formatted_message = self.format_bot_message("Я не знаю що відповісти 😢")
                    self.bot.send_message(message.chat.id, formatted_message, parse_mode='html')
                else:
                    formatted_message = self.format_user_message(message.text)
                    self.bot.send_message(message.chat.id, formatted_message, parse_mode='html')

                if message.text == '📚 Теми':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for topic in self.topics:
                        markup.add(types.KeyboardButton(topic))

                    markup.add(types.KeyboardButton("🔙 Повернутись"))
                    self.bot.send_message(message.chat.id, 'Оберіть тему:', reply_markup=markup)
                    self.state[message.chat.id] = 'topics'

                elif message.text == '🚪 Вихід':
                    self.bot.send_message(message.chat.id, 'Ви завершили сесію. До нових зустрічей!',
                                          reply_markup=types.ReplyKeyboardRemove())
                    self.state[message.chat.id] = None

                elif message.text == '🔙 Повернутись':
                    if self.state[message.chat.id] == 'subtopics':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for topic in self.topics:
                            markup.add(types.KeyboardButton(topic))

                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть тему:', reply_markup=markup)
                        self.state[message.chat.id] = 'topics'
                    elif self.state[message.chat.id] == 'topics':
                        self.bot.send_message(message.chat.id, 'Повертаємося назад', reply_markup=self.start_markup)
                        self.state[message.chat.id] = None

                elif message.text in self.topics:
                    self.current_topic = message.text
                    subtopics = self.topics[self.current_topic]
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for subtopic in subtopics:
                        markup.add(types.KeyboardButton(subtopic))
                    markup.add(types.KeyboardButton("🔙 Повернутись"))
                    self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == '🆘 Допомога' or message.text == '/help':
                    help_message =  "1. Закон всесвітнього тяжіння Ньютона: F = G * (m1 * m2) / r^2, де F - сила притягання між двома тілами, G - гравітаційна стала, m1 та m2 - маси тіл, r - відстань між центрами тіл. (Обчислити F. m1, m2, r – параметри)\n" \
                                   "6. Закон Кулона: F = k * (q1 * q2) / r^2, де F - сила електростатичної взаємодії між двома зарядженими частинками, k - кулонівська стала, q1 та q2 - заряди частинок, r - відстань між центрами частинок. (Обчислити F)\n" \
                                   "11. Вивести сталу Планка\n" \
                                   "12. Вивести кулонівську сталу\n" \
                                   "17. Формула скалярного добутку векторів: A · B = |A| |B| cos(θ), де |A| та |B| - довжини векторів, θ - кут між ними.\n" \
                                   "22. Площа прямокутника: S = a * b, де a та b - довжини сторін прямокутника.\n" \
                                   "27. Вивести число π.\n" \
                                   "32. Назвіть 5 найвищих гір в світі та вкажіть їхні висоти.\n" \
                                   "37. Яка держава має найбільшу кількість озер в світі?\n" \
                                   "38. Яке місто має найбільшу кількість населення в світі?\n" \
                                   "42. Знайти відстань між двома точками А (x1, y1) та В (x2, y2), якщо відомі їх координати.\n" \
                                   "43. Знайти азимут від точки А (x1, y1) до точки В (x2, y2), якщо відомі їх координати.\n" \
                                   "48. Як утворити Passive Voice в Present Simple?\n" \
                                   "53. Як утворити форму множини іменників в українській мові?\n" \
                                   "58. Знайти всі слова, що містять певну літеру (попередньо співрозмовник має запитати літеру).\n" \
                                   "63. Вивести всі слова довші за 10 символів.\n" \
                                   "68. Знайти найдовше речення в тексті.\n" \
                                   "69. Вивести слова в алфавітному порядку.\n" \
                                   "73. Видалити з тексту всі слова, які містять цифри.\n" \
                                   "74. Знайти найдовші слова, які не містять голосних літер.\n" \
                                   "79. Скільки днів у ___ році?\n" \
                                   "84. Заспівати колядку (5 різних, вивести куплет).\n" \
                                   "89. Гра «історія». Співрозмовник задає 5 питань: хто, де, коли, навіщо, що. І підставляє їх у заготований текст і виводить. (5 різних текстів).\n" \
                                   "94. Яка найпоширеніша мова у світі?\n" \
                                   "99. Яка найбільша тварина?\n" \
                                   "100. Яка найвища будівля у світі наразі?\n" \
                                   "104. Яка найвідоміша нагорода у кіноіндустрії?\n" \
                                   "105. Яка найбільш відома статуя у світі?\n" \
                                   "110. Яка найшвидша тварина?\n" \
                                   "115. Який найбільш відомий музичний фестиваль у світі?\n\n"\
                                   "Для виходу, напишіть 🚪 Вихід "

                    self.bot.send_message(message.chat.id, help_message)
                    self.state[message.chat.id] = None

                elif message.text == 'Вийти':
                    self.bot.send_message(message.chat.id, 'До зустрічі! Дякую, що скористалися нашим ботом.',
                                          reply_markup=types.ReplyKeyboardRemove())
                    self.state[message.chat.id] = None


                elif message.text == 'Стала Планка' and self.state[message.chat.id] == 'subtopics':
                    plank_constant = self.get_plank_constant()
                    self.bot.send_message(message.chat.id, f'Стала Планка: {plank_constant}')

                elif message.text == 'Кулонівська стала' and self.state[message.chat.id] == 'subtopics':
                    q_constant = self.get_coulomb_constant()
                    self.bot.send_message(message.chat.id, f'Кулонівська стала: {q_constant}')

                elif message.text == 'Закон Кулона' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть значення заряду q1:')
                    self.state[message.chat.id] = 'charge1'

                elif self.state[message.chat.id] == 'charge1':
                    try:
                        charge1 = float(message.text)
                        self.state['charge1'] = charge1
                        self.bot.send_message(message.chat.id, 'Введіть значення заряду q2:')
                        self.state[message.chat.id] = 'charge2'
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif self.state[message.chat.id] == 'charge2':
                    try:
                        charge2 = float(message.text)
                        self.state['charge2'] = charge2
                        self.bot.send_message(message.chat.id, 'Введіть відстань між зарядами:')
                        self.state[message.chat.id] = 'distance1'
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif self.state[message.chat.id] == 'distance1':
                    try:
                        distance1 = float(message.text)
                        charge1 = self.state['charge1']
                        charge2 = self.state['charge2']
                        electric_force = self.calculate_coulomb_law(charge1, charge2, distance1)
                        self.bot.send_message(message.chat.id, f'Електрична сила: {electric_force}')
                        self.state[message.chat.id] = 'subtopics'
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif message.text == 'Закон Ньютона' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть значення маси m1:')
                    self.state[message.chat.id] = 'mass1'

                elif self.state[message.chat.id] == 'mass1':
                    try:
                        mass1 = float(message.text)
                        self.bot.send_message(message.chat.id, 'Введіть значення маси m2:')
                        self.state[message.chat.id] = 'mass2'
                        self.state['mass1'] = mass1
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif self.state[message.chat.id] == 'mass2':
                    try:
                        mass2 = float(message.text)
                        self.bot.send_message(message.chat.id, 'Введіть значення відстані r:')
                        self.state[message.chat.id] = 'distance'
                        self.state['mass2'] = mass2
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif self.state[message.chat.id] == 'distance':
                    try:
                        distance = float(message.text)
                        mass1 = self.state['mass1']
                        mass2 = self.state['mass2']
                        gravitational_force = self.calculate_newton_law(mass1, mass2, distance)
                        self.bot.send_message(message.chat.id, f'Гравітаційна сила: {gravitational_force}')
                        self.state[message.chat.id] = 'subtopics'
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif message.text == 'Днів у році' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть рік:')
                    self.state[message.chat.id] = 'year'

                elif self.state[message.chat.id] == 'year':
                    try:
                        year = int(message.text)
                        days_in_year = self.calculate_days_in_year(year)
                        self.bot.send_message(message.chat.id, f'Кількість днів у році: {days_in_year}')
                        self.state[
                            message.chat.id] = 'subtopics'
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')

                elif message.text == 'Заспівай колядку' and self.state[message.chat.id] == 'subtopics':
                    carols = [
                        ("Коляда, коляда, дзвенять дзвони!", "Хто в гості до нас прийшов, щедрий Ісус Слава Богу!"),
                        ("З Новим роком вас вітаємо, Христос народився!",
                         "З Новим роком ми вас вітаємо, Веселих свят щиро бажаємо!"),
                        ("Веселі колядки співаймо, зірки світанку розписуймо!",
                         "Радість, щастя й веселість нехай буде вам в домі!"),
                        ("Хто має покришки на колесах, він нехай їздить по багатствах!",
                         "Хто має чобітки на ніжках, він нехай грає по золотках!"),
                        ("Дзвенять колокольчики, щедрівочки співають, зірки сяють, Христос народився!",
                         "Щастя, радість і здоров'я у вашому домі нехай зігрівають!")
                    ]
                    carol = random.choice(carols)
                    verse1, verse2 = carol
                    self.bot.send_message(message.chat.id, f"{verse1}\n{verse2}")
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Гра історія' and self.state[message.chat.id] == 'subtopics':
                    questions = ['Хто', 'Де', 'Коли', 'Навіщо', 'Що']
                    texts = [
                        'Жила-була {0} в {1} {2} році. Вона прийшла туди {3} і робила {4}.',
                        'Був колись {0}, який жив у {1}. У {2} році він зробив це для {3} і отримав {4}.',
                        'У {2} році {0} прийшов до {1}. Це було для {3} і {4} було результатом.',
                        '{0} в {2} році прибув до {1}. Його мета була {3}, і він робив {4}.',
                        'У {2} році {0} вирушив до {1} для {3}. Він зробив це, реалізовуючи {4}.'
                    ]

                    # Генеруємо випадкові відповіді для кожного запитання
                    answers = [
                        'королева', 'країна', '2023', 'розваги', 'реформи',
                        'моряк', 'місто', '1876', 'пригода', 'відкриття',
                        'мандрівник', 'село', '1600', 'пригода', 'відкриття',
                        'вчений', 'лабораторія', '1945', 'дослідження', 'відкриття',
                        'розвідник', 'пустеля', '2020', 'безпека', 'місія'
                    ]

                    for text in texts:
                        # Вибираємо випадкову відповідь для кожного запитання
                        random_answers = [answers.pop(random.randrange(len(answers))) for _ in range(5)]
                        story = text.format(*random_answers)
                        self.bot.send_message(message.chat.id, story)

                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найпоширеніша мова' and self.state[message.chat.id] == 'subtopics':
                    most_spoken_language = self.get_most_spoken_language()
                    self.bot.send_message(message.chat.id, f'Найпоширініша мова: {most_spoken_language}')
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найбільша тварина' and self.state[message.chat.id] == 'subtopics':
                    animal_description = self.get_largest_animal_description()
                    self.bot.send_message(message.chat.id, animal_description)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найвища будівля' and self.state[message.chat.id] == 'subtopics':
                    building_description = self.get_tallest_building_description()
                    self.bot.send_message(message.chat.id, building_description)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найвідоміша нагорода у кіноіндустрії' and self.state[
                    message.chat.id] == 'subtopics':
                    award_description = self.get_most_famous_movie_award_description()
                    self.bot.send_message(message.chat.id, award_description)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найбільш відома статуя' and self.state[message.chat.id] == 'subtopics':
                    statue_description = self.get_most_famous_statue_description()
                    self.bot.send_message(message.chat.id, statue_description)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найшвидша тварина' and self.state[message.chat.id] == 'subtopics':
                    fastest_animal_description = self.get_fastest_animal_description()
                    self.bot.send_message(message.chat.id, fastest_animal_description)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Найбільш відомий музичний фестиваль' and self.state[
                    message.chat.id] == 'subtopics':
                    music_festival_description = self.get_most_famous_music_festival_description()
                    self.bot.send_message(message.chat.id, music_festival_description)
                    self.state[message.chat.id] = 'subtopics'

                if message.text == 'Слова з певною літерою' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть ім\'я вхідного файлу:')
                    self.state[message.chat.id] = 'input_file_name'
                elif self.state[message.chat.id] == 'input_file_name':
                    input_file_name = message.text
                    try:
                        with open(input_file_name, 'r', encoding='utf-8') as file:
                            words = file.read().split()
                        self.state['words'] = words
                        word_list = ", ".join(words)
                        self.bot.send_message(message.chat.id, f"Список слів з файлу '{input_file_name}':\n{word_list}")
                        self.bot.send_message(message.chat.id, 'Введіть літеру:')
                        self.state[message.chat.id] = 'letter_input'
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка читання файлу '{input_file_name}'.")
                        self.state[message.chat.id] = 'subtopics'
                elif self.state[message.chat.id] == 'letter_input':
                    letter = message.text.lower()
                    words = self.state['words']
                    words_with_letter = [word for word in words if letter in word.lower()]
                    if words_with_letter:
                        word_list = ", ".join(words_with_letter)
                        self.bot.send_message(message.chat.id, f"Слова, що містять літеру '{letter}':\n{word_list}")
                    else:
                        self.bot.send_message(message.chat.id, f"Слова, що містять літеру '{letter}' не знайдені.")
                    self.bot.send_message(message.chat.id, 'Введіть ім\'я вихідного файлу:')
                    self.state[message.chat.id] = 'output_file_name'
                    self.state['letter'] = letter
                elif self.state[message.chat.id] == 'output_file_name':
                    output_file_name = message.text
                    letter = self.state['letter']
                    words_with_letter = [word for word in self.state['words'] if letter in word.lower()]
                    if words_with_letter:
                        word_list = "\n".join(words_with_letter)
                        try:
                            with open(output_file_name, 'w', encoding='utf-8') as file:
                                file.write(word_list)
                            self.bot.send_message(message.chat.id,
                                                  f"Слова, що містять літеру '{letter}', записані у файл '{output_file_name}'.")
                        except IOError:
                            self.bot.send_message(message.chat.id, f"Помилка запису в файл '{output_file_name}'.")
                    else:
                        self.bot.send_message(message.chat.id, f"Слова, що містять літеру '{letter}' не знайдені.")
                    self.state[message.chat.id] = 'subtopics'

                if message.text == 'Найдовше речення' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть ім\'я вхідного файлу:')
                    self.state[message.chat.id] = 'input_file_name_longest_sentence'
                elif self.state[message.chat.id] == 'input_file_name_longest_sentence':
                    input_file_name = message.text
                    try:
                        with open(input_file_name, 'r', encoding='utf-8') as file:
                            text = file.read()
                        longest_sentence = self.find_longest_sentence(text)
                        self.bot.send_message(message.chat.id, f"Найдовше речення: {longest_sentence}")
                        self.bot.send_message(message.chat.id, 'Введіть ім\'я вихідного файлу:')
                        self.state[message.chat.id] = 'output_file_name_longest_sentence'
                        self.state['longest_sentence'] = longest_sentence
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка читання файлу '{input_file_name}'.")
                        self.state[message.chat.id] = 'subtopics'
                elif self.state[message.chat.id] == 'output_file_name_longest_sentence':
                    output_file_name = message.text
                    longest_sentence = self.state['longest_sentence']
                    try:
                        with open(output_file_name, 'w', encoding='utf-8') as file:
                            file.write(longest_sentence)
                        self.bot.send_message(message.chat.id,
                                              f"Найдовше речення записане у файл '{output_file_name}'.")
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка запису в файл '{output_file_name}'.")
                    self.state[message.chat.id] = 'subtopics'

                if message.text == 'Алфавітний порядок' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть ім\'я вхідного файлу:')
                    self.state[message.chat.id] = 'input_file_name_alphabetical'
                elif self.state[message.chat.id] == 'input_file_name_alphabetical':
                    input_file_name = message.text
                    try:
                        with open(input_file_name, 'r', encoding='utf-8') as file:
                            text = file.read()
                        words = self.get_words(text)
                        sorted_words = sorted(words, key=lambda x: x.lower())
                        word_list = "\n".join(sorted_words)
                        self.bot.send_message(message.chat.id, f"Список слів в алфавітному порядку:\n{word_list}")
                        self.bot.send_message(message.chat.id, 'Введіть ім\'я вихідного файлу:')
                        self.state[message.chat.id] = 'output_file_name_alphabetical'
                        self.state['sorted_words'] = sorted_words
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка читання файлу '{input_file_name}'.")
                        self.state[message.chat.id] = 'subtopics'
                elif self.state[message.chat.id] == 'output_file_name_alphabetical':
                    output_file_name = message.text
                    sorted_words = self.state['sorted_words']
                    try:
                        with open(output_file_name, 'w', encoding='utf-8') as file:
                            file.write('\n'.join(sorted_words))
                        self.bot.send_message(message.chat.id,
                                              f"Список слів в алфавітному порядку записано у файл '{output_file_name}'.")
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка запису в файл '{output_file_name}'.")
                    self.state[message.chat.id] = 'subtopics'

                if message.text == 'Видалити слова з цифрами' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть ім\'я вхідного файлу:')
                    self.state[message.chat.id] = 'input_file_name_remove_digits'
                elif self.state[message.chat.id] == 'input_file_name_remove_digits':
                    input_file_name = message.text
                    try:
                        with open(input_file_name, 'r', encoding='utf-8') as file:
                            text = file.read()
                        filtered_text = self.remove_digit_words(text)
                        self.bot.send_message(message.chat.id, f"Текст без слів, що містять цифри:\n{filtered_text}")
                        self.bot.send_message(message.chat.id, 'Введіть ім\'я вихідного файлу:')
                        self.state[message.chat.id] = 'output_file_name_remove_digits'
                        self.state['filtered_text'] = filtered_text
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка читання файлу '{input_file_name}'.")
                        self.state[message.chat.id] = 'subtopics'
                elif self.state[message.chat.id] == 'output_file_name_remove_digits':
                    output_file_name = message.text
                    filtered_text = self.state['filtered_text']
                    try:
                        with open(output_file_name, 'w', encoding='utf-8') as file:
                            file.write(filtered_text)
                        self.bot.send_message(message.chat.id,
                                              f"Текст без слів, що містять цифри, записано у файл '{output_file_name}'.")
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка запису в файл '{output_file_name}'.")
                    self.state[message.chat.id] = 'subtopics'

                if message.text == 'Найдовші слова без голосних' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть ім\'я вхідного файлу:')
                    self.state[message.chat.id] = 'input_file_name_longest_words'
                elif self.state[message.chat.id] == 'input_file_name_longest_words':
                    input_file_name = message.text
                    try:
                        with open(input_file_name, 'r', encoding='utf-8') as file:
                            text = file.read()
                        longest_words = self.find_longest_words(text)
                        longest_words_without_vowels = [word for word in longest_words if not self.has_vowels(word)]
                        if longest_words_without_vowels:
                            words_list = "\n".join(longest_words_without_vowels)
                            self.bot.send_message(message.chat.id, f"Найдовші слова без голосних:\n{words_list}")

                            self.bot.send_message(message.chat.id, 'Введіть ім\'я вихідного файлу:')
                            self.state[message.chat.id] = 'output_file_name_longest_words'
                            self.state['longest_words'] = longest_words_without_vowels
                        else:
                            self.bot.send_message(message.chat.id, "Немає найдовших слів без голосних.")
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка читання файлу '{input_file_name}'.")
                        self.state[message.chat.id] = 'subtopics'
                elif self.state[message.chat.id] == 'output_file_name_longest_words':
                    output_file_name = message.text
                    longest_words_without_vowels = self.state['longest_words']
                    try:
                        with open(output_file_name, 'w', encoding='utf-8') as file:
                            file.write('\n'.join(longest_words_without_vowels))
                        self.bot.send_message(message.chat.id, f"Результат записано у файл '{output_file_name}'.")
                    except IOError:
                        self.bot.send_message(message.chat.id, f"Помилка запису в файл '{output_file_name}'.")
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Число π' and self.state[message.chat.id] == 'subtopics':
                    pi_constant = self.get_pi_constant()
                    self.bot.send_message(message.chat.id, f'Число π: {pi_constant}')
                    self.state[message.chat.id] = 'subtopics'


                elif message.text == 'Скалярний добуток векторів' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id,
                                          'Введіть координати першого вектора, розділені пробілом: (x1, y1, z1)')
                    self.state[message.chat.id] = 'vector_1_input'
                elif self.state[message.chat.id] == 'vector_1_input':
                    if message.text == '🔙 Повернутись':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for subtopic in self.topics[self.current_topic]:
                            markup.add(types.KeyboardButton(subtopic))
                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                        self.state[message.chat.id] = 'subtopics'
                        return
                    vector_1_coords = message.text.split()
                    if len(vector_1_coords) != 3:
                        self.bot.send_message(message.chat.id,
                                              'Некоректний ввід. Введіть три координати, розділені пробілом.')
                        return
                    try:
                        vector_1_coords = [float(coord) for coord in vector_1_coords]
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Некоректний ввід. Введіть числові значення координат.')
                        return
                    self.bot.send_message(message.chat.id,
                                          'Введіть координати другого вектора, розділені пробілом: (x2, y2, z2)')
                    self.state[message.chat.id] = 'vector_2_input'
                    self.state['vector_1_coords'] = vector_1_coords
                elif self.state[message.chat.id] == 'vector_2_input':
                    if message.text == '🔙 Повернутись':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for subtopic in self.topics[self.current_topic]:
                            markup.add(types.KeyboardButton(subtopic))
                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                        self.state[message.chat.id] = 'subtopics'
                        return
                    vector_2_coords = message.text.split()
                    if len(vector_2_coords) != 3:
                        self.bot.send_message(message.chat.id,
                                              'Некоректний ввід. Введіть три координати, розділені пробілом.')
                        return
                    try:
                        vector_2_coords = [float(coord) for coord in vector_2_coords]
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Некоректний ввід. Введіть числові значення координат.')
                        return
                    if 'vector_1_coords' not in self.state:
                        self.bot.send_message(message.chat.id, 'Спочатку введіть координати першого вектора.')
                        return
                    vector_1_coords = self.state['vector_1_coords']
                    scalar_product = sum(x * y for x, y in zip(vector_1_coords, vector_2_coords))
                    self.bot.send_message(message.chat.id, f"Скалярний добуток векторів: {scalar_product}")
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Відстань між двома точками' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id,
                                          'Введіть координати першої точки, розділені пробілом: (x1, y1)')
                    self.state[message.chat.id] = 'point1_input'
                elif self.state[message.chat.id] == 'point1_input':
                    if message.text == '🔙 Повернутись':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for subtopic in self.topics[self.current_topic]:
                            markup.add(types.KeyboardButton(subtopic))
                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                        self.state[message.chat.id] = 'subtopics'
                        return
                    point1_coords = message.text.split()
                    if len(point1_coords) != 2:
                        self.bot.send_message(message.chat.id,
                                              'Некоректний ввід. Введіть дві координати, розділені пробілом.')
                        return
                    try:
                        point1_coords = [float(coord) for coord in point1_coords]
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Некоректний ввід. Введіть числові значення координат.')
                        return
                    self.bot.send_message(message.chat.id,
                                          'Введіть координати другої точки, розділені пробілом: (x2, y2)')
                    self.state[message.chat.id] = 'point2_input'
                    self.state['point1_coords'] = point1_coords
                elif self.state[message.chat.id] == 'point2_input':
                    point2_coords = message.text.split()
                    if message.text == '🔙 Повернутись':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for subtopic in self.topics[self.current_topic]:
                            markup.add(types.KeyboardButton(subtopic))
                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                        self.state[message.chat.id] = 'subtopics'
                        return
                    if len(point2_coords) != 2:
                        self.bot.send_message(message.chat.id,
                                              'Некоректний ввід. Введіть дві координати, розділені пробілом.')
                        return
                    try:
                        point2_coords = [float(coord) for coord in point2_coords]
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Некоректний ввід. Введіть числові значення координат.')
                        return
                    if 'point1_coords' not in self.state:
                        self.bot.send_message(message.chat.id, 'Спочатку введіть координати першої точки.')
                        return
                    point1_coords = self.state['point1_coords']
                    distance = self.calculate_distance(point1_coords, point2_coords)
                    self.bot.send_message(message.chat.id, f"Відстань між двома точками: {distance}")
                    self.state[message.chat.id] = 'subtopics'


                elif message.text == 'Як утворити пасив в англійській мові?' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, "В англійській мові конструкція Passive Voice у Present Simple утворюється за допомогою допоміжного дієслова \"to be\" у теперішньому часі (am/is/are) та основного дієслова, яке переводиться у форму причастя минулого часу (Past Participle).\nЗагальний шаблон для утворення Passive Voice у Present Simple:\n\n[Допоміжне дієслово \"to be\" у Present Simple] + [Основне дієслово у формі Past Participle] + [Додаток]")
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Як утворити форму множини в українській мові?' and self.state[message.chat.id] == 'subtopics':
                    response = '''Українська мова має кілька правил для утворення форми множини іменників. Зазвичай для утворення форми множини застосовуються наступні правила: \n· Додавання закінчення "-и" або "-ї" до деяких іменників: кіт - коти, дім - доми, мати - матері. \n· Зміна закінчення на "-а" у деяких іменниках: син - сини, брат - брати. \n· Зміна основи або внутрішнього звуку: дитина - діти, око - очі. \n· Додавання закінчення "-ища" або "-іща" до деяких іменників: стілець - стільці, дерево - дерева. \n· Деякі іменники мають неправильну форму множини, яку потрібно запам'ятати: людина - люди, миша - миші. Ці правила допомагають утворювати форму множини більшості іменників в українській мові. Проте, слід зазначити, що деякі іменники можуть мати винятки та відхилення від цих правил.'''
                    self.bot.send_message(message.chat.id, response)
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == '5 найвищих гір' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, "1. Джомолунгма (Эверест) - 8848,86 метрів \n2. Чогори - 8611 метрів \n3. Канченджанга - 8586 метрів \n4. Лхоцзе - 8516 метрів \n5. Макалу - 8485 метрів")
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Країна з найбільшої кількістю озер' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, "Країна з найбільшою кількістю озер: Канада. 60% всіх озер світу знаходяться на території Канади: більш 3000000 озер, що займають 9% канадських земель.")
                    self.state[message.chat.id] = 'subtopics'

                elif message.text == 'Місто з найбільшою кількістю населення' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, "Місто з найбільшою кількістю населення в світі на сьогоднішній день - це Токіо, Японія. За даними останнього оновлення, населення Токіо становить понад 37 мільйонів людей. Це розгалужене мегаполіс, який відомий своєю величезною площею, густотою населення та культурним багатством.")
                    self.state[message.chat.id] = 'subtopics'



                elif message.text == 'Знайти азимут' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id,
                                          'Введіть координати першої точки, розділені пробілом: (x1, y1)')
                    self.state[message.chat.id] = 'point1_input1'
                elif self.state[message.chat.id] == 'point1_input1':
                    if message.text == '🔙 Повернутись':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for subtopic in self.topics[self.current_topic]:
                            markup.add(types.KeyboardButton(subtopic))
                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                        self.state[message.chat.id] = 'subtopics'
                        return
                    point1_coords = message.text.split()
                    if len(point1_coords) != 2:
                        self.bot.send_message(message.chat.id,
                                              'Некоректний ввід. Введіть дві координати, розділені пробілом.')
                        return
                    try:
                        point1_coords = [float(coord) for coord in point1_coords]
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Некоректний ввід. Введіть числові значення координат.')
                        return
                    self.bot.send_message(message.chat.id,
                                          'Введіть координати другої точки, розділені пробілом: (x2, y2)')
                    self.state[message.chat.id] = 'point2_input1'
                    self.state['point1_coords1'] = point1_coords
                elif self.state[message.chat.id] == 'point2_input1':
                    if message.text == '🔙 Повернутись':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for subtopic in self.topics[self.current_topic]:
                            markup.add(types.KeyboardButton(subtopic))
                        markup.add(types.KeyboardButton("🔙 Повернутись"))
                        self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                        self.state[message.chat.id] = 'subtopics'
                        return
                    point2_coords = message.text.split()
                    if len(point2_coords) != 2:
                        self.bot.send_message(message.chat.id,
                                              'Некоректний ввід. Введіть дві координати, розділені пробілом.')
                        return
                    try:
                        point2_coords = [float(coord) for coord in point2_coords]
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Некоректний ввід. Введіть числові значення координат.')
                        return
                    if 'point1_coords1' not in self.state:
                        self.bot.send_message(message.chat.id, 'Спочатку введіть координати першої точки.')
                        return
                    point1_coords = self.state['point1_coords1']
                    azimuth = self.calculate_azimuth(point1_coords, point2_coords)
                    self.bot.send_message(message.chat.id, f"Азимут між двома точками: {azimuth}")
                    self.state[message.chat.id] = 'subtopics'
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for subtopic in self.topics[self.current_topic]:
                        markup.add(types.KeyboardButton(subtopic))
                    markup.add(types.KeyboardButton("🔙 Повернутись"))
                    self.bot.send_message(message.chat.id, 'Оберіть підтему:', reply_markup=markup)
                    self.state[message.chat.id] = 'subtopics'



                elif message.text == 'Площа прямокутника' and self.state[message.chat.id] == 'subtopics':
                    self.bot.send_message(message.chat.id, 'Введіть довжину прямокутника:')
                    self.state[message.chat.id] = 'rectangle_length'
                elif self.state[message.chat.id] == 'rectangle_length':
                    try:
                        rectangle_length = float(message.text)
                        self.bot.send_message(message.chat.id, 'Введіть ширину прямокутника:')
                        self.state[message.chat.id] = 'rectangle_width'
                        self.state['rectangle_length'] = rectangle_length
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')
                elif self.state[message.chat.id] == 'rectangle_width':
                    try:
                        rectangle_width = float(message.text)
                        rectangle_length = self.state['rectangle_length']
                        rectangle_area = self.calculate_rectangle_area(rectangle_length, rectangle_width)
                        self.bot.send_message(message.chat.id, f'Площа прямокутника: {rectangle_area}')
                        self.state[message.chat.id] = 'subtopics'
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Невірний формат числа. Спробуйте ще раз.')
        self.bot.polling(none_stop=True)

if __name__ == "__main__":
    bot = CorgiBot(config.TOKEN)
    bot.run()
