---------------------------------------------------------------------
--
-- CAS CS 320, Spring 2015
-- Assignment 5 (skeleton code)
-- Linshan Jiang (linshan@bu.edu)
-- Allocation.hs
--

module Allocation where

type Item = Integer
type Bin = Integer

data Alloc = Alloc Bin Bin deriving (Eq, Show)

data Graph a =
    Branch a (Graph a) (Graph a) 
  | Finish a
  deriving (Eq, Show)

type Strategy = Graph Alloc -> Graph Alloc

-- 2.a.
graph :: Alloc -> [Item] -> Graph Alloc
graph (Alloc bin1 bin2) (x:xs) = Branch (Alloc bin1 bin2) (graph (Alloc (bin1+x) bin2) xs) (graph (Alloc bin1 (bin2+x)) xs)
graph (Alloc bin1 bin2) []    = Finish (Alloc bin1 bin2)

-- 2.b.
contents :: Graph a -> a
contents (Branch b g1 g2) = b
contents (Finish b) = b

-- 2.c.
instance Ord Alloc where
	(Alloc a1 b1) < (Alloc c1 d1) = if abs(a1 - b1) < abs(c1 - d1) then True else False

	(Alloc a1 b1) <= (Alloc c1 d1) = if abs(a1 - b1) <= abs(c1 - d1) then True else False

--2.d.
instance Ord a => Ord (Graph a) where
	(Finish a1) < (Finish b1) = if a1 < b1 then True else False

	(Finish a1) <= (Finish b1) = if a1 <= b1 then True else False

-- 2.e.
final :: Graph a -> [a]
final (Branch a1 g1 g2) = final(g1) ++ final(g2)
final (Finish a1) = [a1]

-- 2.f.
depth :: Integer -> Graph a -> [a]
depth 0 (Branch a1 g1 g2) = [a1]
depth 0 (Finish a1) = [a1]
depth n (Branch a1 g1 g2) = depth (n-1) g1 ++ depth (n-1) g2
-- 

-- 3.a.
greedy :: Strategy
greedy (Branch a1 g1 g2) = if (onlyAlloc g1) < (onlyAlloc g2) then g1 else g2
greedy (Finish a1) = (Finish a1)

-- helper function for greedy
onlyAlloc :: Graph Alloc -> Alloc
onlyAlloc (Branch (Alloc a1 b1) g1 g2) = (Alloc a1 b1)
onlyAlloc (Finish (Alloc a1 b1)) = (Alloc a1 b1)

-- 3.b.
patient :: Integer -> Strategy
patient 0 a1 = a1
patient n (Branch a1 g1 g2) = greedy (Branch a1 (patient (n-1) g1) (patient (n-1) g2))

-- 3.c.
optimal :: Strategy
optimal (Branch a1 g1 g2) = greedy (Branch a1 (optimal (g1)) (optimal(g2)))
optimal (Finish a1) = (Finish a1)

-- 3.d.
metaCompose :: Strategy -> Strategy -> Strategy
(metaCompose s1 s2) g1 = s2 (s1 (g1))

--3.e.
metaRepeat :: Integer -> Strategy -> Strategy
(metaRepeat 0 s) g = g
(metaRepeat n s) g = (metaRepeat (n-1) s) (s(g))

-- 3.f.
metaGreedy :: Strategy -> Strategy -> Strategy
(metaGreedy s1 s2) g = greedy (Branch (Alloc 0 0) (s1(g)) (s2(g)))

-- 3.g.
{-
impatient repeats a single strategy for n times while patient 
chooses the best descendant strtegies of depth n.

impatient is better when we have a wide (many children in each depth) 
tree. Because patient can get really slow in this case;

impatient is inferior when we have a narrow (small number of
children in each depth) tree. Because patient looks deeper
and may get better strategy.
-}





--eof