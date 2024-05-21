import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 400
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Flappy Bird")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Carrega as imagens
background = pygame.image.load('assets/background.png')
bird_img = pygame.image.load('assets/bird.png')
pipe_top_img = pygame.image.load('assets/pipe_top.png')
pipe_bottom_img = pygame.image.load('assets/pipe_bottom.png')

# Ajusta as dimensões do pássaro
largura_passaro = bird_img.get_width()
altura_passaro = bird_img.get_height()

# Configurações do jogo
gravidade = 0.5
forca_pulo = -10
velocidade_cano = -3
espaco_cano = 150

font = pygame.font.SysFont(None, 35)
clock = pygame.time.Clock()

class Passaro:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.velocidade_y = 0
        self.image = bird_img

    def pular(self):
        self.velocidade_y = forca_pulo

    def mover(self):
        self.velocidade_y += gravidade
        self.y += self.velocidade_y

    def desenhar(self, tela):
        tela.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, largura_passaro, altura_passaro)

class Cano:
    def __init__(self, x):
        self.x = x
        self.altura_topo = random.randint(100, 400)
        self.altura_base = self.altura_topo + espaco_cano
        self.image_top = pipe_top_img
        self.image_bottom = pipe_bottom_img

    def mover(self):
        self.x += velocidade_cano
        if self.x < -largura_passaro:
            self.x = largura_tela
            self.altura_topo = random.randint(100, 400)
            self.altura_base = self.altura_topo + espaco_cano

    def desenhar(self, tela):
        tela.blit(self.image_top, (self.x, self.altura_topo - self.image_top.get_height()))
        tela.blit(self.image_bottom, (self.x, self.altura_base))

    def get_rects(self):
        return (
            pygame.Rect(self.x, self.altura_topo - self.image_top.get_height(), largura_passaro, self.image_top.get_height()),
            pygame.Rect(self.x, self.altura_base, largura_passaro, self.image_bottom.get_height())
        )

class Jogo:
    def __init__(self):
        self.passaro = Passaro()
        self.cano = Cano(largura_tela)
        self.score = 0

    def reiniciar(self):
        self.passaro = Passaro()
        self.cano = Cano(largura_tela)
        self.score = 0

    def desenhar_tela_inicial(self):
        tela.blit(background, (0, 0))
        titulo = font.render("Flappy Bird", True, PRETO)
        instrucoes = font.render("Pressione ESPAÇO para jogar", True, PRETO)
        tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, altura_tela // 3))
        tela.blit(instrucoes, (largura_tela // 2 - instrucoes.get_width() // 2, altura_tela // 2))
        pygame.display.update()

    def desenhar_tela_fim(self):
        tela.blit(background, (0, 0))
        game_over = font.render("Fim de Jogo", True, PRETO)
        pontuacao_final = font.render(f"Pontuação: {self.score}", True, PRETO)
        instrucoes = font.render("Pressione ESPAÇO para jogar novamente", True, PRETO)
        tela.blit(game_over, (largura_tela // 2 - game_over.get_width() // 2, altura_tela // 3))
        tela.blit(pontuacao_final, (largura_tela // 2 - pontuacao_final.get_width() // 2, altura_tela // 2))
        tela.blit(instrucoes, (largura_tela // 2 - instrucoes.get_width() // 2, altura_tela // 2 + 50))
        pygame.display.update()

    def desenhar_jogo(self):
        tela.blit(background, (0, 0))
        self.passaro.desenhar(tela)
        self.cano.desenhar(tela)
        texto_pontuacao = font.render(f"Pontuação: {self.score}", True, PRETO)
        tela.blit(texto_pontuacao, (10, 10))
        pygame.display.update()

    def verificar_colisao(self):
        passaro_rect = self.passaro.get_rect()
        cano_top_rect, cano_bottom_rect = self.cano.get_rects()

        if passaro_rect.colliderect(cano_top_rect) or passaro_rect.colliderect(cano_bottom_rect):
            return True
        if self.passaro.y < 0 or self.passaro.y + altura_passaro > altura_tela:
            return True
        return False

    def atualizar(self):
        self.passaro.mover()
        self.cano.mover()
        if self.cano.x < self.passaro.x and not hasattr(self, 'contado'):
            self.score += 1
            self.contado = True
        if self.cano.x >= self.passaro.x:
            self.contado = False

def espera_tecla():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False

def main():
    jogo = Jogo()
    jogo.desenhar_tela_inicial()
    espera_tecla()
    while True:
        jogo.reiniciar()
        jogando = True
        while jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogando = False
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        jogo.passaro.pular()
            jogo.atualizar()
            jogo.desenhar_jogo()
            if jogo.verificar_colisao():
                jogando = False
        jogo.desenhar_tela_fim()
        espera_tecla()

if __name__ == "__main__":
    main()
