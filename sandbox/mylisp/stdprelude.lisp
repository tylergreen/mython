(begin

(mac defn (name args body) `(def ,name (fn ,args ,body)))

(defn foldl (f z xs)
  (if (empty? xs)
      z
      (foldl f (f z (car xs)) (cdr xs))))

(defn foldl1 (f xs)
  (foldl f (car xs) (cdr xs)))

(defn flip (f)
  (fn (x y) (f y x)))

(defn comp (f g)
  (fn (x) (f g x)))

(defn map (f xs)
  (foldl (fn (z x) (cons (f x) z)) '() xs))

(defn count (xs)
  (foldl (fn (x y) (+ x 1)) 0 xs))

)