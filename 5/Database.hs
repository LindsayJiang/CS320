---------------------------------------------------------------------
--
-- CAS CS 320, Spring 2015
-- Assignment 5 (skeleton code)
-- Linshan Jiang (linshan@bu.edu)
-- Database.hs
--

module Database where

type Column = String
data User = User String deriving (Eq, Show)
data Table = Table String deriving (Eq, Show)
data Command =
    Add User
  | Create Table
  | Allow (User, Table)
  | Insert (Table, [(Column, Integer)])
  deriving (Eq, Show)

example = [
    Add (User "Alice"),
    Add (User "Bob"),
    Create (Table "Revenue"),
    Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)]),
    Insert (Table "Revenue", [("Day", 2), ("Amount", 1700)]),
    Insert (Table "Revenue", [("Day", 3), ("Amount", 3100)]),
    Allow (User "Alice", Table "Revenue")
  ]

-- Useful function for retrieving a value from a list
-- of (label, value) pairs.
lookup' :: Column -> [(Column, Integer)] -> Integer
lookup' c' ((c,i):cvs) = if c == c' then i else lookup' c' cvs

-- Complete for Assignment 5, Problem 1, part (a).
select :: [Command] -> User -> Table -> Column -> Maybe [Integer]
select example user table column = if [user'|Add user' <- example, user == user']/= []
                                      && [table'|Create table' <- example, table == table']/= []
                                      && [(user',table')|Allow (user', table') <- example, user == user' && table == table']/=[]
                                   then Just [lookup' column da|Insert (ta, da) <- example, table == ta]
                                   else Nothing

-- Type synonym for aggregation operators.
type Operator = Integer -> Integer -> Integer

-- Complete Assignment 5, Problem 1, parts (b) and (c) here.
-- part(b)
aggregate :: [Command] -> User -> Table -> Column -> Operator -> Integer -> Maybe Integer
aggregate example user table column operator integer = if (select example user table column) /= Nothing
                                                       then Just (foldr operator integer (nojust (select example user table column)))
                                                       else Nothing
-- helper function for getting rid of the "Just".
nojust :: Maybe [Integer] -> [Integer]
nojust (Just list) = list

-- part(c)
validate :: [Command] -> Bool
validate x = vali (reverse' x)


reverse' :: [Command] -> [Command]
reverse' [] = []
reverse' xs = (last xs):(reverse' (init xs))


vali :: [Command] -> Bool
vali []     = True
vali (x:xs) = if [tuple|Allow tuple <- [x]] /= []
          then if [user|Allow (user, table) <- [x]]!!0 `elem` [user' | Add user' <- xs]
              then if [table|Allow (user, table) <- [x]]!!0 `elem` [table' | Create table' <- xs]
                  then vali xs
                  else False
              else False
          else if [thing|Insert thing <- [x]] /= []
              then if [table| Insert (table, lis) <- [x]]!!0 `elem` [table' | Create table' <- xs]
                  then vali xs
                  else False
              else vali xs




--eof