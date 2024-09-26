class Duree:
    def __init__(self, h, m, s):
        """Instanciation
        Les minutes et secondes doivent être compris entre 0 et 59
        """
        assert 0 <= m < 60 and 0 <= s < 60
        self.heures = h
        self.minutes = m
        self.secondes = s

    def en_secondes(self):
        """Conversion en secondes"""
        return self.heures * 3600 + self.minutes * 60 + self.secondes

    def ajoute_minutes(self, mins):
        """Ajout de mins minutes"""
        self.heures += (self.minutes + mins) // 60
        self.minutes = (self.minutes + mins) % 60

    def ajoute_secondes(self, secs):
        """Ajout de secs minutes"""
        self.ajoute_minutes((self.secondes + secs) // 60)
        self.secondes = (self.secondes + secs) % 60

    def __repr__(self):
        """Mise en forme pour l'affichage"""
        return f"{self.heures}:{self.minutes}:{self.secondes}"

    def __eq__(self, autre):
        """Test d'égalité"""
        return self.en_secondes() == autre.en_secondes()

    def __le__(self, autre):
        """Teste si cet objet Duree est plus court ou égal que l'objet Duree autre"""
        return self.en_secondes() <= autre.en_secondes()

    def __add__(self, autre):
        """Addition de cette durée et de autre"""
        s = (self.secondes + autre.secondes)%60
        r = (self.secondes + autre.secondes)//60
        m = ((self.minutes + autre.minutes)+r)%60
        r = ((self.minutes + autre.minutes)+r)//60
        h = self.heures + autre.heures + r
        return Duree(h, m, s)

    def __sub__(self, autre):
        """Soustraction de autre à cette durée"""
        assert autre.en_secondes() < self.en_secondes()
        h = self.heures - autre.heures
        m = self.minutes - autre.minutes
        if m < 0:
            h -= 1
            m += 60
        s = self.secondes - autre.secondes
        if s < 0:
            s += 60
            m -= 1
        return Duree(h, m, s)

# Tests

duree_1 = Duree(2, 45, 52)
duree_2 = Duree(2, 45, 52)
duree_3 = Duree(5, 12, 26)
assert duree_1 == duree_2
assert not duree_1 == duree_3
assert duree_1 != duree_3
assert duree_1 <= duree_3
assert duree_1 + duree_3 == Duree(7, 58, 18)
assert duree_3 - duree_1 == Duree(2, 26, 34)
