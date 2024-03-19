import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define screen size
WIDTH = 500
HEIGHT = 500

# Define ball properties
radius = 25

def check_boundaries(x, y):
  """
  This function ensures the ball stays within screen boundaries.
  """
  return (
      max(0, min(x, WIDTH - radius)),  # Limit X between screen edges
      max(0, min(y, HEIGHT - radius))   # Limit Y between screen edges
  )

def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Moving Ball")
  clock = pygame.time.Clock()

  # Initial ball position (center)
  ball_x = WIDTH // 2
  ball_y = HEIGHT // 2

  # Movement speed
  movement_speed = 20

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Update ball position based on pressed keys
    if keys[pygame.K_LEFT]:
      ball_x -= movement_speed
    if keys[pygame.K_RIGHT]:
      ball_x += movement_speed
    if keys[pygame.K_UP]:
      ball_y -= movement_speed
    if keys[pygame.K_DOWN]:
      ball_y += movement_speed

    # Ensure ball stays within boundaries
    ball_x, ball_y = check_boundaries(ball_x, ball_y)

    # Fill screen with white
    screen.fill(WHITE)

    # Draw the red ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), radius)

    # Update the display
    pygame.display.flip()

    # Set frame rate (controls game speed)
    clock.tick(60)

  pygame.quit()

if __name__ == "__main__":
  main()
