#Tutorial : how to use ThorPy with a pre-existing code - step 0
import pygame
import thorpy

pygame.init()
pygame.key.set_repeat(300, 30)

screen = pygame.display.set_mode((400,400))
screen.fill((255,255,255))
rect        = pygame.Rect((0, 0, 50, 50))
rect.center = screen.get_rect().center
clock       = pygame.time.Clock()

pygame.draw.rect(screen, (255,0,0), rect)
pygame.display.flip()
#
# declaration of some ThorPy elements ...
#
slider = thorpy.SliderX.make(100, (12, 35), "My Slider")
button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
box    = thorpy.Box.make(elements=[slider,button])
menu   = thorpy.Menu(box)
#
# important : set the screen as surface for all elements
#
for element in menu.get_population():
    element.surface = screen
#
# use the elements normally...
#
box.set_topleft((100,100))
box.blit()
box.update()

#when left arrow is pressed, the red rect goes to the left
playing_game = True
while playing_game:
    clock.tick(45)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #
                # Delete Old
                #
                pygame.draw.rect(screen, (255,255,255), rect)
                pygame.display.update(rect)
                rect.move_ip((-5,0))
                #
                # Draw new one
                #
                pygame.draw.rect(screen, (255,0,0), rect)
                pygame.display.update(rect)
        # the menu automatically integrate your elements
        menu.react(event)

pygame.quit()
