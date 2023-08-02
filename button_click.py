import pygame

# Window size
WINDOW_WIDTH=400
WINDOW_HEIGHT=400

pygame.init()
window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
pygame.display.set_caption("Point Collision")

BLACK = (  50,  50,  50 )
GREEN = (  34, 139,  34 )
BLUE  = ( 161, 255, 254 )

# The rectangle to click-in
# It is window-centred, and 33% the window size
click_rect  = pygame.Rect( WINDOW_WIDTH//3, WINDOW_HEIGHT//3, WINDOW_WIDTH//3, WINDOW_HEIGHT//3 )
rect_colour = BLACK

### Main Loop
clock = pygame.time.Clock()
done = False
while not done:

    # Handle all the events
    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            done = True

        elif ( event.type == pygame.MOUSEBUTTONUP ):
            mouse_position = pygame.mouse.get_pos()             # Location of the mouse-click
            if ( click_rect.collidepoint( mouse_position ) ):   # Was that click inside our rectangle 
                print( "hit" )
                # Flip the colour of the rect
                if ( rect_colour == BLACK ):
                    rect_colour = GREEN
                else:
                    rect_colour = BLACK
            else:
                print( "click-outside!" )

    # update the screen
    window.fill( BLUE )
    pygame.draw.rect( window, rect_colour, click_rect)  # DRAW OUR RECTANGLE
    pygame.display.flip()

    # Clamp the FPS to an upper-limit
    clock.tick_busy_loop( 60 )


pygame.quit()