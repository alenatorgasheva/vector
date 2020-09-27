import pygame
from random import random
from math import sqrt


SCREEN_SIZE = (1280, 720)


class Vector:
    """Class of vectors"""
    def __init__(self, x_y):
        """Initialization method"""
        x, y = x_y
        self.x = float(x)
        self.y = float(y)

    def add(self, other):
        """Sum of vectors"""
        result = self.x + other.x, self.y + other.y
        return Vector(result)

    def sub(self, other):
        """Difference of vectors"""
        result = self.x - other.x, self.y - other.y
        return Vector(result)

    def mul(self, num):
        """Scalar multiply of vector by number"""
        result = self.x * num, self.y * num
        return Vector(result)

    def scalar_mul(self, other):
        """Scalar multiply of vectors"""
        result = self.x * other.x + self.y * other.y
        return result

    def __len__(self):
        """Vector length"""
        result = sqrt(self.x * self.x + self.y * self.y)
        return Vector(result)


class Line:
    """Class of lines"""

    def __init__(self):
        """Initialization method"""
        self.points = []
        self.speeds = []

    def add_point(self, pos, speed):
        """Adding a point"""
        self.points.append(pos)
        self.speeds.append(speed)

    def change_speed(self, new_speed):
        """Change of speed"""
        for speed_number in range(len(self.speeds)):
            self.speeds[speed_number] = Vector.mul(self.speeds[speed_number], new_speed)

    def delete_point(self):
        """Point removal"""
        self.points = self.points[:-1]
        self.speeds = self.speeds[:-1]

    def draw_points(self, style='point', width=4, color=(255, 255, 255)):
        """Drawing of points and lines"""
        if style == 'line':
            points = self.get_joint()
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (points[point_number].x, points[point_number].y),
                                (points[point_number + 1].x, points[point_number + 1].y), width)

        elif style == 'point':
            for point in self.points:
                pygame.draw.circle(gameDisplay, color, (int(point.x), int(point.y)), width)

    def set_points(self):
        """Point setting"""
        for point in range(len(self.points)):
            self.points[point] = Vector.add(self.points[point], self.speeds[point])

            if self.points[point].x > SCREEN_SIZE[0] or self.points[point].x < 0:
                result = - self.speeds[point].x, self.speeds[point].y
                self.speeds[point] = Vector(result)

            if self.points[point].y > SCREEN_SIZE[1] or self.points[point].y < 0:
                result = self.speeds[point].x, - self.speeds[point].y
                self.speeds[point] = Vector(result)


class Joint(Line):
    """Class of joints"""

    def __init__(self):
        """Initialization method"""
        super().__init__()
        self.steps = 20

    def draw_points(self, color):
        """Drawing of lines"""
        super().draw_points(style='line', color=color)

    def get_joint(self):
        """Getting the joint"""
        result = []
        if len(self.points) < 3:
            return []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append(Vector.mul(Vector.add(self.points[i], self.points[i + 1]), 0.5))
            pnt.append(self.points[i + 1])
            pnt.append(Vector.mul(Vector.add(self.points[i + 1], self.points[i + 2]), 0.5))

            result.extend(self.get_points(pnt))

        return result

    def get_points(self, base_points):
        """Getting points"""
        alpha = 1 / self.steps
        result = []
        for i in range(self.steps):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_point(self, base_points, alpha, deg=None):
        """Getting point"""
        if deg is None:
            deg = len(base_points) - 1

        if deg == 0:
            return base_points[0]

        return Vector.add(Vector.mul(base_points[deg], alpha),
                          Vector.mul(self.get_point(base_points, alpha, deg - 1), 1 - alpha))


def display_help(joint):
    """Help menu"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["H", "Увеличить скорость"])
    data.append(["L", "Уменьшить скорость"])
    data.append(["DELETE", "Удалить точку из кривой"])
    data.append(["", ""])
    data.append([str(joint.steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    working = True
    show_help = False
    pause = False

    line = Line()
    joint = Joint()
    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line.points = []
                    line.speeds = []
                    joint.points = []
                    joint.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    joint.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    joint.steps -= 1 if joint.steps > 1 else 0
                if event.key == pygame.K_h:
                    line.change_speed(2)
                    joint.change_speed(2)
                if event.key == pygame.K_l:
                    line.change_speed(0.5)
                    joint.change_speed(0.5)
                if event.key == pygame.K_DELETE:
                    line.delete_point()
                    joint.delete_point()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = Vector(event.pos)
                speed = random() * 2, random() * 2
                line.add_point(pos, Vector(speed))
                joint.add_point(pos, Vector(speed))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        line.draw_points()
        joint.draw_points(color=color)

        if not pause:
            line.set_points()
            joint.set_points()
        if show_help:
            display_help(joint)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
