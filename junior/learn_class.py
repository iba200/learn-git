import random
import time
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from colorama import init, Fore, Style, Back




class Player:
    """Represents a football player with detailed statistics."""
    
    EMOJI_MAP = {
        "G": "🧤", "RB": "🛡️", "CB": "🛡️", "LB": "🛡️",
        "DM": "⚙️", "CM": "⚙️", "AM": "⚙️",
        "RW": "🏃", "LW": "🏃", "ST": "⚽"
    }
    
    def __init__(
        self,
        name: str,
        position: str,
        attack: int,
        defense: int,
        speed: int = 70,
        technique: int = 70,
        physical: int = 70,
        mental: int = 70,
        age: int = 25
    ):
        self.name = name
        self.position = position
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.technique = technique
        self.physical = physical
        self.mental = mental
        self.age = age
        
        # Match statistics
        self.goals = 0
        self.assists = 0
        self.passes = 0
        self.successful_passes = 0
        self.shots = 0
        self.shots_on_target = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.red_card = False
        self.fatigue = 0
        self.form = random.randint(70, 100)
        self.distance_covered = 0.0
        self.duels_won = 0
        self.duels_lost = 0
        self.interceptions = 0
        self.tackles = 0
        self.crosses = 0
        self.corners_taken = 0
        self.rating = 6.0
        self.injured = False
        
        # Position on the field
        self.x = 0
        self.y = 0
        self.has_ball = False
    
    def get_overall_rating(self) -> int:
        """Calculate the player's overall rating."""
        return int(
            (
                self.attack +
                self.defense +
                self.speed +
                self.technique +
                self.physical +
                self.mental
            ) / 6
        )
    
    def get_fatigue_factor(self) -> float:
        """Calculate the impact of fatigue on performance."""
        return max(0.6, 1 - (self.fatigue / 150))
    
    def get_injury_risk(self) -> float:
        """Calculate injury risk based on age and fatigue."""
        age_factor = 0.02 * (self.age - 25) if self.age > 25 else 0
        return min(0.08, 0.01 + age_factor + self.fatigue / 1200)
    
    def move(self, action: str, zone: str = None):
        """Simulate player movement on the field."""
        if self.injured or self.red_card:
            return
        max_movement = 6
        if action == "attack":
            self.x += random.randint(3, 6)
            self.y += random.randint(-4, 4)
        elif action == "defense":
            self.x -= random.randint(2, 4)
            self.y += random.randint(-3, 3)
        elif action == "pass":
            self.y += random.randint(-5, 5)
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))
    
    def __str__(self) -> str:
        return f"{self.name}"


class Formation:
    """Defines a tactical formation with player positions."""
    
    def __init__(self, name: str, positions: Dict[str, Tuple[int, int]]):
        self.name = name
        self.positions = positions


# Predefined tactical formations
FORMATIONS = {
    "4-3-3": Formation("4-3-3", {
        "G": (5, 50),
        "RB": (20, 80),
        "CB1": (20, 60),
        "CB2": (20, 40),
        "LB": (20, 20),
        "DM": (40, 50),
        "CM1": (40, 70),
        "CM2": (40, 30),
        "RW": (70, 80),
        "ST": (70, 50),
        "LW": (70, 20)
    }),
    "4-4-2": Formation("4-4-2", {
        "G": (5, 50),
        "RB": (20, 80),
        "CB1": (20, 60),
        "CB2": (20, 40),
        "LB": (20, 20),
        "RM": (50, 80),
        "CM1": (50, 60),
        "CM2": (50, 40),
        "LM": (50, 20),
        "ST1": (75, 40),
        "ST2": (75, 60)
    })
}


class Team:
    """Represents a football team with players and tactics."""
    
    def __init__(
        self,
        name: str,
        players: List[Player],
        formation: str = "4-3-3",
        kit_color: str = "Blue",
        manager: str = "Coach"
    ):
        self.name = name
        self.players = players
        self.formation = FORMATIONS.get(formation, FORMATIONS["4-3-3"])
        self.kit_color = kit_color
        self.manager = manager
        self.points = 0
        
        # Team statistics
        self.goals_scored = 0
        self.goals_conceded = 0
        self.shots = 0
        self.shots_on_target = 0
        self.possession = 50.0
        self.passes = 0
        self.successful_passes = 0
        self.fouls = 0
        self.corners = 0
        self.offsides = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.substitutions = 0
        
        # Tactics
        self.mentality = "Balanced"
        self.pressing = 50
        self.width = 50
        
        self.opponent = None
        self.ball_holder = None
        self._position_players()
    
    def _position_players(self):
        """Position players according to the formation."""
        for i, player in enumerate(self.players[:11]):
            if i < len(self.formation.positions):
                player.x, player.y = list(self.formation.positions.values())[i]
    
    def set_opponent(self, opponent: 'Team'):
        self.opponent = opponent
    
    def get_random_player(self, position: str = None, zone: str = None) -> Optional[Player]:
        """Return a random player based on specified criteria."""
        candidates = [
            p for p in self.players[:11]
            if not p.red_card and not p.injured and
            (position is None or p.position == position)
        ]
        
        if zone:
            zone_positions = {
                "defense": ["CB", "RB", "LB", "DM"],
                "midfield": ["CM", "AM", "RM", "LM"],
                "attack": ["ST", "RW", "LW"]
            }
            candidates = [
                p for p in candidates
                if p.position in zone_positions.get(zone, [])
            ]
        
        if candidates:
            weights = [max(1, p.form - p.fatigue / 2) for p in candidates]
            return random.choices(candidates, weights=weights, k=1)[0]
        return None
    
    def get_best_shooter(self) -> Optional[Player]:
        """Return the best available shooter."""
        candidates = [p for p in self.players[:11] if not p.red_card and not p.injured]
        if candidates:
            return max(
                candidates,
                key=lambda p: p.attack * p.technique * p.get_fatigue_factor()
            )
        return None
    
    def make_substitution(self, player_out: Player, player_in: Player):
        """Perform a player substitution."""
        if self.substitutions >= 5 or player_out.red_card or player_out.injured:
            return False
        player_out.x, player_out.y = 0, 0
        player_in.x, player_in.y = player_out.x, player_out.y
        player_in.rating = 6.0
        player_in.fatigue = 0
        self.players[self.players.index(player_out)] = player_in
        self.substitutions += 1
        return True


