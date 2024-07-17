import DotDodgeDemo
import pygame as pyg

class transition():
    
    def difficulty_transition():
        player_score = DotDodgeDemo.player_score
        if player_score >= 20 and player_score < 40:
            text1 = "Still Alive?"
            text2 = "Ok, Not for Long"
        elif player_score >= 40 and player_score < 60:
            text1 = "To Be Honest"
            text2 = "I'm Rooting for Red Square"
        elif player_score >= 60 and player_score < 80:
            text1 = "Really?"
            text2 = "Not Hot Enough for You?"
        elif player_score >= 80 and player_score < 100:
            text1 = "You Made It"
            text2 = "To the End"
        elif player_score >= 100 and player_score < 120:
            text1 = "There's No Way"
            text2 = "Touch Grass"
        elif player_score >= 120 and player_score < 140:
            text1 = "I'm Planning a Party"
            text2 = "Without You"
        elif player_score >= 140 and player_score < 160:
            text1 = "Please Die Already"
            text2 = "I'm Going to Lose My Job"
        elif player_score >= 160 and player_score < 180:
            text1 = "I'm Missing the Party"
            text2 = "And It's Your FAULT!"
        elif player_score >= 180 and player_score < 200:
            text1 = "I Would Be Impressed"
            text2 = "If You Weren't Ruining My Life"
        elif player_score >= 200 and player_score < 220:
            text1 = "I'm Not Talking To You AnyMore"
            text2 = "You Must Hate Anything Red"
        elif player_score >= 220 and player_score %20:
            text1 = ">:3"
            text2 = ">:("


        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        fade_steps = 30  # Number of steps for the fade effect
        SCREEN_WIDTH = DotDodgeDemo.SCREEN_WIDTH
        SCREEN_HEIGHT = DotDodgeDemo.SCREEN_HEIGHT
        TEXT_COLOR = DotDodgeDemo.TEXT_COLOR
        screen = DotDodgeDemo.screen
        font = DotDodgeDemo.font

        for idx, color in enumerate(colors):
            for alpha in range(0, 256, int(256 / fade_steps)):  # Fade in
                fade_surface = pyg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.fill(color)
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
            
                if idx < len(colors) // 2:
                    text = font.render(text1, True, TEXT_COLOR)
                else:
                    text = font.render(text2, True, TEXT_COLOR)
                
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            
                

            for alpha in range(255, -1, -int(256 / fade_steps)):  # Fade out
                fade_surface = pyg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.fill(color)
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
            
                if idx < len(colors) // 2:
                    text = font.render(text1, True, TEXT_COLOR)
                else:
                    text = font.render(text2, True, TEXT_COLOR)
                
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            
                
            
    
    