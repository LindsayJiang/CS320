module ProjectTests where

import AbstractSyntax
import Parse
import TypeCheck
import KeyValueStore
import Interpret
import Validate
--import Compile

allTests = [
  show (failed parseTests),
  show (failed typeCheckTests),
  show (failed interpretTests)
  ]

-- To get the failures for an individual test, query that
-- test using "failed", e.g.:
-- 
-- *> failed parseTests

failed :: Eq a => [(a, a)] -> [(a, a)]
failed tests = [(x, y) | (x, y) <- tests, x /= y]

parseTests :: [(Maybe Stmt, Maybe Stmt)]
parseTests = [
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Return "b"))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign b = set(DATA); return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "b" (MakeSet DATA) (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign b = b; return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "b" (Variable "b") (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign b = DATA; return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "b" DATA (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign a = set(DATA); return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "a" (MakeSet DATA) (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign a = set(DATA); return a;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "a" (MakeSet DATA) (Return "a")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign a = b; return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "a" (Variable "b") (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign a = b; return a;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "a" (Variable "b") (Return "a")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign a = DATA; return b;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "a" DATA (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = union(set(DATA)); assign a = DATA; return a;"), Just (Assign "b" (Union (MakeSet DATA)) (Assign "a" DATA (Return "a")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = sum(DATA); return b;"), Just (Assign "b" (Sum DATA) (Return "b"))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = sum(DATA); assign b = set(DATA); return b;"), Just (Assign "b" (Sum DATA) (Assign "b" (MakeSet DATA) (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = sum(DATA); assign b = b; return b;"), Just (Assign "b" (Sum DATA) (Assign "b" (Variable "b") (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = sum(DATA); assign b = DATA; return b;"), Just (Assign "b" (Sum DATA) (Assign "b" DATA (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = sum(DATA); assign a = set(DATA); return b;"), Just (Assign "b" (Sum DATA) (Assign "a" (MakeSet DATA) (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign y = sum(product(DATA)); assign y = product(y); assign x = set(DATA); return x;"), Just (Assign "y" (Sum (Product DATA)) (Assign "y" (Product (Variable "y")) (Assign "x" (MakeSet DATA) (Return "x"))))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign y = sum(product(DATA)); assign y = product(y); assign x = DATA; return y;"), Just (Assign "y" (Sum (Product DATA)) (Assign "y" (Product (Variable "y")) (Assign "x" DATA (Return "y"))))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign y = sum(product(DATA)); assign y = product(y); assign x = DATA; return x;"), Just (Assign "y" (Sum (Product DATA)) (Assign "y" (Product (Variable "y")) (Assign "x" DATA (Return "x"))))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign y = sum(product(DATA)); assign y = product(DATA); return y;"), Just (Assign "y" (Sum (Product DATA)) (Assign "y" (Product DATA) (Return "y")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = sum(DATA); assign a = DATA; return a;"), Just (Assign "b" (Sum DATA) (Assign "a" DATA (Return "a")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = set(DATA); return b;"), Just (Assign "b" (MakeSet DATA) (Return "b"))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = set(DATA); assign b = set(DATA); return b;"), Just (Assign "b" (MakeSet DATA) (Assign "b" (MakeSet DATA) (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = set(DATA); assign b = b; return b;"), Just (Assign "b" (MakeSet DATA) (Assign "b" (Variable "b") (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign b = set(DATA); assign b = DATA; return b;"), Just (Assign "b" (MakeSet DATA) (Assign "b" DATA (Return "b")))),
  ((tokenizeParse :: String -> Maybe Stmt) ("assign y = union(set(DATA)); assign x = y; return y;"), Just (Assign "y" (Union (MakeSet DATA)) (Assign "x" (Variable "y") (Return "y"))))
  ]

typeCheckTests :: [(Maybe Type, Maybe Type)]
typeCheckTests = [
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "b" (Sum DATA) (Assign "a" (Variable "b") (Return "a"))), Just TyVoid),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "b" (Sum DATA) (Assign "a" (Variable "b") (Return "b"))), Just TyVoid),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "b" (Sum DATA) (Assign "b" (Variable "b") (Return "b"))), Just TyVoid),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "a" (Sum DATA) (Assign "a" (MakeSet DATA) (Return "a"))), Just TyVoid),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "b" (Variable "a") (Return "a")), Nothing),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "a" (Variable "a") (Return "b")), Nothing),
  ((typeCheck [] :: Exp -> Maybe Type) (Product (Product (Max (Product (Product (Min (Product DATA))))))), Just TyNumber),
  ((typeCheck [] :: Exp -> Maybe Type) (Product (Sum (Max (Product (Product (Min (Product DATA))))))), Just TyNumber),
  ((typeCheck [] :: Exp -> Maybe Type) (Product (Product (Product (Product (Product (Min (Product DATA))))))), Just TyNumber),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "p" (Variable "q") (Return "p")), Nothing),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "x" (Sum (Product DATA)) (Assign "y" (Intersection (Intersection (MakeSet (Variable "x")))) (Return "y"))), Just TyVoid),
  ((typeCheck [] :: Stmt -> Maybe Type) (Assign "q" DATA (Return "q")), Just TyVoid),
  ((typeCheck [] :: Exp -> Maybe Type) (Product (Max (Product DATA))), Just TyNumber)
  ]

