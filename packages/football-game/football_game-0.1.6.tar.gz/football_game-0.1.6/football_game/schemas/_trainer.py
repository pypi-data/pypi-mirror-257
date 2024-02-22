from typing import TYPE_CHECKING
import uuid
from sqlmodel import SQLModel, Field, Relationship, Session
import os as os
import pandas as pd

if TYPE_CHECKING:
    from ._team import Team
    from ._player import Player


class Trainer(SQLModel, table=True):
    trainer_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
        index=True,
        sa_column_kwargs={"comment": "Unique identifier for the trainer"},
    )
    name: str
    age: int
    salary: float

    team_id: uuid.UUID | None = Field(default=None, foreign_key="team.team_id")
    team: "Team" = Relationship(back_populates="trainer")

    players: "Player" = Relationship(back_populates="trainer")

    @staticmethod
    def create_trainer(
        trainer: "Trainer", csv_name: str, headers: list, engine
    ) -> None:
        """
        Create a .csv with the trainer's categories if it doesn't exist. Add the trainer to the csv and upload to database

        Args:
            csv_name: str: csv's name
            headers: list: header's columns
            Trainer
            engine
        """
        session = Session(engine)

        if not os.path.exists(csv_name):
            df = pd.DataFrame(columns=headers)

            df.to_csv(csv_name, index=False)

        df = pd.read_csv(csv_name)

        new_trainer = pd.DataFrame(
            [[getattr(trainer, attr) for attr in Trainer.__fields__.keys()]],
            columns=df.columns,
        )

        df = pd.concat([df, new_trainer], ignore_index=True)

        df.to_csv(csv_name, index=False)

        trainer_instance = Trainer(**new_trainer.iloc[0].to_dict())

        session.add(trainer_instance)
        session.commit()
