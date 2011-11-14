
from math import pi, sin, cos
import time
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from pandac.PandaModules import CollisionTraverser, CollisionHandlerEvent
from pandac.PandaModules import CollisionNode, CollisionSphere
import random

from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Vec3

E1posX= 0
E1posY= -100
E1posZ= 3
time = 120
CposX= 0
CposY= -120
CposZ= 7

S1x=30
S1y=30
S1z=3

S2x=-30
S2y= 40
S2z= 3

T1x= -10
T1y= 17
T1z= 3

n=1
x=-8
y=42
z=0
adj=1
adj2=1
gameover=6
score=0
slowadj=0
speed=0

class MyApp(ShowBase):
              
        

    def cleanUpStartScreen( self ):       
        self.startButton.destroy( ) # get rid of the button       
        self.logoModel.detachNode( ) # detach the logo model from the render        
        self.loadGame( ) # load the actual game       
        # end cleanUpStartScreen


    def addInstructions(pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1,1,1,1),pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)
        
    def __init__(self):
	global x,y,z
	#self.loadStartScreen()
        ShowBase.__init__(self)

	#self.setupBackgroundColor(1,1,1)       
        # set the camera position       
        #camera.setPosHpr( Vec3( 0, -10, 0 ), Vec3( 0, 0, 0 ) )       
        # load our logo model       
        self.logoModel = loader.loadModel("bvw-f2004--truck/cartruck.egg")
        self.logoModel.reparentTo( render )       
        # set the logo model's position       
        self.logoModel.setPosHpr( Vec3( 0, 15, 0 ), Vec3( 0, 0, 0 ) )       
        # create and display a start button       
        self.startButton = DirectButton( text = "Go!", relief = DGG.RAISED, scale = .1, pad = ( .5, .5 ), pos = Vec3( 1.0, 0.0, -0.8 ), command = self.cleanUpStartScreen )
	self.disableMouse()
	self.obs = [None] * 100
	self.keyMap = {"forward":0, "slow":0, "left":0, "right":0}

	#self.environ = [None]*100
	self.grb= [None] * 100
	self.env= [None] * 20
	self.env1= [None] * 20
	self.envx= [None] * 20
	self.envy= [None] * 20

	self.title = OnscreenText(text="SCORE: " + str(score), style=1, fg=(1,1,0,1), pos=(-0.95,0.85), scale = .07, mayChange = True)
        self.title1 = OnscreenText(text="LIVES: " + str(int (gameover/2)), style=1, fg=(1,1,0,1), pos=(-0.95,0.7), scale = .07, mayChange = True)
        self.timeleft = OnscreenText(text="TIME LEFT: " + str(int(time/60)) + " : " + str(int(time%60)), style=1, fg=(1,1,0,1), pos=(-0.95,0.55), scale = .07, mayChange = True)
        
	self.model= self.loader.loadModel("alice-farm--cornfield/cornfield.egg")
	self.model.reparentTo(self.render)
	self.model.setPos(-8, 42, 0)
	self.model.setScale(20,1000,20)

        # Reparent the model to render.
	self.environ2 = self.loader.loadModel("bvw-f2004--building/building.egg")
	self.environ2.reparentTo(self.render)
	self.environ2.setPos(S1x, S1y, S1z)
	self.environ2.setScale(0.2, 0.2, 0.2)
	
	for i in range(0,100):
                        self.obs[i]= self.loader.loadModel("alice-objects--anvil/anvil.egg")
                        self.obs[i].reparentTo(self.render)
                        self.obs[i].setX(random.choice([0, 10]))
                        self.obs[i].setY(random.randint(100,100000))
                        self.obs[i].setZ(3)
                        self.obs[i].setScale(10,20,10)

	for j in range(0,100):
			self.grb[j]= self.loader.loadModel("alice-shapes--icosahedron/icosahedron.egg")
			self.grb[j].reparentTo(self.render)
			self.grb[j].setX(random.choice([0, 10]))
			self.grb[j].setY(random.randint(100, 100000))
			self.grb[j].setZ(3)
			self.grb[j].setScale(0.8,3,0.8)

        for k in range(0,20):
                self.envx[k]= self.loader.loadModel("bvw-f2004--building/building.egg")
                self.envx[k].reparentTo(self.render)
                self.envx[k].setX(random.choice([-60, 60]))
                self.envx[k].setY(random.randint(13000, 35000))
                self.envx[k].setZ(0)
                self.envx[k].setScale(0.8, 0.8, 0.8)

        for k in range(0,20):
                self.envy[k]= self.loader.loadModel("bvw-f2004--russianbuilding/tetris-building.egg")
                self.envy[k].reparentTo(self.render)
                self.envy[k].setX(random.choice([-100, 100]))
                self.envy[k].setY(random.randint(38000, 60000))
                self.envy[k].setZ(0)
                self.envy[k].setScale(0.8, 0.8, 0.8)

	self.environ4 = self.loader.loadModel("alice-city--townhouse1/townhouse1.egg")
	self.environ4.reparentTo(self.render)
	self.environ4.setPos(T1x, T1y, T1z)
	self.environ4.setScale(0.6, 0.6, 0.6)

	self.BS = self.loader.loadModel("alice-skies--bluesky/bluesky.egg")
        self.BS.reparentTo(self.render)
        self.BS.setScale(10,10,10)
        self.BS.setPos(-180,0,0)

        self.barn= self.loader.loadModel("alice-farm--farmhouse/farmhouse.egg")
        self.barn.reparentTo(self.render)
        self.barn.setScale(0.5, 0.5, 0.5)
        self.barn.setPos(30,500,0)

        self.barn1= self.loader.loadModel("alice-beach--beachhouse2/beachhouse2.egg")
        self.barn1.reparentTo(self.render)
        self.barn1.setScale(0.5, 0.5, 0.5)
        self.barn1.setPos(40,200,0)

        self.barn2= self.loader.loadModel("alice-beach--beachhouse2/beachhouse2.egg")
        self.barn2.reparentTo(self.render)
        self.barn2.setScale(0.5,0.5,0.5)
        self.barn2.setPos(70,1700,0)

        self.barn3= self.loader.loadModel("bvw-f2004--russianbuilding/tetris-building.egg")
        self.barn3.reparentTo(self.render)
        self.barn3.setScale(0.5,0.5,0.5)
        self.barn3.setPos(-90,1500,0)


        self.barn5= self.loader.loadModel("bvw-f2004--course1/course1.egg")
        self.barn5.reparentTo(self.render)
        self.barn5.setScale(0.25, 0.25, 0.25)
        self.barn5.setPos(-100,900,0)

        

	
        # Apply scale and position transforms on the model.
        self.environ1= self.loader.loadModel("alice-vehicles--zamboni/zamboni.egg")
        self.environ1.reparentTo(self.render)
        self.environ1.setPos(E1posX, E1posY, E1posZ)
        self.environ1.setScale(0.3, 0.3, 0.3)
	print E1posY

    def loadGame(self):

	self.camera.setPos(CposX, CposY, CposZ)
	self.camera.setHpr(0,0,0)

	#for j in range(0, 100):

                #self.environ[j] = self.loader.loadModel("CityTerrain/CityTerrain")
                #self.environ[j].reparentTo(self.render)
                #self.environ[j].setPos(-8,42 + 210*j,0)
                #self.environ[j].setScale(0.25,0.25,0.25)


	self.accept("arrow_up-repeat", self.setKey, ["forward", 1])
	self.accept("arrow_down-repeat", self.setKey, ["slow", 1])
	self.accept("arrow_left", self.setKey, ["left", 1])
	self.accept("arrow_right", self.setKey, ["right", 1])

	base.cTrav = CollisionTraverser()
	
	self.collHandEvent = CollisionHandlerEvent()
	self.collCount=0
        self.collHandEvent.addInPattern('into-%in')
        self.collHandEvent.addOutPattern('outof-%in')
	sColl = self.initCollisionSphere(self.environ1, True)
	base.cTrav.addCollider(sColl[0], self.collHandEvent)

	for child in render.getChildren():	
		if child != camera  and child != self.environ2 and child!= self.environ4 and child != self.BS and child!= self.model and child!= self.barn and child!= self.barn1 and child!= self.barn2 and child!= self.barn3 and child!= self.barn5:
			#print child
			tColl = self.initCollisionSphere(child, True)
			base.cTrav.addCollider(tColl[0], self.collHandEvent)
			self.accept('into-' + tColl[1] , self.collide)
			
			

