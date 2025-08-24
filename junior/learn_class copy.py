import random
import time
import sys
import math
from datetime import datetime
from colorama import init, Fore, Style, Back
from typing import Dict, List, Tuple

# Initialize colorama
init()

class Joueur:
    def __init__(self, nom: str, poste: str, attaque: int, defense: int, vitesse: int = 70, 
                 technique: int = 70, physique: int = 70, mental: int = 70, age: int = 25):
        self.nom = nom
        self.poste = poste  # Gardien, DC, DG, DD, MDC, MC, MOC, AG, AD, BU
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.technique = technique
        self.physique = physique
        self.mental = mental
        self.age = age
        
        # Stats de match
        self.buts = 0
        self.passes = 0
        self.passes_reussies = 0
        self.tirs = 0
        self.tirs_cadres = 0
        self.fautes = 0
        self.cartons_jaunes = 0
        self.carton_rouge = False
        self.fatigue = 0  # 0-100
        self.forme = random.randint(70, 100)  # Forme du jour
        self.distance_parcourue = 0.0
        self.duels_gagnes = 0
        self.duels_perdus = 0
        self.interceptions = 0
        self.tacles = 0
        self.centres = 0
        self.corners_tires = 0
        self.note = 6.0  # Note sur 10
        
        # Position sur le terrain (coordonnées)
        self.x = 0
        self.y = 0
        
    def get_niveau_general(self):
        """Calcule le niveau général du joueur"""
        return int((self.attaque + self.defense + self.vitesse + self.technique + self.physique + self.mental) / 6)
    
    def get_niveau_fatigue(self):
        """Retourne l'impact de la fatigue sur les performances"""
        return max(0.5, 1 - (self.fatigue / 150))
    
    def __str__(self):
        return f"{self.nom}"

class Formation:
    def __init__(self, nom: str, positions: Dict[str, Tuple[int, int]]):
        self.nom = nom
        self.positions = positions  # {"poste": (x, y)}

# Formations tactiques
FORMATIONS = {
    "4-3-3": Formation("4-3-3", {
        "G": (5, 50), "DD": (20, 80), "DC1": (20, 60), "DC2": (20, 40), "DG": (20, 20),
        "MDC": (40, 50), "MC1": (40, 70), "MC2": (40, 30),
        "AD": (70, 80), "BU": (70, 50), "AG": (70, 20)
    }),
    "4-4-2": Formation("4-4-2", {
        "G": (5, 50), "DD": (20, 80), "DC1": (20, 60), "DC2": (20, 40), "DG": (20, 20),
        "MD": (50, 80), "MC1": (50, 60), "MC2": (50, 40), "MG": (50, 20),
        "AT1": (75, 40), "AT2": (75, 60)
    })
}

class Equipe:
    def __init__(self, nom: str, joueurs: List[Joueur], formation: str = "4-3-3", 
                 couleur_maillot: str = "Bleu", entraineur: str = "Coach"):
        self.nom = nom
        self.joueurs = joueurs
        self.formation = FORMATIONS[formation]
        self.couleur_maillot = couleur_maillot
        self.entraineur = entraineur
        
        # Stats équipe
        self.buts_marques = 0
        self.buts_encaisses = 0
        self.tirs = 0
        self.tirs_cadres = 0
        self.possession = 50.0
        self.passes = 0
        self.passes_reussies = 0
        self.fautes = 0
        self.corners = 0
        self.hors_jeux = 0
        self.cartons_jaunes = 0
        self.cartons_rouges = 0
        
        # Tactiques
        self.mentalite = "Equilibré"  # Défensif, Equilibré, Offensif
        self.pressing = 50  # Intensité du pressing 0-100
        self.largeur_jeu = 50  # Largeur du jeu 0-100
        
        self.adversaire = None
        
        # Positionnement des joueurs
        self._positionner_joueurs()
    
    def _positionner_joueurs(self):
        """Positionne les joueurs selon la formation"""
        positions = list(self.formation.positions.values())
        for i, joueur in enumerate(self.joueurs[:11]):  # Titulaires seulement
            if i < len(positions):
                joueur.x, joueur.y = positions[i]
    
    def set_adversaire(self, adversaire):
        self.adversaire = adversaire
    
    def get_joueur_aleatoire(self, poste=None, zone=None):
        """Retourne un joueur aléatoire selon critères"""
        candidats = [j for j in self.joueurs[:11] if not j.carton_rouge and 
                    (poste is None or j.poste == poste)]
        
        if zone:  # "defense", "milieu", "attaque"
            if zone == "defense":
                candidats = [j for j in candidats if j.poste in ["DC", "DD", "DG", "MDC"]]
            elif zone == "milieu":
                candidats = [j for j in candidats if j.poste in ["MC", "MOC", "MD", "MG"]]
            elif zone == "attaque":
                candidats = [j for j in candidats if j.poste in ["BU", "AT1", "AT2", "AD", "AG"]]
        
        if candidats:
            # Favorise les joueurs en forme et moins fatigués
            weights = [max(1, j.forme - j.fatigue/2) for j in candidats]
            return random.choices(candidats, weights=weights, k=1)[0]
        return None
    
    def get_meilleur_tireur(self):
        """Retourne le meilleur tireur disponible"""
        candidats = [j for j in self.joueurs[:11] if not j.carton_rouge]
        if candidats:
            return max(candidats, key=lambda j: j.attaque * j.technique * j.get_niveau_fatigue())
        return None