class Commentator:
    """Manages dynamic and entertaining match commentary."""
    
    def __init__(self):
        self.goal_comments = [
            "⚽ GOOOOAAAL! A rocket into the top corner! 🚀",
            "⚽ WHAT A STRIKE! The stadium is on fire! 🔥",
            "⚽ UNBELIEVABLE! A goal for the history books! 📚",
            "⚽ THUNDERBOLT! The keeper is stunned! 😵",
            "⚽ PURE CLASS! World-class finish! 🌟",
            "⚽ MAGICAL MOMENT! The fans are ecstatic! 🎉",
            "⚽ GOAL OF THE CENTURY! Absolute banger! 💥"
        ]
        
        self.save_comments = [
            "🧤 INCREDIBLE SAVE! The keeper is a fortress! 🏰",
            "🧤 SUPERB STOP! Lightning reflexes! ⚡",
            "🧤 WHAT A SAVE! The crowd is speechless! 😲",
            "🧤 KEEPER'S MASTERCLASS! Denies a sure goal! 🛑",
            "🧤 MIRACLE SAVE! The stadium erupts! 🌋"
        ]
        
        self.action_comments = [
            "🪄 Silky smooth combination play!",
            "🏃 The wing is blazing!",
            "⚙️ TIKI-TAKA perfection!",
            "🔥 Intense pressing from the opposition!",
            "⚽ The ball dances between players!",
            "🚀 Epic run down the flank!",
            "🎯 Pinpoint cross into the box!",
            "💪 Titanic duel in the air!"
        ]
        
        self.foul_comments = [
            "😣 Ouch! That was a bone-crunching tackle!",
            "⚠️ Rough challenge! The ref's eyes are sharp!",
            "🔥 Heavy contact! Things are heating up!",
            "🪓 Lumberjack tackle! Watch those shins!",
            "😡 Heated moment! The crowd is buzzing!",
            "🟨 Yellow card offense! The ref means business!"
        ]
        
        self.crazy_comments = [
            "😱 OH NO! A fan sprints across in their boxers! 🩳",
            "🐦 A seagull snatches the ball! ⚽",
            "📱 The ref's checking their messages mid-game!",
            "🌭 A fan tosses a hot dog onto the pitch!",
            "🤸 The keeper does a cartwheel before the kick!",
            "🎤 The crowd's belting out a pop anthem!"
        ]
    
    def comment_goal(self, scorer: Player, team: Team, goal_type: str, minute: int) -> str:
        """Generate commentary for a goal scored."""
        base = random.choice(self.goal_comments)
        details = (
            f" {scorer.name} with a {goal_type.upper()} at the {minute}th minute! "
            f"Legendary strike for {team.name}! 🏆"
        )
        return f"{Fore.RED}{base}{Style.RESET_ALL}{details}"
    
    def comment_save(self, keeper: Player, shooter: Player) -> str:
        """Generate commentary for a goalkeeper save."""
        base = random.choice(self.save_comments)
        return f"{base} {keeper.name} shuts down {shooter.name} like a boss! 💪"
    
    def comment_crazy(self) -> str:
        """Generate a random entertaining comment."""
        return random.choice(self.crazy_comments)


