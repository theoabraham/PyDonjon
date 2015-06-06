import random

class Donjon():
    def __init__(self):
        print("l'aventure a commencé")
        self.joueur = Aventurier()
        self.tours = 0
        self.tour()

    def tour(self):
        choix = None
        while choix!='s':
            self.tours+=1
            print("Tour #",self.tours)
            self.joueur.whois()
            print("\t(e)ntrer dans une piece")
            print("\tse (r)eposer")
            print("\tse s(o)igner")
            print("\t(m)anger")
            print("\t(i)nventaire")
            print("\t(s)ortir du donjon")
            choix = input("Que voulez vous faire?")
            if choix=='r':
                self.joueur.repos()
            if choix=='o':
                self.joueur.soigner()
            if choix=='m':
                self.joueur.manger()
            if choix=="i":
                self.joueur.inventaire()
            if choix=='e':
                piece=Piece()
                resolution = piece.remplirPiece(self.joueur)
                if resolution=='mort':
                    self.mort()
                    break
        self.fin()
        return(None)

    def fin(self):
        print("La partie se termine apres",self.tours,"tours")
        self.joueur.inventaire()
        if "pieces d'or" in self.joueur.sac.keys():
            print("vous avez",self.joueur.sac["pieces d'or"],"pieces d'or")
        return(None)

    def mort(self):
        print("Voues etes mort mais vous ferez mieux la prochaine fois")
        return(None)


class Piece():
    def __init__(self):
        print('Vous entrez dans une piece...')
        return(None)

    def remplirPiece(self,joueur):
        # chaque piece a 1 chance sur 10 de contenir un monstre
        # et une chance sur 10 de contenir un tresor
        self.monstre = None
        self.tresor = None
        resolution = "victoire"
        # est-ce qu'il y a un tresor?
        if random.randint(1,10)<5:
            self.tresor = {"pieces d'or":random.randint(10,100)}
        if random.randint(1,10)>=5:
            if random.randint(1,3)>1:
                self.monstre = Gobelin()
            else:
                self.monstre = Elfe()
        if not self.monstre is None:
            print("IL Y A UN MONSTRE LA DEDANS!!")
            self.monstre.whois()
            resolution = baston(joueur,self.monstre)
        if resolution=='victoire':
            if not self.tresor is None:
                print("vous avez trouve:")
                for objet,n in self.tresor.items():
                      print(n,objet)
                joueur.sac.update(self.tresor)
            else:
                print("La piece est vide...")
        return(resolution)

class Personnage:
    def __init__(self):
        self.vie = 10
        self.endurance = 10
        self.taco = 10
        self.ac = 0
        self.sac = {}
        self.armes = {}
        self.armures = {}

    def whois(self):
        if self.vie<=2:
            etat2 = "boitillant"
        else:
            etat2 = "en pleine forme"
        if self.endurance <= 5:
            etat1 = "fatigué"
        else:
            etat1 = "fringant"
        print(self.nom,", ",self.classe,", a l'air ",etat1," et ",etat2,sep="")
        return(None)
    
    def inventaire(self):
        print('votre sac contient:')
        for objet in self.sac.keys():
            print('\t',self.sac[objet],objet)
        if len(self.armes)>0:
            print("vous tenez:")
            for arme in self.armes:
                print("\t",arme," (degats 1-",self.armes[arme]," pv)",sep='')
        if len(self.armures)>0:
            print("vous portez:")
            for armure in self.armures:
                print("\t",armure," (ac ",self.armures[armure],")",sep='')
##        print('maintenant rangez tout!')
        return(None)

    def pose(self,quoi):
        if quoi in self.sac.keys():
            self.sac[quoi]-=1
            if self.sac[quoi]==0:
                del self.sac[quoi]
                print("vous n'avez plus de",quoi)
            else:
                print("il vous reste",self.sac[quoi])
        else:
            print("vous n'avez pas de",quoi,"dans votre sac")
        return(None)

    def manger(self):
        if 'rations' in self.sac.keys():
            if self.sac['rations']>0:
                print('miam')
                self.sac['rations']-=1
        else:
            print("vous n'avez plus de rations")
        return(None)

    def soigner(self):
        if 'potions' in self.sac.keys():
            if self.sac['potions']>0:
                print('vous etes soigne')
                self.sac['potions']-=1
                self.vie+=2
        else:
            print("vous n'avez plus de potions")
            return(None)
    
    def marcher(self):
        print('vous marchez 1h')
        self.endurance -= 1
        if self.endurance==0:
            print('vous vous ecroulez de fatigue')
            self.vie-=1
            self.repos()
        if self.endurance<=5:
            print('vous etes fatigue')
        return(None)

    def repos(self):
        print('vous avez dormi')
        self.endurance = 10
        return(None)

    def forceDeFrappe(self):
        fdf = 0
        for arme in self.armes:
            fdf+=random.randint(1,self.armes[arme])
        return(fdf)

    def encaissement(self):
        ac = self.ac
        for armure in self.armures:
            ac+=self.armures[armure]
        return(ac)

