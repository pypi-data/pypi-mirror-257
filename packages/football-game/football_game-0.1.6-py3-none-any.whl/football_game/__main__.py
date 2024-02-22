from decouple import config
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel import Session

from schemas import *


def main():
    postgres_uri: str = config("POSTGRES_URI")
    engine = create_engine(postgres_uri)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        team_csv_name = "football_game/schemas/teams.csv"

        team_headers = [
            "team_id",
            "name",
            "budget",
        ]

        team_data = Team(
            name="Real Madrid",
            budget=99999
        )

        """Team.create_team(
            team_data,
            team_csv_name,
            team_headers,
            engine
        )"""

        trainer_csv_name = "football_game/schemas/trainers.csv"

        trainer_headers = [
            "trainer_id",
            "name",
            "age",
            "salary",
            "team_id"
        ]

        trainer_data = Trainer(
            name="Ancelotti",
            age=59,
            salary=8491,
            budget=99999,
            team=team_data
        )

        """Trainer.create_trainer(
            trainer_data,
            trainer_csv_name,
            trainer_headers,
            engine
        )"""

        player_csv_name = "football_game/schemas/players.csv"

        player_headers = [
            "player_id",
            "name",
            "age",
            "weight",
            "height",
            "salary",
            "position",
            "pac",
            "sho",
            "pas",
            "dri",
            "defe",
            "phy",
            "goalkeeping",
            "team_id",
            "trainer_id",
        ]

        player_data = Player(
            name="Carvajal",
            age=28,
            weight=88,
            height=1.88,
            salary=9000000,
            position="Goalkeeper",
            pac=33.5,
            sho=24.33,
            pas=41.67,
            dri=43.83,
            defe=18.4,
            phy=41,
            goalkeeping=85,
            team=team_data,
            trainer=trainer_data,
        )

        Player.create_player(player_data, player_csv_name, player_headers, engine)


if __name__ == "__main__":
    main()
