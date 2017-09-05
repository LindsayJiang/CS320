---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5
-- Yida Xu  xyds1522@bu.edu  U39436573
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
select ex user table da = if (user == [user' | Add user' <- ex]!!0 || user == [user' | Add user' <- ex]!!1)
                            && table == [table' | Create table' <- ex]!!0
                            && (user, table) == [(user', table') | Allow (user', table') <- ex]!!0
							           then Just [lookup' da da'| Insert (table, da') <- ex]
							           else Nothing

-- Type synonym for aggregation operators.
type Operator = Integer -> Integer -> Integer

-- Complete for Assignment 5, Problem 1, part (b).
aggregate :: [Command] -> User -> Table -> Column -> Operator -> Maybe Integer
aggregate ex user table da operator = Just (foldr operator 0 (fromJust (select ex user table da)))

fromJust :: Maybe [Integer] -> [Integer]
fromJust (Just x) = x

-- Complete for Assignment 5, Problem 1, part (c).
validate :: [Command] -> Bool
validate x = reverse' (rev' x)

rev' :: [Command] -> [Command]
rev' [] = []
rev' x = (last x) : (rev' (init x))

reverse' :: [Command] -> Bool
reverse' []     = True
reverse' (x:xs) = if [bla | Allow bla <- [x]] /= []
					then if [user | Allow (user, _) <- [x]]!!0 `elem` [user' | Add user' <- xs]
							then if [table | Allow (_, table) <- [x]]!!0 `elem ` [table' | Create table' <- xs]
									then reverse' xs
									else False
							else False
					else if [bla | Insert bla <- [x]] /= []
							then if [table | Insert (table, _) <- [x]]!!0 `elem` [table' | Create table' <- xs]
									then reverse' xs
									else False
							else reverse' xs

{-
test cases for validate

[Add (User "Alice"), Create (Table "Revenue"), Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)])] is True
[Add (User "Alice"), Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)]), Create (Table "Revenue")] is False
[Add (User "Allice"), Create (Table "Revenue"), Allow (User "Bob", Table "Revenue"), Add (User "Alice")] is False
-}
--eof