class Match:
    """Simulates a football match with field visualization and events."""
    
    def __init__(
        self,
        team1: Team,
        team2: Team,
        stadium: str = "Municipal Stadium",
        weather: str = "Sunny",
        temperature: int = 22,
        attendance: int = 45000
    ):
        self.team1 = team1
        self.team2 = team2
        self.team1.set_opponent(self.team2)
        self.team2.set_opponent(self.team1)
        
        self.stadium = stadium
        self.weather = weather
        self.temperature = temperature
        self.attendance = attendance
        self.referee = random.choice(["Mr. Dubois", "Mr. Martin", "Ms. Leroux", "Mr. García"])
        
        self.time = 0
        self.halftime = False
        self.match_duration = 90
        self.first_half_added_time = 0
        self.second_half_added_time = 0
        
        self.real_time_duration = 45  # Seconds for simulation
        self.event_interval = 0.7
        
        self.commentator = Commentator()
        self.events = []
        self.ball_x = 50
        self.ball_y = 50
        self.ball_holder_team = None
    
    def display_field(self):
        """Display an ASCII field with player positions and ball."""
        os.system('cls' if os.name == 'nt' else 'clear')
        field = [[" " for _ in range(40)] for _ in range(20)]
        
        # Draw field boundaries
        field[0] = ["═" for _ in range(40)]
        field[-1] = ["═" for _ in range(40)]
        for i in range(1, 19):
            field[i][0] = "║"
            field[i][-1] = "║"
        
        # Place team1 players (blue)
        for player in self.team1.players[:11]:
            if not player.red_card and not player.injured:
                x = int(player.x * 19 / 100)
                y = int(player.y * 39 / 100)
                emoji = Player.EMOJI_MAP.get(player.position, "⚽")
                field[x][y] = f"{Fore.BLUE}{emoji}{Style.RESET_ALL}"
                if player.has_ball:
                    field[x][y] = f"{Fore.BLUE}⚽{Style.RESET_ALL}"
        
        # Place team2 players (yellow)
        for player in self.team2.players[:11]:
            if not player.red_card and not player.injured:
                x = int((100 - player.x) * 19 / 100)
                y = int((100 - player.y) * 39 / 100)
                emoji = Player.EMOJI_MAP.get(player.position, "⚽")
                field[x][y] = f"{Fore.YELLOW}{emoji}{Style.RESET_ALL}"
                if player.has_ball:
                    field[x][y] = f"{Fore.YELLOW}⚽{Style.RESET_ALL}"
        
        # Place the ball if no player has it
        if not any(p.has_ball for p in self.team1.players + self.team2.players):
            ball_x = int(self.ball_x * 19 / 100)
            ball_y = int(self.ball_y * 39 / 100)
            field[ball_x][ball_y] = "⚽"
        
        # Display the field
        print(f"\n{Back.GREEN}{' ⚽ FIELD ⚽ ':^40}{Style.RESET_ALL}")
        for line in field:
            print("".join(line))
        print(
            f"{Fore.GREEN}Score: {self.team1.name} {self.team1.goals_scored} - "
            f"{self.team2.goals_scored} {self.team2.name}{Style.RESET_ALL}"
        )
        print(
            f"Time: {self.time}' | Possession: "
            f"{self.team1.possession:.0f}% - {self.team2.possession:.0f}%"
        )
    
    def display_prematch_info(self):
        """Display pre-match information."""
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═'*80}{Style.RESET_ALL}")
        print(
            f"{Back.BLUE}{Fore.WHITE}"
            f"{'⚽ FOOTBALL SIMULATOR - LIVE MATCH':^80}"
            f"{Style.RESET_ALL}"
        )
        print(f"{Back.BLUE}{Fore.WHITE}{'═'*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}🏟️ Venue:{Style.RESET_ALL} {self.stadium}")
        print(f"{Fore.CYAN}🌤️ Weather:{Style.RESET_ALL} {self.weather}, {self.temperature}°C")
        print(f"{Fore.CYAN}👥 Attendance:{Style.RESET_ALL} {self.attendance:,} spectators")
        print(f"{Fore.CYAN}🧑‍⚖️ Referee:{Style.RESET_ALL} {self.referee}")
        print(f"{Fore.CYAN}🕐 Time:{Style.RESET_ALL} {datetime.now().strftime('%H:%M')}")
        
        print(f"\n{Back.GREEN}{Fore.WHITE} ⚽ TEAMS ⚽ {Style.RESET_ALL}")
        print(f"\n{Fore.MAGENTA}🏠 {self.team1.name.upper()}{Style.RESET_ALL} ({self.team1.formation.name})")
        print(f"   👨‍💼 Manager: {self.team1.manager}")
        print(f"   👕 Kit: {self.team1.kit_color}")
        
        print(f"\n{Fore.YELLOW}✈️ {self.team2.name.upper()}{Style.RESET_ALL} ({self.team2.formation.name})")
        print(f"   👨‍💼 Manager: {self.team2.manager}")
        print(f"   👕 Kit: {self.team2.kit_color}")
        
        print(f"\n{Back.WHITE}{Fore.BLACK} ⚽ LINE-UPS ⚽ {Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}{self.team1.name}:{Style.RESET_ALL}")
        for i, player in enumerate(self.team1.players[:11], 1):
            print(f"  {i:2d}. {player.name:15} ({player.position}) - Rating: {player.get_overall_rating()}")
        
        print(f"\n{Fore.YELLOW}{self.team2.name}:{Style.RESET_ALL}")
        for i, player in enumerate(self.team2.players[:11], 1):
            print(f"  {i:2d}. {player.name:15} ({player.position}) - Rating: {player.get_overall_rating()}")
        
        print(f"\n{Fore.GREEN}🎮 Press Enter to start the match...{Style.RESET_ALL}")
        input()
    
    def calculate_probabilities(self, attacking_team: Team, action_type: str) -> float:
        """Calculate event probabilities based on context."""
        active_players = [p for p in attacking_team.players[:11] if not p.red_card and not p.injured]
        if not active_players:
            return 0.0
        avg_rating = sum(p.get_overall_rating() for p in active_players) / len(active_players)
        avg_fatigue = sum(p.fatigue for p in active_players) / len(active_players)
        possession = attacking_team.possession / 100
        
        weather_factor = {
            "Sunny": 1.0,
            "Cloudy": 0.95,
            "Rainy": 0.80,
            "Windy": 0.85
        }.get(self.weather, 1.0)
        
        fatigue_factor = max(0.65, 1 - avg_fatigue / 130)
        
        if self.time > 75:
            fatigue_factor *= 0.80
        if self.time > 85:
            fatigue_factor *= 0.70
            
        base_multiplier = (avg_rating / 100) * weather_factor * fatigue_factor * possession
        
        probabilities = {
            "goal": max(0.01, 0.05 * base_multiplier),
            "shot_on_target": max(0.03, 0.10 * base_multiplier),
            "shot_off_target": max(0.05, 0.15 * base_multiplier)
        }
        
        return probabilities.get(action_type, base_multiplier)
    
    def move_ball(self, player: Player, action: str):
        """Move the ball based on player action."""
        if action == "attack":
            self.ball_x = player.x + random.randint(1, 3)
            self.ball_y = player.y + random.randint(-2, 2)
        elif action == "pass":
            self.ball_x += random.randint(-2, 2)
            self.ball_y += random.randint(-3, 3)
        elif action == "shot":
            self.ball_x = 95 if player in self.team1.players else 5
            self.ball_y = random.randint(40, 60)
        self.ball_x = max(0, min(100, self.ball_x))
        self.ball_y = max(0, min(100, self.ball_y))
    
    def assign_ball(self, team: Optional[Team], player: Optional[Player] = None):
        """Assign the ball to a player or team."""
        for p in self.team1.players + self.team2.players:
            p.has_ball = False
        if player:
            player.has_ball = True
            self.ball_holder_team = team
            self.ball_x = player.x
            self.ball_y = player.y
        else:
            self.ball_holder_team = team
    
    def simulate_shot(self, shooter: Player, keeper: Player, shot_type: str = "strike") -> str:
        """Simulate a shot with realistic calculations."""
        shooter.move("attack")
        self.move_ball(shooter, "shot")
        shot_accuracy = (shooter.attack + shooter.technique) * shooter.get_fatigue_factor()
        distance = random.randint(5, 35)
        difficult_angle = random.random() < 0.30
        
        difficulty = 100
        if distance > 25:
            difficulty += 30
        if difficult_angle:
            difficulty += 20
        if shot_type == "volley":
            difficulty += 25
        elif shot_type == "header":
            difficulty += 15
            
        keeper_quality = keeper.defense * keeper.get_fatigue_factor()
        
        goal_chance = max(5, shot_accuracy - difficulty + random.randint(-10, 10))
        save_chance = keeper_quality + random.randint(-8, 8)
        
        if goal_chance > save_chance + 30:
            return "goal"
        elif goal_chance > save_chance:
            return "save"
        elif random.random() < 0.60:
            return "on_target"
        return "off_target"
    
    def simulate_event(self):
        """Simulate a match event with realistic visualization."""
        self.display_field()
        
        # Random entertaining event
        if random.random() < 0.02:
            print(f"{Fore.MAGENTA}{self.commentator.comment_crazy()}{Style.RESET_ALL}")
            time.sleep(2)
        
        # Check for substitutions
        if random.random() < 0.05 and self.time > 60:
            for team in [self.team1, self.team2]:
                tired_player = min(
                    [p for p in team.players[:11] if not p.red_card and not p.injured],
                    key=lambda p: p.get_fatigue_factor(),
                    default=None
                )
                if tired_player and len(team.players) > 11:
                    sub = team.players[11]
                    if team.make_substitution(tired_player, sub):
                        print(
                            f"{Fore.YELLOW}{self.time}' - 🔄 Substitution for {team.name}: "
                            f"{tired_player.name} OUT, {sub.name} IN{Style.RESET_ALL}"
                        )
                        time.sleep(1)
        
        momentum = (self.team1.goals_scored - self.team2.goals_scored) * 0.06
        possession_adj = self.team1.possession + momentum * 3
        
        attacking_team = random.choices(
            [self.team1, self.team2],
            weights=[possession_adj, 100 - possession_adj],
            k=1
        )[0]
        defending_team = attacking_team.opponent
        
        possession_change = random.gauss(0, 1.2)
        if random.random() < 0.06:
            possession_change = random.gauss(0, 5)
            
        attacking_team.possession += possession_change
        attacking_team.possession = max(35, min(65, attacking_team.possession))
        defending_team.possession = 100 - attacking_team.possession
        
        base_weights = [1.5, 8, 6, 25, 8, 6, 3, 1, 2, 40]
        
        if self.time > 80:
            base_weights[0] *= 1.5
            base_weights[4] *= 1.3
            
        if abs(self.team1.goals_scored - self.team2.goals_scored) >= 3:
            base_weights[0] *= 0.60
            base_weights[-1] *= 1.5
        
        event = random.choices(
            ["goal", "shot_on_target", "shot_off_target", "pass", "foul",
             "corner", "card", "injury", "offside", "nothing"],
            weights=base_weights,
            k=1
        )[0]
        
        time_str = f"{Fore.YELLOW}{self.time:2d}'{Style.RESET_ALL}"
        
        # Assign ball to a player if not already assigned
        if not self.ball_holder_team:
            self.assign_ball(attacking_team, attacking_team.get_random_player())
        
        if event == "goal":
            self.handle_goal(attacking_team, defending_team, time_str)
        elif event == "shot_on_target":
            self.handle_shot_on_target(attacking_team, defending_team, time_str)
        elif event == "shot_off_target":
            self.handle_shot_off_target(attacking_team, time_str)
        elif event == "pass":
            self.handle_pass(attacking_team, time_str)
        elif event == "foul":
            self.handle_foul(attacking_team, defending_team, time_str)
        elif event == "corner":
            self.handle_corner(attacking_team, time_str)
        elif event == "card":
            self.handle_card(attacking_team, time_str)
        elif event == "injury":
            self.handle_injury(attacking_team, time_str)
        elif event == "offside":
            self.handle_offside(attacking_team, time_str)
        
        for player in attacking_team.players[:11]:
            if not player.red_card and not player.injured:
                player.fatigue += random.uniform(0.3, 0.5)
                player.distance_covered += random.uniform(0.08, 0.20)
    
    def handle_goal(self, attacking_team: Team, defending_team: Team, time_str: str):
        """Handle a goal event with realistic details."""
        goal_types = ["strike", "header", "volley", "free_kick", "penalty", "lob", "counter_attack"]
        type_weights = [35, 25, 10, 8, 5, 8, 15]
        
        goal_zone = random.choice(["box", "six_yard", "edge_box", "long_range"])
        
        if goal_zone == "long_range":
            type_weights = [45, 2, 8, 20, 0, 15, 10]
        elif goal_zone == "six_yard":
            type_weights = [10, 50, 5, 0, 0, 5, 30]
            
        goal_type = random.choices(goal_types, weights=type_weights, k=1)[0]
        
        if goal_type == "free_kick":
            scorer = attacking_team.get_best_shooter()
        elif goal_type == "penalty":
            scorer = attacking_team.get_best_shooter()
        elif goal_type == "header":
            scorer = attacking_team.get_random_player(zone="attack") or attacking_team.get_random_player()
        else:
            scorer = (
                attacking_team.get_random_player(zone="attack") or
                attacking_team.get_random_player(zone="midfield")
            )
        
        if not scorer:
            return
            
        scorer.move("attack")
        self.assign_ball(attacking_team, scorer)
        
        assister = None
        if goal_type not in ["free_kick", "penalty"] and random.random() < 0.60:
            assister = attacking_team.get_random_player()
            if assister == scorer:
                assister = None
            else:
                assister.move("pass")
        
        scorer.goals += 1
        scorer.shots += 1
        scorer.shots_on_target += 1
        scorer.fatigue += random.randint(4, 8)
        scorer.rating += random.uniform(0.7, 1.4)
        
        if assister:
            assister.assists += 1
            assister.passes += 1
            assister.successful_passes += 1
            assister.rating += random.uniform(0.4, 0.8)
        
        attacking_team.goals_scored += 1
        attacking_team.shots += 1
        attacking_team.shots_on_target += 1
        defending_team.goals_conceded += 1
        
        keeper = defending_team.get_random_player(position="G")
        if keeper:
            keeper.rating -= random.uniform(0.5, 1.0)
        
        print(f"\n{time_str} ═══════════════════════════════════")
        print(self.commentator.comment_goal(scorer, attacking_team, goal_type, self.time))
        
        if assister:
            print(f"   🎯 {Fore.BLUE}Assist by {assister.name}{Style.RESET_ALL}")
        
        print(f"   📍 Zone: {goal_zone.replace('_', ' ').title()}")
        print(
            f"   ⚽ {Fore.GREEN}Score: {self.team1.name} {self.team1.goals_scored} - "
            f"{self.team2.goals_scored} {self.team2.name}{Style.RESET_ALL}"
        )
        print(f"════════════════════════════════════")
        
        crowd_reactions = [
            "🎉 The crowd is going ABSOLUTELY WILD!",
            "😶 Stunned silence in the stands!",
            "🎉 Fans are throwing confetti everywhere!",
            "🎉 Pure ecstasy in the stadium!"
        ]
        print(f"   🎭 {random.choice(crowd_reactions)}")
        
        self.assign_ball(None, None)  # Reset ball to center
        self.ball_x = 50
        self.ball_y = 50
        self.display_field()
        time.sleep(2)
    
    def handle_shot_on_target(self, attacking_team: Team, defending_team: Team, time_str: str):
        """Handle shots on target with goalkeeper saves."""
        shooter = (
            attacking_team.get_random_player(zone="attack") or
            attacking_team.get_random_player()
        )
        keeper = defending_team.get_random_player(position="G")
        
        if not shooter or not keeper:
            return
            
        shooter.move("attack")
        self.assign_ball(attacking_team, shooter)
        shot_types = ["strike", "header", "volley", "lob"]
        shot_type = random.choice(shot_types)
        
        shooter.shots += 1
        shooter.shots_on_target += 1
        shooter.fatigue += random.randint(2, 5)
        attacking_team.shots += 1
        attacking_team.shots_on_target += 1
        
        keeper.fatigue += random.randint(3, 6)
        keeper.rating += random.uniform(0.2, 0.5)
        
        save_types = ["dive", "reflex", "block", "parry", "leap"]
        save_type = random.choice(save_types)
        
        print(f"{time_str} - 🎯 {Fore.CYAN}Shot by {shooter.name}{Style.RESET_ALL} ({attacking_team.name})")
        print(f"   {self.commentator.comment_save(keeper, shooter)}")
        print(f"   🧤 {save_type.title()} save by {keeper.name}")
        
        if random.random() < 0.10:
            print(f"   ⚡ Rebound in the box! DANGER!")
        
        self.assign_ball(defending_team, keeper)
        self.display_field()
    
    def handle_shot_off_target(self, attacking_team: Team, time_str: str):
        """Handle shots off target."""
        shooter = (
            attacking_team.get_random_player(zone="attack") or
            attacking_team.get_random_player()
        )
        if not shooter:
            return
            
        shooter.move("attack")
        self.assign_ball(attacking_team, shooter)
        directions = ["wide", "over", "off the post", "off the bar"]
        direction = random.choice(directions)
        
        shooter.shots += 1
        shooter.fatigue += random.randint(1, 3)
        attacking_team.shots += 1
        
        if direction in ["off the post", "off the bar"]:
            print(
                f"{time_str} - 😱 {Fore.YELLOW}OH! {shooter.name}'s shot {direction}! "
                f"So close!{Style.RESET_ALL}"
            )
            shooter.rating += 0.3
        else:
            print(f"{time_str} - 🎯 Shot {direction} by {shooter.name} ({attacking_team.name})")
        
        self.assign_ball(attacking_team.opponent, None)
        self.display_field()
    
    def handle_pass(self, attacking_team: Team, time_str: str):
        """Handle passes and build-up play."""
        passer = attacking_team.get_random_player()
        if not passer:
            return
            
        passer.move("pass")
        self.assign_ball(attacking_team, passer)
        pass_types = ["short", "long", "cross", "one-two", "backheel"]
        pass_weights = [45, 20, 15, 15, 5]
        
        if passer.position in ["CB", "DM"]:
            pass_weights = [30, 35, 10, 20, 5]
        elif passer.position in ["RW", "LW"]:
            pass_weights = [20, 15, 45, 15, 5]
            
        pass_type = random.choices(pass_types, weights=pass_weights, k=1)[0]
        
        passer.passes += 1
        success_rate = (passer.technique + passer.mental) / 140
        is_successful = random.random() < success_rate
        
        if is_successful:
            passer.successful_passes += 1
            attacking_team.successful_passes += 1
            passer.rating += 0.07
            new_holder = attacking_team.get_random_player()
            if new_holder and new_holder != passer:
                self.assign_ball(attacking_team, new_holder)
        
        attacking_team.passes += 1
        
        if random.random() < 0.10:
            adjective = random.choice(["BRILLIANT", "FANTASTIC", "PRECISE", "PINPOINT"])
            if pass_type == "long" and is_successful:
                print(f"{time_str} - 📐 {adjective} long pass by {passer.name}")
            elif pass_type == "cross":
                print(f"{time_str} - 🎯 Cross by {passer.name} into the DANGER ZONE!")
                attacking_team.corners += random.choice([0, 0, 0, 1])
        
        if not is_successful:
            self.assign_ball(attacking_team.opponent, None)
        
        self.display_field()
    
    def handle_foul(self, attacking_team: Team, defending_team: Team, time_str: str):
        """Handle fouls with realistic outcomes."""
        offender = attacking_team.get_random_player()
        victim = defending_team.get_random_player()
        
        if not offender or not victim:
            return
        
        offender.move("defense")
        self.assign_ball(attacking_team, offender)
        foul_types = ["tackle", "push", "charge", "kick", "handball", "unsportsmanlike"]
        severities = ["minor", "moderate", "severe"]
        
        if offender.position in ["CB", "RB", "LB"]:
            foul_type = random.choices(foul_types, weights=[40, 20, 20, 10, 5, 5], k=1)[0]
        else:
            foul_type = random.choices(foul_types, weights=[20, 30, 15, 15, 15, 5], k=1)[0]
        
        severity = random.choices(severities, weights=[70, 20, 10], k=1)[0]
        
        zones = ["attacking_box", "30m", "midfield", "defensive_box"]
        zone = random.choice(zones)
        
        offender.fouls += 1
        offender.fatigue += random.randint(1, 4)
        attacking_team.fouls += 1
        
        sanction = "none"
        if severity == "severe" or (severity == "moderate" and random.random() < 0.30):
            if offender.yellow_cards == 1:
                sanction = "red"
                offender.red_card = True
                attacking_team.red_cards += 1
                offender.rating -= 2.5
            elif random.random() < 0.70:
                sanction = "yellow"
                offender.yellow_cards += 1
                attacking_team.yellow_cards += 1
                offender.rating -= 0.6
        elif severity == "moderate" and random.random() < 0.12:
            sanction = "yellow"
            offender.yellow_cards += 1
            attacking_team.yellow_cards += 1
            offender.rating -= 0.6
        
        if sanction == "red":
            print(
                f"{time_str} - 🟥 {Fore.RED}RED CARD! {offender.name} is sent off!"
                f"{Style.RESET_ALL}"
            )
            print(f"   ⚡ {attacking_team.name} down to 10 men!")
        elif sanction == "yellow":
            print(
                f"{time_str} - 🟨 Yellow card for {offender.name} ({attacking_team.name}) - "
                f"{foul_type}"
            )
        elif severity == "severe":
            print(f"{time_str} - ⚠️ Harsh foul by {offender.name} on {victim.name}")
        elif random.random() < 0.20:
            print(f"{time_str} - Foul by {offender.name} on {victim.name}")
        
        if zone == "attacking_box" and severity in ["moderate", "severe"]:
            if random.random() < 0.10:
                print(f"   ⚽ PENALTY for {defending_team.name}!")
                time.sleep(1)
                self.handle_penalty(defending_team, attacking_team)
        elif zone in ["30m", "attacking_box"]:
            print(f"   🎯 Dangerous free kick for {defending_team.name}")
            if random.random() < 0.07:
                time.sleep(0.5)
                self.handle_free_kick(defending_team, attacking_team)
        
        self.assign_ball(defending_team, None)
        self.display_field()
    
    def handle_penalty(self, shooting_team: Team, defending_team: Team):
        """Handle a penalty sequence."""
        shooter = shooting_team.get_best_shooter()
        keeper = defending_team.get_random_player(position="G")
        
        if not shooter or not keeper:
            return
        
        shooter.move("attack")
        self.assign_ball(shooting_team, shooter)
        print(f"   🎯 {shooter.name} vs {keeper.name}")
        print(f"   🔥 The stadium holds its breath...")
        time.sleep(2)
        
        shooter_accuracy = shooter.attack + shooter.technique + shooter.mental
        keeper_quality = keeper.defense + keeper.mental
        
        goal_chance = shooter_accuracy + random.randint(-20, 20)
        save_chance = keeper_quality + random.randint(-10, 30)
        
        if goal_chance > save_chance + 25:
            shooter.goals += 1
            shooter.shots += 1
            shooter.shots_on_target += 1
            shooting_team.goals_scored += 1
            defending_team.goals_conceded += 1
            shooter.rating += 1.0
            keeper.rating -= 0.4
            print(f"   ⚽ {Fore.GREEN}GOAL! {shooter.name} smashes it!{Style.RESET_ALL}")
            print(
                f"   📊 Score: {self.team1.name} {self.team1.goals_scored} - "
                f"{self.team2.goals_scored} {self.team2.name}"
            )
        elif save_chance > goal_chance:
            keeper.rating += 1.3
            shooter.rating -= 0.7
            shooter.shots += 1
            shooter.shots_on_target += 1
            print(f"   🧤 {Fore.YELLOW}EPIC SAVE! {keeper.name} stops the penalty!{Style.RESET_ALL}")
            print(f"   🎭 The crowd goes wild!")
        else:
            shooter.shots += 1
            shooter.rating -= 0.9
            print(f"   😱 {Fore.RED}MISSED! {shooter.name} blasts it over!{Style.RESET_ALL}")
        
        self.assign_ball(None, None)
        self.ball_x = 50
        self.ball_y = 50
        self.display_field()
    
    def handle_free_kick(self, shooting_team: Team, defending_team: Team):
        """Handle dangerous free kicks."""
        shooter = shooting_team.get_best_shooter()
        keeper = defending_team.get_random_player(position="G")
        
        if not shooter or not keeper:
            return
        
        shooter.move("attack")
        self.assign_ball(shooting_team, shooter)
        print(f"   🎯 Free kick taken by {shooter.name}...")
        
        fk_types = ["direct", "curled", "powerful", "placed"]
        fk_type = random.choice(fk_types)
        
        goal_chance = (shooter.attack + shooter.technique) * 0.70 + random.randint(-10, 10)
        
        if goal_chance > 80:
            shooter.goals += 1
            shooting_team.goals_scored += 1
            defending_team.goals_conceded += 1
            shooter.rating += 1.4
            print(f"   ⚽ {Fore.GREEN}STUNNING! {fk_type.title()} free kick in the top corner!{Style.RESET_ALL}")
        elif goal_chance > 60:
            print(f"   🧤 Great save by the keeper on the {fk_type} free kick")
            keeper.rating += 0.4
        else:
            print(f"   📐 {fk_type.title()} free kick hits the wall or goes wide!")
        
        self.assign_ball(defending_team, None)
        self.display_field()
    
    def handle_corner(self, attacking_team: Team, time_str: str):
        """Handle corners."""
        attacking_team.corners += 1
        corner_taker = attacking_team.get_random_player()
        
        if corner_taker:
            corner_taker.move("pass")
            self.assign_ball(attacking_team, corner_taker)
            corner_taker.corners_taken += 1
            corner_taker.crosses += 1
        
        print(f"{time_str} - 📐 Corner for {Fore.CYAN}{attacking_team.name}{Style.RESET_ALL}")
        
        if random.random() < 0.12:
            print(f"   🎯 Dangerous cross into the box!")
            if random.random() < 0.10:
                time.sleep(0.5)
                self.handle_corner_goal(attacking_team)
        
        self.assign_ball(attacking_team.opponent, None)
        self.display_field()
    
    def handle_corner_goal(self, attacking_team: Team):
        """Handle a goal from a corner."""
        scorer = attacking_team.get_random_player(zone="attack") or attacking_team.get_random_player()
        if not scorer:
            return
        
        scorer.move("attack")
        self.assign_ball(attacking_team, scorer)
        scorer.goals += 1
        attacking_team.goals_scored += 1
        attacking_team.opponent.goals_conceded += 1
        scorer.rating += 1.2
        
        print(f"   ⚽ {Fore.GREEN}GOAL FROM CORNER! {scorer.name} rises highest!{Style.RESET_ALL}")
        print(
            f"   📊 Score: {self.team1.name} {self.team1.goals_scored} - "
            f"{self.team2.goals_scored} {self.team2.name}"
        )
        
        self.assign_ball(None, None)
        self.ball_x = 50
        self.ball_y = 50
        self.display_field()
    
    def handle_card(self, attacking_team: Team, time_str: str):
        """Handle isolated card events."""
        player = attacking_team.get_random_player()
        if not player:
            return
        
        player.move("defense")
        self.assign_ball(attacking_team, player)
        if random.random() < 0.08 and player.yellow_cards < 2:
            player.yellow_cards += 1
            player.rating -= 0.5
            print(f"{time_str} - 🟨 Yellow card for {player.name} (dissent or sneaky tackle!)")
        
        self.assign_ball(attacking_team.opponent, None)
        self.display_field()
    
    def handle_injury(self, attacking_team: Team, time_str: str):
        """Handle injury events."""
        player = attacking_team.get_random_player()
        if not player:
            return
        
        player.move("defense")
        self.assign_ball(attacking_team, player)
        if random.random() < player.get_injury_risk():
            player.injured = True
            player.rating -= 1.0
            print(f"{time_str} - 🤕 INJURY! {player.name} is down and can't continue!")
            if len(attacking_team.players) > 11:
                sub = attacking_team.players[11]
                if attacking_team.make_substitution(player, sub):
                    print(
                        f"   🔄 Substitution for {attacking_team.name}: "
                        f"{player.name} OUT, {sub.name} IN"
                    )
        
        self.assign_ball(attacking_team.opponent, None)
        self.display_field()
    
    def handle_offside(self, attacking_team: Team, time_str: str):
        """Handle offside events."""
        attacking_team.offsides += 1
        offside_player = attacking_team.get_random_player(zone="attack")
        if offside_player:
            offside_player.move("attack")
            self.assign_ball(attacking_team, offside_player)
            print(f"{time_str} - 🚩 Offside! {offside_player.name} caught napping!")
        
        self.assign_ball(attacking_team.opponent, None)
        self.display_field()
    
    def display_halftime(self):
        """Display halftime statistics."""
        print(f"\n{Back.YELLOW}{Fore.BLACK}{'⏸️ HALFTIME':^80}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}📊 FIRST HALF STATS:{Style.RESET_ALL}")
        print(f"{'='*60}")
        
        print(f"{Fore.MAGENTA}{self.team1.name:20}{Style.RESET_ALL} | {Fore.YELLOW}{self.team2.name:20}{Style.RESET_ALL}")
        print(f"{'-'*60}")
        print(f"{'Goals:':15} {self.team1.goals_scored:^10} | {self.team2.goals_scored:^10}")
        print(f"{'Shots:':15} {self.team1.shots:^10} | {self.team2.shots:^10}")
        print(f"{'On Target:':15} {self.team1.shots_on_target:^10} | {self.team2.shots_on_target:^10}")
        print(f"{'Possession:':15} {self.team1.possession:^8.0f}% | {self.team2.possession:^8.0f}%")
        print(f"{'Corners:':15} {self.team1.corners:^10} | {self.team2.corners:^10}")
        print(f"{'Fouls:':15} {self.team1.fouls:^10} | {self.team2.fouls:^10}")
        print(f"{'Yellow Cards:':15} {self.team1.yellow_cards:^10} | {self.team2.yellow_cards:^10}")
        print(f"{'Red Cards:':15} {self.team1.red_cards:^10} | {self.team2.red_cards:^10}")
        print(f"{'='*60}")
        
        print(f"\n⭐ {Fore.CYAN}STANDOUT PLAYERS:{Style.RESET_ALL}")
        all_players = self.team1.players[:11] + self.team2.players[:11]
        top_players = sorted(
            [p for p in all_players if p.rating >= 7.0],
            key=lambda x: x.rating,
            reverse=True
        )[:3]
        
        for i, player in enumerate(top_players, 1):
            team = self.team1 if player in self.team1.players else self.team2
            print(f"   {i}. {player.name} ({team.name}) - Rating: {player.rating:.1f}")
        
        print(f"\n{Fore.GREEN}⚽ Halftime - Players refuel and regroup!{Style.RESET_ALL}")
        time.sleep(3)
    
    def display_final_stats(self):
        """Display final match statistics."""
        print(f"\n{Back.GREEN}{Fore.WHITE}{'🏁 MATCH ENDED - STATS':^80}{Style.RESET_ALL}")
        
        print(f"\n{Back.WHITE}{Fore.BLACK}{'FINAL SCORE':^80}{Style.RESET_ALL}")
        print(
            f"{Fore.MAGENTA}{self.team1.name:^25}{Style.RESET_ALL} "
            f"{self.team1.goals_scored:^5} - {self.team2.goals_scored:^5} "
            f"{Fore.YELLOW}{self.team2.name:^25}{Style.RESET_ALL}"
        )
        
        if self.team1.goals_scored > self.team2.goals_scored:
            print(f"\n🏆 {Fore.GREEN}EPIC VICTORY FOR {self.team1.name.upper()}!{Style.RESET_ALL}")
            self.team1.points += 3
        elif self.team2.goals_scored > self.team1.goals_scored:
            print(f"\n🏆 {Fore.GREEN}EPIC VICTORY FOR {self.team2.name.upper()}!{Style.RESET_ALL}")
            self.team2.points += 3
        else:
            print(f"\n🤝 {Fore.YELLOW}DRAMATIC DRAW!{Style.RESET_ALL}")
            self.team1.points += 1
            self.team2.points += 1
        
        print(f"\n{Back.BLUE}{Fore.WHITE}{'DETAILED STATS':^80}{Style.RESET_ALL}")
        print(f"{'='*80}")
        print(
            f"{'Statistic':^20} | {self.team1.name:^25} | {self.team2.name:^25}"
        )
        print(f"{'-'*80}")
        
        stats = [
            ("Goals", self.team1.goals_scored, self.team2.goals_scored),
            ("Shots", self.team1.shots, self.team2.shots),
            ("Shots on Target", self.team1.shots_on_target, self.team2.shots_on_target),
            ("Possession %", f"{self.team1.possession:.0f}", f"{self.team2.possession:.0f}"),
            ("Passes", self.team1.passes, self.team2.passes),
            (
                "Pass Success %",
                f"{(self.team1.successful_passes/max(1, self.team1.passes)*100):.0f}",
                f"{(self.team2.successful_passes/max(1, self.team2.passes)*100):.0f}"
            ),
            ("Corners", self.team1.corners, self.team2.corners),
            ("Offsides", self.team1.offsides, self.team2.offsides),
            ("Fouls", self.team1.fouls, self.team2.fouls),
            ("Yellow Cards", self.team1.yellow_cards, self.team2.yellow_cards),
            ("Red Cards", self.team1.red_cards, self.team2.red_cards),
        ]
        
        for stat, val1, val2 in stats:
            print(f"{stat:^20} | {str(val1):^25} | {str(val2):^25}")
        
        print(f"{'='*80}")
        
        print(f"\n⚽ {Fore.GREEN}GOALSCORERS:{Style.RESET_ALL}")
        all_scorers = [
            (p, self.team1) for p in self.team1.players if p.goals > 0
        ] + [
            (p, self.team2) for p in self.team2.players if p.goals > 0
        ]
        
        if all_scorers:
            all_scorers.sort(key=lambda x: x[0].goals, reverse=True)
            for player, team in all_scorers:
                print(
                    f"   🥅 {player.name} ({team.name}) - "
                    f"{player.goals} goal{'s' if player.goals > 1 else ''}"
                )
        else:
            print("   No goals scored in this match")
        
        print(f"\n⭐ {Fore.CYAN}PLAYER RATINGS:{Style.RESET_ALL}")
        
        for team in [self.team1, self.team2]:
            print(f"\n{Fore.MAGENTA if team == self.team1 else Fore.YELLOW}{team.name}:{Style.RESET_ALL}")
            rated_players = sorted(team.players[:11], key=lambda x: x.rating, reverse=True)
            
            for player in rated_players:
                rating_color = (
                    Fore.GREEN if player.rating >= 7.5 else
                    Fore.YELLOW if player.rating >= 6.5 else
                    Fore.RED
                )
                cards = (
                    " 🟥" if player.red_card else
                    f" 🟨x{player.yellow_cards}" if player.yellow_cards > 0 else
                    ""
                )
                injury = " 🤕" if player.injured else ""
                player_stats = (
                    f"({player.goals}⚽, {player.shots}🎯, {player.fouls}⚠️)"
                )
                print(
                    f"   {player.name:15} ({player.position:3}) - "
                    f"Rating: {rating_color}{player.rating:4.1f}{Style.RESET_ALL} "
                    f"{player_stats}{cards}{injury}"
                )
        
        all_players = self.team1.players[:11] + self.team2.players[:11]
        man_of_match = max(all_players, key=lambda x: x.rating)
        motm_team = self.team1 if man_of_match in self.team1.players else self.team2
        
        print(
            f"\n🏅 {Fore.YELLOW}MAN OF THE MATCH: {man_of_match.name} ({motm_team.name}) - "
            f"Rating: {man_of_match.rating:.1f}{Style.RESET_ALL}"
        )
        
        print(f"\n{Back.BLACK}{Fore.WHITE}{'Thanks for following the live match!':^80}{Style.RESET_ALL}")
        print(f"{Back.BLACK}{Fore.WHITE}{'⚽ FOOTBALL SIMULATOR - END':^80}{Style.RESET_ALL}")
    
    def simulate(self):
        """Simulate a full match with visualization and atmosphere."""
        self.display_prematch_info()
        
        print(f"\n{Fore.GREEN}🔴 LIVE - KICK-OFF!{Style.RESET_ALL}")
        print(f"⚽ {self.referee} starts the match with authority!")
        print(f"🌡️ Temperature: {self.temperature}°C - Conditions: {self.weather}")
        self.assign_ball(self.team1, self.team1.get_random_player())
        time.sleep(1)
        
        while self.time < 45:
            self.time += random.randint(1, 3)
            if self.time > 45:
                self.time = 45
            self.simulate_event()
            time.sleep(self.event_interval)
        
        self.first_half_added_time = random.randint(1, 3)
        print(
            f"\n{Fore.YELLOW}⏱️ Added time: +{self.first_half_added_time} "
            f"minute{'s' if self.first_half_added_time > 1 else ''}{Style.RESET_ALL}"
        )
        
        for _ in range(random.randint(0, 2)):
            self.time += 1
            self.simulate_event()
            time.sleep(self.event_interval)
        
        self.display_halftime()
        
        print(f"\n{Fore.GREEN}🟢 SECOND HALF - IT'S ON!{Style.RESET_ALL}")
        self.time = 45
        self.assign_ball(self.team2, self.team2.get_random_player())
        
        while self.time < 90:
            self.time += random.randint(1, 3)
            if self.time > 90:
                self.time = 90
            self.simulate_event()
            time.sleep(self.event_interval)
        
        self.second_half_added_time = random.randint(2, 5)
        print(
            f"\n{Fore.YELLOW}⏱️ Added time: +{self.second_half_added_time} "
            f"minutes{Style.RESET_ALL}"
        )
        
        for _ in range(random.randint(1, 3)):
            self.time += 1
            self.simulate_event()
            time.sleep(self.event_interval)
        
        print(f"\n{Fore.RED}📯 FINAL WHISTLE! MATCH OVER!{Style.RESET_ALL}")
        time.sleep(2)
        
        self.display_final_stats()




