import PySimpleGUI as sg
import random
from PIL import Image
import io

class Enemy():
    def __init__(self, path):
        self.health = 4
        self.path = path
        self.armed = None
        self.block_tedency = 4
        self.block = None;

class Player():
    def __init__(self):
        self.health = 4
        self.armed = None
        self.block = None
        self.score = 0

class GameScreen():
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy("out.gif")
        sg.theme('Black')
        self.col1 = [[sg.Image(key = "-IMAGE-")], [sg.Button('  ', disabled = True, key ="-nextenemy-")]]
        self.col2 = [
            self.healthBar("EN",self.enemy.health),#0
            [sg.Text("Enemy Action", key = '-enemyevent-')],
            [sg.Text("Welcome to the game!", key = '-outcome-')],
            [sg.Text("Your Action", key = '-playerevent-')],
            [sg.Text('Score: ' + str(self.player.score), key = '-score-')],
            self.healthBar("US",self.player.health),#5
            [sg.Button("Reload", key = '-action-')],
            [sg.Button('Block', key = '-block-')]
        ]
        self.layout = [[sg.Column(self.col1)], [sg.Column(self.col2)]]
        self.window = sg.Window('Window Title', self.layout, finalize = True)
        self.loop()

    def healthBar(self, character, health):
        data = []
        for i in range(4):
            if i < health:
                data.append(sg.Image(character+"_FULL.png"))
            else:
                data.append(sg.Image(character+"_EMPTY.png"))
        return data

    def loop(self):
        event, values = self.window.read(timeout = 100)
        self.window.Element('-IMAGE-').update_animation_no_buffering(self.enemy.path)
        if event == sg.WIN_CLOSED:
            self.window.close()
        else:
            if self.player.armed == None:
                self.player.armed = False
                self.enemy.armed = False
                self.enemy.block = False
            self.contest(event)
            self.loop()

    def playerAction(self, event):
        if event == '-action-':
            self.player.block = False
            if self.player.armed == False:
                self.window['-action-'].Update("Attack")
                self.window['-playerevent-'].Update("You reloaded!")
                self.player.armed = True
                self.enemyAction()
            elif self.player.armed == True:
                self.window['-action-'].Update("Reload")
                self.window['-playerevent-'].Update("You attacked!")
                self.player.armed = False
                self.enemyAction()
        elif event == '-block-':
            self.player.block = True
            self.window['-playerevent-'].Update("You blocked!")
            self.enemyAction()

    def enemyAction(self):
        action = random.randrange(1,self.enemy.block_tedency+1)
        if action == self.enemy.block_tedency:
            self.window['-enemyevent-'].Update("Enemy blocked!")
            self.enemy.block = True
        else:
            self.enemy.block = False
            if self.enemy.armed == False:
                self.window['-enemyevent-'].Update("Enemy reloaded!")
                self.enemy.armed = True
            else:
                self.window['-enemyevent-'].Update("Enemy attacked!")
                self.enemy.armed = False

    def getHit(self):
        if (self.player.health - 1) == 0:
            self.player.score -= 50
            self.window['-outcome-'].Update("You lose! Game Over -50\nFinal Score:" + str(self.player.score))
            self.window['-score-'].Update("Score: " + str(self.player.score))
            self.window['-nextenemy-'].Update("Play again?")
            self.window['-action-'].Update(disabled = True)
            self.window['-block-'].Update(disabled = True)
            self.player.armed = None
            self.player.block = None
            self.enemy.armed = None
            self.enemy.block = None
        else:
            self.player.health -= 1
            self.player.score -= 10
            self.window['-score-'].Update("Score: " + str(self.player.score))
            self.col2[5] = self.healthBar("US",self.player.health)

    def hit(self):
        if (self.enemy.health - 1) == 0:
            self.player.score += 20
            self.window['-outcome-'].Update("You won! +20\nCurrent score: " + str(self.player.score))
            self.window['-nextenemy-'].Update(disabled = False)
            self.window['-nextenemy-'].Update("Next enemy?")
            self.window['-action-'].Update(disabled = True)
            self.window['-block-'].Update(disabled = True)
            self.window['-score-'].Update("Score: " + str(self.player.score))
            self.player.armed = None
            self.player.block = None
            self.enemy.armed = None
            self.enemy.block = None
        else:
            self.enemy.health -= 1
            self.player.score += 10
            self.window['-score-'].Update("Score: " + str(self.player.score))
            self.col2[0] = self.healthBar("EN",self.enemy.health)


    def contest(self, event):
        self.playerAction(event)
        if self.enemy.block == True and self.player.block == True: #both players block
            self.window['-outcome-'].Update("Both of you blocked!")
        elif self.enemy.block == True and self.player.block == False: #enemy blocks, player does not
            if self.player.armed == False: #player can't shoot
                self.window['-outcome-'].Update("Enemy blocked the attack!")#must reload if not
            else:#player can shoot
                self.window['-outcome-'].Update("Nothing happened!")#enemy is blocking
        elif self.enemy.block == False and self.player.block == True: #enemy does not block, player does
            if self.enemy.armed == False: #enemy can't shoot
                self.window['-outcome-'].Update("You blocked the attack!") #enemy reloads
            else: #enemy can shoot
                self.window['-outcome-'].Update("Nothing happened!") #player is blocking
        elif self.enemy.block == False and self.player.block == False: #neither block
            if self.enemy.armed == False and self.player.armed == True: #enemy is unarmed, player is armed
                self.window['-outcome-'].Update("You are hit!") #enemy is hit
                self.getHit()
            elif self.enemy.armed == True and self.player.armed == False:
                self.window['-outcome-'].Update("Enemy is hit!")
                self.hit()
            elif self.enemy.armed == True and self.player.armed == True:
                self.window['-outcome-'].Update("Both of you reloaded!")
            elif self.enemy.armed == False and self.player.armed == False: #both are reloading
                self.window['-outcome-'].Update("Both of you are hit!")
            else:
                self.window['-outcome-'].Update("")




g = GameScreen()
