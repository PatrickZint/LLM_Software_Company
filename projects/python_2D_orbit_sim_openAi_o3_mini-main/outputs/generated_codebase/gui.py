import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_r, K_e, K_k
from config import Config

class GUI:
    """Handles the graphical interface, rendering, and user interactions using Pygame."""

    def __init__(self, simulation):
        pygame.init()
        self.simulation = simulation
        self.width = Config.WINDOW_WIDTH
        self.height = Config.WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Two-Body Orbital Simulator')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 14)
        
    def draw(self):
        # Clear screen
        self.screen.fill(Config.BG_COLOR)
        
        # Get current simulation state
        bodies = self.simulation.get_state()
        
        for body in bodies:
            # Convert simulation coordinates to screen coordinates
            pos = body['pos'] * Config.SCALE
            x = int(pos[0] + self.width/2)
            y = int(pos[1] + self.height/2)
            
            # Draw the body (circle)
            pygame.draw.circle(self.screen, Config.BODY_COLOR, (x, y), 5)
            
            # Draw trail
            trail = body.get('trail', [])
            if len(trail) > 1:
                pts = [ (int(p[0]*Config.SCALE + self.width/2), int(p[1]*Config.SCALE + self.height/2)) for p in trail ]
                pygame.draw.lines(self.screen, Config.TRAIL_COLOR, False, pts, 2)

        # Render simulation time
        time_text = self.font.render(f"Time: {self.simulation.get_time():.2f} s", True, Config.TEXT_COLOR)
        self.screen.blit(time_text, (10, 10))
        
        # Render integration method
        method_text = self.font.render(f"Integration: {self.simulation.engine.integration_method}", True, Config.TEXT_COLOR)
        self.screen.blit(method_text, (10, 30))

        pygame.display.flip()

    def handle_events(self):
        """Handle user inputs: start/pause, reset, and switch integration methods."""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Toggle pause/resume
                    if self.simulation.is_paused:
                        self.simulation.resume()
                    else:
                        self.simulation.pause()
                if event.key == K_r:
                    self.simulation.reset()
                if event.key == K_e:
                    # Switch to Euler integration
                    self.simulation.engine.set_integration_method('euler')
                if event.key == K_k:
                    # Switch to Runge-Kutta 4 integration
                    self.simulation.engine.set_integration_method('rk4')
        return True

    def run(self):
        """Main GUI loop."""
        running = True
        while running:
            running = self.handle_events()
            self.draw()

            # Ensure at least 30 frames per second
            self.clock.tick(30)
        pygame.quit()
