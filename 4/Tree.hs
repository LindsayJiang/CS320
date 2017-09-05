---------------------------------------------------------------------
--
-- CAS CS 320, Spring 2015
-- Assignment 4 (skeleton code)
-- Linshan Jiang(linshan@bu.edu)
-- Tree.hs
--

-- 3.a.
data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show)

-- 3.b.
twigs :: Tree -> Integer
twigs (Branch t1 t2 t3) = twigs(t1) + twigs(t2) + twigs(t3)
twigs (Leaf) = 0
twigs (Twig) = 1

-- 3.c.
branches :: Tree -> Integer
branches (Branch t1 t2 t3) = 1 + branches(t1) + branches(t2) + branches(t3)
branches (Leaf) = 0
branches (Twig) = 0

-- 3.d.
height :: Tree -> Integer
height (Branch t1 t2 t3) = 1 + (max (height(t1)) (max(height(t2)) (height (t3))))
height (Leaf) = 0
height (Twig) = 1

-- 3.e.
perfect :: Tree -> Bool
perfect (Branch t1 t2 t3) = height(t1) == height(t2) && height(t2) == height(t3) && twigs(Branch t1 t2 t3) == 0
perfect (Leaf) = True
perfect (Twig) = False

-- 3.f.
degenerate :: Tree -> Bool
degenerate (Leaf) = True
degenerate (Twig) = True
degenerate (Branch t Leaf Leaf) = degenerate (t)
degenerate (Branch t Leaf Twig) = degenerate (t)
degenerate (Branch t Twig Leaf) = degenerate (t)
degenerate (Branch t Twig Twig) = degenerate (t)
degenerate (Branch Leaf t Leaf) = degenerate (t)
degenerate (Branch Leaf t Twig) = degenerate (t)
degenerate (Branch Twig t Leaf) = degenerate (t)
degenerate (Branch Twig t Twig) = degenerate (t)
degenerate (Branch Leaf Leaf t) = degenerate (t)
degenerate (Branch Leaf Twig t) = degenerate (t)
degenerate (Branch Twig Leaf t) = degenerate (t)
degenerate (Branch Twig Twig t) = degenerate (t)
-- the rest cases are those when a tree has two branch children. Flase immediately.
degenerate (          _          ) = False

-- 3.g.
infinite :: Tree
infinite = Branch infinite infinite infinite









--eof