##        for m in range(0,100):
##                tgrb= self.initCollisionSphere(self.grb[i], True)
##                base.cTrav.addCollider(tgrb[0], self.collHandEvent)
##                self.accept('into-' + tgrb[1], self.collide)
##
##        for n in range(0,100):
##                tobs= self.initCollisionSphere(self.obs[i], True)
##                base.cTrav.addCollider(tobs[0], self.collHandEvent)
##                self.accept('into-' + tobs[1], self.collide)
			
               
	self.taskMgr.add(self.move, "moveTask")
	

    def initCollisionSphere(self, obj,show=False):
        # Get the size of the object for the collision sphere.
        bounds = obj.getChild(0).getBounds()
        center = bounds.getCenter()
        radius = bounds.getRadius() *0.5
 
        # Create a collison sphere
        collSphereStr = 'CollisionHull' + str(self.collCount) + "_" + obj.getName()
        self.collCount += 1
        cNode = CollisionNode(collSphereStr)
        cNode.addSolid(CollisionSphere(center, radius))
 
        cNodepath = obj.attachNewNode(cNode)
	#cNodepath.show()
        
 
        # Return a tuple with the collision node and its corrsponding string so
        # that the bitmask can be set.
        return (cNodepath, collSphereStr)

    def collide(self, collEntry):
        global score,E1posY,gameover,adj, CposY
        if self.environ1.getY()==-100:
            return
        if(collEntry.getIntoNodePath().getParent().getName()== "icosahedron.egg"):
            #print collEntry.getIntoNodePath().getParent().getName() 
            collEntry.getIntoNodePath().getParent().remove()
            score= score +10
            print score
            self.title.detachNode()
            self.title = OnscreenText(text="SCORE: " + str(score), style=1, fg=(1,1,0,1), pos=(-0.95,0.85), scale = .07, mayChange = True)

        elif(collEntry.getIntoNodePath().getParent().getName()== "anvil.egg"):
                E1posY= E1posY-50
                CposY= CposY-50
                self.camera.setPos(CposX, CposY, CposZ)
                self.environ1.setPos(E1posX, E1posY, E1posZ)
                gameover= gameover - 1
                self.title1.detachNode()
                self.title1= OnscreenText(text="LIVES: " + str(int(gameover/2)), style=1, fg=(1,1,0,1), pos=(-0.95, 0.7), scale = .07, mayChange = True)
                print gameover
                if(gameover<=0):
                    print "Game Over"
