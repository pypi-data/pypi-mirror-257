from typing import TYPE_CHECKING
import uuid
from sqlmodel import SQLModel, Field, Relationship, Session
import pandas as pd
import os as os

if TYPE_CHECKING:
    from ._team import Team
    from ._trainer import Trainer


class Player(SQLModel, table=True):
    player_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
        index=True,
        sa_column_kwargs={"comment": "Unique identifier for the player"},
    )
    name: str
    age: int
    weight: int
    height: float
    salary: float
    position: str
    pac: float
    sho: float
    pas: float
    dri: float
    defe: float
    phy: float
    goalkeeping: float

    team_id: uuid.UUID | None = Field(default=None, foreign_key="team.team_id")
    team: "Team" = Relationship(back_populates="players")

    trainer_id: uuid.UUID | None = Field(default=None, foreign_key="trainer.trainer_id")
    trainer: "Trainer" = Relationship(back_populates="players")

    @staticmethod
    def create_player(player: "Player", csv_name: str, headers: list, engine) -> None:
        """
        Create a .csv with the player's categories if it doesn't exist. Add the player to the csv and upload to database

        Args:
            csv_name: str: csv's name
            headers: list: header's columns
            Player
            engine
        """
        session = Session(engine)

        if not os.path.exists(csv_name):
            df = pd.DataFrame(columns=headers)

            df.to_csv(csv_name, index=False)

        df = pd.read_csv(csv_name)

        new_player = pd.DataFrame(
            [[getattr(player, attr) for attr in Player.__fields__.keys()]],
            columns=df.columns,
        )

        df = pd.concat([df, new_player], ignore_index=True)

        df.to_csv(csv_name, index=False)

        player_instance = Player(**new_player.iloc[0].to_dict())

        session.add(player_instance)
        session.commit()
