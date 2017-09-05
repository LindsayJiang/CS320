---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
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
twigs (Leaf        ) = 0
twigs (Twig        ) = 1
twigs (Branch a b c) = twigs a + twigs b + twigs c
  
-- 3.c.
branches :: Tree -> Integer
branches (Branch a b c) = 1 + branches a + branches b + branches c
branches (      _     ) = 0

-- 3.d.
height :: Tree -> Integer
height (Leaf        ) = 0
height (Twig        ) = 1
height (Branch a b c) = 1 + (max (max (height a) (height b)) (height c))

-- 3.e.
perfect :: Tree -> Bool
perfect (Branch a b c) = (height a == height b) && (height a == height c) && (twigs a + twigs b + twigs c == 0)
perfect (      _     ) = False
  
-- 3.f.
degenerate :: Tree -> Bool
degenerate (Branch Leaf Leaf Leaf) = True
degenerate (Branch Leaf Leaf Twig) = True
degenerate (Branch Leaf Twig Leaf) = True
degenerate (Branch Leaf Twig Twig) = True
degenerate (Branch Twig Leaf Leaf) = True
degenerate (Branch Twig Leaf Twig) = True
degenerate (Branch Twig Twig Leaf) = True
degenerate (Branch Twig Twig Twig) = True
degenerate (Branch t    Leaf Leaf) = True && degenerate t
degenerate (Branch t    Leaf Twig) = True && degenerate t
degenerate (Branch t    Twig Leaf) = True && degenerate t
degenerate (Branch t    Twig Twig) = True && degenerate t
degenerate (Branch Leaf t    Leaf) = True && degenerate t
degenerate (Branch Leaf t    Twig) = True && degenerate t
degenerate (Branch Twig t    Leaf) = True && degenerate t
degenerate (Branch Twig t    Twig) = True && degenerate t
degenerate (Branch Leaf Leaf t   ) = True && degenerate t
degenerate (Branch Leaf Twig t   ) = True && degenerate t
degenerate (Branch Twig Leaf t   ) = True && degenerate t
degenerate (Branch Twig Twig t   ) = True && degenerate t
degenerate (          _          ) = False  

-- 3.g.
infinite :: Tree
infinite = Branch infinite infinite infinite
  
--eof