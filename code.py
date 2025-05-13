import pygame
import time
import os
import sys

# Game setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("🎵 LyricTyper")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (210, 210, 210)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)

# Song loading
def load_song(folder_name):
    base_path = os.path.join("songs", folder_name)
    song_file = os.path.join(base_path, "song.mp3")
    lyrics_file = os.path.join(base_path, "lyrics.txt")

    lyrics_lines = []
    line_timings = []

    with open(lyrics_file, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                time_sec, lyric = line.strip().split(":", 1)
                line_timings.append(int(time_sec))
                lyrics_lines.append(lyric.strip())

    return song_file, lyrics_lines, line_timings

# Song selector
def choose_song():
    screen.fill(WHITE)
    title = font.render("Choose a Song:", True, BLACK)
    screen.blit(title, (320, 50))

    songs = os.listdir("songs")
    buttons = []
    for idx, song in enumerate(songs):
        label = font.render(song.capitalize(), True, WHITE)
        rect = pygame.Rect(300, 120 + idx * 60, 200, 40)
        pygame.draw.rect(screen, BLUE, rect)
        screen.blit(label, (rect.x + 20, rect.y + 5))
        buttons.append((rect, song))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, name in buttons:
                    if rect.collidepoint(event.pos):
                        return name

# Typing game
def typing_game(song_path, lyrics_lines, line_timings):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    current_line = 0
    typed_text = ""
    score = 0
    start_time = time.time()

    running = True
    while running:
        screen.fill(WHITE)
        current_time = time.time() - start_time

        # Show current lyric
        if current_line < len(line_timings) and current_time >= line_timings[current_line]:
            lyric = lyrics_lines[current_line]
        else:
            lyric = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # Optional: skip line
                else:
                    typed_text += event.unicode

                # Check match
                if lyric and typed_text.strip().lower() == lyric.strip().lower():
                    score += len(lyric) * 10
                    typed_text = ""
                    current_line += 1

        # Draw lyrics and typed text
        lyric_surface = font.render("♪ " + lyric, True, BLACK)
        screen.blit(lyric_surface, (50, 100))

        color = GREEN if lyric.lower().startswith(typed_text.lower()) else RED
        typed_surface = font.render(typed_text, True, color)
        screen.blit(typed_surface, (50, 160))

        # Score
        score_surface = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (50, 20))

        pygame.display.flip()
        clock.tick(30)

# Run game
if __name__ == "__main__":
    selected_song = choose_song()
    song_path, lyrics, timings = load_song(selected_song)
    typing_game(song_path, lyrics, timings)
