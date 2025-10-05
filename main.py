import pygame
import asyncio
import random

# เริ่มต้น pygame
pygame.init()

# ตั้งค่าหน้าจอ
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("เกมงู Snake")

# สี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# ตัวแปรเกม
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        dx, dy = new_direction
        # ป้องกันไม่ให้งูถอยหลัง
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction
    
    def check_collision(self):
        head = self.body[0]
        # ชนกำแพง
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # ชนตัวเอง
        if head in self.body[1:]:
            return True
        return False
    
    def eat(self):
        self.grow = True

class Food:
    def __init__(self):
        self.position = self.randomize()
    
    def randomize(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)
    
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*self.position, GRID_SIZE, GRID_SIZE))

# ฟังก์ชันวาดงู
def draw_snake(surface, snake):
    for i, segment in enumerate(snake.body):
        color = GREEN if i == 0 else BLUE  # หัวงูเป็นสีเขียว
        pygame.draw.rect(surface, color, (*segment, GRID_SIZE, GRID_SIZE))

# ฟังก์ชันแสดงคะแนน
def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (10, 10))

# ฟังก์ชันแสดงหน้า Game Over
def draw_game_over(surface, score):
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    text1 = font_large.render("GAME OVER", True, RED)
    text2 = font_small.render(f"Score: {score}", True, WHITE)
    text3 = font_small.render("Press SPACE to restart", True, WHITE)
    
    surface.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 60))
    surface.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
    surface.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 40))

# ฟังก์ชันหลัก
async def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # รีสตาร์ทเกม
                        snake = Snake()
                        food = Food()
                        score = 0
                        game_over = False
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction((0, -GRID_SIZE))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction((0, GRID_SIZE))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction((-GRID_SIZE, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction((GRID_SIZE, 0))
        
        if not game_over:
            # อัพเดทเกม
            snake.move()
            
            # เช็คว่ากินอาหาร
            if snake.body[0] == food.position:
                snake.eat()
                food.position = food.randomize()
                score += 10
            
            # เช็คชน
            if snake.check_collision():
                game_over = True
        
        # วาดทุกอย่าง
        screen.fill(BLACK)
        
        if not game_over:
            draw_snake(screen, snake)
            food.draw(screen)
            draw_score(screen, score)
        else:
            draw_game_over(screen, score)
        
        pygame.display.flip()
        clock.tick(10)  # ความเร็วเกม
        await asyncio.sleep(0)  # สำคัญสำหรับ pygbag
    
    pygame.quit()

# รันเกม
if __name__ == "__main__":
    asyncio.run(main())