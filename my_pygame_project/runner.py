import pygame
from sys import exit
import random
import os

bordersX = [0, 1240]
bordersY = [0, 680]

pygame.init()
screen = pygame.display.set_mode((1240, 680))
pygame.display.set_caption("runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("C:\Windows\Fonts\ITCBLKAD.TTF", 100)

# images
base_path = os.path.dirname(__file__)
images_path = os.path.join(base_path, 'images')

# ufo in making
moving_surface = pygame.image.load(os.path.join(images_path, 'ufo0.png'))
moving_rect = moving_surface.get_rect(topleft=(random.randint(bordersX[0], bordersX[1]), random.randint(bordersY[0], bordersY[1])))

# space  img
background_img = pygame.image.load(os.path.join(images_path, 'space.jpg'))

#circle~comet
circle_image = pygame.image.load(os.path.join(images_path, 'rocky1.png'))
circle_image = pygame.transform.scale(circle_image, (random.randint(20, 50), random.randint(20, 50)))

score = 0
speed = 10
running = True
circle_spawn_time = 0
max_balls = 50

class Circle:
    def __init__(self, x, y, speed=None, angle=None):
        self.image = circle_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed if speed else random.uniform(2, 4)

        if angle is not None:
            self.direction = pygame.math.Vector2(1, 0).rotate(angle)
        else:
            # for calculating angle towards the target position
            target_x = moving_rect.centerx
            target_y = moving_rect.centery
            self.angle = pygame.math.Vector2(target_x - self.rect.centerx, target_y - self.rect.centery).angle_to(pygame.math.Vector2(1, 0))
            self.direction = pygame.math.Vector2(1, 0).rotate(self.angle)

    def move(self):
        move_vector = self.direction * self.speed
        self.rect.x += move_vector.x
        self.rect.y += move_vector.y

        # for bouncing
        if self.rect.left <= 0 or self.rect.right >= 1240:
            self.direction.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 680:
            self.direction.y *= -1

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

circles = [Circle(random.randint(10, 1230), random.randint(10, 670))]

def check_collision(circle, rect):
    circle_dist = pygame.math.Vector2(circle.rect.centerx - rect.centerx, circle.rect.centery - rect.centery)
    if circle_dist.length() < circle.rect.width / 2 + rect.width / 2:
        return True
    return False

last_spawn_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and moving_rect.right < bordersX[1]:
        moving_rect.x += speed
    if keys[pygame.K_LEFT] and moving_rect.left > bordersX[0]:
        moving_rect.x -= speed
    if keys[pygame.K_UP] and moving_rect.top > bordersY[0]:
        moving_rect.y -= speed
    if keys[pygame.K_DOWN] and moving_rect.bottom < bordersY[1]:
        moving_rect.y += speed

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > 5000 and len(circles) < max_balls:
        new_circles = []
        for circle in circles:
            if len(circles) + len(new_circles) < max_balls:
                new_circles.append(Circle(circle.rect.centerx, circle.rect.centery, angle=random.uniform(0, 360)))
        circles.extend(new_circles)
        last_spawn_time = current_time

    for circle in circles:
        circle.move()
        if check_collision(circle, moving_rect):
            running = False

    screen.blit(background_img, (0, 0))

    for circle in circles:
        circle.draw()

    screen.blit(moving_surface, moving_rect.topleft)

    score += 1 / 60
    text_surface = test_font.render("not_empty                                 Score: {}".format(round(score)), False, "green")
    screen.blit(text_surface, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()
