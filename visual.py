from dijkstras_algorithm import dijkstras_algorithm as dijkstra
import tkinter as tk
import math
from tkinter import messagebox
from tkinter import ttk

DEBUG = True

WIDTH = 800
HEIGHT = WIDTH / 2
RADIUS = int(WIDTH / 50)


class Circle:
    radius = RADIUS

    def __init__(self, x, y, position):
        self.x = x
        self.y = y
        self.position = position
        self.is_selected = False
        print('Круг создан', self.x, self.y, self.position)


class Line:
    def __init__(self, circle_start, circle_end, weight):
        self.circle_start = circle_start
        self.circle_end = circle_end
        self.weight = weight
        self.is_active = False

    def __repr__(self):
        return f"Линия: {self.circle_start.position}-{self.circle_end.position}, {self.weight}"


class CanvasPage(tk.Tk):

    def create_interface_elements(self):
        self.title('Алгоритм Дейкстры')
        self.resizable(False, False)

        self.start_node.set('0')
        self.end_node.set('4')
        self.weight_edge.set('1')

        button_run_algorithm = tk.Button(self, text='Запуск алгоритма', width=20, height=1, bg="white",
                                         fg="black", command=self.run_algorithm)
        button_clear_canvas = tk.Button(self, text='Очистить', width=20, height=1, bg="white",
                                        fg="black", command=self.clear_canvas)

        label_weight_edge = tk.Label(self, text="Вес ребра:", height=1, font='Arial 10')
        entry_weight_edge = tk.Entry(self, width=3, font='Arial 14', textvariable=self.weight_edge)

        label_start_node = tk.Label(self, text="Начальная вершина:", height=1, font='Arial 10')
        entry_start_node = tk.Entry(self, width=3, font='Arial 14', textvariable=self.start_node)

        label_end_node = tk.Label(self, text="Конечная вершина:", height=1, font='Arial 10')
        entry_end_node = tk.Entry(self, width=3, font='Arial 14', textvariable=self.end_node)

        self.canvas.grid(row=1, column=0, columnspan=9)
        label_weight_edge.grid(row=0, column=1, sticky='w')
        entry_weight_edge.grid(row=0, column=2, sticky='w')
        label_start_node.grid(row=0, column=3, sticky='w')
        entry_start_node.grid(row=0, column=4, sticky='w')
        label_end_node.grid(row=0, column=5, sticky='w')
        entry_end_node.grid(row=0, column=6, sticky='w')
        button_run_algorithm.grid(row=0, column=7, sticky='e')
        button_clear_canvas.grid(row=0, column=8, sticky='e')

    def __init__(self, *args, **kwargs):
        self.width = WIDTH
        self.height = HEIGHT
        self.radius = RADIUS
        self.circles = []
        self.matrix = []
        self.lines = []

        self.selected_circle: Circle | None = None

        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='white')

        self.start_node = tk.StringVar()
        self.end_node = tk.StringVar()
        self.weight_edge = tk.StringVar()

        self.create_interface_elements()

        self.canvas.bind('<Button-1>', self.canvas_click)

    def clear_canvas(self):
        self.circles = []
        self.matrix = []
        self.lines = []
        self.unselect_all()
        self.paint_canvas()

    def run_algorithm(self):
        start_node = self.get_start_node()
        end_node = self.get_end_node()
        order = dijkstra(self.matrix, start_node, end_node)

        self.unselect_all()
        for position in range(len(order) - 1):
            for line in self.lines:
                if line.circle_start.position == order[position] and line.circle_end.position == order[position + 1]:
                    line.is_active = True
        for circle in self.circles:
            if circle.position in order:
                circle.is_selected = True
        self.paint_canvas()
        self.unselect_all()

    def canvas_click(self, event):
        print(event.x, event.y)
        not_match = True
        if self.radius < event.x < self.width - self.radius and self.radius < event.y < self.height - self.radius:
            for circle in self.circles:
                distance = self.find_distance(event.x, event.y, circle.x, circle.y)

                if 3 * self.radius > distance > self.radius:
                    return

                if distance < self.radius:
                    if self.selected_circle is None:
                        circle.is_selected = True
                        self.selected_circle = circle
                        not_match = False
                        break
                    else:
                        if not (circle is self.selected_circle):
                            weight = self.get_weight()
                            line = self.get_line_between_circles(self.selected_circle, circle)
                            if line:
                                line.weight = weight
                            else:
                                line = Line(self.selected_circle, circle, weight)
                                self.lines.append(line)
                            self.matrix[self.selected_circle.position][circle.position] = weight
                        self.unselect_all()
                        not_match = False
                        break
            if not_match:
                self.create_circle(event.x, event.y)

            self.paint_canvas()
            self.log_matrix()

    def get_line_between_circles(self, circle_one, circle_two):
        for line in self.lines:
            if line.circle_start is circle_one and line.circle_end is circle_two:
                return line
        return None

    def get_weight(self):
        weight = self.weight_edge.get()
        if weight == 'inf':
            return float('inf')
        try:
            weight = int(weight)
            if weight >= 0:
                return weight
            else:
                raise Exception("Отрицательный вес")
        except:
            raise Exception("Кривой вес")

    def get_start_node(self):
        try:
            node = int(self.start_node.get())
            print(node)
            if 0 <= node < len(self.circles):
                return node
            else:
                raise Exception("Проблемы с диапазоном")
        except:
            raise Exception("Проблемы с начальной вершиной")

    def get_end_node(self):
        try:
            node = int(self.end_node.get())
            if 0 <= node < len(self.circles):
                return node
            else:
                raise Exception("Проблемы с конечной вершиной")
        except:
            raise Exception("Проблемы с конечной вершиной")

    def unselect_all(self):
        for circle in self.circles:
            circle.is_selected = False
        self.selected_circle = None
        for line in self.lines:
            line.is_active = False

    def create_circle(self, x, y):
        self.unselect_all()
        circle = Circle(x, y, len(self.circles))
        #self.selected_circle = circle
        #self.selected_circle.is_selected = True
        self.circles.append(circle)
        for row in self.matrix:
            row.append(None)
        self.matrix.append([None] * (len(self.matrix) + 1))

    def log_matrix(self):
        if DEBUG:
            print('-' * 20)
            for row in self.matrix:
                print(row)
            print('-' * 20)
            for line in self.lines:
                print(line)

    def paint_canvas(self):
        self.canvas.delete("all")
        for line in self.lines:
            self.paint_line(line)
        for circle in self.circles:
            self.paint_circle(circle)

    def paint_circle(self, circle: Circle):
        color = 'yellow' if circle.is_selected else 'white'
        width = 2 if circle.is_selected else 1
        self.canvas.create_oval(circle.x - circle.radius, circle.y - circle.radius, circle.x + circle.radius,
                                circle.y + circle.radius, fill=color, outline='black', width=width)
        self.canvas.create_text(circle.x, circle.y,
                                text=circle.position, fill='black',
                                justify=tk.CENTER, font="Verdana 14")

    def paint_line(self, line):
        circle_start = line.circle_start
        circle_end = line.circle_end
        color_line = 'red' if line.is_active else 'black'
        color_text = 'red' if line.is_active else 'grey'
        line_width = 3 if line.is_active else 1
        self.canvas.create_line(circle_start.x, circle_start.y, circle_end.x, circle_end.y, fill=color_line,
                                width=line_width, arrow=tk.LAST, activefill='black', arrowshape=(35, 35, 3))

        text_x = min(circle_start.x, circle_end.x) + abs((circle_start.x - circle_end.x) / 2)
        text_y = min(circle_start.y, circle_end.y) + abs((circle_start.y - circle_end.y) / 2)
        text_x += 12
        text_y += 12
        self.canvas.create_text(text_x, text_y,
                                text=line.weight, fill=color_text,
                                justify=tk.CENTER, font="Verdana 14")

    @staticmethod
    def find_distance(x0, y0, x1, y1):
        return math.sqrt(((x0 - x1) ** 2) + ((y0 - y1) ** 2))