class Commentateur:
    def __init__(self):
        self.commentaires_but = [
            "BUUUUUUUUT ! Quel magnifique enchaînement !",
            "GOOOOOOOOOL ! La foule est en délire !",
            "Frappe sublime ! Le gardien ne pouvait rien faire !",
            "But exceptionnel ! Du grand art !",
            "Quelle finition ! C'est du football de classe mondiale !",
            "INCREDIBLE ! What a strike!",
            "Pure magic ! Absolutement fantastique !",
        ]
        
        self.commentaires_arret = [
            "Arrêt MAGNIFIQUE du gardien !",
            "Quelle parade ! Réflexes de félin !",
            "INCROYABLE ! Comment a-t-il sorti ça ?",
            "Arrêt décisif ! Les supporters sont debout !",
            "Parade du siècle ! Quel gardien !",
        ]
        
        self.commentaires_action = [
            "Belle combinaison dans l'axe...",
            "Joli mouvement sur le côté droit...",
            "L'équipe construit patiemment...",
            "Pressing intense de l'adversaire...",
            "Le ballon circule bien...",
            "Montée rapide sur le flanc gauche...",
            "Centre rentrant dans la surface...",
            "Duel aérien intense...",
        ]
        
        self.commentaires_faute = [
            "Faute un peu sévère...",
            "Contact litigieux...",
            "L'arbitre siffle immédiatement !",
            "Intervention dangereuse !",
            "Geste d'humeur du défenseur...",
            "Tacle par derrière ! Carton mérité !",
        ]

    def commenter_but(self, marqueur, equipe, type_but, minute):
        base = random.choice(self.commentaires_but)
        details = f" {marqueur.nom} trouve la lucarne à la {minute}e minute ! {type_but.upper()} exceptionnel pour {equipe.nom} !"
        return f"{Fore.RED}{base}{Style.RESET_ALL}{details}"
    
    def commenter_arret(self, gardien, tireur):
        base = random.choice(self.commentaires_arret)
        return f"{base} {gardien.nom} repousse la tentative de {tireur.nom} !"

