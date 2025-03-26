# python -m venv .venv / para poder isolar as bibliotecas

# source .venv/bin/activate / para ativar o ambiente virtual

# python -m pygame.examples.aliens

#  o display no pygame é responsavel por controlar a janela (window) e a tela (Screen) de maneira geral 

# python -i game.py / abre o jogo e devolve  terminal 

# Display.set_mode((1280, 720)) / vai conseguir parar o terminal e editar a dimensão

# pygame.image / faz carregamento de imagen no disco / salva imagem no disco

# pygame.transform / executa operações em imagens (bitmap) / zoom, redimensionamento, rotação

# Bit Blit 
from random import randint
import pygame
from pygame import font
from pygame import display 
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event            
from pygame.locals import QUIT, KEYUP, K_SPACE 
from pygame.time import Clock

pygame.init()

tamanho = 1920, 1080
fonte = font.SysFont("comicsans", 50)

superficie = display.set_mode(
    size=tamanho, 
    display=0
    )

display.set_caption("brow")

fundo = scale (
   load('image/space.jpg'),
   tamanho
   )


class EliteCam(Sprite):
    def __init__(self, alexa):
        super().__init__()

        self.image = load('image/images.png')
        self.rect = self.image.get_rect()
        self.alexa = alexa
        self.velocidade = 7

    def tacar_alexa(self):
        

        if len(self.alexa) < 5:
         self.alexa.add(
            Alexa(*self.rect.center)
        )


    def update(self):
        
        keys=pygame.key.get_pressed()

        alexa_fonte = fonte.render(
            f'Alexa: {15 - len(self.alexa)}',
            True,
            (255, 255, 255)

        )
        superficie.blit(alexa_fonte, (20, 20))

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade

        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade
        
class Alexa(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('image/alexa.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    

    def update(self):
        self.rect.x += 10

        if self.rect.x > tamanho[0]:
            self.kill()


class Virus(Sprite):
    def __init__(self):
        super().__init__()

        self.image = load('image/ocpd.png')
        self.rect = self.image.get_rect(
            center=(800, randint(20, 1080))
       )

    def update(self):
        self.rect.x -= 1

        if self.rect.x == 0:
           self.kill()





 
grupo_inimigos = Group()
grupo_alexa = Group()
elitecam = EliteCam(grupo_alexa)
grupo_elite = GroupSingle(elitecam)


grupo_inimigos.add(Virus())


clock = Clock()
 
mortes = 0
round = 0



while True: #Segura a tela 
   #loop de eventos

   clock.tick(120) #FPS

   if round % 120 == 0:
       if mortes < 1000000:
           grupo_inimigos.add(Virus())
           for i in range(int(mortes / 20)):
              grupo_inimigos.add(Virus())

       print(mortes)    
           


  
   
   #Espaço dos eventos
   for evento in event.get(): #retorna lista de events. que é um objeto do pygame
       if evento.type == QUIT:
         pygame.quit()

       if evento.type == KEYUP:
         if evento.key == K_SPACE:
             elitecam.tacar_alexa()


    #Espaço de colisão
   if groupcollide(grupo_inimigos, grupo_alexa, True, False):
       mortes += 1


   



   #Espaço do display
   superficie.blit(fundo, (0, 0))  

   fonte_mortes = fonte.render(
            f'Mortes: {mortes}',
            True,
            (255, 255, 255) 
 
   )
   superficie.blit(fonte_mortes, (20, 70))

   grupo_elite.draw(superficie)
   grupo_inimigos.draw(superficie)
   grupo_alexa.draw(superficie)
   

   grupo_elite.update()
   grupo_inimigos.update()
   grupo_alexa.update()



   display.update()
   round += 1