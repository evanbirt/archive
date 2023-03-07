{-# LANGUAGE ParallelListComp #-}

-- CS 3210 - Principles of Programming Languages - Spring 2020
-- Author(s): Evan Birt

import Data.List

type Seq   = [Char]
type Board = [Seq]

--DONE 01/17
-- setup​ takes an integer ​n >= 4 ​and creates an ​nxn​ board with all locations empty. If ​n < 4​ ​setup​ should return a ​4x4​ board.
setup :: Int -> Board
setup n
  | n > 4 = take n $ repeat $ concat $ replicate n "-"      -- using $ to remove following parenthesis for readability
  | otherwise = ["----","----", "----", "----"]             -- 4 or less

-- DONE 02/17 
-- rows​ takes a ​board​ and returns its number of rows.
rows :: Board -> Int
rows b = length b

-- DONE 03/17 -- also in suduko game
-- cols​ takes a ​board​ and returns its number of columns if all rows have the same number of columns; it returns zero, otherwise.
cols :: Board -> Int
cols b
  | length (nub colsPerRow) == 1 = head colsPerRow
  | otherwise = 0
  where
    colsPerRow = [ length row | row <- b ]

-- DONE 04/17
-- size​ takes a ​board​ and returns its size, which is the same as its number of rows (if it matches its number of columns), or zero, otherwise.
size :: Board -> Int
size b
  | rows(b) == cols(b) = rows(b)
  | otherwise = 0

-- DONE 05/17
-- queensSeq ​takes a ​sequence​ and returns the number of queens found in it.
queensSeq :: Seq -> Int 
queensSeq = length . filter (=='Q')   -- shortened from s = length (filter (=='Q')  s), removes extra s

-- DONE 06/17
--queensBoard ​takes a ​board​ and returns the number of queens found in it.
queensBoard :: Board -> Int
queensBoard q = sum (map queensSeq q) -- Help from Brian Prow refered me to (sum) function intead of writing a counter 

-- DONE 07/17
-- seqValid​ takes a ​sequence​ and returns true/false depending whether the sequence no more than ​1​ queen.
seqValid :: Seq -> Bool
seqValid s
  | queensSeq(s) >= 2 =False
  | otherwise = True

-- DONE 08/17
-- rowsValid​ takes a ​board​ and returns true/false depending whether ALL of its rows correspond to valid sequences.
rowsValid :: Board -> Bool
rowsValid b = and [ seqValid row | row <- b ]

-- DONE 09/17
-- colsValid​ takes a ​board​ and returns true/false depending whether ALL of its columns correspond to valid sequences.
colsValid :: Board -> Bool
colsValid b = and [ seqValid col | col <- transpose b ]

-- DONE 10/17
diagonals :: Board -> Int
diagonals b = 2 * size(b) -1

-- DONE 11/17
--allMainDiagIndices​ takes a ​board​ and returns a list of all primary diagonal indices.
allMainDiagIndices :: Board -> [[ (Int, Int) ]]
allMainDiagIndices b = [mainDiagIndices (b) i | i <- [0 .. diagonals(b)-1]]

-- DONE 12/17
--mainDiag​ takes a ​board​ and returns a list of all primary diagonal elements.
mainDiag :: Board -> [Seq]
mainDiag b =  (map . map) (\(x,y) ->  (b !! y) !! x) $ allMainDiagIndices(b)

-- DONE 13/17
--allSecDiagIndices​ takes a ​board​ and returns a list of all secondary diagonal indices.
allSecDiagIndices :: Board -> [[ (Int, Int) ]]
allSecDiagIndices b = [secDiagIndices (b) i | i <- [0 .. diagonals(b)-1]]

-- DONE 14/17
--secDiag​ takes a ​board​ and returns a list of all secondary diagonal elements.
secDiag :: Board -> [Seq]
secDiag b = ( map . map ) (\(x,y) ->  (b !! y) !! x) $ allSecDiagIndices(b)

-- DONE 15/17
--diagsValid​ takes a ​board​ and returns true/false depending whether all of its primary and secondary diagonals are valid.
diagsValid :: Board -> Bool
diagsValid b = and [rowsValid(mainDiag(b)), rowsValid(secDiag(b))]

-- DONE 16/17
--valid​ takes a ​board​ and returns true/false depending whether the board configuration is valid (i.e., no queen is threatening another queen).
valid :: Board -> Bool
valid b = and [rowsValid b, colsValid b, diagsValid b]

-- DONE 17/17
--solved​ takes a ​board​ and returns true/false depending whether the board configuration is solved (i.e., the configuration is valid and also has the right amount of queens based on the board’s size).
solved :: Board -> Bool
solved b = and [ queensBoard (b) == size(b), valid b ]

mainDiagIndices :: Board -> Int -> [ (Int, Int) ]
mainDiagIndices b p
  | p < n = [ (n - 1 - qr, q) | q <- [0..p] | qr <- [p,p-1..0] ]
  | otherwise = [ (q, (n - 1 - qr)) | q <- [0..2 * (n - 1) - p] | qr <- [2 * (n - 1) - p,2 * (n - 1) - p - 1..0] ]
  where n = size b

secDiagIndices :: Board -> Int -> [ (Int, Int) ]
secDiagIndices b p
  | p < n = [ (p - q, q) | q <- [0..p] ]
  | otherwise = [ (p - (n - 1 - q), n - 1 - q) | q <- [2 * (n - 1) - p, 2 * (n - 1) - p - 1..0] ]
  where n = size b

setQueenAt :: Board -> Int -> [Board]
setQueenAt b i = do
  let z = replicate ((size b) - 1) '-'
  let p = nub (permutations ("Q" ++ z))
  [ [ (b!!k) | k <- [0..(i-1)] ] ++ [r] ++ [ (b!!k) | k <- [(i+1)..((rows b) - 1)] ] | r <- p ]

nextRow :: Board -> Int
nextRow b = head [ i | i <- [0 .. (size b) - 1], queensSeq (b!!i) == 0 ]

solve :: Board -> [Board]
solve b
  | solved b = [b]
  | otherwise = concat [ solve newB | newB <- setQueenAt b i, valid newB ]
    where i = nextRow b

main = do
  let b = setup 6
  let solution = [ solution | solution <- solve b ]
  print (solution)
