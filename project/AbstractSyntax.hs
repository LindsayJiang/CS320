-- Linshan Jiang (linshan@bu.edu)
-- Collaborators: Qi Want (wangqi03@bu.edu)
--                Claudia Ng (claudiaw@bu.edu)
-- AbstractSyntax.hs

module AbstractSyntax where

import Data.List (union, intersect)

data Exp =
    DATA
  | Variable String
  | Max Exp
  | Min Exp
  | Sum Exp
  | Product Exp
  | Union Exp
  | Intersection Exp
  | MakeSet Exp
  deriving (Eq, Show)

data Stmt =
    Assign String Exp Stmt
  | Return String
  deriving (Eq, Show)

data Type =
    TyNumber
  | TySet
  | TyVoid
  deriving (Eq, Show)

data Value =
    Set [Integer]
  | Number Integer
  | Error
  deriving (Eq, Show)

instance Num Value where
  -- Complete for Problem 1, part (b).
  fromInteger n = Number n
  (Number x) + (Number y) = Number (x + y)
  _ + _ = Error
  (Number x) * (Number y) = Number (x * y)
  _ * _ = Error

instance Ord Value where
  --  Complete for Problem 1, part (b).
  Error < Error = False
  (Number x) < Error = False
  (Number x) < (Number y) = if x < y then True else False
  Error < (Number x) = True
  Error <= Error = False
  Error <=  (Number x) = True
  (Number x) <= (Number y) = if x <= y then True else False
  (Number x) <= Error = False


(\/) :: Value -> Value -> Value
-- Complete for Problem 1, part (c).
(\/) (Set s1) (Set s2) = Set (s1 `union` s2)
(\/) _ _ = Error

(/\) :: Value -> Value -> Value
-- Complete for Problem 1, part (c).
(/\) (Set s1) (Set s2) = Set (s1 `intersect` s2)
(/\) _ _ = Error


-- Type class Foldable for a fold function on data types.
--
--  * The first argument is a constant that will replace all
--    leaf nodes that contain no variable.
--  * The second argument is a function that will be applied to
--    (i.e., and will replace) any variables.
--  * The third argument is the aggregator for combining
--    results of recursive folds.
--  * The fourth argument is the data value that will be folded.

class Foldable a where
  fold :: b -> (String -> b) -> ([b] -> b) -> a -> b

instance Foldable Exp where
-- Complete for Problem 1, part (d).
  fold b v f (DATA) = b
  fold b v f (Variable s) = v s
  fold b v f (Max e) = f [fold b v f e]
  fold b v f (Min e) = f [fold b v f e]
  fold b v f (Sum e) = f [fold b v f e]
  fold b v f (Product e) = f [fold b v f e]
  fold b v f (Union e) = f [fold b v f e]
  fold b v f (Intersection e) = f [fold b v f e]
  fold b v f (MakeSet e) = f [fold b v f e]


instance Foldable Stmt where
-- Complete for Problem 1, part (d).
  fold b v f (Return x) = (v x)
  fold b v f (Assign x e st) = f [f [fold b v f e, fold b v f st], v x]


vars :: Stmt -> [String]
-- Complete for Problem 1, part (e).
vars stm = (fold [] (\x->[x]) (concat) stm) 

operations :: Stmt -> Integer
-- Complete for Problem 1, part (e).
operations stm = (fold 0 (\x->0) (\x -> (head x)+1) stm)

-- eof