class Aventurier(Personnage):
    def __init__(self):
        super(Aventurier,self).__init__()
        self.sac = {'ustensils de cuisine':1,
                 'sac de couchage':1,
                 'rations':10,
                 'potions':4,
                 'Gallions':300}
        self.nom = input('Quel est votre nom, aventurier?')
        self.classe = "aventurier"
        self.armes['couteau suisse'] = 3
        self.armures['cuir'] = 1
        
        return(None)

class Gobelin(Personnage):
    def __init__(self):
         super(Gobelin,self).__init__()
         self.vie = 4
         self.sac = {'ustensils de cuisine':1,
                     'rations':10}
         self.nom = self.nomDeGob()
         self.classe = 'gobelin'
         self.armes['coutelas rouille'] = 4
         
         return(None)

    def nomDeGob(self):
        syl1 = ["Glo","Fro","Kro","Tro"]
        syl2 = ["bo","do","po","fo"]

        return(syl1[random.randint(0,len(syl1)-1)]+
               syl2[random.randint(0,len(syl2)-1)])

class Elfe(Personnage):
    def __init__(self):
        super(Elfe,self).__init__()
        self.endurance = 12
        self.taco = 8
        self.ac = 1
        self.sac = {'fleches':1,
                    'rations':10}
        self.armes['arc composite'] = 3
        self.armures = {'armure de camouflage':4}
        self.armures['armure de camouflage'] = 4
        self.classe = "Elfe"
        self.nom = self.nomDElfe()

        return(None)
    
    def nomDElfe(self):
        comp1 = ["Ra","Sa","La","Ma"]
        comp2 = ["lon","son","mon","ron"]

        return(comp1[random.randint(0,len(comp1)-1)]+
               comp2[random.randint(0,len(comp2)-1)])
               

def baston(joueur1,joueur2):
    def d20():
        return(random.randint(1,20))

    def frappe(joueurs):
        if d20() > (joueurs[0].taco + joueurs[1].encaissement()):
            print(joueurs[0].nom,"a touche",joueurs[1].nom,"!")
            boum = joueurs[0].forceDeFrappe()
            print(joueurs[1].nom,"perds",boum,"points de vie")
            joueurs[1].vie-=boum
        else:
            print(joueurs[0].nom,"a loupe",joueurs[1].nom,"!")
        return(joueurs)

    i = 0 
    choix = 'c'
    while choix=='c' :
        choix = input('(c)ombattre ou (f)uir? ')
        if choix=='c':
            print("Tour #",i+1)
            print("vie des joueurs:")
            print(joueur1.nom,joueur1.vie,joueur2.nom,joueur2.vie)
            #definir l'initiative
            init1 = random.randint(1,6)
            init2 = random.randint(1,6)
            if init1<init2:
                joueurs = [joueur1,joueur2]
            else:
                joueurs = [joueur2,joueur1]
            print(joueurs[0].nom,"a l'initiative!")  
            # premier joueurs frappe
            joueurs = frappe(joueurs)
            # deuxieme joueur vivant?
            if joueurs[1].vie>0:
                # deuxieme joueur frappe
                joueurs.reverse()
                joueurs = frappe(joueurs)
            if min(joueur1.vie,joueur2.vie)<=0:
                if joueur1.vie<0:
                    print(joueur1.nom,"a ete tue par",joueur2.nom)
                    resolution='mort'
                else:
                    print(joueur2.nom,"a ete tue par",joueur1.nom)
                    resolution='victoire'
                break
            print()
            i+=1 # i = i+1
        elif choix=='f':
            print("Vous prenez la fuite...")
            if random.randint(1,6)==1:
                print("... Mais",joueur2.nom,"vous rattrape!")
                perdu = list(joueur1.sac.keys())
                perdu = perdu[random.randint(0,len(perdu)-1)]
                print(joueur2.nom,"vous a pris un",perdu)
                joueur1.pose(perdu)
            else:
                print("... et vous reussissez a echapper a",joueur2.nom)
            resolution='fuite'
    return(resolution)

if __name__=='__main__':
##    print("l'aventure a commencé")
##    joueur = Aventurier()
##    joueur.whois()
##    joueur.inventaire()
##    joueur.pose('rations')
##    joueur.inventaire()
##    joueur.pose("sac de couchage")
##    joueur.inventaire()
##    joueur.manger()
##    joueur.soigner()
##    joueur.inventaire()
##    joueur.marcher()
##    joueur.repos()
##    monstre = Gobelin()
##    monstre2 = Elfe()
##    monstre.whois()
##    monstre.inventaire()
##    baston(monstre,monstre2)
##    piece = Piece()
##    resolution = piece.remplirPiece(joueur)
##    print(resolution)
    Donjon()
