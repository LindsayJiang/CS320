-- Linshan Jiang (linshan@bu.edu)
-- Collaborators: Qi Want (wangqi03@bu.edu)
--                Claudia Ng (claudiaw@bu.edu)
-- TypeCheck.hs

module TypeCheck where
import AbstractSyntax
import Parse

class Typeable a where
  typeCheck :: [(String, Type)] -> a -> Maybe Type

-- Complete for Problem 2, part (a).
instance Typeable Exp where
  typeCheck env DATA = Just TyNumber
  typeCheck env (Variable s) = let ls = [Just t|(str, t) <- env, str == s]
                               in if ls == [] then Nothing else head ls
  typeCheck env (Max e) = if (typeCheck env e) == Just TyNumber then Just TyNumber else Nothing
  typeCheck env (Min e) = if (typeCheck env e) == Just TyNumber then Just TyNumber else Nothing
  typeCheck env (Sum e) = if (typeCheck env e) == Just TyNumber then Just TyNumber else Nothing
  typeCheck env (Product e) = if (typeCheck env e) == Just TyNumber then Just TyNumber else Nothing
  typeCheck env (Union e) = if (typeCheck env e) == Just TySet then Just TySet else Nothing
  typeCheck env (Intersection e) = if (typeCheck env e) == Just TySet then Just TySet else Nothing
  typeCheck env (MakeSet e) = if (typeCheck env e) == Just TyNumber then Just TySet else Nothing
  typeCheck _ _ = Nothing 

-- Complete for Problem 2, part (b).
instance Typeable Stmt where 
  typeCheck env (Assign x e st) = 
  	let etype = typeCheck env e
  	in if etype == Nothing then 
      if typeCheck env st == Just TyVoid then Just TyVoid else Nothing
    else 
      if typeCheck ([(x, noJust etype)]++env) st == Just TyVoid then Just TyVoid else Nothing
  typeCheck env (Return st) = if st `elem` [s|(s,t)<-env] then Just TyVoid else Nothing


-- helper functino for Problem 2, part(b).
noJust :: Maybe Type -> Type
noJust (Just t) = t


liftMaybe :: (a -> b) -> (Maybe a -> Maybe b)
-- Complete for Problem 2, part (c).
liftMaybe f (Nothing) = Nothing
liftMaybe f (Just a) = Just (f a)

joinMaybe :: Maybe (Maybe a) -> Maybe a
-- Complete for Problem 2, part (c).
joinMaybe (Just Nothing) = Nothing
joinMaybe (Just (Just x)) = Just x
joinMaybe Nothing = Nothing

tokenizeParseTypeCheck :: String -> Maybe Type
tokenizeParseTypeCheck s = joinMaybe (liftMaybe (typeCheck [] :: Stmt -> Maybe Type) (tokenizeParse s))
  
-- eof