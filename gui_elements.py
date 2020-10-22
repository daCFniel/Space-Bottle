import pygame


class Button:
    def __init__(self, x, y, width, height, text_color, background_color, text, is_custom_surface=False, border_thic=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.background_color = background_color
        r = 50
        g = 50
        b = 50
        if self.background_color[0] + 50 > 255:
            r = 255 - self.background_color[0]
        if self.background_color[1] + 50 > 255:
            g = 255 - self.background_color[1]
        if self.background_color[2] + 50 > 255:
            b = 255 - self.background_color[2]
        self.background_color_bright = (
            self.background_color[0] + r, self.background_color[1] + g, self.background_color[2] + b)
        # prevent rgb values going higher than 255 as it is error
        self.is_custom_surface = is_custom_surface
        self.border_thic = border_thic

    def check_mouse_collision(self):
        pos = pygame.mouse.get_pos()  # mouse position coordinates
        if self.is_custom_surface:
            return self.rect.collidepoint(pos[0] - 150, pos[1] - 134)  # fixed pos according to custom surface
        else:
            return self.rect.collidepoint(pos[0], pos[1])  # fixed pos according to custom surface

    def on_click_action(self, action):
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and self.check_mouse_collision():
            action()

    def draw(self, surface):  # with a hover effect
        if self.check_mouse_collision():
            pygame.draw.rect(surface, self.background_color_bright, self.rect)
        else:
            pygame.draw.rect(surface, self.background_color, self.rect)

    def draw_border(self, surface, color):
        pygame.draw.rect(surface, color, self.rect, self.border_thic)

    def write(self, surface, font):
        text_obj = font.render(self.text, True, self.text_color)
        text_rect = text_obj.get_rect()
        text_rect.center = self.rect.center
        surface.blit(text_obj, text_rect)


class InputBox(Button):
    def __init__(self, x, y, width, height, text_color, background_color, text, is_custom_surface=False):
        super().__init__(x, y, width, height, text_color, background_color, text, is_custom_surface)
        self.active = False  # when player clicks
        self.active2 = False  # when player presses enter

    def check_if_active(self):
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if self.check_mouse_collision():
                self.active = True
                self.text = ""
            else:
                self.active = False

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active2 = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.background_color_bright, self.rect)
        else:
            pygame.draw.rect(surface, self.background_color, self.rect)


class Text:
    def __init__(self, text, text_color, font, background_color=None):
        self.font = font
        self.text = text
        self.text_color = text_color
        self.background_color = background_color
        self.text_obj = self.font.render(self.text, True, self.text_color, self.background_color)
        self.rect = self.text_obj.get_rect()

    def write(self, surface):
        self.text_obj = self.font.render(self.text, True, self.text_color, self.background_color)
        surface.blit(self.text_obj, self.rect)
