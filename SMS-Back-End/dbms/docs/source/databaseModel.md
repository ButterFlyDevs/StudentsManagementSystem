
+-----------------+------------+------+-----+---------+----------------+
| Field           | Type       | Null | Key | Default | Extra          |
+-----------------+------------+------+-----+---------+----------------+
| studentId       | int(11)    | NO   | PRI | NULL    | auto_increment |
| name            | char(50)   | YES  |     | NULL    |                |
| surname         | char(100)  | YES  |     | NULL    |                |
| dni             | int(11)    | YES  | UNI | NULL    |                |
| address         | char(100)  | YES  |     | NULL    |                |
| locality        | char(50)   | YES  |     | NULL    |                |
| province        | char(50)   | YES  |     | NULL    |                |
| birthdate       | date       | YES  |     | NULL    |                |
| phone           | char(50)   | YES  |     | NULL    |                |
| profileImageUrl | char(200)  | YES  |     | NULL    |                |
| createdBy       | int(11)    | YES  |     | NULL    |                |
| createdAt       | date       | YES  |     | NULL    |                |
| modifyBy        | int(11)    | YES  |     | NULL    |                |
| modifyAt        | date       | YES  |     | NULL    |                |
| deletedBy       | int(11)    | YES  |     | NULL    |                |
| deletedAt       | date       | YES  |     | NULL    |                |
| deleted         | tinyint(1) | YES  |     | NULL    |                |
+-----------------+------------+------+-----+---------+----------------+
