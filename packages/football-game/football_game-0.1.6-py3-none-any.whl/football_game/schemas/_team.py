from typing import TYPE_CHECKING
import uuid
from sqlmodel import SQLModel, Field, Relationship, Session
import os as os
import pandas as pd

if TYPE_CHECKING:
    from ._player import Player
    from ._trainer import Trainer


class Team(SQLModel, table=True):
    team_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
        index=True,
        sa_column_kwargs={"comment": "Unique identifier for the team"},
    )
    name: str
    budget: float

    players: "Player" = Relationship(back_populates="team")
    trainer: "Trainer" = Relationship(back_populates="team")

    @staticmethod
    def create_team(team: "Team", csv_name: str, headers: list, engine) -> None:
        """
        Create a .csv with the team's categories if it doesn't exist. Add the team to the csv and upload to database

        Args:
            csv_name: str: csv's name
            headers: list: header's columns
            Team
            engine
        """
        session = Session(engine)

        if not os.path.exists(csv_name):
            df = pd.DataFrame(columns=headers)

            df.to_csv(csv_name, index=False)

        df = pd.read_csv(csv_name)

        new_team = pd.DataFrame(
            [[getattr(team, attr) for attr in Team.__fields__.keys()]],
            columns=df.columns,
        )

        df = pd.concat([df, new_team], ignore_index=True)

        df.to_csv(csv_name, index=False)

        team_instance = Team(**new_team.iloc[0].to_dict())

        session.add(team_instance)
        session.commit()
