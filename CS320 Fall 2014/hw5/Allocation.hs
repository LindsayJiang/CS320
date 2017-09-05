---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Yida Xu  xyds1522@bu.edu  U39436573
-- Allocation.hs
--

module Allocation where
import qualified Data.List as List
type Item = Integer
type Bin = Integer

data Alloc = Alloc Bin Bin deriving (Eq, Show)

data Graph =
    Branch Alloc Graph Graph 
  | Finish Alloc
  deriving (Eq, Show)

-- 2.a.
graph :: Alloc -> [Item] -> Graph
graph (Alloc a b) (i:r) = Branch (Alloc a b) (graph (Alloc (a+i) b) r) (graph (Alloc a (b+i)) r)
graph (Alloc a b) []    = Finish (Alloc a b)

-- 2.b.
alloc :: Graph -> Alloc
alloc (Finish (Alloc a b)) = Alloc a b
alloc (Branch (Alloc a b) g1 g2) = Alloc a b

-- 2.c.
instance Ord Alloc where
	(Alloc a1 a2) < (Alloc b1 b2)  = if (abs(a1 - a2) < abs(b1 - b2))
									 then True
									 else False
	(Alloc a1 a2) <= (Alloc b1 b2) = if (abs(a1 - a2) <= abs(b1 - b2))
									 then True
									 else False

-- 2.d.									 
instance Ord Graph where
	(Finish (Alloc a1 a2)) < (Finish (Alloc b1 b2))  = if (abs(a1 - a2)) < (abs(b1 - b2))
													   then True
													   else False
	(Finish (Alloc a1 a2)) <= (Finish (Alloc b1 b2)) = if (abs(a1 - a2)) <= (abs(b1 - b2))
													   then True
													   else False

-- 2.e.													   
final :: Graph -> [Alloc]
final (Branch a g1 g2) = final(g1) ++ final(g2)
final (Finish a) = [a]

-- 2.f.
depth :: Integer -> Graph -> [Alloc]
depth 0 (Branch a g1 g2) = [a]
depth n (Branch a g1 g2) = depth (n - 1) g1 ++ depth (n - 1) g2	
												   
type Strategy = Graph -> Graph

-- 3.a.
greedy :: Strategy
greedy (Finish a) = Finish a
greedy (Branch a g1 g2) = if (alloc g1) < (alloc g2)
						  then g1
						  else g2
			
-- 3.b.
patient :: Integer -> Strategy
patient 0 g = g
patient n (Branch a g1 g2) = greedy (Branch a (patient (n-1) g1) (patient (n-1) g2))

-- 3.c.
optimal :: Strategy
optimal (Finish a) = Finish a
optimal (Branch a g1 g2) = greedy (Branch a (optimal g1) (optimal g2))

-- 3.d.
metaCompose :: Strategy -> Strategy -> Strategy
(metaCompose a b) c = b(a(c))

-- 3.e.
metaRepeat :: Integer -> Strategy -> Strategy
(metaRepeat 0 a) g = g
(metaRepeat n a) g = (metaRepeat (n-1) a) (a(g))

-- 3.f.
metaGreedy :: Strategy -> Strategy -> Strategy
(metaGreedy a b) g = greedy (Branch (Alloc 0 0) (a(g)) (b(g)))

-- 3.g. 
{-
impatient repeats a specific strategy on a graph for n times while patient looks
into the strategy for n depths.
impatient is width-first algorithm, patient is a depth-first algorithm
patient is slower than impatient if depth is bigger than a certain number
-}

--4.

fit :: Graph -> [Strategy] -> Strategy
fit g [s1:s2] = List.minimumBy greedy [(s1 g), (s2 g)]
--fit g s:r = List.minimumBy greedy [s(g), (fit g r)]


--eof