##                    time2= int(time-(task.time*0.5))
##                    if time1!=time2:
##                    self.inst2.detachNode()
##                    self.inst2 = addInstructions(0.89, "Time: "+str(time2))   
##                    time1=time2
##                    if time2==0:
                    OnscreenText(text= "GAME OVER", style=1, fg=(1,1,1,1),pos=(-0.9,0), align=TextNode.ALeft, scale = 0.35)
                    OnscreenText(text= "Your Final Score is " + str(score), style=1, fg=(1,1,0,1), pos=(-0.95, -0.05), align=TextNode.ALeft, scale=0.015)
                    #time.sleep(10)
                    #sys.exit
                    self.environ1.detachNode()
                    self.camera.detachNode()

    def setKey(self, key, value):
	self.keyMap[key]= value

    def move(self, task):
	global E1posX, E1posY, E1posY, CposX, CposY, CposZ, S1y, S2y, T1y, n, y,speed, time
	self.over=0
	ts= int(task.time)
	time= 120 -ts
	print time,ts
	self.timeleft.detachNode()
	self.timeleft=  OnscreenText(text="TIME LEFT: " + str(int(time/60)) + " : " + str(int(time%60)), style=1, fg=(1,1,0,1), pos=(-0.95,0.55), scale = .07, mayChange = True)
	if(time<=0):
                    time=0
                    OnscreenText(text= "GAME OVER", style=1, fg=(1,1,1,1),pos=(-0.9,0), align=TextNode.ALeft, scale = 0.35)
                    OnscreenText(text= "Your Final Score is " + str(score), style=1,fg=(1,1,0,1), pos=(-0.95, -0.05), align=TextNode.ALeft, scale=0.02)
                    #time.sleep(10)
                    #sys.exit
                    self.environ1.detachNode()
                    self.over=1
            
	if(self.keyMap["forward"]==1):
		self.keyMap["forward"]=0
		speed= 10
		if speed>=10:
                    speed= 20
                elif speed>=20:
                    speed= 30
		dist= speed
		print dist
		E1posY= E1posY + dist
		CposY= CposY + dist
		S1y= S1y + dist
		S2y= S2y + dist
		T1y= T1y + dist
		y= y+ dist
		self.environ1.setPos(E1posX, E1posY, E1posZ)
		self.camera.setPos(CposX, CposY, CposZ)
		if(E1posY==7500 * n or E1posY== 7500 *n +20):
			n= n+1
			self.environ4.setPos(T1x, T1y, T1z)
			#self.environ3.setPos(S2x, S2y, S2z)
			self.environ2.setPos(S1x, S1y, S1z)
			self.model.setPos(x,y + 550,z)
			
		print E1posX, E1posY, E1posZ, CposX, CposY, CposZ, x, y, z

	elif(self.keyMap["slow"]==1):
                global slowadj
                self.keyMap["slow"]=0
                if slowadj<100:
                    slowadj+= slowadj
                    speed= speed-10
                    if speed<0:
                        speed=0
                elif slowadj<200:
                    slowadj+= slowadj
                    speed= speed-10
                    if speed<0:
                        speed=0

                elif slowadj<300:
                    slowadj+= slowadj
                    speed= speed-10
                    if speed<0:
                        speed=0

                elif slowadj>=300:
                        speed=0

                print speed    
		E1posY= E1posY + speed
                CposY= CposY + speed
		S1y= S1y + speed
		S2y= S2y + speed
		T1y= T1y + speed
		y= y + speed
                self.environ1.setPos(E1posX, E1posY, E1posZ)
                self.camera.setPos(CposX, CposY, CposZ)
		if(E1posY>=7700 * n and E1posY<= 7700 *n + 30):
			n= n+1
			self.environ4.setPos(T1x, T1y, T1z)
			self.environ3.setPos(S2x, S2y, S2z)
			self.environ2.setPos(S1x, S1y, S1z)
			self.model.setPos(x,y + 550,z)

		print E1posX, E1posY, E1posZ, CposX, CposY, CposZ

	elif(self.keyMap["left"]==1):
                self.keyMap["left"]=0
		if(E1posX!=0):
			E1posX=0
			CposX=0

                self.environ1.setPos(E1posX, E1posY, E1posZ)
                self.camera.setPos(CposX, CposY, CposZ)

	elif(self.keyMap["right"]==1):
		self.keyMap["right"]=0
		if(E1posX!=10):
			E1posX=10
			CposX=10

		self.environ1.setPos(E1posX, E1posY, E1posZ)
		self.camera.setPos(CposX, CposY, CposZ)

        elif(self.keyMap["forward"]==0):
                if(self.over==1):
                    CposY= CposY
                elif(self.over==0):
                
                    print E1posY, CposY, speed
                    E1posY= E1posY + speed
                    CposY= CposY + speed
                    S1y= S1y + speed
                    S2y= S2y + speed
                    T1y= T1y + speed
                    y= y + speed
                    self.environ1.setPos(E1posX, E1posY, E1posZ)
                    self.camera.setPos(CposX, CposY, CposZ)
                    if(E1posY>=7500 * n and E1posY<= 7500 *n + 30):
                            n= n+1
                            self.environ4.setPos(T1x, T1y, T1z)
                            #self.environ3.setPos(S2x, S2y, S2z)
                            self.environ2.setPos(S1x, S1y, S1z)
                            self.model.setPos(x,y + 550,z)
	
	return Task.cont 
	
app = MyApp()
app.run()