interpretTests :: [(Maybe KeyValueStore, Maybe KeyValueStore)]
interpretTests = [
  (typeCheckInterpret (Assign "u" (Min (Product DATA)) (Assign "v" (Min (Product (Variable "u"))) (Return "v"))) testKVS, Just [([],Number 900),([],Number 900)]),
  (typeCheckInterpret (Assign "x" (Min (Max DATA)) (Assign "y" (Union (Union (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [5]),([],Set [5])]),
  (typeCheckInterpret (Assign "x" (Sum (Max DATA)) (Assign "y" (Intersection (Intersection (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [5]),([],Set [5])]),
  (typeCheckInterpret (Assign "x" (Sum (Max DATA)) (Assign "y" (Union (Union (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [5]),([],Set [5])]),
  (typeCheckInterpret (Assign "a" (Min (Sum DATA)) (Assign "b" (Union (Union (MakeSet (Variable "a")))) (Return "b"))) testKVS, Just [([],Set [9]),([],Set [9])]),
  (typeCheckInterpret (Assign "s" (Product (Min DATA)) (Assign "t" (Min (Min (Variable "s"))) (Return "t"))) testKVS, Just [([],Number (-1)),([],Number (-1))]),
  (typeCheckInterpret (Assign "s" (Product (Product DATA)) (Assign "t" (Product (Product (Variable "s"))) (Return "t"))) testKVS, Just [([],Number 729000000),([],Number 729000000)]),
  (typeCheckInterpret (Assign "s" (Product (Sum DATA)) (Assign "t" (Sum (Sum (Variable "s"))) (Return "t"))) testKVS, Just [([],Number 54),([],Number 54)]),
  (typeCheckInterpret (Assign "x" (Sum (Product DATA)) (Assign "y" (Intersection (Intersection (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [-30]),([],Set [-30])]),
  (typeCheckInterpret (Assign "x" (Sum (Product DATA)) (Assign "y" (Union (Union (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [-30]),([],Set [-30])]),
  (typeCheckInterpret (Assign "x" (Product (Product DATA)) (Assign "y" (Intersection (Intersection (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [-30]),([],Set [-30])]),
  (typeCheckInterpret (Assign "x" (Product (Product DATA)) (Assign "y" (Union (Union (MakeSet (Variable "x")))) (Return "y"))) testKVS, Just [([],Set [-30]),([],Set [-30])]),
  (typeCheckInterpret (Assign "x" (Sum (Min DATA)) (Assign "y" (Min (Min (Variable "x"))) (Return "y"))) testKVS, Just [([],Number (-1)),([],Number (-1))]),
  (typeCheckInterpret (Assign "x" (Sum (Max DATA)) (Assign "y" (Max (Max (Variable "x"))) (Return "y"))) testKVS, Just [([],Number 5),([],Number 5)]),
  (typeCheckInterpret (Assign "x" (Sum (Sum DATA)) (Assign "y" (Sum (Sum (Variable "x"))) (Return "y"))) testKVS, Just [([],Number 54),([],Number 54)]),
  (typeCheckInterpret (Assign "u" (Product (Product DATA)) (Assign "v" (Product (Product (Variable "u"))) (Return "v"))) testKVS, Just [([],Number 729000000),([],Number 729000000)]),
  (typeCheckInterpret (Assign "x" (Product (Max DATA)) (Assign "y" (Max (Max (Variable "x"))) (Return "y"))) testKVS, Just [([],Number 5),([],Number 5)]),
  (typeCheckInterpret (Assign "x" (Product (Sum DATA)) (Assign "y" (Sum (Sum (Variable "x"))) (Return "y"))) testKVS, Just [([],Number 54),([],Number 54)])
  ]

testKVS = (dats [["T"], ["C", "D"], ["X", "Y", "Z"], ["a", "b"]] [-1,2,3,5]) !! 3

--eof