class Match:
    def __init__(self, equipe1: Equipe, equipe2: Equipe, stade: str = "Stade Municipal", 
                 meteo: str = "Ensoleillé", temperature: int = 22, affluence: int = 45000):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.equipe1.set_adversaire(self.equipe2)
        self.equipe2.set_adversaire(self.equipe1)
        
        # Infos match
        self.stade = stade
        self.meteo = meteo
        self.temperature = temperature
        self.affluence = affluence
        self.arbitre = random.choice(["M. Dubois", "M. Martin", "Mme Leroux", "M. García"])
        
        # Temps
        self.temps = 0
        self.mi_temps = False
        self.duree_match = 90
        self.temps_additionnel_1 = 0
        self.temps_additionnel_2 = 0
        
        # Rythme de simulation
        self.duree_reelle_seconde = 45
        self.intervalle_evenement = 0.8
        
        self.commentateur = Commentateur()
        self.evenements = []  # Historique des événements
        
    def afficher_infos_pre_match(self):
        """Affiche les informations pré-match"""
        print(f"\n{Back.BLUE}{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'🏟️  FOOTBALL SIMULATOR - MATCH EN DIRECT':^80}{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}📍 LIEU:{Style.RESET_ALL} {self.stade}")
        print(f"{Fore.CYAN}🌤️  MÉTÉO:{Style.RESET_ALL} {self.meteo}, {self.temperature}°C")
        print(f"{Fore.CYAN}👥 AFFLUENCE:{Style.RESET_ALL} {self.affluence:,} spectateurs")
        print(f"{Fore.CYAN}👨‍⚖️ ARBITRE:{Style.RESET_ALL} {self.arbitre}")
        print(f"{Fore.CYAN}🕐 HEURE:{Style.RESET_ALL} {datetime.now().strftime('%H:%M')}")
        
        print(f"\n{Back.GREEN}{Fore.WHITE} ÉQUIPES EN PRÉSENCE {Style.RESET_ALL}")
        print(f"\n{Fore.MAGENTA}🏠 {self.equipe1.nom.upper()}{Style.RESET_ALL} ({self.equipe1.formation.nom})")
        print(f"   Entraîneur: {self.equipe1.entraineur}")
        print(f"   Maillot: {self.equipe1.couleur_maillot}")
        
        print(f"\n{Fore.YELLOW}✈️  {self.equipe2.nom.upper()}{Style.RESET_ALL} ({self.equipe2.formation.nom})")
        print(f"   Entraîneur: {self.equipe2.entraineur}")
        print(f"   Maillot: {self.equipe2.couleur_maillot}")
        
        print(f"\n{Back.WHITE}{Fore.BLACK} COMPOSITIONS D'ÉQUIPE {Style.RESET_ALL}")
        
        # Afficher les compositions
        print(f"\n{Fore.MAGENTA}{self.equipe1.nom}:{Style.RESET_ALL}")
        for i, joueur in enumerate(self.equipe1.joueurs[:11]):
            print(f"  {i+1:2d}. {joueur.nom:15} ({joueur.poste}) - Niveau: {joueur.get_niveau_general()}")
        
        print(f"\n{Fore.YELLOW}{self.equipe2.nom}:{Style.RESET_ALL}")
        for i, joueur in enumerate(self.equipe2.joueurs[:11]):
            print(f"  {i+1:2d}. {joueur.nom:15} ({joueur.poste}) - Niveau: {joueur.get_niveau_general()}")
        
        print(f"\n{Fore.GREEN}🎮 Appuyez sur Entrée pour commencer le match...{Style.RESET_ALL}")
        input()
    
    def calculer_probabilites(self, equipe_attaquante, type_action):
        """Calcule les probabilités d'événements selon le contexte"""
        # Facteurs d'influence
        niveau_equipe = sum(j.get_niveau_general() for j in equipe_attaquante.joueurs[:11]) / 11
        fatigue_moyenne = sum(j.fatigue for j in equipe_attaquante.joueurs[:11]) / 11
        possession = equipe_attaquante.possession / 100
        
        # Influence météo
        meteo_factor = 1.0
        if self.meteo == "Pluvieux":
            meteo_factor = 0.85
        elif self.meteo == "Venteux":
            meteo_factor = 0.9
            
        # Facteur de fatigue
        fatigue_factor = max(0.6, 1 - fatigue_moyenne / 120)
        
        # Ajustements selon le temps
        if self.temps > 70:
            fatigue_factor *= 0.8
        if self.temps > 80:
            fatigue_factor *= 0.7
            
        base_multiplier = (niveau_equipe / 100) * meteo_factor * fatigue_factor * possession
        
        if type_action == "but":
            return max(0.02, 0.08 * base_multiplier)
        elif type_action == "tir_cadre":
            return max(0.05, 0.15 * base_multiplier)
        elif type_action == "tir_non_cadre":
            return max(0.08, 0.25 * base_multiplier)
        
        return base_multiplier

    def simuler_tir(self, tireur, gardien, type_tir="frappe"):
        """Simule un tir avec calculs réalistes"""
        # Qualité du tir
        precision_tir = (tireur.attaque + tireur.technique) * tireur.get_niveau_fatigue()
        
        # Distance et angle (simulé)
        distance = random.randint(5, 30)
        angle_difficile = random.random() < 0.3
        
        # Facteurs de difficulté
        difficulte = 100
        if distance > 20:
            difficulte += 30
        if angle_difficile:
            difficulte += 20
        if type_tir == "volée":
            difficulte += 15
        elif type_tir == "tête":
            difficulte += 10
            
        # Qualité gardien
        qualite_gardien = gardien.defense * gardien.get_niveau_fatigue()
        
        # Calcul final
        chance_but = max(5, precision_tir - difficulte + random.randint(-20, 20))
        chance_arret = qualite_gardien + random.randint(-15, 15)
        
        if chance_but > chance_arret + 20:
            return "but"
        elif chance_but > chance_arret:
            return "arret"
        elif random.random() < 0.7:
            return "cadre"
        else:
            return "a_cote"

    def simuler_evenement(self):
        """Simule un événement de match ultra-réaliste"""
        # Choix de l'équipe selon possession et momentum
        momentum = (self.equipe1.buts_marques - self.equipe2.buts_marques) * 0.1
        possession_adj = self.equipe1.possession + momentum * 5
        
        equipe_attaquante = random.choices(
            [self.equipe1, self.equipe2], 
            weights=[possession_adj, 100 - possession_adj], 
            k=1
        )[0]
        equipe_defendante = equipe_attaquante.adversaire
        
        # Mise à jour possession (plus réaliste)
        var_possession = random.gauss(0, 2)
        if random.random() < 0.1:  # Changements brusques parfois
            var_possession = random.gauss(0, 8)
            
        equipe_attaquante.possession += var_possession
        equipe_attaquante.possession = max(25, min(75, equipe_attaquante.possession))
        equipe_defendante.possession = 100 - equipe_attaquante.possession
        
        # Types d'événements avec poids dynamiques
        poids_base = [3, 12, 8, 15, 12, 8, 5, 3, 2, 35]  # but, tir_cadre, tir_non_cadre, passe, faute, corner, carton, blessure, hors_jeu, rien
        
        # Ajustements selon contexte
        if self.temps > 80:  # Fin de match plus intense
            poids_base[0] *= 1.5  # Plus de buts
            poids_base[4] *= 1.3  # Plus de fautes
            
        if abs(self.equipe1.buts_marques - self.equipe2.buts_marques) >= 2:  # Score déséquilibré
            poids_base[0] *= 0.7  # Moins de buts
            poids_base[-1] *= 1.5  # Plus de temps mort
        
        evenement = random.choices(
            ["but", "tir_cadre", "tir_non_cadre", "passe", "faute", "corner", "carton", "blessure", "hors_jeu", "rien"],
            weights=poids_base, k=1
        )[0]
        
        temps_str = f"{Fore.YELLOW}{self.temps:2d}'{Style.RESET_ALL}"
        
        # Traitement des événements
        if evenement == "but":
            self.gerer_but(equipe_attaquante, equipe_defendante, temps_str)
        elif evenement == "tir_cadre":
            self.gerer_tir_cadre(equipe_attaquante, equipe_defendante, temps_str)
        elif evenement == "tir_non_cadre":
            self.gerer_tir_non_cadre(equipe_attaquante, temps_str)
        elif evenement == "passe":
            self.gerer_passe(equipe_attaquante, temps_str)
        elif evenement == "faute":
            self.gerer_faute(equipe_attaquante, equipe_defendante, temps_str)
        elif evenement == "corner":
            self.gerer_corner(equipe_attaquante, temps_str)
        elif evenement == "carton":
            self.gerer_carton(equipe_attaquante, temps_str)
        elif evenement == "hors_jeu":
            self.gerer_hors_jeu(equipe_attaquante, temps_str)
        
        # Mise à jour fatigue
        for joueur in equipe_attaquante.joueurs[:11]:
            joueur.fatigue += random.uniform(0.1, 0.3)
            joueur.distance_parcourue += random.uniform(0.05, 0.15)
    
    def gerer_but(self, equipe_att, equipe_def, temps_str):
        """Gère l'événement but avec détails"""
        types_but = ["frappe", "tête", "volée", "coup_franc", "penalty", "lob", "contre_attaque"]
        poids_types = [25, 15, 10, 8, 5, 7, 15]
        
        # Ajuste selon la zone
        zone_but = random.choice(["surface", "6_metres", "limite_surface", "lointaine"])
        
        if zone_but == "lointaine":
            poids_types = [35, 5, 15, 20, 0, 10, 10]  # Plus de frappes, moins de têtes
        elif zone_but == "6_metres":
            poids_types = [15, 40, 5, 0, 0, 5, 25]  # Plus de têtes et contres
            
        type_but = random.choices(types_but, weights=poids_types, k=1)[0]
        
        # Choix du buteur selon le type
        if type_but == "coup_franc":
            marqueur = equipe_att.get_meilleur_tireur()
        elif type_but == "penalty":
            marqueur = equipe_att.get_meilleur_tireur()  # Normalement le tireur de penalty
        elif type_but == "tête":
            marqueur = equipe_att.get_joueur_aleatoire(zone="attaque") or equipe_att.get_joueur_aleatoire()
        else:
            marqueur = equipe_att.get_joueur_aleatoire(zone="attaque") or equipe_att.get_joueur_aleatoire(zone="milieu")
        
        if not marqueur:
            return
            
        # Passeur potentiel
        passeur = None
        if type_but not in ["coup_franc", "penalty"] and random.random() < 0.7:
            passeur = equipe_att.get_joueur_aleatoire()
            if passeur == marqueur:
                passeur = None
        
        # Mise à jour stats
        marqueur.buts += 1
        marqueur.tirs += 1
        marqueur.tirs_cadres += 1
        marqueur.fatigue += random.randint(3, 8)
        marqueur.note += random.uniform(0.5, 1.2)
        
        if passeur:
            passeur.passes += 1
            passeur.passes_reussies += 1
            passeur.note += random.uniform(0.2, 0.6)
        
        equipe_att.buts_marques += 1
        equipe_att.tirs += 1
        equipe_att.tirs_cadres += 1
        equipe_def.buts_encaisses += 1
        
        # Gardien adverse pénalisé
        gardien_def = equipe_def.get_joueur_aleatoire(poste="G")
        if gardien_def:
            gardien_def.note -= random.uniform(0.3, 0.8)
        
        # Affichage dramatique
        print(f"\n{temps_str} ═══════════════════════════════════")
        print(self.commentateur.commenter_but(marqueur, equipe_att, type_but, self.temps))
        
        if passeur:
            print(f"   🎯 {Fore.BLUE}Passe décisive de {passeur.nom}{Style.RESET_ALL}")
        
        print(f"   📍 Zone: {zone_but.replace('_', ' ').title()}")
        print(f"   ⚽ {Fore.GREEN}Score: {self.equipe1.nom} {self.equipe1.buts_marques} - {self.equipe2.buts_marques} {self.equipe2.nom}{Style.RESET_ALL}")
        print(f"════════════════════════════════════")
        
        # Réaction foule
        reactions_foule = ["La foule explose de joie !", "Quel silence dans le stade...", 
                          "Les supporters sont en délire !", "Standing ovation !"]
        print(f"   🎭 {random.choice(reactions_foule)}")
        
        time.sleep(2)
    
    def gerer_tir_cadre(self, equipe_att, equipe_def, temps_str):
        """Gère les tirs cadrés avec arrêts du gardien"""
        tireur = equipe_att.get_joueur_aleatoire(zone="attaque") or equipe_att.get_joueur_aleatoire()
        gardien = equipe_def.get_joueur_aleatoire(poste="G")
        
        if not tireur or not gardien:
            return
            
        # Type de tir
        types_tir = ["frappe", "tête", "volée", "lob"]
        type_tir = random.choice(types_tir)
        
        # Stats
        tireur.tirs += 1
        tireur.tirs_cadres += 1
        tireur.fatigue += random.randint(2, 5)
        equipe_att.tirs += 1
        equipe_att.tirs_cadres += 1
        
        gardien.fatigue += random.randint(3, 6)
        gardien.note += random.uniform(0.1, 0.4)
        
        # Types d'arrêts
        types_arret = ["plongeon", "réflexe", "sortie", "claquette", "détente"]
        type_arret = random.choice(types_arret)
        
        print(f"{temps_str} - 🎯 {Fore.CYAN}Tir de {tireur.nom}{Style.RESET_ALL} ({equipe_att.nom})")
        print(f"   {self.commentateur.commenter_arret(gardien, tireur)}")
        print(f"   🧤 Arrêt en {type_arret} par {gardien.nom}")
        
        # Rebond possible
        if random.random() < 0.15:
            print(f"   ⚡ Le ballon rebondit dans la surface ! Situation chaude !")
    
    def gerer_tir_non_cadre(self, equipe_att, temps_str):
        """Gère les tirs non cadrés"""
        tireur = equipe_att.get_joueur_aleatoire(zone="attaque") or equipe_att.get_joueur_aleatoire()
        if not tireur:
            return
            
        directions = ["à côté", "au-dessus", "sur le poteau", "sur la barre"]
        direction = random.choice(directions)
        
        tireur.tirs += 1
        tireur.fatigue += random.randint(1, 3)
        equipe_att.tirs += 1
        
        if direction in ["sur le poteau", "sur la barre"]:
            print(f"{temps_str} - 😱 {Fore.YELLOW}OH ! Tir de {tireur.nom} {direction} ! Il s'en est fallu de peu !{Style.RESET_ALL}")
            tireur.note += 0.2
        else:
            print(f"{temps_str} - 🎯 Tir {direction} de {tireur.nom} ({equipe_att.nom})")
    
    def gerer_passe(self, equipe_att, temps_str):
        """Gère les passes et la construction du jeu"""
        passeur = equipe_att.get_joueur_aleatoire()
        if not passeur:
            return
            
        types_passe = ["courte", "longue", "centre", "une-deux", "talonnade"]
        poids = [40, 20, 15, 15, 5]
        
        # Ajuste selon la position
        if passeur.poste in ["DC", "MDC"]:
            poids = [25, 35, 10, 20, 5]  # Plus de passes longues
        elif passeur.poste in ["AD", "AG"]:
            poids = [20, 15, 45, 15, 5]  # Plus de centres
            
        type_passe = random.choices(types_passe, weights=poids, k=1)[0]
        
        passeur.passes += 1
        reussite = random.random() < (passeur.technique + passeur.mental) / 120
        
        if reussite:
            passeur.passes_reussies += 1
            equipe_att.passes_reussies += 1
            passeur.note += 0.05
        
        equipe_att.passes += 1
        
        if random.random() < 0.15:  # Affichage sélectif des passes notables
            qualificatif = random.choice(["Belle", "Magnifique", "Superbe", "Précise"])
            if type_passe == "longue" and reussite:
                print(f"{temps_str} - 📐 {qualificatif} passe longue de {passeur.nom}")
            elif type_passe == "centre":
                print(f"{temps_str} - 🎯 Centre de {passeur.nom} dans la surface")
                equipe_att.corners += random.choice([0, 0, 0, 1])  # Parfois mène à un corner
    
    def gerer_faute(self, equipe_att, equipe_def, temps_str):
        """Gère les fautes avec plus de réalisme"""
        fautif = equipe_att.get_joueur_aleatoire()
        victime = equipe_def.get_joueur_aleatoire()
        
        if not fautif or not victime:
            return
        
        # Types de fautes
        types_faute = ["tacle", "accrochage", "charge", "coup_pied", "main", "antisportive"]
        gravites = ["légère", "moyenne", "grave"]
        
        # Probabilités selon le poste du fautif
        if fautif.poste in ["DC", "DD", "DG"]:
            type_faute = random.choices(types_faute, weights=[35, 25, 20, 10, 5, 5], k=1)[0]
        else:
            type_faute = random.choices(types_faute, weights=[20, 30, 15, 15, 15, 5], k=1)[0]
        
        gravite = random.choices(gravites, weights=[60, 30, 10], k=1)[0]
        
        # Zone de la faute
        zones = ["surface_att", "30m", "milieu", "surface_def"]
        zone = random.choice(zones)
        
        fautif.fautes += 1
        fautif.fatigue += random.randint(1, 4)
        equipe_att.fautes += 1
        
        # Détermination sanction
        sanction = "aucune"
        if gravite == "grave" or (gravite == "moyenne" and random.random() < 0.4):
            if fautif.cartons_jaunes == 1:
                sanction = "rouge"
                fautif.carton_rouge = True
                equipe_att.cartons_rouges += 1
                fautif.note -= 2.0
            elif random.random() < 0.8:
                sanction = "jaune"
                fautif.cartons_jaunes += 1
                equipe_att.cartons_jaunes += 1
                fautif.note -= 0.5
        elif gravite == "moyenne" and random.random() < 0.2:
            sanction = "jaune"
            fautif.cartons_jaunes += 1
            equipe_att.cartons_jaunes += 1
            fautif.note -= 0.5
        
        # Affichage selon gravité
        if sanction == "rouge":
            print(f"{temps_str} - 🟥 {Fore.RED}CARTON ROUGE !{Style.RESET_ALL} {fautif.nom} est expulsé ! ({type_faute})")
            print(f"   ⚡ {equipe_att.nom} se retrouve à 10 contre 11 !")
        elif sanction == "jaune":
            print(f"{temps_str} - 🟨 Carton jaune pour {fautif.nom} ({equipe_att.nom}) - {type_faute}")
        elif gravite == "grave":
            print(f"{temps_str} - ⚠️  Faute dangereuse de {fautif.nom} sur {victime.nom}")
        elif random.random() < 0.3:  # Affichage sélectif
            print(f"{temps_str} - Faute de {fautif.nom} sur {victime.nom}")
        
        # Coup franc / Penalty
        if zone == "surface_att" and gravite in ["moyenne", "grave"]:
            if random.random() < 0.15:
                print(f"   ⚽ PENALTY pour {equipe_def.nom} !")
                time.sleep(1)
                self.gerer_penalty(equipe_def, equipe_att)
        elif zone in ["30m", "surface_att"]:
            print(f"   🎯 Coup franc dangereux pour {equipe_def.nom}")
            if random.random() < 0.1:  # Chance de but sur CF
                time.sleep(0.5)
                self.gerer_coup_franc(equipe_def, equipe_att)
    
    def gerer_penalty(self, equipe_tireur, equipe_gardien):
        """Gère la séquence penalty"""
        tireur = equipe_tireur.get_meilleur_tireur()
        gardien = equipe_gardien.get_joueur_aleatoire(poste="G")
        
        if not tireur or not gardien:
            return
        
        print(f"   🎯 {tireur.nom} se présente face à {gardien.nom}")
        print(f"   🔥 Tension maximale dans le stade...")
        time.sleep(2)
        
        # Calcul réaliste
        precision_tireur = tireur.attaque + tireur.technique + tireur.mental
        qualite_gardien = gardien.defense + gardien.mental
        
        chance_but = precision_tireur + random.randint(-30, 30)
        chance_arret = qualite_gardien + random.randint(-20, 40)  # Plus difficile d'arrêter
        
        if chance_but > chance_arret + 20:
            # But
            tireur.buts += 1
            tireur.tirs += 1
            tireur.tirs_cadres += 1
            equipe_tireur.buts_marques += 1
            equipe_gardien.buts_encaisses += 1
            tireur.note += 0.8
            gardien.note -= 0.3
            
            print(f"   ⚽ {Fore.GREEN}BUT ! {tireur.nom} ne tremble pas !{Style.RESET_ALL}")
            print(f"   📊 Score: {self.equipe1.nom} {self.equipe1.buts_marques} - {self.equipe2.buts_marques} {self.equipe2.nom}")
        elif chance_arret > chance_but:
            # Arrêt
            gardien.note += 1.0
            tireur.note -= 0.5
            tireur.tirs += 1
            tireur.tirs_cadres += 1
            print(f"   🧤 {Fore.YELLOW}ARRÊT ! {gardien.nom} détourne le penalty !{Style.RESET_ALL}")
            print(f"   🎭 Quelle parade ! Le stade explose !")
        else:
            # À côté
            tireur.tirs += 1
            tireur.note -= 0.8
            print(f"   😱 {Fore.RED}RATÉ ! {tireur.nom} envoie le ballon dans les tribunes !{Style.RESET_ALL}")
    
    def gerer_coup_franc(self, equipe_tireur, equipe_gardien):
        """Gère les coups francs dangereux"""
        tireur = equipe_tireur.get_meilleur_tireur()
        gardien = equipe_gardien.get_joueur_aleatoire(poste="G")
        
        if not tireur or not gardien:
            return
        
        print(f"   🎯 Coup franc tiré par {tireur.nom}...")
        
        # Types de coup franc
        types_cf = ["direct", "enroulé", "puissant", "placé"]
        type_cf = random.choice(types_cf)
        
        chance_but = (tireur.attaque + tireur.technique) * 0.6 + random.randint(-20, 20)
        
        if chance_but > 70:
            tireur.buts += 1
            equipe_tireur.buts_marques += 1
            equipe_gardien.buts_encaisses += 1
            tireur.note += 1.2
            print(f"   ⚽ {Fore.GREEN}MAGNIFIQUE ! Coup franc {type_cf} dans la lucarne !{Style.RESET_ALL}")
        elif chance_but > 50:
            print(f"   🧤 Arrêt du gardien sur le coup franc {type_cf}")
            gardien.note += 0.3
        else:
            print(f"   📐 Coup franc {type_cf} dans le mur ou à côté")
    
    def gerer_corner(self, equipe_att, temps_str):
        """Gère les corners"""
        equipe_att.corners += 1
        tireur_corner = equipe_att.get_joueur_aleatoire()
        
        if tireur_corner:
            tireur_corner.corners_tires += 1
            tireur_corner.centres += 1
        
        print(f"{temps_str} - 📐 Corner pour {Fore.CYAN}{equipe_att.nom}{Style.RESET_ALL}")
        
        # Chance d'action dangereuse sur corner
        if random.random() < 0.2:
            print(f"   🎯 Centre dangereux dans la surface !")
            if random.random() < 0.15:  # Chance de but sur corner
                time.sleep(0.5)
                self.gerer_but_corner(equipe_att)
    
    def gerer_but_corner(self, equipe_att):
        """Gère un but sur corner"""
        marqueur = equipe_att.get_joueur_aleatoire()
        if not marqueur:
            return
        
        marqueur.buts += 1
        equipe_att.buts_marques += 1
        equipe_att.adversaire.buts_encaisses += 1
        marqueur.note += 1.0
        
        print(f"   ⚽ {Fore.GREEN}BUT SUR CORNER ! {marqueur.nom} place sa tête !{Style.RESET_ALL}")
        print(f"   📊 Score: {self.equipe1.nom} {self.equipe1.buts_marques} - {self.equipe2.buts_marques} {self.equipe2.nom}")
    
    def gerer_carton(self, equipe_att, temps_str):
        """Gère les cartons isolés"""
        joueur = equipe_att.get_joueur_aleatoire()
        if not joueur:
            return
        
        if random.random() < 0.1 and joueur.cartons_jaunes < 2:
            joueur.cartons_jaunes += 1
            joueur.note -= 0.4
            print(f"{temps_str} - 🟨 Carton jaune pour {joueur.nom} (protestation)")
    
    def gerer_hors_jeu(self, equipe_att, temps_str):
        """Gère les hors-jeux"""
        equipe_att.hors_jeux += 1
        joueur_hj = equipe_att.get_joueur_aleatoire(zone="attaque")
        if joueur_hj:
            print(f"{temps_str} - 🚩 Hors-jeu signalé ! {joueur_hj.nom} était en position irrégulière")
    
    def afficher_mi_temps(self):
        """Affiche les stats de mi-temps"""
        print(f"\n{Back.YELLOW}{Fore.BLACK}{'⏸️  MI-TEMPS':^80}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}📊 STATISTIQUES 1ÈRE MI-TEMPS:{Style.RESET_ALL}")
        print(f"{'='*60}")
        
        print(f"{Fore.MAGENTA}{self.equipe1.nom:20}{Style.RESET_ALL} | {Fore.YELLOW}{self.equipe2.nom:20}{Style.RESET_ALL}")
        print(f"{'-'*60}")
        print(f"{'Buts:':15} {self.equipe1.buts_marques:^10} | {self.equipe2.buts_marques:^10}")
        print(f"{'Tirs:':15} {self.equipe1.tirs:^10} | {self.equipe2.tirs:^10}")
        print(f"{'Cadrés:':15} {self.equipe1.tirs_cadres:^10} | {self.equipe2.tirs_cadres:^10}")
        print(f"{'Possession:':15} {self.equipe1.possession:^8.0f}% | {self.equipe2.possession:^8.0f}%")
        print(f"{'Corners:':15} {self.equipe1.corners:^10} | {self.equipe2.corners:^10}")
        print(f"{'Fautes:':15} {self.equipe1.fautes:^10} | {self.equipe2.fautes:^10}")
        print(f"{'Cartons J:':15} {self.equipe1.cartons_jaunes:^10} | {self.equipe2.cartons_jaunes:^10}")
        print(f"{'Cartons R:':15} {self.equipe1.cartons_rouges:^10} | {self.equipe2.cartons_rouges:^10}")
        print(f"{'='*60}")
        
        # Meilleurs joueurs
        print(f"\n⭐ {Fore.CYAN}JOUEURS EN VUE:{Style.RESET_ALL}")
        tous_joueurs = self.equipe1.joueurs[:11] + self.equipe2.joueurs[:11]
        meilleurs = sorted([j for j in tous_joueurs if j.note >= 7.0], key=lambda x: x.note, reverse=True)[:3]
        
        for i, joueur in enumerate(meilleurs, 1):
            equipe = self.equipe1 if joueur in self.equipe1.joueurs else self.equipe2
            print(f"   {i}. {joueur.nom} ({equipe.nom}) - Note: {joueur.note:.1f}")
        
        print(f"\n{Fore.GREEN}⚽ Repos des joueurs - 15 minutes d'analyse tactique...{Style.RESET_ALL}")
        time.sleep(3)
    
    def afficher_statistiques_finales(self):
        """Affiche les statistiques complètes du match"""
        print(f"\n{Back.GREEN}{Fore.WHITE}{'🏁 FIN DE MATCH - STATISTIQUES COMPLÈTES':^80}{Style.RESET_ALL}")
        
        # Score final avec style
        print(f"\n{Back.WHITE}{Fore.BLACK}{'SCORE FINAL':^80}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{self.equipe1.nom:^25}{Style.RESET_ALL} {self.equipe1.buts_marques:^5} - {self.equipe2.buts_marques:^5} {Fore.YELLOW}{self.equipe2.nom:^25}{Style.RESET_ALL}")
        
        # Résultat
        if self.equipe1.buts_marques > self.equipe2.buts_marques:
            print(f"\n🏆 {Fore.GREEN}VICTOIRE DE {self.equipe1.nom.upper()} !{Style.RESET_ALL}")
            self.equipe1.points += 3
        elif self.equipe2.buts_marques > self.equipe1.buts_marques:
            print(f"\n🏆 {Fore.GREEN}VICTOIRE DE {self.equipe2.nom.upper()} !{Style.RESET_ALL}")
            self.equipe2.points += 3
        else:
            print(f"\n🤝 {Fore.YELLOW}MATCH NUL !{Style.RESET_ALL}")
            self.equipe1.points += 1
            self.equipe2.points += 1
        
        # Stats détaillées
        print(f"\n{Back.BLUE}{Fore.WHITE}{'STATISTIQUES DÉTAILLÉES':^80}{Style.RESET_ALL}")
        print(f"{'='*80}")
        print(f"{'Statistique':^20} | {self.equipe1.nom:^25} | {self.equipe2.nom:^25}")
        print(f"{'-'*80}")
        
        stats = [
            ("Buts", self.equipe1.buts_marques, self.equipe2.buts_marques),
            ("Tirs", self.equipe1.tirs, self.equipe2.tirs),
            ("Tirs cadrés", self.equipe1.tirs_cadres, self.equipe2.tirs_cadres),
            ("Possession %", f"{self.equipe1.possession:.0f}", f"{self.equipe2.possession:.0f}"),
            ("Passes", self.equipe1.passes, self.equipe2.passes),
            ("% Passes réussies", f"{(self.equipe1.passes_reussies/max(1,self.equipe1.passes)*100):.0f}", 
             f"{(self.equipe2.passes_reussies/max(1,self.equipe2.passes)*100):.0f}"),
            ("Corners", self.equipe1.corners, self.equipe2.corners),
            ("Hors-jeux", self.equipe1.hors_jeux, self.equipe2.hors_jeux),
            ("Fautes", self.equipe1.fautes, self.equipe2.fautes),
            ("Cartons jaunes", self.equipe1.cartons_jaunes, self.equipe2.cartons_jaunes),
            ("Cartons rouges", self.equipe1.cartons_rouges, self.equipe2.cartons_rouges),
        ]
        
        for stat, val1, val2 in stats:
            print(f"{stat:^20} | {str(val1):^25} | {str(val2):^25}")
        
        print(f"{'='*80}")
        
        # Buteurs
        print(f"\n⚽ {Fore.GREEN}BUTEURS:{Style.RESET_ALL}")
        tous_buteurs = [(j, self.equipe1) for j in self.equipe1.joueurs if j.buts > 0] + \
                      [(j, self.equipe2) for j in self.equipe2.joueurs if j.buts > 0]
        
        if tous_buteurs:
            tous_buteurs.sort(key=lambda x: x[0].buts, reverse=True)
            for joueur, equipe in tous_buteurs:
                print(f"   🥅 {joueur.nom} ({equipe.nom}) - {joueur.buts} but{'s' if joueur.buts > 1 else ''}")
        else:
            print("   Aucun buteur dans ce match")
        
        # Joueurs du match
        print(f"\n⭐ {Fore.CYAN}NOTES DES JOUEURS:{Style.RESET_ALL}")
        
        for equipe in [self.equipe1, self.equipe2]:
            print(f"\n{Fore.MAGENTA if equipe == self.equipe1 else Fore.YELLOW}{equipe.nom}:{Style.RESET_ALL}")
            joueurs_notes = sorted(equipe.joueurs[:11], key=lambda x: x.note, reverse=True)
            
            for joueur in joueurs_notes:
                note_color = Fore.GREEN if joueur.note >= 7.5 else Fore.YELLOW if joueur.note >= 6.5 else Fore.RED
                cartons = ""
                if joueur.carton_rouge:
                    cartons = " 🟥"
                elif joueur.cartons_jaunes > 0:
                    cartons = f" 🟨x{joueur.cartons_jaunes}"
                    
                stats_joueur = f"({joueur.buts}⚽, {joueur.tirs}🎯, {joueur.fautes}⚠️)"
                print(f"   {joueur.nom:15} ({joueur.poste:3}) - Note: {note_color}{joueur.note:4.1f}{Style.RESET_ALL} {stats_joueur}{cartons}")
        
        # Homme du match
        tous_joueurs = self.equipe1.joueurs[:11] + self.equipe2.joueurs[:11]
        homme_match = max(tous_joueurs, key=lambda x: x.note)
        equipe_hdm = self.equipe1 if homme_match in self.equipe1.joueurs else self.equipe2
        
        print(f"\n🏅 {Fore.GOLD}HOMME DU MATCH: {homme_match.nom} ({equipe_hdm.nom}) - Note: {homme_match.note:.1f}{Style.RESET_ALL}")
        
        print(f"""\n{Back.BLACK}{Fore.WHITE}{"Merci d'avoir suivi ce match en direct !":^80}{Style.RESET_ALL}""")
        print(f"{Back.BLACK}{Fore.WHITE}{'⚽ FOOTBALL SIMULATOR - Simulation terminée ⚽':^80}{Style.RESET_ALL}")
    
    def simuler(self):
        """Simule le match complet avec ambiance réaliste"""
        self.afficher_infos_pre_match()
        
        print(f"\n{Fore.GREEN}🔴 DIRECT - COUP D'ENVOI !{Style.RESET_ALL}")
        print(f"⚽ {self.arbitre} donne le coup d'envoi !")
        print(f"🌡️  Température: {self.temperature}°C - Conditions: {self.meteo}")
        time.sleep(1)
        
        # 1ère mi-temps
        while self.temps < 45:
            self.temps += random.randint(1, 4)
            if self.temps > 45:
                self.temps = 45
            self.simuler_evenement()
            time.sleep(self.intervalle_evenement)
        
        # Temps additionnel 1ère MT
        self.temps_additionnel_1 = random.randint(1, 4)
        print(f"\n{Fore.YELLOW}⏱️  Temps additionnel: +{self.temps_additionnel_1} minute{'s' if self.temps_additionnel_1 > 1 else ''}{Style.RESET_ALL}")
        
        for _ in range(random.randint(0, 2)):
            self.temps += 1
            self.simuler_evenement()
            time.sleep(self.intervalle_evenement)
        
        # Mi-temps
        self.afficher_mi_temps()
        
        # 2ème mi-temps
        print(f"\n{Fore.GREEN}🟢 2ÈME MI-TEMPS - C'EST REPARTI !{Style.RESET_ALL}")
        self.temps = 45
        
        while self.temps < 90:
            self.temps += random.randint(1, 4)
            if self.temps > 90:
                self.temps = 90
            self.simuler_evenement()
            time.sleep(self.intervalle_evenement)
        
        # Temps additionnel 2ème MT
        self.temps_additionnel_2 = random.randint(2, 6)
        print(f"\n{Fore.YELLOW}⏱️  Temps additionnel: +{self.temps_additionnel_2} minutes{Style.RESET_ALL}")
        
        for _ in range(random.randint(1, 4)):
            self.temps += 1
            self.simuler_evenement()
            time.sleep(self.intervalle_evenement)
        
        # Coup de sifflet final
        print(f"\n{Fore.RED}📯 COUP DE SIFFLET FINAL ! L'ARBITRE MET FIN AU MATCH !{Style.RESET_ALL}")
        time.sleep(2)
        
        self.afficher_statistiques_finales()

