DROP TABLE IF EXISTS Scores;
CREATE TABLE Scores(
    name TEXT,
    composer TEXT
);

DROP TABLE IF EXISTS Events;
CREATE TABLE Events(
    event_id INTEGER NOT NULL PRIMARY KEY,
    location FLOAT,
    duration FLOAT,
    part_id INTEGER,
    score_id INTEGER NOT NULL,
    FOREIGN KEY (score_id) REFERENCES Scores(rowid)
            ON DELETE CASCADE ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS Nodes;
CREATE TABLE Nodes(
    state INTEGER,
		node_type TEXT
);

DROP TABLE IF EXISTS Noteheads;
CREATE TABLE Noteheads(
    midi INTEGER,
    spelling TEXT,
    event_id INTEGER NOT NULL,
    sharpnode_id INTEGER,
    flatnode_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
            ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (sharpnode_id) REFERENCES Nodes(rowid)
            ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (flatnode_id) REFERENCES Nodes(rowid)
            ON DELETE NO ACTION ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS EdgeWeights;
CREATE TABLE EdgeWeights(
		lower_pitch INTEGER,
		lower_node_type TEXT,
		higher_pitch INTEGER,
		higer_node_type TEXT
);

DROP TABLE IF EXISTS DirectedEdges;
CREATE TABLE DirectedEdges(
    startnode_id INTEGER,
    endnode_id INTEGER,
    weight_id INTEGER,
    FOREIGN KEY (startnode_id) REFERENCES Nodes(rowid)
            ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (endnode_id) REFERENCES Nodes(rowid)
            ON DELETE CASCADE ON UPDATE NO ACTION
);
