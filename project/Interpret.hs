-- Linshan Jiang (linshan@bu.edu)
-- Collaborators: Qi Want (wangqi03@bu.edu)
--                Claudia Ng (claudiaw@bu.edu)
-- Interpret.hs
module Interpret where

import AbstractSyntax
import KeyValueStore
import TypeCheck

makeSet :: Value -> Value
makeSet Error      = Error
makeSet (Number n) = Set [n]
makeSet (Set ns)   = Set ns

type KeyValueStore = [([String], Value)]
type Algorithm = KeyValueStore -> Maybe KeyValueStore

lJust :: Maybe (KeyValueStore) -> KeyValueStore
lJust (Just k) = k

eval :: [(String, KeyValueStore)] -> Exp -> Algorithm
-- Complete for Problem 3, part (d).
eval env DATA a = if a == [] then Nothing else Just a
eval env (Variable s) a = let result = [k|(s',k)<- env, s'==s]
                          in if result == [] then Nothing else Just (head result)
eval env (MakeSet e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                        Just [(keys, makeSet value)|(keys,value)<-(lJust store)]

eval env (Min e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                     	let result = (suffix (combine 1 (min) (lJust store)))
                        in if result == [] then Nothing else Just result
eval env (Max e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                     	let result = (suffix (combine 1 (max) (lJust store)))
                        in if result == [] then Nothing else Just result
eval env (Sum e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                     	let result = (suffix (combine 1 (+) (lJust store)))
                        in if result == [] then Nothing else Just result
eval env (Product e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                     	let result = (suffix (combine 1 (*) (lJust store)))
                        in if result == [] then Nothing else Just result
eval env (Union e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                     	let result = (suffix (combine 1 (\/) (lJust store)))
                        in if result == [] then Nothing else Just result
eval env (Intersection e) a = let store = (eval env e a)
                     in if store == Nothing then Nothing else
                     	let result = (suffix (combine 1 (/\) (lJust store)))
                        in if result == [] then Nothing else Just result

                     	
exec :: [(String, KeyValueStore)] -> Stmt -> Algorithm
-- Complete for Problem 3, part (d).
{-
exec env (Assign x e s) a = let store = eval env e a
                            in if store == Nothing then Nothing else 
                                let env2 = (env ++ [(x,(lJust store))]) 
                            	in exec env2 s a
                                -}
exec env (Assign x e s) a = if eval env e a == Nothing then Nothing else
                                exec (env++[(x,lJust (eval env e a))]) s a
exec env (Return x) a = eval env (Variable x) a


typeCheckInterpret :: Stmt -> Algorithm
-- Complete for Problem 3, part (e).
typeCheckInterpret sta kvs = if (typeCheck [] sta) == Nothing then Nothing
	                         else exec [] sta kvs

--eof