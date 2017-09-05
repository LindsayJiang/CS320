-- Linshan Jiang (linshan@bu.edu)
-- Collaborators: Qi Want (wangqi03@bu.edu)
--                Claudia Ng (claudiaw@bu.edu)
-- KeyValueStore.hs
module KeyValueStore where

import Data.List (sort)

-- A function for finding two elements in a key-value store
-- that have the same key.
--
--  * The first argument is the key-value store, assumed
--    to already be sorted so pairs with the same key
--    are contiguous.
--  * The second argument is an accumulator list that
--    will maintain all the list entries that have no
--    partners with duplicate keys (thus, they must be kept
--    in the key-value store).
--  * If no duplicate keys are found, the result is Nothing;
--    otherwise, the result will be a tuple containing the
--    key, the two values under that key, and a new key-value
--    store that contains everything from the original one
--    except the two entries corresponding to the two values.

twoWithSameKeyHelper :: (Ord a, Ord b, Eq a) => [(a,b)] -> [(a,b)] -> Maybe (a, b, b, [(a,b)])
-- Complete recursive case for Problem 3, part (a).
twoWithSameKeyHelper ((k1,v1):(k2,v2):kvs) keep  = if k1 == k2 then Just (k1,v1,v2,keep++kvs)
	                                               else twoWithSameKeyHelper ([(k2,v2)]++kvs) ([(k1,v1)]++keep)
twoWithSameKeyHelper _  _ = Nothing

-- Complete for Problem 3, part (b).
twoWithSameKey :: (Ord a, Ord b, Eq a) => [(a,b)] -> Maybe (a, b, b, [(a,b)])
twoWithSameKey kvs = twoWithSameKeyHelper (sort kvs) []

suffix :: [([a],b)] -> [([a],b)]
-- Complete for Problem 3, part (c).
suffix [] = []
suffix kvs = [((tail la),b)|(la,b)<-kvs]


-- A function for simulating the application of an operation to
-- a key-value store.
--
--  * The first argument specifies how many duplicates of the 
--    result of each pair-wise operation will be added to the
--    resulting database.
--  * The second argument is the operation to be applied to
--    all pairs of entries that have the same key.
--  * The third argument is the key-value store itself.
--  * The result is the new key-value store in which all pairs
--    with identical keys have been combined.

combine :: (Ord a, Ord b, Eq a) =>  Int -> (b -> b -> b) -> [([a],b)] -> [([a],b)]
combine n op kvs =
  case twoWithSameKey kvs of
    Nothing -> kvs
    Just (k, v1, v2, kvs') -> combine n op (take n (repeat (k, op v1 v2)) ++ kvs')

--eof