def creer_joueur_realiste(nom, poste, niveau_base=75):
    """Crée un joueur avec des stats réalistes selon son poste"""
    base = niveau_base + random.randint(-15, 15)
    
    if poste == "G":  # Gardien
        return Joueur(nom, poste, 
                     attaque=random.randint(10, 30),
                     defense=base + random.randint(0, 15),
                     vitesse=random.randint(40, 70),
                     technique=random.randint(60, 85),
                     physique=random.randint(70, 90),
                     mental=random.randint(70, 95),
                     age=random.randint(20, 35))
    
    elif poste in ["DC", "DD", "DG"]:  # Défenseurs
        return Joueur(nom, poste,
                     attaque=random.randint(30, 60),
                     defense=base + random.randint(0, 10),
                     vitesse=random.randint(55, 85),
                     technique=random.randint(50, 80),
                     physique=random.randint(75, 95),
                     mental=random.randint(65, 85),
                     age=random.randint(20, 35))
    
    elif poste in ["MDC", "MC", "MOC"]:  # Milieux
        return Joueur(nom, poste,
                     attaque=random.randint(50, 85),
                     defense=random.randint(45, 80),
                     vitesse=random.randint(60, 85),
                     technique=base + random.randint(0, 15),
                     physique=random.randint(65, 85),
                     mental=random.randint(70, 90),
                     age=random.randint(19, 33))
    
    else:  # Attaquants
        return Joueur(nom, poste,
                     attaque=base + random.randint(0, 15),
                     defense=random.randint(25, 50),
                     vitesse=random.randint(70, 95),
                     technique=random.randint(70, 95),
                     physique=random.randint(60, 85),
                     mental=random.randint(65, 85),
                     age=random.randint(18, 32))

