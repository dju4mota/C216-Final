DROP TABLE IF EXISTS "pets";

CREATE TABLE "pets" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "animal" VARCHAR(255) NOT NULL,
    "raca" VARCHAR(255) NOT NULL,
    "idade" INTEGER NOT NULL,
    "sociavel" BOOLEAN NOT NULL,
    "adotavel" BOOLEAN NOT NULL
);


INSERT INTO "pets" ("nome", "animal", "raca", "idade", "sociavel", "adotavel")
VALUES ('morgana', 'gato', 'frajola', 1, TRUE, FALSE);

INSERT INTO "pets" ("nome", "animal", "raca", "idade", "sociavel", "adotavel")
VALUES ('github', 'gato', 'rajado', 1, FALSE, FALSE);


INSERT INTO "pets" ("nome", "animal", "raca", "idade", "sociavel", "adotavel")
VALUES ('dustin', 'cachorro', 'border collie', 3, TRUE, FALSE);