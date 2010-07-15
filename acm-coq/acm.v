(** Acm Presentation - Proving stuff with Coq
   
*)

(** Here we can see some examples of Propositional Logic *)

Require Import Classical.


Theorem silly_prop :forall (A B C: Prop), 
  (A -> (B -> C)) -> (A -> B) -> (A -> C).
Proof.
  intros A B C H1 HA H2. 
  apply H1.
  apply H2.
  apply HA.
  assumption.
Qed.

Lemma and_comm : forall (A B : Prop), A /\ B -> B /\ A.
Proof.
intros A B H.
elim H.
split.
apply H1.
apply H0.
Qed.


Lemma or_comm : forall (A B : Prop), A \/ B -> B \/ A.
Proof.
intros A B H.
elim H.
right. trivial.
left. trivial.
Qed.


Theorem silly_ex : forall (A B C : Prop),
  (A \/ B) /\ (A \/ C) /\ ~ A -> B /\ C.
Proof.
intros.
destruct H. destruct H0. 
destruct H.
destruct (H1 H).
destruct H0.
destruct (H1 H0).
split.
assumption.
assumption.
Qed.

Theorem ex1 : forall (A B C D:Prop),
  (A \/ B) -> (B /\ C) -> (B -> C) \/ D.
Proof.
intros.
destruct H0.
left.
intros.
apply H1.
Qed.

Theorem ex2: forall (A B C D:Prop),
  ~(A /\ B) /\ (B \/ C) /\ (C -> D) -> (A -> D).
Proof.
intros.
destruct H.
destruct H1.
apply H2.
destruct H1.
generalize(conj H0 H1).
intros.
destruct(H H3).
apply H1.
Qed.

Theorem ex3 : forall (A  B C D:Prop),
  A /\ ((A -> B) \/ (C /\ D)) -> (~B -> C).
Proof.
intros ? ? ? ? [H1 H2] ?.
destruct H2. destruct H.
apply H0.
apply H1.
apply H0.
Qed.

Theorem ex4 : forall (A B : Prop),
  A -> (B -> (A /\ B)).
Proof.
Admitted.