# Création des équipes ultra-réalistes
def main():
    print(f"{Back.BLUE}{Fore.WHITE}{'🏟️ FOOTBALL SIMULATOR ULTRA-RÉALISTE 🏟️':^80}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{'Simulation FIFA-Style avec IA avancée':^80}{Style.RESET_ALL}")
    
    # Real Madrid
    real_joueurs = [
        creer_joueur_realiste("Courtois", "G", 88),
        creer_joueur_realiste("Carvajal", "DD", 84),
        creer_joueur_realiste("Militão", "DC", 82),
        creer_joueur_realiste("Alaba", "DC", 85),
        creer_joueur_realiste("Mendy", "DG", 80),
        creer_joueur_realiste("Casemiro", "MDC", 87),
        creer_joueur_realiste("Modrić", "MC", 88),
        creer_joueur_realiste("Kroos", "MC", 86),
        creer_joueur_realiste("Vinícius Jr", "AG", 86),
        creer_joueur_realiste("Benzema", "BU", 91),
        creer_joueur_realiste("Rodrygo", "AD", 82),
    ]
    
    # FC Barcelone  
    barca_joueurs = [
        creer_joueur_realiste("ter Stegen", "G", 87),
        creer_joueur_realiste("Dest", "DD", 76),
        creer_joueur_realiste("Araújo", "DC", 81),
        creer_joueur_realiste("García", "DC", 78),
        creer_joueur_realiste("Alba", "DG", 83),
        creer_joueur_realiste("Busquets", "MDC", 85),
        creer_joueur_realiste("de Jong", "MC", 84),
        creer_joueur_realiste("Gavi", "MC", 79),
        creer_joueur_realiste("Dembélé", "AD", 81),
        creer_joueur_realiste("Lewandowski", "BU", 91),
        creer_joueur_realiste("Ansu Fati", "AG", 80),
    ]
    
    # Création des équipes
    real_madrid = Equipe("Real Madrid CF", real_joueurs, "4-3-3", "Blanc", "Carlo Ancelotti")
    fc_barcelone = Equipe("FC Barcelone", barca_joueurs, "4-3-3", "Bleu/Rouge", "Xavi Hernández")
    
    # Configuration du match
    match = Match(
        real_madrid, 
        fc_barcelone,
        stade="Santiago Bernabéu",
        meteo=random.choice(["Ensoleillé", "Nuageux", "Pluvieux"]),
        temperature=random.randint(15, 28),
        affluence=random.randint(75000, 85000)
    )
    
    # Lancement de la simulation
    match.simuler()

if __name__ == "__main__":
    main()