# Initialize colorama for colored output
init()

# [Existing Player, Formation, Team, Commentator, Match classes assumed here]

def create_realistic_player(name: str, position: str, base_rating: int = 75) -> Player:
    """Create a player with realistic stats based on position."""
    base = base_rating + random.randint(-10, 10)
    
    if position == "G":
        return Player(
            name,
            position,
            attack=random.randint(15, 35),
            defense=base + random.randint(5, 15),
            speed=random.randint(45, 75),
            technique=random.randint(65, 85),
            physical=random.randint(75, 90),
            mental=random.randint(75, 95),
            age=random.randint(22, 36)
        )
    
    elif position in ["CB", "RB", "LB"]:
        return Player(
            name,
            position,
            attack=random.randint(35, 65),
            defense=base + random.randint(5, 15),
            speed=random.randint(60, 85),
            technique=random.randint(55, 80),
            physical=random.randint(80, 95),
            mental=random.randint(70, 90),
            age=random.randint(22, 34)
        )
    
    elif position in ["DM", "CM", "AM"]:
        return Player(
            name,
            position,
            attack=random.randint(55, 85),
            defense=random.randint(50, 80),
            speed=random.randint(65, 90),
            technique=base + random.randint(5, 15),
            physical=random.randint(70, 90),
            mental=random.randint(75, 95),
            age=random.randint(20, 32)
        )
    
    else:
        return Player(
            name,
            position,
            attack=base + random.randint(5, 15),
            defense=random.randint(30, 55),
            speed=random.randint(75, 95),
            technique=random.randint(75, 95),
            physical=random.randint(65, 85),
            mental=random.randint(70, 90),
            age=random.randint(19, 31)
        )

