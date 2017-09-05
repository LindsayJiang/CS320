-- Linshan Jiang (linshan@bu.edu)
-- Collaborators: Qi Want (wangqi03@bu.edu)
--                Claudia Ng (claudiaw@bu.edu)
-- Compile.hs
module Compile where

import Data.List (union, (\\))
import AbstractSyntax
import TypeCheck
import Interpret
import KeyValueStore

data Instruction =
    Reliable (Value -> Value -> Value)
  | Unreliable (Value -> Value -> Value)
  | MakeSets
  | DropKeySuffixes

-- If a variable assignment statement will never affect the
-- final returned key-value store at the bottom of the abstract
-- syntax tree, remove that statement.
rmvDeadCode :: Stmt -> Stmt
rmvDeadCode (Assign x e s) = if not (x `elem` unbound (rmvDeadCode s)) then (rmvDeadCode s) else Assign x e (rmvDeadCode s)
rmvDeadCode (Return x    ) = Return x

unbound :: Stmt -> [String]
unbound (Assign x e s) = vars (Assign "" e (Return "")) `union` (unbound s \\ [x])
unbound (Return x    ) = [x]

compileExp :: Exp -> [Instruction]
compileExp (Max e          ) = compileExp e ++ [Reliable max]
compileExp (Min e          ) = compileExp e ++ [Reliable min]
compileExp (Sum e          ) = compileExp e ++ [Reliable (+)]
compileExp (Product e      ) = compileExp e ++ [Reliable (*)]
compileExp (Union e        ) = compileExp e ++ [Reliable (\/)]
compileExp (Intersection e ) = compileExp e ++ [Reliable (/\)]
compileExp (MakeSet e      ) = compileExp e ++ [MakeSets]
compileExp _                 = []

compileStmt :: Stmt -> [Instruction]
compileStmt (Assign _ e s) = compileExp e ++ compileStmt s
compileStmt (Return _    ) = []

simulate :: [Instruction] -> KeyValueStore ->  KeyValueStore
simulate ((Reliable f)   :insts) kvs = simulate insts (combine 1 f kvs)
simulate ((Unreliable f) :insts) kvs = simulate insts (combine 2 f kvs)
simulate (DropKeySuffixes:insts) kvs = simulate insts (suffix kvs)
simulate (MakeSets       :insts) kvs = simulate insts ([([y], makeSet x)| ([y],x) <- kvs]) -- Complete for Problem 5, part (a).

compile :: Stmt -> KeyValueStore -> Maybe KeyValueStore
compile st kvs = if (typeCheck [] st) == Just TyVoid then 
	Just (simulate (compileStmt (rmvDeadCode st)) kvs) 
  else Nothing-- Complete for Problem 5, part (b).
--eof