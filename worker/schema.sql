CREATE TABLE IF NOT EXISTS votes (
  result_id  TEXT    NOT NULL,
  voter      TEXT    NOT NULL,              -- salted hash of the client address
  value      INTEGER NOT NULL CHECK (value IN (-1, 1)),
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (result_id, voter)
);