def main():
    """Launch the match simulation with expanded Champions League teams."""
    print(f"{Back.BLUE}{Fore.WHITE}{'🏟️ ULTRA-REALISTIC FOOTBALL SIMULATOR':^80}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{'FIFA-Style Simulation with AI':^80}{Style.RESET_ALL}")
    
    # Expanded list of Champions League 2025 teams with realistic rosters
    teams = [
        Team(
            "Real Madrid CF",
            [
                create_realistic_player("Courtois", "G", 90),
                create_realistic_player("Carvajal", "RB", 86),
                create_realistic_player("Militão", "CB", 84),
                create_realistic_player("Alaba", "CB", 87),
                create_realistic_player("Mendy", "LB", 82),
                create_realistic_player("Casemiro", "DM", 89),
                create_realistic_player("Modrić", "CM", 90),
                create_realistic_player("Kroos", "CM", 88),
                create_realistic_player("Vinícius Jr", "LW", 88),
                create_realistic_player("Benzema", "ST", 92),
                create_realistic_player("Rodrygo", "RW", 84),
                create_realistic_player("Valverde", "CM", 85),  # Substitute
                create_realistic_player("Asensio", "RW", 83)    # Substitute
            ],
            "4-3-3",
            "White",
            "Carlo Ancelotti"
        ),
        Team(
            "FC Barcelona",
            [
                create_realistic_player("ter Stegen", "G", 89),
                create_realistic_player("Dest", "RB", 78),
                create_realistic_player("Araújo", "CB", 83),
                create_realistic_player("García", "CB", 80),
                create_realistic_player("Alba", "LB", 85),
                create_realistic_player("Busquets", "DM", 87),
                create_realistic_player("de Jong", "CM", 86),
                create_realistic_player("Gavi", "CM", 81),
                create_realistic_player("Dembélé", "RW", 83),
                create_realistic_player("Lewandowski", "ST", 92),
                create_realistic_player("Ansu Fati", "LW", 82),
                create_realistic_player("Pedri", "CM", 86),     # Substitute
                create_realistic_player("Raphinha", "RW", 84)   # Substitute
            ],
            "4-3-3",
            "Blue/Red",
            "Xavi Hernández"
        ),
        Team(
            "Manchester City",
            [
                create_realistic_player("Ederson", "G", 89),
                create_realistic_player("Walker", "RB", 85),
                create_realistic_player("Dias", "CB", 88),
                create_realistic_player("Akanji", "CB", 83),
                create_realistic_player("Cancelo", "LB", 84),
                create_realistic_player("Rodri", "DM", 90),
                create_realistic_player("De Bruyne", "CM", 91),
                create_realistic_player("Gündoğan", "CM", 85),
                create_realistic_player("Foden", "RW", 87),
                create_realistic_player("Haaland", "ST", 93),
                create_realistic_player("Grealish", "LW", 84),
                create_realistic_player("Bernardo Silva", "CM", 86),  # Substitute
                create_realistic_player("Álvarez", "ST", 83)          # Substitute
            ],
            "4-3-3",
            "Sky Blue",
            "Pep Guardiola"
        ),
        Team(
            "Bayern Munich",
            [
                create_realistic_player("Neuer", "G", 88),
                create_realistic_player("Davies", "LB", 85),
                create_realistic_player("de Ligt", "CB", 85),
                create_realistic_player("Upamecano", "CB", 83),
                create_realistic_player("Pavard", "RB", 82),
                create_realistic_player("Kimmich", "DM", 89),
                create_realistic_player("Goretzka", "CM", 86),
                create_realistic_player("Musiala", "AM", 87),
                create_realistic_player("Sané", "RW", 85),
                create_realistic_player("Kane", "ST", 90),
                create_realistic_player("Coman", "LW", 84),
                create_realistic_player("Müller", "AM", 84),  # Substitute
                create_realistic_player("Tel", "ST", 80)      # Substitute
            ],
            "4-2-3-1",
            "Red",
            "Thomas Tuchel"
        ),
        Team(
            "Liverpool FC",
            [
                create_realistic_player("Alisson", "G", 89),
                create_realistic_player("Alexander-Arnold", "RB", 87),
                create_realistic_player("van Dijk", "CB", 89),
                create_realistic_player("Konaté", "CB", 84),
                create_realistic_player("Robertson", "LB", 86),
                create_realistic_player("Mac Allister", "DM", 84),
                create_realistic_player("Szoboszlai", "CM", 83),
                create_realistic_player("Elliott", "CM", 80),
                create_realistic_player("Salah", "RW", 90),
                create_realistic_player("Núñez", "ST", 84),
                create_realistic_player("Díaz", "LW", 85),
                create_realistic_player("Gravenberch", "CM", 81),  # Substitute
                create_realistic_player("Jota", "LW", 83)           # Substitute
            ],
            "4-3-3",
            "Red",
            "Arne Slot"
        ),
        Team(
            "Paris Saint-Germain",
            [
                create_realistic_player("Donnarumma", "G", 88),
                create_realistic_player("Hakimi", "RB", 85),
                create_realistic_player("Marquinhos", "CB", 86),
                create_realistic_player("Skriniar", "CB", 83),
                create_realistic_player("Mendes", "LB", 82),
                create_realistic_player("Vitinha", "DM", 84),
                create_realistic_player("Verratti", "CM", 85),
                create_realistic_player("Zaïre-Emery", "CM", 80),
                create_realistic_player("Dembélé", "RW", 85),
                create_realistic_player("Mbappé", "ST", 92),
                create_realistic_player("Barcola", "LW", 81),
                create_realistic_player("Ruiz", "CM", 82),  # Substitute
                create_realistic_player("Kolo Muani", "ST", 82)  # Substitute
            ],
            "4-3-3",
            "Navy Blue",
            "Luis Enrique"
        ),
        Team(
            "Arsenal FC",
            [
                create_realistic_player("Raya", "G", 85),
                create_realistic_player("White", "RB", 83),
                create_realistic_player("Saliba", "CB", 87),
                create_realistic_player("Gabriel", "CB", 85),
                create_realistic_player("Zinchenko", "LB", 82),
                create_realistic_player("Rice", "DM", 87),
                create_realistic_player("Ødegaard", "CM", 88),
                create_realistic_player("Havertz", "AM", 84),
                create_realistic_player("Saka", "RW", 88),
                create_realistic_player("Jesus", "ST", 83),
                create_realistic_player("Martinelli", "LW", 84),
                create_realistic_player("Partey", "DM", 82),  # Substitute
                create_realistic_player("Trossard", "LW", 82)  # Substitute
            ],
            "4-3-3",
            "Red/White",
            "Mikel Arteta"
        ),
        Team(
            "Inter Milan",
            [
                create_realistic_player("Sommer", "G", 85),
                create_realistic_player("Pavard", "RB", 83),
                create_realistic_player("Acerbi", "CB", 82),
                create_realistic_player("Bastoni", "CB", 85),
                create_realistic_player("Dimarco", "LB", 84),
                create_realistic_player("Barella", "CM", 86),
                create_realistic_player("Çalhanoğlu", "CM", 85),
                create_realistic_player("Mkhitaryan", "CM", 82),
                create_realistic_player("Frattesi", "AM", 81),
                create_realistic_player("Lautaro", "ST", 89),
                create_realistic_player("Thuram", "ST", 84),
                create_realistic_player("Dumfries", "RB", 81),  # Substitute
                create_realistic_player("Arnautović", "ST", 80)  # Substitute
            ],
            "3-5-2",
            "Blue/Black",
            "Simone Inzaghi"
        )
    ]
    
    # Select two teams randomly for the match (or customize as needed)
    team1, team2 = random.sample(teams, 2)
    
    match = Match(
        team1,
        team2,
        stadium=f"{team1.name} Stadium",
        weather=random.choice(["Sunny", "Cloudy", "Rainy", "Windy"]),
        temperature=random.randint(15, 28),
        attendance=random.randint(30000, 85000)
    )
    
    match.simulate()

if __name__ == "__main__":
    main()
