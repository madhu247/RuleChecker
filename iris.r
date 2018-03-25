! This rule file was created from: n-iris-aca.rul and from: m-iris.d
! --------------------------------------------------------

1, 50, 57
(petal_width,0.1..1) -> (class,Iris-setosa)

2, 45, 46
(petal_width,1..1.7) & (petal_length,1..4.8) -> (class,Iris-versicolor)

3, 4, 5
(petal_length,4.8..5.1) & (sepal_length,6.2..7.9) & (petal_width,1..1.7)
     -> (class,Iris-versicolor)

3, 2, 3
(petal_length,4.8..5.1) & (sepal_width,3..3.1) & (sepal_length,6.2..7.9)
     -> (class,Iris-versicolor)

2, 2, 4
(petal_length,4.8..5.1) & (sepal_width,3.1..4.4) -> (class,Iris-versicolor)

3, 20, 20
(sepal_width,2.7..3) & (petal_width,1..1.7) & (sepal_length,4.3..6.2)
     -> (class,Iris-versicolor)

2, 38, 38
(petal_width,1.7..2.5) & (petal_length,5.1..6.9) -> (class,Iris-viginica)

3, 3, 3
(petal_length,4.8..5.1) & (sepal_length,4.3..6.2) & (sepal_width,3..3.1)
     -> (class,Iris-viginica)

2, 24, 25
(petal_width,1.7..2.5) & (sepal_width,2.7..3) -> (class,Iris-viginica)

3, 4, 5
(sepal_width,2..2.7) & (sepal_length,4.3..6.2) & (petal_length,4.8..5.1)
     -> (class,Iris-viginica)

2, 9, 9
(sepal_width,2..2.7) & (petal_width,1.7..2.5) -> (class,Iris-viginica)

2, 36, 36
(petal_length,5.1..6.9) & (sepal_length,6.2..7.9) -> (class,Iris-viginica)

2, 6, 7
(sepal_width,2..2.7) & (petal_length,5.1..6.9) -> (class,Iris-viginica)
