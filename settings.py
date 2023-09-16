class Settings:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.unit = 20
        self.gameAreaX = [0, self.width]
        self.gameAreaY = [self.unit*2, self.height]
        self.gridX = [self.gameAreaX[0] // self.unit, self.gameAreaX[1] // self.unit]
        self.gridY = [self.gameAreaY[0] // self.unit, self.gameAreaY[1] // self.unit]

        # 设置分数
        self.score = 10

        # 设置速度
        self.speed = 200
        
        self.lineWidth = 1
        
        # 设置颜色
        self.bg = (40,40,60)
        self.BLACK = (0, 0, 0)
        self.LIGHT = (200, 200, 200)
        self.RED = (200, 30, 30)
        self.BLUE = (20, 20, 230)
        self.DARK = (50, 50, 50)
