import pygame


class SimulationWindow:
    def __init__(self, window_size):
        self.width, self.height = window_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('N-Body Simulation')
        self.font = pygame.font.SysFont('Arial', 14)

    def render(self, state):
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Render each celestial body
        for body_id, body in state.items():
            x, y = int(body['position'][0]), int(body['position'][1])
            # Scale radius by mass (simple approach)
            radius = max(2, int(body['mass'] ** 0.33))
            color = (255, 255, 255)  # white
            pygame.draw.circle(self.screen, color, (x, y), radius)

        # Optionally, display extra info (e.g., FPS, instructions) here
        info_text = self.font.render('Press SPACE to start/pause, ESC to quit', True, (200, 200, 200))
        self.screen.blit(info_text, (10, 10))

    def handle_events(self, controller):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controller.stop()
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    controller.stop()
                    pygame.quit()
                    exit(0)
                elif event.key == pygame.K_SPACE:
                    if controller.is_running():
                        controller.pause()
                    else:
                        controller.resume()
                # Additional key events for zoom, pan or adding bodies could be added here
