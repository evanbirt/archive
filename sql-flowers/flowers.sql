-- CS 3810 Database Project 1
-- authors: Nicole Weickert, Evan Birt, Cory Gamble

CREATE DATABASE flowers;
USE flowers;

CREATE TABLE Zones(
	id INT PRIMARY KEY CHECK(CHAR_LENGTH(id) <= 2),
	lowerTemp INT NOT NULL, CHECK(lowerTemp between -99 and 99),
	higherTemp INT NOT NULL, CHECK(lowerTemp between -99 and 99)
	);

INSERT INTO Zones
VALUES
	(2, -50, -40),	
	(3, -40, -30),
	(4, -30, -20),
	(5, -20, -10),
	(6, -10, 0),
	(7, 0, 10),
	(8, 10, 20),
	(9, 20, 30),
	(10, 30, 40);

CREATE TABLE Deliveries (
	id INT PRIMARY KEY CHECK(CHAR_LENGTH(id) = 1),
	categ VARCHAR(5) NOT NULL,
	delSize DECIMAL(5,3)
	);

INSERT INTO Deliveries
VALUES
	(1, 'pot', 1.500),
	(2, 'pot', 2.250),
	(3, 'pot', 2.625),
	(4, 'pot', 4.250),
	(5, 'plant', NULL),
	(6, 'bulb', NULL),
	(7, 'hedge', 18.000),
	(8, 'shrub', 24.000),
	(9, 'tree', 36.000);

CREATE TABLE FlowersInfo (
	id INT PRIMARY KEY CHECK(CHAR_LENGTH(id) = 3),
	comName VARCHAR(30) NOT NULL,
	latName VARCHAR(35) NOT NULL,
	cZone INT NOT NULL,
	hZone INT NOT NULL,
	deliver INT,
	sunNeeds VARCHAR(5) NOT NULL,

	FOREIGN KEY (cZone) REFERENCES Zones(id),
	FOREIGN KEY (hZone) REFERENCES Zones(id),
	FOREIGN KEY (deliver) REFERENCES Deliveries(id)
	);

INSERT INTO FlowersInfo
VALUES
	(101, 'Lady Fern', 'Atbyrium filix-femina', 2, 9, 5, 'SH'),
	(102, 'Pink Caladiums', 'C.x bortulanum', 10, 10, 6, 'PtoSH'),
	(103, 'Lily-of-the-Valley', 'Convallaria majalis', 2, 8, 5, 'PtoSH'),
	(105, 'Purple Liatris', 'Liatris spicata', 3, 9, 6, 'StoP'),
	(106, 'Black Eyed Susan', 'Rudbeckia fulgida var. specios', 4, 10, 2, 'StoP'),
	(107, 'Nikko Blue Hydrangea', 'Hydrangea macrophylla', 5, 9, 4, 'StoSH'),
	(108, 'Variegated Weigela', 'W. florida Variegata', 4, 9, 8, 'StoP'),
	(110, 'Lombardy Poplar', 'Populus nigra Italica', 3, 9, 9, 'S'),
	(111, 'Purple Leaf Plum Hedge', 'Prunus x cistena', 2, 8, 7, 'S'),
	(114, 'Thorndale Ivy', 'Hedera belix Thorndale', 3, 9, 1, 'StoSH');

-- a) total number of zones
SELECT COUNT(id) as 'Total Zones'
FROM Zones;

-- b) number of flowers per cool zone
SELECT cZone AS 'Cool Zone', COUNT(*) AS 'Number of Flowers'
FROM FlowersInfo
GROUP BY cZone 
ORDER BY cZone;

-- c) common names of plants that have delivery sizes less than 5
SELECT comName AS 'Common Name', delSize AS 'Delivery Size'
FROM FLowersInfo
INNER JOIN Deliveries ON FlowersInfo.deliver = Deliveries.id
WHERE delSize < 5;

-- d) common names of plants that require full sun (i.e. sun needs contains 'S')
SELECT comName AS 'Common Name', sunNeeds AS 'Sun Needs'
FROM FLowersInfo
WHERE sunNeeds LIKE 'S' 
	OR sunNeeds LIKE 'Sto%'
	OR sunNeeds LIKE '%toS';

-- e) all delivery category names order alphabetically without repetition
SELECT DISTINCT categ AS 'Delivery Categories'
FROM Deliveries
ORDER BY categ ASC;

-- f) the exact output (by name)
SELECT
	FlowersInfo.comName AS 'Name',
	Zones.lowerTemp AS 'Cool Zone (low)',
	Zones.higherTemp AS 'Cool Zone (high)',
	Deliveries.categ AS 'Delivery Category'
FROM
	((FlowersInfo INNER JOIN Zones on FlowersInfo.cZone = Zones.id) 
INNER JOIN deliveries on FlowersInfo.deliver = Deliveries.id) 
ORDER by 1;

-- g) plant names that have the same hot zone as 'Pink Caladiums' (solution must get the hot zone of pink caladiums in a variable)
SET @hotZone = (
	SELECT hZone
	FROM FlowersInfo
	WHERE comName='Pink Caladiums'
	);

SELECT comName AS 'Common Name'
FROM FlowersInfo
WHERE hZone = @hotZone;

-- h) total number of plants, minimum delivery size, maximum delivery size, and average size based on plants that have delivery sizes (the avg value should be rounded using 2 decimals)
SELECT COUNT(*) AS 'Total',
ROUND(MIN(delSize), 1) AS 'Min',
ROUND(MAX(delSize), 1) AS 'Max',
ROUND(AVG(delSize), 2) AS 'Average'
FROM FlowersInfo
INNER JOIN Deliveries ON FlowersInfo.deliver = Deliveries.id
WHERE delSize IS NOT NULL;

-- i) the Latin name of the plant that has the word 'Eyed' in its name (must use LIKE)
SELECT latName AS 'Latin Name'
FROM FlowersInfo
WHERE comName like '%Eyed%';

-- j) the exact output (category then name)
SELECT 
	categ AS 'Category', comName AS 'Name'
FROM FlowersInfo
INNER JOIN deliveries
ON FlowersInfo.deliver = Deliveries.id
ORDER BY 1,2;
