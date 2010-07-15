(** First we need to tell Coq how to construct a list *)
Inductive natlist : Type :=
  | nil : natlist
  | cons : nat -> natlist -> natlist.

(** Using this constructor we can then define lists *)

Definition l_123 := cons 1 (cons 2 (cons 3 nil)).

(** Is is trivial to add notation for easier use of the list constructor *)
Notation "x :: l" := (cons x l) (at level 60, right associativity).
Notation "[ ]" := nil.
Notation "[ x , .. , y ]" := (cons x .. (cons y nil) ..).


(** Now we can define a few functions over lists *)

Fixpoint repeat (n count : nat) {struct count} : natlist := 
  match count with
  | O => nil
  | S count' => n :: (repeat n count')
  end.

(** The [length] function calculates the length of a
    list. *)

Fixpoint length (l:natlist) {struct l} : nat := 
  match l with
  | nil => O
  | h :: t => S (length t)
  end.

(** The [app] function concatenates two lists. *)

Fixpoint app (l1 l2 : natlist) {struct l1} : natlist := 
  match l1 with
  | nil    => l2
  | h :: t => h :: (app t l2)
  end.

(** In fact, [app] will be used so pervasively in
    some parts of what follows that it is convenient to
    have an infix operator for it. *)

Notation "x ++ y" := (app x y) 
                     (right associativity, at level 60).

(** One trivial theorem we can show is the indentity of a list using [] *)
Theorem nil_app : forall l:natlist,
  [] ++ l = l.
Proof.
   reflexivity.  Qed.

(** A more complex theorem involving induction *)
Theorem ass_app : forall l1 l2 l3 : natlist, 
  l1 ++ (l2 ++ l3) = (l1 ++ l2) ++ l3.   
Proof.
  intros l1 l2 l3.
  Case "l1 = nil".
    reflexivity.
  Case "l1 = cons n l1'".
    simpl. rewrite -> IHl1'. reflexivity.  Qed.