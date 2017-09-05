---------------------------------------------------------------------
--
-- CAS CS 320, Spring 2015
-- Assignment 4 (skeleton code)
-- Linshan Jiang (linshan@bu.edu)
-- Term.hs
--

data Term =
    Number Integer
  | Abs Term
  | Plus Term Term
  | Mult Term Term

evaluate :: Term -> Integer
-- Modify and complete for Problem 4.
evaluate (Plus n1 n2) = evaluate(n1) + evaluate(n2)
evaluate (Mult n1 n2) = evaluate(n1) * evaluate(n2)
evaluate (Abs t) = if evaluate(t) > 0 then evaluate(t) else -evaluate(t)
evaluate (Number n) = n

--eof