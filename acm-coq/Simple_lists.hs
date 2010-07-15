module Simple_lists where

import qualified Prelude
import qualified Datatypes


data Coq_natlist = Coq_nil
                   | Coq_cons Datatypes.Coq_nat Coq_natlist

natlist_rect :: a1 -> (Datatypes.Coq_nat -> Coq_natlist -> a1 -> a1) ->
                Coq_natlist -> a1
natlist_rect f f0 n =
  case n of
    Coq_nil -> f
    Coq_cons n0 n1 -> f0 n0 n1 (natlist_rect f f0 n1)

natlist_rec :: a1 -> (Datatypes.Coq_nat -> Coq_natlist -> a1 -> a1) ->
               Coq_natlist -> a1
natlist_rec f f0 n =
  natlist_rect f f0 n

l_123 :: Coq_natlist
l_123 =
  Coq_cons (Datatypes.S Datatypes.O) (Coq_cons (Datatypes.S (Datatypes.S
    Datatypes.O)) (Coq_cons (Datatypes.S (Datatypes.S (Datatypes.S
    Datatypes.O))) Coq_nil))

repeat :: Datatypes.Coq_nat -> Datatypes.Coq_nat -> Coq_natlist
repeat n count =
  case count of
    Datatypes.O -> Coq_nil
    Datatypes.S count' -> Coq_cons n (repeat n count')

length :: Coq_natlist -> Datatypes.Coq_nat
length l =
  case l of
    Coq_nil -> Datatypes.O
    Coq_cons h t -> Datatypes.S (length t)

app :: Coq_natlist -> Coq_natlist -> Coq_natlist
app l1 l2 =
  case l1 of
    Coq_nil -> l2
    Coq_cons h t -> Coq_cons h (app t l2)

