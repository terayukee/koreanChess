from django.db import models

class Game(models.Model):
    game_id = models.CharField(max_length=32)
    
    cho_user_id = models.CharField(max_length=50, null=True)
    cho_position = models.CharField(max_length=20, null=True)
    han_user_id = models.CharField(max_length=50, null=True)
    han_position = models.CharField(max_length=20, null=True)
    
    cho_king = models.CharField(max_length=3, default='e2')
    cho_rook1 = models.CharField(max_length=3, default='a1')
    cho_rook2 = models.CharField(max_length=3, default='i1')
    cho_knight1 = models.CharField(max_length=3, default='b1')
    cho_knight2 = models.CharField(max_length=3, default='h1')
    cho_elephant1 = models.CharField(max_length=3, default='c1')
    cho_elephant2 = models.CharField(max_length=3, default='g1')
    cho_advisor1 = models.CharField(max_length=3, default='d1')
    cho_advisor2 = models.CharField(max_length=3, default='f1')
    cho_cannon1 = models.CharField(max_length=3, default='b3')
    cho_cannon2 = models.CharField(max_length=3, default='h3')
    cho_pawn1 = models.CharField(max_length=3, default='a4')
    cho_pawn2 = models.CharField(max_length=3, default='c4')
    cho_pawn3 = models.CharField(max_length=3, default='e4')
    cho_pawn4 = models.CharField(max_length=3, default='g4')
    cho_pawn5 = models.CharField(max_length=3, default='i4')
    
    han_king = models.CharField(max_length=3, default='e9')
    han_rook1 = models.CharField(max_length=3, default='a10')
    han_rook2 = models.CharField(max_length=3, default='i10')
    han_knight1 = models.CharField(max_length=3, default='c10')
    han_knight2 = models.CharField(max_length=3, default='g10')
    han_elephant1 = models.CharField(max_length=3, default='b10')
    han_elephant2 = models.CharField(max_length=3, default='h10')
    han_advisor1 = models.CharField(max_length=3, default='d10')
    han_advisor2 = models.CharField(max_length=3, default='f10')
    han_cannon1 = models.CharField(max_length=3, default='b8')
    han_cannon2 = models.CharField(max_length=3, default='h8')
    han_pawn1 = models.CharField(max_length=3, default='a7')
    han_pawn2 = models.CharField(max_length=3, default='c7')
    han_pawn3 = models.CharField(max_length=3, default='e7')
    han_pawn4 = models.CharField(max_length=3, default='g7')
    han_pawn5 = models.CharField(max_length=3, default='i7')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.cho_position == 'coupled_knight':
            self.cho_knight1 = 'b1'
            self.cho_knight2 = 'h1'
            self.cho_elephant1 = 'c1'
            self.cho_elephant2 = 'g1'
        elif self.cho_position == 'doubled_knight':
            self.cho_knight1 = 'c1'
            self.cho_knight2 = 'g1'
            self.cho_elephant1 = 'b1'
            self.cho_elephant2 = 'h1'
        elif self.cho_position == 'left_knight':
            self.cho_knight1 = 'c1'
            self.cho_knight2 = 'h1'
            self.cho_elephant1 = 'b1'
            self.cho_elephant2 = 'g1'
        elif self.cho_position == 'right_knight':
            self.cho_knight1 = 'b1'
            self.cho_knight2 = 'g1'
            self.cho_elephant1 = 'c1'
            self.cho_elephant2 = 'h1'
            
class Match(models.Model) :
    user_id = models.CharField(max_length=100)
    match_id = models.CharField(max_length=100)