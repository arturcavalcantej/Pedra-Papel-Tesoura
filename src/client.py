import pygame
from network import Network
import pickle
import logging

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename='client.log',
                    # w -> sobrescreve o arquivo a cada log
                    # a -> não sobrescreve o arquivo
                    filemode='w',
                    level=logging.DEBUG,
                    format=log_format)
logger = logging.getLogger('root')


pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cliente")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), border_radius = 15)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Aguardando oponente...", 1, (0,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Você:", 1, (0, 0, 0))
        win.blit(text, (80, 300))

        text = font.render("Oponente:", 1, (0, 0, 0))
        win.blit(text, (80, 350))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Jogou", 1, (0, 0, 0))
            else:
                text1 = font.render("Esperando...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Jogou", 1, (0, 0, 0))
            else:
                text2 = font.render("Esperando...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (200, 300))
            win.blit(text1, (290, 350))
        else:
            win.blit(text1, (200, 300))
            win.blit(text2, (290, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("PEDRA", 50, 500, (0,0,0)), Button("TESOURA", 250, 500, (0,0,0)), Button("PAPEL", 450, 500, (0,0,0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("Você é o jogador", player)
    logger.info(f'Jogador {player} entrou.')

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 120)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Vitória!", 1, (0,255,0))
            elif game.winner() == -1:
                text = font.render("Empate!", 1, (0,0,255))
            else:
                text = font.render("Você perdeu...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, 150))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((200, 200, 200))
        font = pygame.font.SysFont(None, 75)
        font2 = pygame.font.SysFont(None, 34)
        text = pygame.image.load("media/4144475.png").convert_alpha()
        text2 = font.render("Pedra, Papel e Tesoura!", 1, (10,10,0))
        text3 = font2.render("REDES - Guilherme Monteiro e Artur Cavalcante", 1, (10,10,0))
        win.blit(text, (100,200))
        win.blit(text2, (60,50))
        win.blit(text3, (75,120))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()